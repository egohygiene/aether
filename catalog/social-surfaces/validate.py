#!/usr/bin/env python3
"""Validate social-surface catalog structure, provenance, and publication gates."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CATALOG = Path(__file__).with_name("catalog.v1.json")
SCHEMA_PATH = REPO_ROOT / "catalog" / "schemas" / "aether.social-surface-catalog.v1.schema.json"
SOURCE_CANDIDATES_PATH = REPO_ROOT / "catalog" / "external" / "source-candidates.v1.json"


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate(catalog_path: Path) -> list[str]:
    catalog = load_json(catalog_path)
    schema = load_json(SCHEMA_PATH)
    errors = [f"schema: {error.message}" for error in Draft202012Validator(schema).iter_errors(catalog)]
    if errors:
        return sorted(errors)

    metadata = catalog["catalog"]
    records = catalog["records"]
    ids = [record["id"] for record in records]
    if ids != sorted(ids):
        errors.append("records must be sorted by id")
    if len(ids) != len(set(ids)):
        errors.append("record IDs must be unique")

    candidates = load_json(SOURCE_CANDIDATES_PATH).get("entries", [])
    candidate_ids = {entry.get("id") for entry in candidates if isinstance(entry, dict)}
    declared_candidates = set(metadata["source_candidates"])
    missing_candidates = sorted(declared_candidates - candidate_ids)
    if missing_candidates:
        errors.append(f"catalog references unknown source candidates: {missing_candidates}")

    source_snapshot = metadata["source_snapshot"]
    for record in records:
        if record["source"]["candidate_id"] not in declared_candidates:
            errors.append(f"{record['id']}: source candidate is not declared by catalog")
        if record["source"]["snapshot_digest"] != source_snapshot["digest"]:
            errors.append(f"{record['id']}: source snapshot digest does not match catalog snapshot")
        safe_zone = record["safe_zone"]
        if safe_zone["state"] in {"unknown", "not-applicable"} and safe_zone["insets_px"] is not None:
            errors.append(f"{record['id']}: non-known safe zones must not invent insets")
        if safe_zone["state"] == "known" and safe_zone["insets_px"] is None:
            errors.append(f"{record['id']}: known safe zone requires explicit insets")

    lifecycle = metadata["lifecycle"]["state"]
    rights_state = metadata["rights_review"]["state"]
    release_included = metadata["release"]["included"]
    if release_included and (lifecycle != "stable" or rights_state != "approved"):
        errors.append("release-included catalog must be stable and rights-approved")
    if lifecycle == "stable" and not release_included:
        errors.append("stable catalog must explicitly be release-included")
    if rights_state != "approved" and records:
        errors.append("source-derived records cannot be published before rights review is approved")
    return sorted(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    args = parser.parse_args()
    try:
        errors = validate(args.catalog)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        return 1
    print("social-surface catalog validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
