#!/usr/bin/env python3
"""Build deterministic portable skill distributions from canonical source.

Usage:
    python3 library/organization/skills/build-distributions.py [--check] [--output-directory dist]

Options:
    --check    Verify that existing distributions are up to date; exit non-zero
               if any drift is detected without writing files.

Distribution layout
-------------------
For each canonical skill at:

    library/organization/skills/<domain>/<skill-name>/

This script writes a self-contained distribution package at:

    dist/skills/<skill-name>/
    ├── SKILL.md                           # copied verbatim from canonical source
    ├── evals/                             # copied verbatim (when present)
    ├── references/                        # copied verbatim (when present)
    ├── templates/                         # copied verbatim (when present)
    ├── scripts/                           # copied verbatim (when present)
    └── distribution-manifest.v1.json     # generated provenance manifest

Rules
-----
1. Canonical source is never modified.
2. Generated files are never hand-edited; the manifest header makes this explicit.
3. The source digest covers only the canonical SKILL.md file (UTF-8, LF-normalised).
4. Companion directories (evals/, references/, templates/, scripts/) are copied
   verbatim, excluding generated Python bytecode caches.
5. Frontmatter may declare narrowly scoped repository resources for a portable
   package in ``metadata.aether-distribution-resources``. Each resource must
   name a repository-relative source file and a package-relative destination.
6. If ``--check`` is passed the script prints OK/DRIFT lines and exits non-zero
   on any drift without writing anything.
7. Generation/I/O failures and unexpected entries in the owned subtree fail
   both modes. Unknown output is reported and retained, never deleted.
"""

from __future__ import annotations

import argparse
import os
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path, PureWindowsPath

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_DIR = REPO_ROOT / "library" / "organization" / "skills"
DIST_DIR = REPO_ROOT / "dist" / "skills"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
GENERATOR_ID = "library/organization/skills/build-distributions.py"
COMPANION_DIRS = ("evals", "references", "templates", "scripts")
STABLE_ID_RE = re.compile(r"^[a-z](?:[a-z0-9-]*[a-z0-9])?$")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _normalized_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def _source_digest(path: Path) -> str:
    return hashlib.sha256(_normalized_bytes(path)).hexdigest()


def _canonical_json(data: object) -> str:
    return json.dumps(data, sort_keys=True, indent=2)


def _read_frontmatter(path: Path, content: bytes | None = None) -> dict:
    text = content.decode("utf-8") if content is not None else path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"no YAML frontmatter in {path}")
    value = yaml.safe_load(m.group(1))
    if not isinstance(value, dict):
        raise ValueError("skill frontmatter must be a mapping")
    return value


def _distribution_resources(frontmatter: dict) -> list[tuple[Path, Path]]:
    """Return validated (repository source, package destination) resources.

    Canonical skills are usually self-contained. This narrow escape hatch keeps
    a governed catalog canonical in one location while placing an immutable
    copy in an installed package.
    """
    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        return []
    resources = metadata.get("aether-distribution-resources", [])
    if resources is None:
        return []
    if not isinstance(resources, list):
        raise ValueError("metadata.aether-distribution-resources must be a list")

    result: list[tuple[Path, Path]] = []
    destinations: set[Path] = set()
    for resource in resources:
        if not isinstance(resource, dict):
            raise ValueError("each aether-distribution-resources entry must be a mapping")
        source_value = resource.get("source")
        destination_value = resource.get("destination")
        if not isinstance(source_value, str) or not isinstance(destination_value, str):
            raise ValueError("distribution resources require string source and destination fields")

        source_relative = Path(source_value)
        destination = Path(destination_value)
        if source_relative.is_absolute() or ".." in source_relative.parts or "\\" in source_value or PureWindowsPath(source_value).drive:
            raise ValueError(f"distribution resource source escapes repository: {source_value}")
        if destination.is_absolute() or ".." in destination.parts or destination == Path(".") or "\\" in destination_value or PureWindowsPath(destination_value).drive:
            raise ValueError(f"distribution resource destination escapes package: {destination_value}")

        source = (REPO_ROOT / source_relative).resolve()
        try:
            source.relative_to(REPO_ROOT.resolve())
        except ValueError as exc:
            raise ValueError(f"distribution resource source escapes repository: {source_value}") from exc
        if not source.is_file():
            raise ValueError(f"distribution resource source is not a file: {source_value}")
        if destination in destinations:
            raise ValueError(f"duplicate distribution resource destination: {destination_value}")
        destinations.add(destination)
        result.append((source, destination))

    return sorted(result, key=lambda item: item[1].as_posix())


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def _canonical_source(path: Path, source_root: Path, *, directory: bool = False) -> Path:
    """Reject implicit redirects before listing or reading canonical inputs."""
    repository = REPO_ROOT.absolute()
    try:
        relative = path.absolute().relative_to(repository)
        source_root.resolve(strict=True).relative_to(repository.resolve())
    except ValueError as exc:
        raise ValueError("canonical source escapes its repository") from exc
    cursor = repository
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError(f"canonical source symlink is not supported: {path}")
    resolved = path.resolve(strict=True)
    try:
        resolved.relative_to(source_root.resolve(strict=True))
    except ValueError as exc:
        raise ValueError("canonical source escapes its declared tree") from exc
    if not (resolved.is_dir() if directory else resolved.is_file()):
        raise ValueError("canonical source must be a regular file or declared directory")
    return resolved


def _confined_output(base: Path, relative: Path) -> Path:
    """Anchor every read/write to the explicitly selected output root."""
    if relative.is_absolute() or ".." in relative.parts or "\\" in str(relative) or PureWindowsPath(str(relative)).drive:
        raise ValueError("unsafe generated-output path")
    root = base.resolve()
    cursor = root
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise ValueError(f"generated-output symlink is not supported: {relative}")
    try:
        cursor.resolve().relative_to(root)
    except ValueError as exc:
        raise ValueError("generated output escapes the selected root") from exc
    return cursor


def find_skills() -> list[tuple[str, Path]]:
    """Discover without following implicit source-directory/file symlinks."""
    _canonical_source(SKILLS_DIR, SKILLS_DIR, directory=True)
    results: list[tuple[str, Path]] = []
    for domain_dir in sorted(SKILLS_DIR.iterdir()):
        if domain_dir.is_symlink():
            raise ValueError(f"canonical skill domain symlink is not supported: {domain_dir}")
        if not domain_dir.is_dir():
            continue
        for skill_dir in sorted(domain_dir.iterdir()):
            if skill_dir.is_symlink():
                raise ValueError(f"canonical skill directory symlink is not supported: {skill_dir}")
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if skill_md.is_symlink():
                raise ValueError(f"canonical SKILL.md symlink is not supported: {skill_md}")
            if skill_md.is_file():
                results.append((skill_dir.name, skill_dir))
    return results


# ---------------------------------------------------------------------------
# Distribution manifest
# ---------------------------------------------------------------------------

def _build_manifest(
    skill_name: str,
    fm: dict,
    source_path: Path,
    generated_paths: list[str],
    source_content: bytes | None = None,
) -> dict:
    artifact_id = f"skill/{skill_name}"
    artifact_version = (fm.get("metadata") or {}).get("aether-version", "0.0.0")
    compatibility = fm.get("compatibility") or {"required_tools": []}
    if "required_tools" not in compatibility:
        compatibility = {"required_tools": [], **compatibility}

    return {
        "schema_version": "aether.distribution-manifest/v1",
        "distribution_id": f"distribution/{skill_name}",
        "artifact_id": artifact_id,
        "artifact_version": artifact_version,
        "source_digest": {
            "algorithm": "sha256-utf8-lf",
            "value": hashlib.sha256(source_content).hexdigest() if source_content is not None else _source_digest(source_path),
        },
        "generated_paths": generated_paths,
        "generator": GENERATOR_ID,
        "compatibility": compatibility,
    }


# ---------------------------------------------------------------------------
# Per-skill distribution
# ---------------------------------------------------------------------------

def _companion_sources(source_dir: Path) -> list[Path]:
    found: list[Path] = []

    def fail_scan(error: OSError) -> None:
        raise error

    for companion in COMPANION_DIRS:
        root = source_dir / companion
        if root.is_symlink():
            raise ValueError(f"companion directory symlink is not supported: {root}")
        if not root.exists():
            continue
        _canonical_source(root, source_dir, directory=True)
        for parent, directories, files in os.walk(root, onerror=fail_scan, followlinks=False):
            directories[:] = sorted(name for name in directories if name != "__pycache__")
            for name in directories:
                path = Path(parent) / name
                if path.is_symlink():
                    raise ValueError(f"companion directory symlink is not supported: {path}")
            for name in sorted(files):
                path = Path(parent) / name
                if path.suffix in {".pyc", ".pyo"}:
                    continue
                _canonical_source(path, source_dir)
                found.append(path)
    return sorted(found, key=lambda path: (COMPANION_DIRS.index(path.relative_to(source_dir).parts[0]), path.as_posix()))


def _collect_generated_paths(skill_name: str, source_dir: Path, frontmatter: dict) -> list[str]:
    paths = [f"dist/skills/{skill_name}/SKILL.md"]
    paths.extend(f"dist/skills/{skill_name}/{path.relative_to(source_dir).as_posix()}" for path in _companion_sources(source_dir))
    paths.extend(f"dist/skills/{skill_name}/{destination.as_posix()}" for _, destination in _distribution_resources(frontmatter))
    paths.append(f"dist/skills/{skill_name}/distribution-manifest.v1.json")
    return paths


def _is_companion_source(path: Path, source_dir: Path) -> bool:
    relative = path.relative_to(source_dir)
    if "__pycache__" in relative.parts or path.suffix in {".pyc", ".pyo"}:
        return False
    _canonical_source(path, source_dir)
    return True


def _build_skill_dist(skill_name: str, source_dir: Path) -> dict[str, bytes]:
    if STABLE_ID_RE.fullmatch(skill_name) is None:
        raise ValueError("skill id must be a lowercase kebab-case stable identifier")
    source_md = _canonical_source(source_dir / "SKILL.md", source_dir)
    source_content = _normalized_bytes(source_md)
    fm = _read_frontmatter(source_md, source_content)
    if fm.get("name") != skill_name:
        raise ValueError("skill frontmatter name must match its canonical directory")
    companions = _companion_sources(source_dir)
    resources = _distribution_resources(fm)
    prefix = f"dist/skills/{skill_name}/"
    manifest_path = prefix + "distribution-manifest.v1.json"
    paths = [prefix + "SKILL.md"]
    paths.extend(prefix + path.relative_to(source_dir).as_posix() for path in companions)
    resource_paths = [prefix + destination.as_posix() for _, destination in resources]
    if set(paths).intersection(resource_paths) or manifest_path in resource_paths:
        raise ValueError("explicit resource destination collides with owned skill output")
    paths.extend(resource_paths)
    paths.append(manifest_path)
    out = {prefix + "SKILL.md": source_content}
    for path in companions:
        out[prefix + path.relative_to(source_dir).as_posix()] = path.read_bytes()
    for source, destination in resources:
        out[prefix + destination.as_posix()] = source.read_bytes()
    manifest = _build_manifest(skill_name, fm, source_md, paths, source_content)
    out[manifest_path] = (_canonical_json(manifest) + "\n").encode("utf-8")
    return out


# ---------------------------------------------------------------------------
# Build / check
# ---------------------------------------------------------------------------

def _report_unexpected(dist_dir: Path, expected_files: set[Path]) -> int:
    """Compare the complete owned subtree, including empty directories.

    Unknown files are evidence to review, never implicit deletion candidates.
    Other generators' subtrees and files beside this subtree are not inspected.
    """
    expected_entries = set(expected_files)
    for path in expected_files:
        expected_entries.update(
            parent for parent in path.parents
            if parent != dist_dir and dist_dir in parent.parents
        )
    if not dist_dir.exists():
        return 0

    def fail_scan(error: OSError) -> None:
        raise error

    unexpected = 0
    for parent, directories, files in os.walk(dist_dir, onerror=fail_scan, followlinks=False):
        directories.sort()
        for name in sorted(directories + files):
            path = Path(parent) / name
            if path not in expected_entries:
                print(f"DRIFT  unexpected (retained): {_normalized_display_path(path)}")
                unexpected += 1
    return unexpected


def build(check: bool = False, output_directory: Path | None = None) -> int:
    try:
        output_base = (output_directory or (REPO_ROOT / "dist")).resolve()
        dist_dir = _confined_output(output_base, Path("skills"))
        skills = find_skills()
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR  skills discovery: {exc}", file=sys.stderr)
        return 1
    if not skills:
        print("WARNING: no SKILL.md files found under library/organization/skills/", file=sys.stderr)

    drift = errors = written = generated = 0
    expected_files: set[Path] = set()
    for skill_name, source_dir in skills:
        try:
            file_map = _build_skill_dist(skill_name, source_dir)
            output_map = {
                _confined_output(output_base, Path(path).relative_to("dist")): content
                for path, content in file_map.items()
            }
            if expected_files.intersection(output_map):
                raise ValueError("output inventory collides with another skill")
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR  skill {skill_name} generation: {exc}", file=sys.stderr)
            errors += 1
            continue

        generated += 1
        expected_files.update(output_map)
        for out_path, content in output_map.items():
            display_path = _normalized_display_path(out_path)
            try:
                out_path = _confined_output(output_base, out_path.relative_to(output_base))
                if check:
                    if not out_path.exists():
                        print(f"DRIFT  missing: {display_path}")
                        drift += 1
                    elif out_path.read_bytes() != content:
                        print(f"DRIFT  stale:   {display_path}")
                        drift += 1
                    else:
                        print(f"OK     {display_path}")
                else:
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    out_path.write_bytes(content)
                    print(f"wrote  {display_path}")
                    written += 1
            except (OSError, ValueError, RuntimeError) as exc:
                print(f"ERROR  skill {skill_name} output {display_path}: {exc}", file=sys.stderr)
                errors += 1

    try:
        unexpected = _report_unexpected(dist_dir, expected_files)
    except OSError as exc:
        print(f"ERROR  skills inventory: {exc}", file=sys.stderr)
        errors += 1
        unexpected = 0

    if errors or drift or unexpected:
        print(
            f"\nSkill distributions incomplete: {generated}/{len(skills)} artifact(s) generated, "
            f"{written} file(s) written, {errors} error(s), {drift} missing/stale file(s), "
            f"{unexpected} unexpected path(s) retained. Review errors and inventory before reuse.",
            file=sys.stderr,
        )
        return 1
    if check:
        print(f"\nAll {len(skills)} skill distribution(s) are up to date.")
    else:
        print(f"\n{written} file(s) written for {generated} skill(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Detect drift without writing files",
    )
    parser.add_argument(
        "--output-directory",
        default="dist",
        help="Base output directory for generated distributions.",
    )
    args = parser.parse_args()
    return build(check=args.check, output_directory=(REPO_ROOT / args.output_directory))


def _normalized_display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    sys.exit(main())
