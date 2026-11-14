#!/usr/bin/env python3
"""Build deterministic portable specification distributions from canonical source.

Usage:
    python3 library/organization/specs/build-distributions.py [--check] [--output-directory dist]
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path, PureWindowsPath

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
SPECS_DIR = REPO_ROOT / "library" / "organization" / "specs"
STABLE_ID_RE = re.compile(r"^[a-z](?:[a-z0-9-]*[a-z0-9])?$")
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _normalized_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _display_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


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


def find_specs() -> list[Path]:
    _canonical_source(SPECS_DIR, SPECS_DIR, directory=True)
    found: list[Path] = []

    def fail_scan(error: OSError) -> None:
        raise error

    for parent, directories, files in os.walk(SPECS_DIR, onerror=fail_scan, followlinks=False):
        directories.sort()
        for name in directories + sorted(files):
            path = Path(parent) / name
            if path.is_symlink():
                raise ValueError(f"canonical specification symlink is not supported: {path}")
        found.extend(Path(parent) / name for name in sorted(files) if name.endswith(".spec.md"))
    return sorted(found)


def _spec_distribution(source_path: Path) -> tuple[str, bytes]:
    source = _canonical_source(source_path, SPECS_DIR)
    content = _normalized_bytes(source)
    match = FRONTMATTER_RE.match(content.decode("utf-8"))
    if not match:
        raise ValueError(f"missing YAML frontmatter in {source_path}")
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter in {source_path}") from exc
    spec_id = frontmatter.get("id") if isinstance(frontmatter, dict) else None
    if not isinstance(spec_id, str) or STABLE_ID_RE.fullmatch(spec_id) is None:
        raise ValueError("specification id must be a lowercase kebab-case stable identifier")
    return f"{spec_id}.spec.md", content


def _distribution_filename(source_path: Path) -> str:
    return _spec_distribution(source_path)[0]


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
                print(f"DRIFT  unexpected (retained): {_display_path(path)}")
                unexpected += 1
    return unexpected


def build(check: bool = False, output_directory: Path | None = None) -> int:
    try:
        output_base = (output_directory or (REPO_ROOT / "dist")).resolve()
        dist_dir = _confined_output(output_base, Path("specs"))
        if not SPECS_DIR.is_dir():
            raise OSError("canonical specification directory is missing")
        specs = find_specs()
    except (OSError, ValueError, RuntimeError) as exc:
        print(f"ERROR  specs discovery: {exc}", file=sys.stderr)
        return 1
    if not specs:
        print("WARNING: no *.spec.md files found under library/organization/specs/", file=sys.stderr)

    drift = errors = written = generated = 0
    expected_files: set[Path] = set()
    for source_path in specs:
        try:
            filename, content = _spec_distribution(source_path)
            out_path = _confined_output(output_base, Path("specs") / filename)
            if out_path in expected_files:
                raise ValueError("output inventory collides with another specification")
        except (OSError, ValueError, RuntimeError) as exc:
            print(f"ERROR  spec {_display_path(source_path)} generation: {exc}", file=sys.stderr)
            errors += 1
            continue
        generated += 1
        expected_files.add(out_path)
        display_path = _display_path(out_path)
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
            print(f"ERROR  spec {_display_path(source_path)} output {display_path}: {exc}", file=sys.stderr)
            errors += 1

    try:
        unexpected = _report_unexpected(dist_dir, expected_files)
    except OSError as exc:
        print(f"ERROR  specs inventory: {exc}", file=sys.stderr)
        errors += 1
        unexpected = 0

    if errors or drift or unexpected:
        print(
            f"\nSpecification distributions incomplete: {generated}/{len(specs)} artifact(s) generated, "
            f"{written} file(s) written, {errors} error(s), {drift} missing/stale file(s), "
            f"{unexpected} unexpected path(s) retained. Review errors and inventory before reuse.",
            file=sys.stderr,
        )
        return 1
    if check:
        print(f"\nAll {len(specs)} specification distribution(s) are up to date.")
    else:
        print(f"\n{written} file(s) written for {generated} specification(s).")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Detect drift without writing files")
    parser.add_argument(
        "--output-directory",
        default="dist",
        help="Base output directory for generated distributions.",
    )
    args = parser.parse_args()
    return build(check=args.check, output_directory=(REPO_ROOT / args.output_directory))


if __name__ == "__main__":
    sys.exit(main())
