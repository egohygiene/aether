#!/usr/bin/env python3
"""Build deterministic release metadata for first-party skill publications.

Usage:
    python3 library/organization/skills/build-release-artifacts.py \
        --release-tag v1.2.3 [--output-directory dist] [--commit-sha <sha>]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import io
import json
import re
import stat
import sys
import tarfile
from pathlib import Path, PurePosixPath

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[3]
CATALOG_PATH = REPO_ROOT / "catalog" / "first-party" / "catalog.v1.json"
RELEASE_SCHEMA_PATH = REPO_ROOT / "catalog" / "schemas" / "aether.release-manifest.v1.schema.json"
LICENSE_PATH = REPO_ROOT / "LICENSE"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
SOCIAL_SURFACE_CATALOG_PATH = REPO_ROOT / "catalog" / "social-surfaces" / "catalog.v1.json"
METADATA_FILES = ("release-manifest.v1.json", "LICENSE.notices.txt", "release-notes.md",
                  "release-provenance.v1.json", "checksums.txt")


def _canonical_json(data: object) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_release_records(catalog_path: Path) -> list[dict]:
    catalog = _read_json(catalog_path)
    records = []
    for record in catalog.get("artifacts", []):
        if record.get("kind") != "skill":
            continue
        if ((record.get("lifecycle") or {}).get("state")) != "stable":
            continue
        if (record.get("release") or {}).get("included") is not True:
            continue
        records.append(record)
    return sorted(records, key=lambda item: item["id"])


def _load_distribution_manifest(output_directory: Path, skill_name: str) -> dict:
    manifest_path = (
        output_directory
        / "skills"
        / skill_name
        / "distribution-manifest.v1.json"
    )
    if not manifest_path.exists():
        raise ValueError(f"missing distribution manifest: {manifest_path}")
    return _read_json(_regular_file(output_directory, f"skills/{skill_name}/distribution-manifest.v1.json"))


def _load_release_catalogs(output_directory: Path) -> list[dict]:
    """Return stable, rights-approved catalogs eligible for this release."""
    catalog = _read_json(SOCIAL_SURFACE_CATALOG_PATH)
    metadata = catalog.get("catalog") if isinstance(catalog.get("catalog"), dict) else {}
    lifecycle = metadata.get("lifecycle") if isinstance(metadata.get("lifecycle"), dict) else {}
    rights_review = metadata.get("rights_review") if isinstance(metadata.get("rights_review"), dict) else {}
    release = metadata.get("release") if isinstance(metadata.get("release"), dict) else {}
    if not (
        lifecycle.get("state") == "stable"
        and rights_review.get("state") == "approved"
        and release.get("included") is True
    ):
        return []

    catalog_name = str(metadata.get("id", "")).split("/", 1)[-1]
    manifest_path = output_directory / "catalogs" / catalog_name / "distribution-manifest.v1.json"
    if not manifest_path.exists():
        raise ValueError(f"missing catalog distribution manifest: {manifest_path}")
    manifest = _read_json(_regular_file(output_directory, f"catalogs/{catalog_name}/distribution-manifest.v1.json"))
    catalog_digest = manifest.get("catalog_digest") or {}
    if manifest.get("catalog_id") != metadata.get("id"):
        raise ValueError("catalog distribution id does not match canonical catalog")
    if manifest.get("catalog_version") != metadata.get("version"):
        raise ValueError("catalog distribution version does not match canonical catalog")
    return [{
        "catalog_id": metadata["id"],
        "catalog_version": metadata["version"],
        "catalog_digest": catalog_digest,
    }]


def _build_release_manifest(release_tag: str, records: list[dict], output_directory: Path) -> dict:
    artifacts = []
    for record in records:
        skill_name = record["id"].split("/", 1)[1]
        dist_manifest = _load_distribution_manifest(output_directory, skill_name)
        if dist_manifest.get("artifact_id") != record["id"]:
            raise ValueError(
                f"distribution artifact mismatch for {record['id']}: "
                f"{dist_manifest.get('artifact_id')!r}"
            )
        if dist_manifest.get("artifact_version") != record["artifact_version"]:
            raise ValueError(
                f"distribution version mismatch for {record['id']}: "
                f"{dist_manifest.get('artifact_version')!r}"
            )
        if (dist_manifest.get("source_digest") or {}).get("value") != (
            (record.get("source_digest") or {}).get("value")
        ):
            raise ValueError(f"distribution source digest mismatch for {record['id']}")
        artifacts.append(
            {
                "artifact_id": record["id"],
                "artifact_version": record["artifact_version"],
                "source_digest": dist_manifest["source_digest"],
            }
        )

    if not artifacts:
        raise ValueError(
            "no release-eligible first-party skills found; "
            "only catalog records with lifecycle.state=stable and release.included=true may be released"
        )

    manifest = {
        "schema_version": "aether.release-manifest/v1",
        "repository_release_tag": release_tag,
        "artifacts": artifacts,
    }
    catalogs = _load_release_catalogs(output_directory)
    if catalogs:
        manifest["catalogs"] = catalogs
    return manifest


def _validate_release_manifest(release_manifest: dict, schema_path: Path) -> None:
    schema = _read_json(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(release_manifest), key=lambda err: list(err.path))
    if errors:
        raise ValueError(f"release manifest failed schema validation: {errors[0].message}")


def _regular_file(root: Path, relative: str) -> Path:
    """Refuse manifest escapes, links and special files before reading bytes."""
    parts = PurePosixPath(relative).parts
    if (not relative or "\\" in relative or relative.startswith("/")
            or any(ord(character) < 32 or ord(character) == 127 for character in relative)
            or any(part in {"", ".", ".."} for part in relative.split("/"))
            or PurePosixPath(relative).as_posix() != relative):
        raise ValueError(f"unsafe release path: {relative!r}")
    current = root
    if root.is_symlink() or not root.is_dir():
        raise ValueError("release input must be a real directory")
    for index, part in enumerate(parts):
        current = current / part
        mode = current.lstat().st_mode
        expected = stat.S_ISREG if index == len(parts) - 1 else stat.S_ISDIR
        if not expected(mode):
            raise ValueError(f"release input is not an ordinary file/directory: {relative!r}")
    return current


def _selected_payload_paths(output_directory: Path, manifest: dict) -> list[str]:
    """Use only the release-selected distribution inventories, never all dist/."""
    selected: set[str] = set()
    packages = [("skills", item["artifact_id"].split("/", 1)[1])
                for item in manifest["artifacts"]]
    packages.extend(("catalogs", item["catalog_id"].split("/", 1)[1])
                    for item in manifest.get("catalogs", []))
    for family, name in packages:
        prefix = f"{family}/{name}/"
        manifest_path = prefix + "distribution-manifest.v1.json"
        distribution = _read_json(_regular_file(output_directory, manifest_path))
        paths = distribution.get("generated_paths")
        if not isinstance(paths, list) or not paths or not all(isinstance(p, str) for p in paths):
            raise ValueError(f"missing generated_paths inventory: {manifest_path}")
        if len(paths) != len(set(paths)) or f"dist/{manifest_path}" not in paths:
            raise ValueError(f"invalid generated_paths inventory: {manifest_path}")
        if family == "skills" and f"dist/{prefix}SKILL.md" not in paths:
            raise ValueError(f"missing selected skill entry point: {manifest_path}")
        for path in paths:
            if not path.startswith(f"dist/{prefix}"):
                raise ValueError(f"release inventory escapes its selected package: {path!r}")
            relative = path.removeprefix("dist/")
            _regular_file(output_directory, relative)
            if relative in selected:
                raise ValueError(f"duplicate release path: {relative}")
            selected.add(relative)
    return sorted(selected)


def _build_checksums(output_directory: Path, paths: list[str]) -> str:
    return "".join(f"{_sha256_file(_regular_file(output_directory, path))}  {path}\n"
                   for path in sorted(paths))


def _build_license_notices(records: list[dict], license_path: Path) -> str:
    header = [
        "Aether release license notices",
        "",
        "Repository license file: LICENSE",
        "",
        "Included first-party skills:",
        "",
    ]
    for record in records:
        header.append(
            f"- {record['id']} | version {record['artifact_version']} | license {record.get('license', 'UNKNOWN')}"
        )
    header.extend(
        [
            "",
            "--- LICENSE BEGIN ---",
            license_path.read_text(encoding="utf-8").rstrip(),
            "--- LICENSE END ---",
            "",
        ]
    )
    return "\n".join(header)


def _extract_unreleased_changelog(changelog_path: Path) -> str:
    lines = changelog_path.read_text(encoding="utf-8").splitlines()
    capture = []
    active = False
    for line in lines:
        if line in {"## [Unreleased]", "## Unreleased"}:
            active = True
            capture.append(line)
            continue
        if active and line.startswith("## "):
            break
        if active:
            capture.append(line)
    return "\n".join(capture).strip()


def _build_release_notes(release_tag: str, release_manifest: dict, changelog_path: Path) -> str:
    artifact_lines = [
        f"- `{artifact['artifact_id']}` @ `{artifact['artifact_version']}`"
        for artifact in release_manifest["artifacts"]
    ]
    changelog_excerpt = _extract_unreleased_changelog(changelog_path)
    lines = [
        f"# Release notes for {release_tag}",
        "",
        "This release is published explicitly from a tagged commit after deterministic validation.",
        "",
        "## Included first-party skills",
        *artifact_lines,
    ]
    catalog_lines = [
        f"- `{catalog['catalog_id']}` @ `{catalog['catalog_version']}`"
        for catalog in release_manifest.get("catalogs", [])
    ]
    if catalog_lines:
        lines.extend(["", "## Included governed catalogs", *catalog_lines])
    if changelog_excerpt:
        lines.extend(["", "## Changelog excerpt", changelog_excerpt])
    lines.append("")
    return "\n".join(lines)


def _build_provenance(
    release_tag: str,
    commit_sha: str,
    release_manifest: dict,
    output_directory: Path,
    paths: list[str],
) -> dict:
    output_files = []
    for relative in sorted(paths):
        output_files.append({"path": relative,
                             "sha256": _sha256_file(_regular_file(output_directory, relative))})
    return {
        "schema_version": "aether.release-provenance/v1",
        "repository_release_tag": release_tag,
        "commit_sha": commit_sha,
        "artifacts": release_manifest["artifacts"],
        "output_files": output_files,
    }


def build_release_artifacts(
    release_tag: str,
    output_directory: Path,
    commit_sha: str,
) -> Path:
    if not re.fullmatch(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", release_tag):
        raise ValueError("release tag must be exact vMAJOR.MINOR.PATCH")
    if not re.fullmatch(r"[0-9a-f]{40}", commit_sha):
        raise ValueError("release provenance requires a full immutable source SHA")
    records = _load_release_records(CATALOG_PATH)
    release_dir = output_directory / "release"
    release_manifest = _build_release_manifest(release_tag, records, output_directory)
    _validate_release_manifest(release_manifest, RELEASE_SCHEMA_PATH)
    payload_paths = _selected_payload_paths(output_directory, release_manifest)
    # Unknown prior outputs are retained but cannot become new release inputs.
    # Known metadata paths must also refuse symlinks and special files.
    if release_dir.is_symlink():
        raise ValueError("release metadata directory must not be a symlink")
    release_dir.mkdir(parents=True, exist_ok=True)
    for name in METADATA_FILES:
        path = release_dir / name
        if path.is_symlink() or (path.exists() and not stat.S_ISREG(path.lstat().st_mode)):
            raise ValueError(f"unsafe release metadata output: {name}")

    (release_dir / "release-manifest.v1.json").write_text(
        _canonical_json(release_manifest),
        encoding="utf-8",
    )
    (release_dir / "LICENSE.notices.txt").write_text(
        _build_license_notices(records, LICENSE_PATH),
        encoding="utf-8",
    )
    (release_dir / "release-notes.md").write_text(
        _build_release_notes(release_tag, release_manifest, CHANGELOG_PATH),
        encoding="utf-8",
    )
    provenance_inputs = payload_paths + [f"release/{name}" for name in METADATA_FILES[:3]]
    (release_dir / "release-provenance.v1.json").write_text(
        _canonical_json(_build_provenance(release_tag, commit_sha, release_manifest,
                                          output_directory, provenance_inputs)),
        encoding="utf-8",
    )
    (release_dir / "checksums.txt").write_text(
        _build_checksums(output_directory, provenance_inputs + ["release/release-provenance.v1.json"]),
        encoding="utf-8",
    )
    return release_dir


def build_release_payload(output_directory: Path, payload_directory: Path, archive: Path) -> None:
    """Materialize the exact selected channel payload and a reproducible archive.

    New destinations prevent overwriting an unrelated caller-owned tree. The
    archive lives outside the payload, avoiding archive/checksum recursion.
    """
    source = output_directory.resolve()
    payload = payload_directory.resolve()
    archive_path = archive.resolve()
    if (source == payload or source in payload.parents or payload in source.parents
            or payload == archive_path or payload in archive_path.parents):
        raise ValueError("payload must be separate from dist and archive must be outside payload")
    if payload_directory.is_symlink() or payload.exists() or archive.is_symlink() or archive_path.exists():
        raise ValueError("payload and archive destinations must be unused")
    manifest = _read_json(_regular_file(output_directory, "release/release-manifest.v1.json"))
    _validate_release_manifest(manifest, RELEASE_SCHEMA_PATH)
    paths = _selected_payload_paths(output_directory, manifest)
    paths.extend(f"release/{name}" for name in METADATA_FILES)
    # Check the entire inventory before creating either destination.
    sources = {path: _regular_file(output_directory, path) for path in paths}
    contents = {path: source_path.read_bytes() for path, source_path in sources.items()}
    checksums: dict[str, str] = {}
    for line in contents["release/checksums.txt"].decode("utf-8").splitlines():
        digest, separator, relative = line.partition("  ")
        if not separator or not re.fullmatch(r"[a-f0-9]{64}", digest) or relative in checksums:
            raise ValueError("release checksums are malformed")
        checksums[relative] = digest
    expected_checksums = {path: hashlib.sha256(content).hexdigest()
                          for path, content in contents.items() if path != "release/checksums.txt"}
    if checksums != expected_checksums:
        raise ValueError("release checksums differ from selected payload bytes")
    provenance = json.loads(contents["release/release-provenance.v1.json"])
    expected_inputs = [{"path": path, "sha256": digest}
                       for path, digest in sorted(expected_checksums.items())
                       if path != "release/release-provenance.v1.json"]
    if (provenance.get("output_files") != expected_inputs
            or provenance.get("repository_release_tag") != manifest["repository_release_tag"]
            or provenance.get("artifacts") != manifest["artifacts"]
            or not re.fullmatch(r"[a-f0-9]{40}", provenance.get("commit_sha", ""))):
        raise ValueError("release provenance differs from selected payload")
    payload.mkdir(parents=True)
    for relative, source_path in sources.items():
        target = payload / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(contents[relative])
        target.chmod(0o755 if source_path.stat().st_mode & 0o111 else 0o644)
    archive_path.parent.mkdir(parents=True, exist_ok=True)
    with archive_path.open("xb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.USTAR_FORMAT) as bundle:
                for relative in sorted(paths):
                    content = contents[relative]
                    item = tarfile.TarInfo(relative)
                    item.size = len(content)
                    item.mode = (payload / relative).stat().st_mode & 0o777
                    bundle.addfile(item, io.BytesIO(content))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--release-tag", required=True, help="Repository release tag.")
    parser.add_argument(
        "--output-directory",
        default="dist",
        help="Base output directory containing generated release payloads.",
    )
    parser.add_argument(
        "--commit-sha",
        required=True,
        help="Commit SHA used to build the release payload.",
    )
    parser.add_argument("--payload-directory", help="Unused directory for the selected publication payload.")
    parser.add_argument("--archive", help="Unused archive path outside the publication payload.")
    args = parser.parse_args(argv)
    if bool(args.payload_directory) != bool(args.archive):
        parser.error("--payload-directory and --archive must be supplied together")

    try:
        release_dir = build_release_artifacts(
            release_tag=args.release_tag,
            output_directory=REPO_ROOT / args.output_directory,
            commit_sha=args.commit_sha,
        )
        if args.payload_directory:
            build_release_payload(REPO_ROOT / args.output_directory,
                                  REPO_ROOT / args.payload_directory, REPO_ROOT / args.archive)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"Wrote release metadata to {release_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
