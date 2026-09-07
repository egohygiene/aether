#!/usr/bin/env python3
"""Deterministic, model-independent validation for Aether evidence artifacts."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "catalog" / "schemas"
PACKET_SCHEMA = SCHEMA_DIR / "aether.cross-agent-evidence-packet.v1.schema.json"
REQUEST_SCHEMA = SCHEMA_DIR / "aether.sanitized-research-request.v1.schema.json"
PROJECTION_SCHEMA = SCHEMA_DIR / "aether.evidence-projection.v1.schema.json"
SCHEMA_BY_KIND = {
    "packet": PACKET_SCHEMA,
    "request": REQUEST_SCHEMA,
    "projection": PROJECTION_SCHEMA,
}
MAX_IMPORT_ATTACHMENT_COUNT = 1000
MAX_IMPORT_ATTACHMENT_BYTES = 100 * 1024 * 1024
CREDENTIAL_PATTERN = re.compile(
    r"(?i)(?:bearer\s+[a-z0-9._~-]{16,}|(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*\S{12,})"
)


class EvidenceValidationError(ValueError):
    """Raised when an evidence artifact cannot be admitted."""


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object without interpreting its contents."""

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise EvidenceValidationError("artifact root must be a JSON object")
    return data


def canonical_json_bytes(data: Any) -> bytes:
    """Return the canonical bytes used by all evidence artifact digests."""

    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def canonical_envelope_digest(data: dict[str, Any], identity_key: str) -> str:
    """Digest schema, identity, and payload while excluding integrity."""

    envelope = {
        "schema_version": data["schema_version"],
        identity_key: data[identity_key],
        "payload": data["payload"],
    }
    return hashlib.sha256(canonical_json_bytes(envelope)).hexdigest()


def _schema_errors(kind: str, data: dict[str, Any]) -> list[str]:
    schema = load_json(SCHEMA_BY_KIND[kind])
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = []
    for error in sorted(validator.iter_errors(data), key=lambda item: list(item.absolute_path)):
        location = "/".join(str(part) for part in error.absolute_path) or "<root>"
        errors.append(f"schema violation at {location}: {error.message}")
    return errors


def _parse_timestamp(value: str, field: str, errors: list[str]) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (AttributeError, ValueError):
        errors.append(f"{field} must be an RFC 3339 timestamp")
        return None


def _duplicate_ids(items: list[dict[str, Any]], label: str) -> list[str]:
    identifiers = [item.get("id") for item in items]
    duplicates = sorted({identifier for identifier in identifiers if identifiers.count(identifier) > 1})
    return [f"duplicate {label} id: {identifier}" for identifier in duplicates]


def _verify_digest(data: dict[str, Any], identity_key: str) -> list[str]:
    expected = canonical_envelope_digest(data, identity_key)
    digest = data["integrity"]["envelope_digest"]
    errors = []
    if digest["algorithm"] != "sha256-canonical-json":
        errors.append("envelope digest algorithm must be sha256-canonical-json")
    if digest["value"] != expected:
        errors.append(f"envelope digest mismatch: expected {expected}")
    return errors


def _scan_for_credentials(data: Any, path: str = "<root>") -> list[str]:
    errors: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            errors.extend(_scan_for_credentials(value, f"{path}/{key}"))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            errors.extend(_scan_for_credentials(value, f"{path}/{index}"))
    elif isinstance(data, str) and CREDENTIAL_PATTERN.search(data):
        errors.append(f"credential-like material is prohibited at {path}")
    return errors


def _relative_attachment_path(value: str) -> bool:
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and value == path.as_posix()
        and ".." not in path.parts
        and "\\" not in value
        and re.match(r"^[A-Za-z]:", value) is None
    )


def _verify_attachments(
    evidence: dict[str, Any],
    policy: dict[str, Any],
    attachments_root: Path | None,
) -> tuple[list[str], dict[str, bytes]]:
    attachments = evidence["attachments"]
    errors = _duplicate_ids(attachments, "attachment")
    content_by_id: dict[str, bytes] = {}
    declared_limit = min(policy["max_attachment_count"], MAX_IMPORT_ATTACHMENT_COUNT)
    byte_limit = min(policy["max_attachment_bytes"], MAX_IMPORT_ATTACHMENT_BYTES)
    if len(attachments) > declared_limit:
        errors.append(f"attachment count {len(attachments)} exceeds limit {declared_limit}")

    total_bytes = 0
    root = attachments_root.resolve() if attachments_root is not None else None
    for attachment in attachments:
        identifier = attachment["id"]
        declared_bytes = attachment["bytes"]
        total_bytes += declared_bytes
        if declared_bytes > byte_limit:
            errors.append(f"{identifier} declares {declared_bytes} bytes above limit {byte_limit}")
        if attachment["digest"]["algorithm"] != "sha256-bytes":
            errors.append(f"{identifier} digest algorithm must be sha256-bytes")

        if attachment["kind"] == "immutable-reference":
            continue
        value = attachment["path"]
        if not _relative_attachment_path(value):
            errors.append(f"{identifier} path must be normalized, relative, and traversal-free")
            continue
        if root is None:
            errors.append(f"{identifier} requires an explicit attachment root")
            continue
        candidate = (root / value).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            errors.append(f"{identifier} path escapes the attachment root")
            continue
        if not candidate.is_file():
            errors.append(f"{identifier} file does not exist: {value}")
            continue
        content = candidate.read_bytes()
        content_by_id[identifier] = content
        if len(content) != declared_bytes:
            errors.append(f"{identifier} byte count mismatch: expected {declared_bytes}, got {len(content)}")
        actual_digest = hashlib.sha256(content).hexdigest()
        if actual_digest != attachment["digest"]["value"]:
            errors.append(f"{identifier} digest mismatch")

    if total_bytes > byte_limit:
        errors.append(f"declared attachment bytes {total_bytes} exceed packet limit {byte_limit}")
    return errors, content_by_id


def _verify_sources(
    evidence: dict[str, Any],
    content_by_id: dict[str, bytes],
) -> tuple[list[str], set[str], set[str]]:
    attachments = {item["id"] for item in evidence["attachments"]}
    errors = _duplicate_ids(evidence["sources"], "source")
    source_ids: set[str] = set()
    excerpt_ids: set[str] = set()
    for source in evidence["sources"]:
        source_ids.add(source["id"])
        if source["digest"]["algorithm"] != "sha256-bytes":
            errors.append(f"{source['id']} digest algorithm must be sha256-bytes")
        missing = sorted(set(source["attachment_ids"]) - attachments)
        if missing:
            errors.append(f"{source['id']} references unknown attachments: {', '.join(missing)}")
        errors.extend(_duplicate_ids(source["excerpts"], "excerpt"))
        for excerpt in source["excerpts"]:
            identifier = excerpt["id"]
            if identifier in excerpt_ids:
                errors.append(f"duplicate excerpt id across sources: {identifier}")
            excerpt_ids.add(identifier)
            attachment_id = excerpt["attachment_id"]
            if attachment_id not in source["attachment_ids"]:
                errors.append(f"{identifier} attachment is not owned by its source")
            if excerpt["end_byte"] <= excerpt["start_byte"]:
                errors.append(f"{identifier} end_byte must be greater than start_byte")
            content = content_by_id.get(attachment_id)
            if content is None:
                continue
            start, end = excerpt["start_byte"], excerpt["end_byte"]
            if end > len(content):
                errors.append(f"{identifier} byte range exceeds attachment")
                continue
            actual = hashlib.sha256(content[start:end]).hexdigest()
            if excerpt["digest"]["algorithm"] != "sha256-bytes":
                errors.append(f"{identifier} digest algorithm must be sha256-bytes")
            if actual != excerpt["digest"]["value"]:
                errors.append(f"{identifier} exact-span digest mismatch")
    return errors, source_ids, excerpt_ids


def _verify_findings(findings: dict[str, Any], allowed_refs: set[str]) -> list[str]:
    errors = _duplicate_ids(findings["items"], "finding")
    for finding in findings["items"]:
        missing = sorted(set(finding["evidence_refs"]) - allowed_refs)
        if missing:
            errors.append(f"{finding['id']} references unknown evidence: {', '.join(missing)}")
        if finding["status"] == "supported" and not finding["evidence_refs"]:
            errors.append(f"{finding['id']} is supported without evidence")
        if finding["status"] in {"partial", "unknown"} and not finding["uncertainty"]:
            errors.append(f"{finding['id']} must state uncertainty for status {finding['status']}")
    return errors


def _verify_lifecycle(payload: dict[str, Any]) -> list[str]:
    lifecycle = payload["lifecycle"]
    state = lifecycle["state"]
    freshness = lifecycle["freshness"]
    review = payload["review"]
    errors: list[str] = []
    evaluated = _parse_timestamp(freshness["evaluated_at"], "freshness.evaluated_at", errors)
    valid_until = None
    if freshness["valid_until"] is not None:
        valid_until = _parse_timestamp(freshness["valid_until"], "freshness.valid_until", errors)
    if evaluated and valid_until:
        expired = valid_until < evaluated
        if freshness["status"] == "current" and expired:
            errors.append("stale authority cannot be represented as current")
        if freshness["status"] == "stale" and not expired:
            errors.append("stale freshness requires valid_until before evaluated_at")
    if state == "ready":
        if freshness["status"] != "current":
            errors.append("ready packet requires current freshness")
        if review["human"]["status"] != "approved":
            errors.append("ready packet requires approved human review")
        if review["sanitization"]["status"] != "approved":
            errors.append("ready packet requires approved sanitization review")
        if lifecycle["superseded_by"] or lifecycle["revocation"]:
            errors.append("ready packet cannot be superseded or revoked")
    if state == "partial" and not lifecycle["partial_failures"]:
        errors.append("partial packet must name at least one partial failure")
    if state == "stale" and freshness["status"] != "stale":
        errors.append("stale packet requires stale freshness")
    if state == "superseded" and not lifecycle["superseded_by"]:
        errors.append("superseded packet must name its replacement")
    if state == "revoked" and not lifecycle["revocation"]:
        errors.append("revoked packet must include revocation evidence")
    if state == "incompatible" and not lifecycle["incompatibility"]:
        errors.append("incompatible packet must name the incompatibility")
    return errors


def validate_packet(data: dict[str, Any], attachments_root: Path | None) -> list[str]:
    """Validate one evidence packet and return deterministic error strings."""

    errors = _schema_errors("packet", data)
    if errors:
        return errors
    errors.extend(_verify_digest(data, "packet"))
    payload = data["payload"]
    errors.extend(_scan_for_credentials(data))
    attachment_errors, content_by_id = _verify_attachments(
        payload["evidence"], payload["policy"], attachments_root
    )
    errors.extend(attachment_errors)
    source_errors, source_ids, excerpt_ids = _verify_sources(payload["evidence"], content_by_id)
    errors.extend(source_errors)
    errors.extend(_verify_findings(payload["findings"], source_ids | excerpt_ids))
    errors.extend(_verify_lifecycle(payload))
    signature = data["integrity"]["signature"]
    signature_material = (signature["algorithm"], signature["key_id"], signature["value"])
    if signature["status"] == "unsigned" and any(item is not None for item in signature_material):
        errors.append("unsigned signature must not contain signature material")
    if signature["status"] != "unsigned" and any(not item for item in signature_material):
        errors.append(f"{signature['status']} signature must contain algorithm, key_id, and value")
    return sorted(set(errors))


def admit_packet(
    data: dict[str, Any],
    attachments_root: Path | None,
    destination: str | None,
    admitted_policy_ids: set[str],
    session_capabilities: set[str],
) -> list[str]:
    """Apply deterministic destination, policy, capability, and state admission."""

    errors = validate_packet(data, attachments_root)
    if errors:
        return errors
    payload = data["payload"]
    policy = payload["policy"]
    if destination is None:
        errors.append("admission requires an explicit destination")
    elif destination not in policy["destination_scope"]:
        errors.append("destination is outside packet scope")
    missing_policies = sorted(set(policy["required_policy_ids"]) - admitted_policy_ids)
    if missing_policies:
        errors.append(f"required policy admission is missing: {', '.join(missing_policies)}")
    missing_capabilities = sorted(
        set(policy["required_session_capabilities"]) - session_capabilities
    )
    if missing_capabilities:
        errors.append(f"required session capabilities are missing: {', '.join(missing_capabilities)}")
    if payload["lifecycle"]["state"] != "ready":
        errors.append("admission requires packet lifecycle state ready")
    return sorted(set(errors))


def _request_review_envelope(data: dict[str, Any]) -> dict[str, Any]:
    """Return the request material a human decision must bind."""

    return {
        "schema_version": data["schema_version"],
        "request": data["request"],
        "payload": {key: value for key, value in data["payload"].items() if key != "review"},
    }


def validate_request(data: dict[str, Any]) -> list[str]:
    """Validate a separately reviewed outbound public request."""

    errors = _schema_errors("request", data)
    if errors:
        return errors
    errors.extend(_verify_digest(data, "request"))
    errors.extend(_scan_for_credentials(data))
    reviewed_digest = hashlib.sha256(canonical_json_bytes(_request_review_envelope(data))).hexdigest()
    for name in ("sanitization", "declassification"):
        decision = data["payload"]["review"][name]
        if decision["reviewed_digest"]["value"] != reviewed_digest:
            errors.append(f"{name} review is not bound to the exact public request")
    return sorted(set(errors))


def validate_projection(data: dict[str, Any], packet: dict[str, Any] | None) -> list[str]:
    """Validate a transport projection and, when supplied, its authority ceiling."""

    errors = _schema_errors("projection", data)
    if errors or packet is None:
        return errors
    packet_errors = _schema_errors("packet", packet)
    if packet_errors:
        return [f"packet {error}" for error in packet_errors]
    packet_policy = packet["payload"]["policy"]
    authority = data["authority"]
    if data["packet_ref"]["id"] != packet["packet"]["id"]:
        errors.append("projection references a different packet id")
    if data["packet_ref"]["digest"]["value"] != packet["integrity"]["envelope_digest"]["value"]:
        errors.append("projection packet digest does not match")
    for field in (
        "destination_scope",
        "maximum_sensitivity",
        "required_policy_ids",
        "required_session_capabilities",
        "grants_capabilities",
    ):
        if authority[field] != packet_policy[field]:
            errors.append(f"projection may not broaden or alter packet {field}")
    return sorted(set(errors))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--packet", type=Path, help="evidence packet JSON")
    group.add_argument("--request", type=Path, help="sanitized request JSON")
    group.add_argument("--projection", type=Path, help="transport projection JSON")
    parser.add_argument("--packet-for-projection", type=Path, help="packet bound by --projection")
    parser.add_argument("--attachments-root", type=Path, help="root for relative packet attachments")
    parser.add_argument("--admit", action="store_true", help="apply destination and session admission")
    parser.add_argument("--destination", help="destination requesting admission")
    parser.add_argument("--admitted-policy-id", action="append", default=[], help="externally admitted policy ID; repeat as needed")
    parser.add_argument("--session-capability", action="append", default=[], help="available session capability; repeat as needed")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.packet:
            packet = load_json(args.packet)
            if args.admit:
                errors = admit_packet(
                    packet,
                    args.attachments_root,
                    args.destination,
                    set(args.admitted_policy_id),
                    set(args.session_capability),
                )
                kind = "packet-admission"
            else:
                errors = validate_packet(packet, args.attachments_root)
                kind = "packet"
        elif args.request:
            errors = validate_request(load_json(args.request))
            kind = "request"
        else:
            packet = load_json(args.packet_for_projection) if args.packet_for_projection else None
            errors = validate_projection(load_json(args.projection), packet)
            kind = "projection"
    except (EvidenceValidationError, json.JSONDecodeError, OSError, KeyError) as exc:
        errors = [str(exc)]
        kind = "artifact"

    result = {"valid": not errors, "kind": kind, "errors": errors}
    if args.format == "json":
        print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    elif errors:
        print(f"INVALID {kind} -- {len(errors)} error(s)")
        for error in errors:
            print(f"  x {error}")
    else:
        print(f"VALID {kind}")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
