#!/usr/bin/env python3
"""Deterministic validator for v1 catalog contracts."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = ROOT / "catalog"
SCHEMAS_DIR = CATALOG_DIR / "schemas"
FIXTURES_DIR = CATALOG_DIR / "fixtures"
CATALOG_PATH = CATALOG_DIR / "first-party" / "catalog.v1.json"
EXTERNAL_SOURCE_CANDIDATES_PATH = CATALOG_DIR / "external" / "source-candidates.v1.json"
SOCIAL_SURFACE_CATALOG_PATH = CATALOG_DIR / "social-surfaces" / "catalog.v1.json"
SOCIAL_SURFACE_VALIDATOR_PATH = CATALOG_DIR / "social-surfaces" / "validate.py"

SCHEMA_FILES = [
    "aether.artifact-record.v1.schema.json",
    "aether.artifact-catalog.v1.schema.json",
    "aether.external-source-record.v1.schema.json",
    "aether.distribution-manifest.v1.schema.json",
    "aether.release-manifest.v1.schema.json",
    "aether.staging-disposition-record.v1.schema.json",
    "aether.evaluation-definition.v1.schema.json",
    "aether.evaluation-result.v1.schema.json",
    "aether.social-surface-catalog.v1.schema.json",
    "aether.social-campaign-handoff.v1.schema.json",
    "aether.catalog-distribution-manifest.v1.schema.json",
]

SKILLS_DIR = ROOT / "library" / "organization" / "skills"
SPECS_DIR = ROOT / "library" / "organization" / "specs"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_json_bytes(data) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def normalized_text_bytes(path: Path) -> bytes:
    text = path.read_text(encoding="utf-8")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return text.encode("utf-8")


def source_digest(path: Path) -> str:
    return hashlib.sha256(normalized_text_bytes(path)).hexdigest()


def build_validators():
    validators = {}
    for sf in SCHEMA_FILES:
        schema = load_json(SCHEMAS_DIR / sf)
        validators[sf.removesuffix(".json")] = Draft202012Validator(schema)
    return validators


def validate_fixtures(validators):
    errors = []
    for key, validator in validators.items():
        fixture_dir = FIXTURES_DIR / key
        valid = load_json(fixture_dir / "valid.json")
        invalid = load_json(fixture_dir / "invalid.json")

        valid_errors = list(validator.iter_errors(valid))
        if valid_errors:
            errors.append(f"Fixture should be valid: {key}/valid.json -> {valid_errors[0].message}")

        invalid_errors = list(validator.iter_errors(invalid))
        if not invalid_errors:
            errors.append(f"Fixture should be invalid: {key}/invalid.json")
    return errors


def validate_catalog(validators):
    errors = []
    catalog = load_json(CATALOG_PATH)
    schema_validator = validators["aether.artifact-catalog.v1.schema"]

    schema_errors = list(schema_validator.iter_errors(catalog))
    for err in schema_errors:
        errors.append(f"Catalog schema violation at {'/'.join(map(str, err.path)) or '<root>'}: {err.message}")

    artifacts = catalog.get("artifacts", [])
    ids = [a.get("id") for a in artifacts]
    if len(ids) != len(set(ids)):
        errors.append("Catalog IDs are not unique")

    spec_files = sorted(SPECS_DIR.rglob("*.spec.md"))
    skill_files = sorted(SKILLS_DIR.rglob("SKILL.md"))
    expected_paths = {str(p.relative_to(ROOT)) for p in spec_files + skill_files}

    by_path = {}
    for a in artifacts:
        path = a.get("source_path")
        by_path.setdefault(path, []).append(a.get("id"))

    if set(by_path.keys()) != expected_paths:
        missing = sorted(expected_paths - set(by_path.keys()))
        extra = sorted(set(by_path.keys()) - expected_paths)
        if missing:
            errors.append(f"Catalog missing canonical paths: {missing}")
        if extra:
            errors.append(f"Catalog has non-canonical paths: {extra}")

    for path, recs in sorted(by_path.items()):
        if len(recs) != 1:
            errors.append(f"Path appears {len(recs)} times in catalog: {path}")

    spec_count = sum(1 for a in artifacts if a.get("kind") == "specification")
    skill_count = sum(1 for a in artifacts if a.get("kind") == "skill")
    if spec_count != len(spec_files):
        errors.append(f"Expected {len(spec_files)} specification records, got {spec_count}")
    if skill_count != len(skill_files):
        errors.append(f"Expected {len(skill_files)} skill records, got {skill_count}")

    id_set = set(ids)
    for a in artifacts:
        for key in ("dependencies", "related_ids", "supersedes_ids"):
            for target in a.get(key, []):
                if target not in id_set:
                    errors.append(f"Unresolved relationship target '{target}' in {a.get('id')}")

        replacement = (a.get("deprecation") or {}).get("replacement_id")
        if replacement is not None and replacement not in id_set:
            errors.append(f"Unresolved deprecation replacement '{replacement}' in {a.get('id')}")

        src = ROOT / a.get("source_path", "")
        if not src.exists():
            errors.append(f"Missing source path: {a.get('source_path')}")
            continue

        expected_digest = source_digest(src)
        actual_digest = ((a.get("source_digest") or {}).get("value"))
        if expected_digest != actual_digest:
            errors.append(f"Digest mismatch for {a.get('id')}: expected {expected_digest}, got {actual_digest}")

    snapshot_1 = subprocess.check_output(
        [sys.executable, str(Path(__file__).resolve()), "--print-digest-snapshot"],
        text=True,
    ).strip()
    snapshot_2 = subprocess.check_output(
        [sys.executable, str(Path(__file__).resolve()), "--print-digest-snapshot"],
        text=True,
    ).strip()
    if snapshot_1 != snapshot_2:
        errors.append("Determinism failure: snapshots differ across consecutive runs")

    return errors


def validate_external_source_candidates(validators):
    errors = []
    candidate_catalog = load_json(EXTERNAL_SOURCE_CANDIDATES_PATH)
    if candidate_catalog.get("schema_version") != "aether.external-source-candidates/v1":
        errors.append("External source candidates use an unexpected schema version")
    entries = candidate_catalog.get("entries")
    if not isinstance(entries, list):
        return errors + ["External source candidates entries must be an array"]
    identifiers = [entry.get("id") for entry in entries if isinstance(entry, dict)]
    if identifiers != sorted(identifiers):
        errors.append("External source candidate records must be sorted by id")
    if len(identifiers) != len(set(identifiers)):
        errors.append("External source candidate record IDs are not unique")
    validator = validators["aether.external-source-record.v1.schema"]
    for entry in entries:
        for error in validator.iter_errors(entry):
            errors.append(f"External source candidate schema violation: {error.message}")
    return errors


def validate_social_surface_catalog():
    result = subprocess.run(
        [sys.executable, str(SOCIAL_SURFACE_VALIDATOR_PATH), "--catalog", str(SOCIAL_SURFACE_CATALOG_PATH)],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return []
    detail = (result.stderr or result.stdout).strip() or "unknown social-surface catalog validation failure"
    return [f"Social-surface catalog validation failed: {detail}"]


def main() -> int:
    if "--print-digest-snapshot" in sys.argv:
        catalog = load_json(CATALOG_PATH)
        artifacts = catalog.get("artifacts", [])
        snapshot = {
            "catalog_digest": hashlib.sha256(canonical_json_bytes(catalog)).hexdigest(),
            "source_digests": {
                artifact["id"]: source_digest(ROOT / artifact["source_path"])
                for artifact in artifacts
            },
        }
        print(json.dumps(snapshot, sort_keys=True, separators=(",", ":")))
        return 0

    validators = build_validators()
    errors = []
    errors.extend(validate_fixtures(validators))
    errors.extend(validate_catalog(validators))
    errors.extend(validate_external_source_candidates(validators))
    errors.extend(validate_social_surface_catalog())

    if errors:
        print(f"VALIDATION FAILED -- {len(errors)} error(s):")
        for err in errors:
            print(f"  x  {err}")
        return 1

    print("VALIDATION PASSED -- fixtures, schemas, catalog coverage, relationships, and digest determinism are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
