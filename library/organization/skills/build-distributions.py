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
from pathlib import Path

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


def _read_frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError(f"no YAML frontmatter in {path}")
    return yaml.safe_load(m.group(1)) or {}


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
        if source_relative.is_absolute() or ".." in source_relative.parts:
            raise ValueError(f"distribution resource source escapes repository: {source_value}")
        if destination.is_absolute() or ".." in destination.parts or destination == Path("."):
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

def find_skills() -> list[tuple[str, Path]]:
    """Return sorted list of (skill-name, source-dir) for every canonical skill."""
    results = []
    for domain_dir in sorted(SKILLS_DIR.iterdir()):
        if not domain_dir.is_dir():
            continue
        for skill_dir in sorted(domain_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
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
            "value": _source_digest(source_path),
        },
        "generated_paths": generated_paths,
        "generator": GENERATOR_ID,
        "compatibility": compatibility,
    }


# ---------------------------------------------------------------------------
# Per-skill distribution
# ---------------------------------------------------------------------------

def _collect_generated_paths(skill_name: str, source_dir: Path, frontmatter: dict) -> list[str]:
    """Enumerate all paths that will be written to dist/skills/<name>/."""
    paths = [f"dist/skills/{skill_name}/SKILL.md"]
    for companion in COMPANION_DIRS:
        src = source_dir / companion
        if src.is_dir():
            for f in sorted(src.rglob("*")):
                if _is_companion_source(f, source_dir):
                    rel = f.relative_to(source_dir)
                    paths.append(f"dist/skills/{skill_name}/{rel.as_posix()}")
    for _source, destination in _distribution_resources(frontmatter):
        paths.append(f"dist/skills/{skill_name}/{destination.as_posix()}")
    paths.append(f"dist/skills/{skill_name}/distribution-manifest.v1.json")
    return paths


def _is_companion_source(path: Path, source_dir: Path) -> bool:
    """Exclude interpreter output so running a skill cannot change its package."""
    relative = path.relative_to(source_dir)
    return (
        path.is_file()
        and "__pycache__" not in relative.parts
        and path.suffix not in {".pyc", ".pyo"}
    )


def _build_skill_dist(skill_name: str, source_dir: Path) -> dict[str, bytes]:
    """Return mapping of relative-to-repo-root path → file bytes for one skill."""
    source_md = source_dir / "SKILL.md"
    fm = _read_frontmatter(source_md)
    generated_paths = _collect_generated_paths(skill_name, source_dir, fm)

    out: dict[str, bytes] = {}

    # SKILL.md — copied verbatim
    out[f"dist/skills/{skill_name}/SKILL.md"] = _normalized_bytes(source_md)

    # companion directories — copied verbatim
    for companion in COMPANION_DIRS:
        src = source_dir / companion
        if src.is_dir():
            for f in sorted(src.rglob("*")):
                if _is_companion_source(f, source_dir):
                    rel = f.relative_to(source_dir)
                    out[f"dist/skills/{skill_name}/{rel.as_posix()}"] = f.read_bytes()

    for source, destination in _distribution_resources(fm):
        out[f"dist/skills/{skill_name}/{destination.as_posix()}"] = source.read_bytes()

    # distribution manifest
    manifest = _build_manifest(skill_name, fm, source_md, generated_paths)
    manifest_bytes = (_canonical_json(manifest) + "\n").encode("utf-8")
    out[f"dist/skills/{skill_name}/distribution-manifest.v1.json"] = manifest_bytes

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
    dist_dir = (output_directory or (REPO_ROOT / "dist")) / "skills"
    try:
        skills = find_skills()
    except OSError as exc:
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
                dist_dir / Path(path).relative_to("dist/skills"): content
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
            except OSError as exc:
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
