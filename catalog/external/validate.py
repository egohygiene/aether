#!/usr/bin/env python3
"""Validate Aether's bounded external-source review and allowlist contracts."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
EXTERNAL_DIR = ROOT / "catalog" / "external"
APPROVED_PATH = EXTERNAL_DIR / "approved-skills.v1.json"
CANDIDATES_PATH = EXTERNAL_DIR / "source-candidates.v1.json"
REGISTER_PATH = EXTERNAL_DIR / "source-review-register.v1.json"
ALLOWLIST_PATH = EXTERNAL_DIR / "initial-allowlist.v1.json"
DATE_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")
DATETIME_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$")


def _load(path: Path) -> dict[str, Any]:
    """Load a JSON object from a canonical external-catalog path."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _external_entries(
    approved_path: Path, candidates_path: Path
) -> tuple[list[dict[str, Any]], set[str]]:
    """Return all external records and the IDs that may be allowlisted."""
    approved = _load(approved_path).get("entries")
    candidates = _load(candidates_path).get("entries")
    if not isinstance(approved, list) or not isinstance(candidates, list):
        raise ValueError("external catalogs must contain entries arrays")
    records = [entry for entry in [*approved, *candidates] if isinstance(entry, dict)]
    return records, {str(entry.get("id")) for entry in approved if isinstance(entry, dict)}


def validate(
    *,
    approved_path: Path = APPROVED_PATH,
    candidates_path: Path = CANDIDATES_PATH,
    register_path: Path = REGISTER_PATH,
    allowlist_path: Path = ALLOWLIST_PATH,
) -> list[str]:
    """Return deterministic governance errors for the external source corpus."""
    errors: list[str] = []
    records, approved_ids = _external_entries(approved_path, candidates_path)
    register = _load(register_path)
    allowlist = _load(allowlist_path)

    if register.get("schema_version") != "aether.external-source-review-register/v1":
        errors.append("review register has an unexpected schema version")
    if allowlist.get("schema_version") != "aether.external-source-allowlist/v1":
        errors.append("allowlist has an unexpected schema version")
    if allowlist.get("review_register") != "source-review-register.v1.json":
        errors.append("allowlist must name the canonical review register")
    if allowlist.get("default_disposition") != "deny":
        errors.append("allowlist default disposition must be deny")
    if not DATETIME_RE.fullmatch(str(register.get("reviewed_at", ""))):
        errors.append("review register reviewed_at must be a UTC RFC 3339 timestamp")
    if not DATETIME_RE.fullmatch(str(allowlist.get("reviewed_at", ""))):
        errors.append("allowlist reviewed_at must be a UTC RFC 3339 timestamp")

    records_by_repository: dict[str, list[dict[str, Any]]] = defaultdict(list)
    records_by_id: dict[str, dict[str, Any]] = {}
    for record in records:
        identifier = str(record.get("id", ""))
        repository = str(record.get("upstream_repository", ""))
        if not identifier or not repository:
            errors.append("external records require id and upstream_repository")
            continue
        if identifier in records_by_id:
            errors.append(f"duplicate external record identifier: {identifier}")
        records_by_id[identifier] = record
        records_by_repository[repository].append(record)

    coverage = register.get("coverage")
    if not isinstance(coverage, dict):
        errors.append("review register coverage must be an object")
    else:
        if coverage.get("captured_source_count") != len(records_by_repository):
            errors.append("review register captured_source_count does not match external catalogs")
        if coverage.get("captured_artifact_count") != len(records):
            errors.append("review register captured_artifact_count does not match external catalogs")

    reviews = register.get("sources")
    if not isinstance(reviews, list) or not reviews:
        return errors + ["review register sources must be a non-empty array"]
    reviews_by_repository: dict[str, dict[str, Any]] = {}
    reviews_by_id: dict[str, dict[str, Any]] = {}
    required_assessments = {
        "license",
        "maintenance",
        "trust",
        "duplication",
        "relevance",
        "vulnerability",
    }
    for review in reviews:
        if not isinstance(review, dict):
            errors.append("review register sources must contain objects")
            continue
        source_id = str(review.get("id", ""))
        repository = str(review.get("upstream_repository", ""))
        if source_id in reviews_by_id:
            errors.append(f"duplicate source review identifier: {source_id}")
        if repository in reviews_by_repository:
            errors.append(f"multiple source reviews for {repository}")
        reviews_by_id[source_id] = review
        reviews_by_repository[repository] = review
        if review.get("decision") not in {"allowlisted", "deferred", "rejected"}:
            errors.append(f"{source_id}: decision must be allowlisted, deferred, or rejected")
        if not str(review.get("decision_reason", "")).strip():
            errors.append(f"{source_id}: decision_reason is required")
        if not isinstance(review.get("constraints"), list) or not review["constraints"]:
            errors.append(f"{source_id}: at least one constraint is required")
        next_review = review.get("next_review")
        if not isinstance(next_review, dict) or not DATE_RE.fullmatch(str(next_review.get("not_after", ""))):
            errors.append(f"{source_id}: next_review.not_after must be an ISO date")
        assessments = review.get("assessment")
        if not isinstance(assessments, dict) or set(assessments) != required_assessments:
            errors.append(f"{source_id}: assessment must cover every required review dimension")
        elif any(
            not isinstance(value, dict)
            or not str(value.get("state", "")).strip()
            or not str(value.get("evidence", "")).strip()
            for value in assessments.values()
        ):
            errors.append(f"{source_id}: every assessment requires state and evidence")
        expected_count = len(records_by_repository.get(repository, []))
        if review.get("captured_artifact_count") != expected_count:
            errors.append(f"{source_id}: captured_artifact_count does not match external catalogs")

    if set(reviews_by_repository) != set(records_by_repository):
        missing = sorted(set(records_by_repository) - set(reviews_by_repository))
        extra = sorted(set(reviews_by_repository) - set(records_by_repository))
        if missing:
            errors.append(f"review register is missing captured sources: {missing}")
        if extra:
            errors.append(f"review register has sources absent from external catalogs: {extra}")

    selected = allowlist.get("entries")
    if not isinstance(selected, list) or not selected:
        return errors + ["allowlist entries must be a non-empty array"]
    selected_ids = [str(entry.get("artifact_id", "")) for entry in selected if isinstance(entry, dict)]
    if selected_ids != sorted(selected_ids):
        errors.append("allowlist entries must be sorted by artifact_id")
    duplicate_ids = sorted(identifier for identifier, count in Counter(selected_ids).items() if count > 1)
    if duplicate_ids:
        errors.append(f"allowlist has duplicate artifact identifiers: {duplicate_ids}")

    allowlisted_sources: dict[str, set[str]] = defaultdict(set)
    for entry in selected:
        if not isinstance(entry, dict):
            errors.append("allowlist entries must contain objects")
            continue
        artifact_id = str(entry.get("artifact_id", ""))
        source_id = str(entry.get("source_id", ""))
        artifact = records_by_id.get(artifact_id)
        review = reviews_by_id.get(source_id)
        if artifact_id not in approved_ids:
            errors.append(f"{artifact_id}: only reviewed external skill records may be allowlisted")
            continue
        if artifact is None:
            errors.append(f"{artifact_id}: missing from external catalogs")
            continue
        if review is None:
            errors.append(f"{artifact_id}: references an unknown source review {source_id}")
            continue
        if review.get("decision") != "allowlisted":
            errors.append(f"{artifact_id}: source decision must be allowlisted")
        if review.get("upstream_repository") != artifact.get("upstream_repository"):
            errors.append(f"{artifact_id}: source review does not own the artifact repository")
        if entry.get("upstream_ref") != artifact.get("upstream_ref"):
            errors.append(f"{artifact_id}: allowlist pin does not match the reviewed external record")
        if entry.get("content_hash") != artifact.get("content_hash"):
            errors.append(f"{artifact_id}: allowlist digest does not match the reviewed external record")
        if artifact.get("executable_resources") != "no":
            errors.append(f"{artifact_id}: executable external resources cannot enter the initial allowlist")
        if artifact.get("redistribution_permission") != "allowed" or artifact.get("redistribution_status") != "verified":
            errors.append(f"{artifact_id}: redistribution evidence is insufficient for allowlisting")
        if entry.get("use_boundary") != "agent-assisted-reference-only":
            errors.append(f"{artifact_id}: use boundary must remain agent-assisted-reference-only")
        if entry.get("requires_human_review") is not True:
            errors.append(f"{artifact_id}: human review is required")
        prohibited = set(entry.get("prohibited_actions", []))
        required_prohibitions = {
            "automatic installation",
            "automatic execution",
            "first-party promotion",
            "external delivery",
        }
        if not required_prohibitions.issubset(prohibited):
            errors.append(f"{artifact_id}: required action prohibitions are missing")
        allowlisted_sources[source_id].add(artifact_id)

    for source_id, review in reviews_by_id.items():
        source_records = {
            str(record.get("id"))
            for record in records_by_repository.get(str(review.get("upstream_repository")), [])
            if str(record.get("id")) in approved_ids
        }
        selected_for_source = allowlisted_sources.get(source_id, set())
        if review.get("decision") == "allowlisted" and selected_for_source != source_records:
            errors.append(f"{source_id}: allowlisted source must select exactly its reviewed external records")
        if review.get("decision") != "allowlisted" and selected_for_source:
            errors.append(f"{source_id}: deferred or rejected source cannot have allowlisted records")

    return errors


def main() -> int:
    """Run the validator as a deterministic command-line contract check."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--approved", type=Path, default=APPROVED_PATH)
    parser.add_argument("--candidates", type=Path, default=CANDIDATES_PATH)
    parser.add_argument("--register", type=Path, default=REGISTER_PATH)
    parser.add_argument("--allowlist", type=Path, default=ALLOWLIST_PATH)
    arguments = parser.parse_args()
    try:
        errors = validate(
            approved_path=arguments.approved,
            candidates_path=arguments.candidates,
            register_path=arguments.register,
            allowlist_path=arguments.allowlist,
        )
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors = [str(error)]
    if errors:
        print(f"EXTERNAL SOURCE GOVERNANCE VALIDATION FAILED -- {len(errors)} error(s):")
        for error in errors:
            print(f"  x  {error}")
        return 1
    print("EXTERNAL SOURCE GOVERNANCE VALIDATION PASSED -- reviewed sources and bounded allowlist are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
