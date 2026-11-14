#!/usr/bin/env python3
"""Validate Aether's bounded external-source review and allowlist contracts."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
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


def _date(value: Any) -> date | None:
    if not isinstance(value, str) or not DATE_RE.fullmatch(value):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _instant(value: Any) -> datetime | None:
    if not isinstance(value, str) or not DATETIME_RE.fullmatch(value):
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def assess_freshness(register: dict[str, Any], as_of: date) -> list[dict[str, Any]]:
    """Assess calendar deadlines only; never renew a review or authorize use."""
    if type(as_of) is not date:
        raise ValueError("as_of must be an explicit calendar date")
    reviewed = _instant(register.get("reviewed_at"))
    result = []
    for source in register.get("sources", []):
        if not isinstance(source, dict):
            continue
        next_review = source.get("next_review")
        deadline = _date(next_review.get("not_after")) if isinstance(next_review, dict) else None
        status = "unknown" if reviewed is None or deadline is None or as_of < reviewed.date() else (
            "current" if as_of <= deadline else "overdue"
        )
        followups = [entry for entry in source.get("followups", [])
                     if isinstance(entry, dict) and (at := _instant(entry.get("assessed_at")))
                     and at.date() <= as_of]
        result.append({"source_id": source.get("id"), "freshness": status,
                       "reviewed_at": register.get("reviewed_at"),
                       "deadline": deadline.isoformat() if deadline else None,
                       "decision": source.get("decision"),
                       "followup_state": followups[-1].get("state") if followups else None,
                       "use_boundary": "agent-assisted-reference-only" if source.get("decision") == "allowlisted" else "deny"})
    return result


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
    reviewed_at = _instant(register.get("reviewed_at"))
    allowlisted_at = _instant(allowlist.get("reviewed_at"))
    if reviewed_at is None:
        errors.append("review register reviewed_at must be a UTC RFC 3339 timestamp")
    if allowlisted_at is None:
        errors.append("allowlist reviewed_at must be a UTC RFC 3339 timestamp")
    if reviewed_at and allowlisted_at and allowlisted_at < reviewed_at:
        errors.append("allowlist reviewed_at cannot precede its source review")

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
        deadline = _date(next_review.get("not_after")) if isinstance(next_review, dict) else None
        if deadline is None:
            errors.append(f"{source_id}: next_review.not_after must be a real ISO calendar date")
        elif reviewed_at and deadline < reviewed_at.date():
            errors.append(f"{source_id}: next review cannot precede reviewed_at")
        previous = reviewed_at
        followups = review.get("followups", [])
        if not isinstance(followups, list):
            errors.append(f"{source_id}: followups must be an array")
            followups = []
        for followup in followups:
            if not isinstance(followup, dict):
                errors.append(f"{source_id}: followups must contain objects")
                continue
            at = _instant(followup.get("assessed_at"))
            if at is None or (previous and at < previous):
                errors.append(f"{source_id}: followup assessed_at must be valid and chronological")
            if at:
                previous = at
            evidence = followup.get("evidence")
            if (followup.get("state") not in {"blocked", "unknown"}
                    or followup.get("renews_review") is not False
                    or not str(followup.get("next_action", "")).strip()
                    or not isinstance(evidence, list) or not evidence
                    or any(not isinstance(item, str) or not item.strip() for item in evidence)):
                errors.append(f"{source_id}: followup needs blocked/unknown evidence, next action and renews_review=false")
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
    parser.add_argument("--as-of", help="Explicit YYYY-MM-DD freshness assessment; overdue/unknown exits 1")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    arguments = parser.parse_args()
    assessment_date = _date(arguments.as_of) if arguments.as_of is not None else None
    if arguments.as_of is not None and assessment_date is None:
        parser.error("--as-of must be a real YYYY-MM-DD calendar date")
    freshness = []
    try:
        errors = validate(
            approved_path=arguments.approved,
            candidates_path=arguments.candidates,
            register_path=arguments.register,
            allowlist_path=arguments.allowlist,
        )
        if assessment_date is not None and not errors:
            freshness = assess_freshness(_load(arguments.register), assessment_date)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        errors = [str(error)]
    complete = not errors and (assessment_date is None or bool(freshness) and all(
        source["freshness"] == "current" for source in freshness
    ))
    if arguments.format == "json":
        print(json.dumps({"schema_version": "aether.external-source-assessment/v1",
                          "structural_status": "fail" if errors else "pass", "errors": errors,
                          "assessment_date": assessment_date.isoformat() if assessment_date else None,
                          "freshness": freshness, "complete": complete,
                          "scope": "Offline structure and optional frozen-date freshness; no live source/advisory qualification"},
                         indent=2, sort_keys=True))
        return 0 if complete else 1
    if errors:
        print(f"EXTERNAL SOURCE GOVERNANCE VALIDATION FAILED -- {len(errors)} error(s):")
        for error in errors:
            print(f"  x  {error}")
        return 1
    print("EXTERNAL SOURCE GOVERNANCE STRUCTURE PASSED -- consistency only, not current source/advisory qualification.")
    for source in freshness:
        print(f"{source['source_id']}: {source['freshness']} at {assessment_date}; deadline={source['deadline']}; decision={source['decision']}; followup={source['followup_state']}")
    return 0 if complete else 1


if __name__ == "__main__":
    raise SystemExit(main())
