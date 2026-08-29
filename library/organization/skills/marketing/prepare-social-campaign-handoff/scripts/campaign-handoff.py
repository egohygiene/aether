#!/usr/bin/env python3
"""Prepare and validate review-gated social campaign handoff packets."""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Sequence

PACKET_SCHEMA = "aether.social-campaign-handoff/v1"
BRIEF_SCHEMA = "aether.social-campaign-brief/v1"
APPROVAL_SCHEMA = "aether.social-campaign-approval/v1"
IDENTITY_SCHEMA = "identity.social-surface-package/v1"
CATALOG_SCHEMA = "aether.social-surface-catalog/v1"
FRESHNESS_NOTICE = (
    "This packet uses a dated, offline catalog. Verify consequential or changed "
    "requirements against every linked official source before export."
)
SEMVER = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
CAMPAIGN_ID = re.compile(r"^campaign/[a-z0-9]+(?:-[a-z0-9]+)*$")
APPROVAL_ID = re.compile(r"^approval/[a-z0-9]+(?:-[a-z0-9]+)*$")
IDENTIFIER = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HTTPS_URL = re.compile(r"^https://[^\s]+$")
SHA256 = re.compile(r"^[a-f0-9]{64}$")
SECRET_PATTERNS = (
    re.compile(r"\bghp_[A-Za-z0-9]{20,}\b"),
    re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=-]{12,}\b", re.IGNORECASE),
    re.compile(r"-----BEGIN (?:RSA|OPENSSH|EC|DSA) PRIVATE KEY-----"),
)
SECRET_KEYS = {
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "bearer_token",
    "client_secret",
    "cookie",
    "credentials",
    "password",
    "passwd",
    "platform_credentials",
    "secret",
    "session_cookie",
    "token",
}
DIRECT_ACTION_KEYS = {
    "ad_spend",
    "direct_publish",
    "publish_now",
    "schedule_at",
    "scheduler_account",
}
ROOT_KEYS = {
    "schema_version",
    "packet",
    "intent",
    "identity",
    "catalog",
    "channels",
    "review",
    "publishing_checklist",
    "external_handoff",
    "publication",
    "lifecycle",
}
BRIEF_KEYS = {
    "schema_version",
    "campaign_id",
    "version",
    "created_at",
    "created_by",
    "objective",
    "audience",
    "context",
    "selections",
}
SELECTION_KEYS = {
    "id",
    "target_id",
    "candidate_copy",
    "copy_source",
    "claims",
    "required_link",
    "attribution",
}
CHECKLIST_IDS = (
    "identity-integrity",
    "catalog-lock",
    "catalog-freshness",
    "surface-constraints",
    "copy-and-claims",
    "links-and-attribution",
    "final-creative",
    "credential-free-export",
)


class HandoffError(ValueError):
    """Raised when source or lifecycle evidence cannot support an operation."""


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise HandoffError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    """Load one object-shaped JSON document and reject duplicate keys."""

    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise HandoffError(f"cannot load JSON document {path}: {error}") from error
    if not isinstance(value, dict):
        raise HandoffError(f"JSON document must be an object: {path}")
    return value


def canonical_json(value: object) -> str:
    """Return stable, reviewable JSON."""

    return f"{json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)}\n"


def canonical_digest(value: object) -> str:
    """Return SHA-256 over compact canonical JSON."""

    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def reviewed_basis(packet: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct the exact reviewed packet bound by an approval record."""

    basis = deepcopy(packet)
    basis["packet"]["state"] = "reviewed"
    basis["packet"]["superseded_by"] = None
    basis["review"]["status"] = "reviewed"
    basis["review"]["approval"] = None
    basis["external_handoff"].update(
        {
            "authorized": False,
            "authorization_approval_id": None,
            "adapter": None,
        }
    )
    basis["publication"] = {"status": "not-published", "receipt": None}
    for channel in basis["channels"]:
        channel["copy"]["status"] = "candidate"
        channel["copy"]["approval_id"] = None
        for claim in channel["copy"]["claims"]:
            claim["status"] = "candidate"
            claim["approval_id"] = None
    basis["lifecycle"]["history"] = [
        event
        for event in basis["lifecycle"]["history"]
        if event.get("to") in {"draft", "reviewed"}
    ]
    return basis


def approved_basis(packet: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct the immutable approved packet exported to an adapter."""

    basis = deepcopy(packet)
    basis["packet"]["state"] = "approved-for-export"
    basis["packet"]["superseded_by"] = None
    basis["external_handoff"]["adapter"] = None
    basis["publication"] = {"status": "not-published", "receipt": None}
    basis["lifecycle"]["history"] = [
        event
        for event in basis["lifecycle"]["history"]
        if event.get("to") in {"draft", "reviewed", "approved-for-export"}
    ]
    return basis


def normalized_text_digest(path: Path) -> str:
    """Return the Aether sha256-utf8-lf digest for a text artifact."""

    value = (
        path.read_text(encoding="utf-8")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .encode("utf-8")
    )
    return hashlib.sha256(value).hexdigest()


def require_closed(
    value: Any,
    keys: set[str],
    label: str,
    *,
    required: set[str] | None = None,
) -> dict[str, Any]:
    """Require one closed object with explicit required fields."""

    if not isinstance(value, dict):
        raise HandoffError(f"{label} must be an object")
    unknown = sorted(set(value) - keys)
    missing = sorted((required or keys) - set(value))
    if unknown:
        raise HandoffError(f"{label} contains unsupported fields: {', '.join(unknown)}")
    if missing:
        raise HandoffError(f"{label} is missing required fields: {', '.join(missing)}")
    return value


def require_text(value: Any, label: str) -> str:
    """Require one non-empty string."""

    if not isinstance(value, str) or not value.strip():
        raise HandoffError(f"{label} must be a non-empty string")
    return value


def require_timestamp(value: Any, label: str) -> str:
    """Require one timezone-aware RFC 3339 timestamp."""

    text = require_text(value, label)
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as error:
        raise HandoffError(f"{label} must be an RFC 3339 timestamp") from error
    if parsed.tzinfo is None:
        raise HandoffError(f"{label} must include a timezone")
    return text


def unsafe_fields(value: Any, pointer: str = "$") -> list[str]:
    """Find embedded credentials or direct-platform action fields."""

    errors: list[str] = []
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = key.lower().replace("-", "_")
            if normalized in SECRET_KEYS:
                errors.append(f"{pointer}.{key}: credential field is prohibited")
            if normalized in DIRECT_ACTION_KEYS:
                errors.append(f"{pointer}.{key}: direct platform action is prohibited")
            errors.extend(unsafe_fields(item, f"{pointer}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            errors.extend(unsafe_fields(item, f"{pointer}[{index}]"))
    elif isinstance(value, str):
        if any(pattern.search(value) for pattern in SECRET_PATTERNS):
            errors.append(f"{pointer}: credential-like value is prohibited")
    return errors


def validate_brief(brief: dict[str, Any]) -> None:
    """Validate the closed credential-free campaign brief input."""

    require_closed(brief, BRIEF_KEYS, "campaign brief")
    if brief.get("schema_version") != BRIEF_SCHEMA:
        raise HandoffError(f"campaign brief schema must be {BRIEF_SCHEMA}")
    if not isinstance(brief.get("campaign_id"), str) or CAMPAIGN_ID.fullmatch(
        brief["campaign_id"]
    ) is None:
        raise HandoffError("campaign_id must use campaign/<lowercase-kebab-id>")
    if not isinstance(brief.get("version"), str) or SEMVER.fullmatch(brief["version"]) is None:
        raise HandoffError("campaign brief version must be semantic x.y.z")
    require_timestamp(brief.get("created_at"), "created_at")
    require_text(brief.get("created_by"), "created_by")
    for field in ("objective", "audience", "context"):
        sourced = require_closed(brief.get(field), {"value", "source"}, field)
        require_text(sourced.get("value"), f"{field}.value")
        if sourced.get("source") != "user-supplied":
            raise HandoffError(f"{field}.source must be user-supplied")
    selections = brief.get("selections")
    if not isinstance(selections, list) or not selections:
        raise HandoffError("campaign brief requires at least one selection")
    selection_ids: set[str] = set()
    target_ids: set[str] = set()
    for index, item in enumerate(selections):
        selection = require_closed(item, SELECTION_KEYS, f"selections[{index}]")
        identifier = selection.get("id")
        if not isinstance(identifier, str) or IDENTIFIER.fullmatch(identifier) is None:
            raise HandoffError(f"selections[{index}].id must be lowercase kebab-case")
        if identifier in selection_ids:
            raise HandoffError(f"duplicate campaign channel id: {identifier}")
        selection_ids.add(identifier)
        target_id = require_text(selection.get("target_id"), f"selections[{index}].target_id")
        if target_id in target_ids:
            raise HandoffError(f"duplicate Identity target selection: {target_id}")
        target_ids.add(target_id)
        require_text(selection.get("candidate_copy"), f"selections[{index}].candidate_copy")
        if selection.get("copy_source") not in {"user-supplied", "identity-approved"}:
            raise HandoffError(f"selections[{index}].copy_source is unsupported")
        claims = selection.get("claims")
        if not isinstance(claims, list):
            raise HandoffError(f"selections[{index}].claims must be an array")
        for claim_index, claim in enumerate(claims):
            claim_value = require_closed(
                claim,
                {"text", "evidence"},
                f"selections[{index}].claims[{claim_index}]",
            )
            require_text(claim_value.get("text"), "claim.text")
            evidence = claim_value.get("evidence")
            if evidence is not None:
                require_text(evidence, "claim.evidence")
        link = selection.get("required_link")
        if link is not None and (not isinstance(link, str) or HTTPS_URL.fullmatch(link) is None):
            raise HandoffError(f"selections[{index}].required_link must be HTTPS or null")
        attribution = require_closed(
            selection.get("attribution"),
            {"required", "text"},
            f"selections[{index}].attribution",
        )
        if not isinstance(attribution.get("required"), bool):
            raise HandoffError(f"selections[{index}].attribution.required must be boolean")
        if attribution["required"]:
            require_text(attribution.get("text"), f"selections[{index}].attribution.text")
        elif attribution.get("text") is not None:
            require_text(attribution["text"], f"selections[{index}].attribution.text")
    unsafe = unsafe_fields(brief)
    if unsafe:
        raise HandoffError(unsafe[0])


def projected_catalog_surface(record: dict[str, Any]) -> dict[str, Any]:
    """Return the exact Aether-to-Identity surface projection."""

    dimensions = record.get("dimensions")
    if not isinstance(dimensions, dict):
        raise HandoffError(f"catalog record has no usable dimensions: {record.get('id')}")
    lifecycle = record.get("lifecycle")
    if not isinstance(lifecycle, dict) or lifecycle.get("state") != "stable":
        raise HandoffError(f"catalog record is not stable: {record.get('id')}")
    return {
        "id": record["id"],
        "platform": record["platform"],
        "placement": record["placement"],
        "use": record["use"],
        "contentType": record["content_type"],
        "mediaFormat": record["media_format"],
        "dimensions": {
            "widthPx": dimensions["width_px"],
            "heightPx": dimensions["height_px"],
        },
        "aspectRatio": record["aspect_ratio"],
        "fileTypes": record["file_types"],
        "fileSizeLimitBytes": record["file_size_limit_bytes"],
        "durationLimitSeconds": record["duration_limit_seconds"],
        "safeZone": record["safe_zone"],
        "verification": record["verification"],
        "source": record["source"],
        "lifecycle": lifecycle["state"],
    }


def validate_inputs(
    identity: dict[str, Any],
    identity_path: Path,
    catalog: dict[str, Any],
    catalog_path: Path,
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]], str]:
    """Validate immutable Identity and catalog inputs and return indexes."""

    if identity.get("schema") != IDENTITY_SCHEMA:
        raise HandoffError(f"Identity artifact schema must be {IDENTITY_SCHEMA}")
    if not isinstance(identity.get("source"), dict):
        raise HandoffError("Identity artifact has no source lock")
    source_digest = identity["source"].get("digest")
    projection_version = identity["source"].get("projectionVersion")
    if not isinstance(source_digest, str) or SHA256.fullmatch(source_digest) is None:
        raise HandoffError("Identity source digest is invalid")
    if not isinstance(projection_version, str) or SEMVER.fullmatch(projection_version) is None:
        raise HandoffError("Identity projection version is invalid")
    handoff = identity.get("handoff")
    if not isinstance(handoff, dict) or handoff.get("publicationAuthorized") is not False:
        raise HandoffError("Identity artifact must explicitly deny publication authority")

    if catalog.get("schema_version") != CATALOG_SCHEMA:
        raise HandoffError(f"catalog schema must be {CATALOG_SCHEMA}")
    metadata = catalog.get("catalog")
    if not isinstance(metadata, dict):
        raise HandoffError("catalog metadata is missing")
    lifecycle = metadata.get("lifecycle")
    rights = metadata.get("rights_review")
    release = metadata.get("release")
    if not isinstance(lifecycle, dict) or lifecycle.get("state") != "stable":
        raise HandoffError("campaign handoff requires a stable Aether catalog")
    if not isinstance(rights, dict) or rights.get("state") != "approved":
        raise HandoffError("campaign handoff requires a rights-approved Aether catalog")
    if not isinstance(release, dict) or release.get("included") is not True:
        raise HandoffError("campaign handoff requires a release-included Aether catalog")

    identity_catalog = identity.get("catalog")
    if not isinstance(identity_catalog, dict):
        raise HandoffError("Identity artifact has no catalog lock")
    lock_digest = identity_catalog.get("digest")
    if not isinstance(lock_digest, dict) or lock_digest.get("algorithm") != "sha256-utf8-lf":
        raise HandoffError("Identity catalog lock must use sha256-utf8-lf")
    actual_catalog_digest = normalized_text_digest(catalog_path)
    if lock_digest.get("value") != actual_catalog_digest:
        raise HandoffError("Identity catalog digest does not match supplied catalog bytes")
    if identity_catalog.get("id") != metadata.get("id"):
        raise HandoffError("Identity catalog ID does not match supplied catalog")
    if identity_catalog.get("version") != metadata.get("version"):
        raise HandoffError("Identity catalog version does not match supplied catalog")

    records = catalog.get("records")
    if not isinstance(records, list):
        raise HandoffError("catalog records must be an array")
    record_index: dict[str, dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("id"), str):
            raise HandoffError("catalog record has no stable ID")
        if record["id"] in record_index:
            raise HandoffError(f"duplicate catalog record: {record['id']}")
        record_index[record["id"]] = record

    targets = identity.get("targets")
    if not isinstance(targets, list) or not targets:
        raise HandoffError("Identity artifact has no social targets")
    target_index: dict[str, dict[str, Any]] = {}
    for target in targets:
        if not isinstance(target, dict) or not isinstance(target.get("id"), str):
            raise HandoffError("Identity target has no stable ID")
        if target["id"] in target_index:
            raise HandoffError(f"duplicate Identity target: {target['id']}")
        surface = target.get("surface")
        if not isinstance(surface, dict) or not isinstance(surface.get("id"), str):
            raise HandoffError(f"Identity target has no surface: {target['id']}")
        record = record_index.get(surface["id"])
        if record is None:
            raise HandoffError(f"Identity target uses unsupported catalog surface: {surface['id']}")
        try:
            expected_surface = projected_catalog_surface(record)
        except KeyError as error:
            raise HandoffError(f"catalog surface is incomplete: {surface['id']}") from error
        if surface != expected_surface:
            raise HandoffError(f"Identity target differs from pinned catalog facts: {target['id']}")
        content = target.get("content")
        required_content = {
            "assetId",
            "inputPath",
            "mediaType",
            "sha256",
            "altText",
            "license",
            "origin",
            "copy",
            "link",
        }
        if not isinstance(content, dict) or not required_content.issubset(content):
            raise HandoffError(f"Identity target has incomplete asset provenance: {target['id']}")
        if not isinstance(content.get("sha256"), str) or SHA256.fullmatch(content["sha256"]) is None:
            raise HandoffError(f"Identity target asset digest is invalid: {target['id']}")
        if not isinstance(content.get("altText"), str) or not content["altText"].strip():
            raise HandoffError(f"Identity target lacks accessibility text: {target['id']}")
        status = target.get("status")
        if not isinstance(status, dict) or status.get("state") != "ready-for-rendering":
            raise HandoffError(f"Identity target is not ready for rendering: {target['id']}")
        target_index[target["id"]] = target
    return target_index, record_index, actual_catalog_digest


def prepare_packet(
    identity: dict[str, Any],
    identity_path: Path,
    catalog: dict[str, Any],
    catalog_path: Path,
    brief: dict[str, Any],
) -> dict[str, Any]:
    """Build a deterministic draft from approved local inputs."""

    validate_brief(brief)
    targets, records, catalog_digest = validate_inputs(
        identity,
        identity_path,
        catalog,
        catalog_path,
    )
    channels: list[dict[str, Any]] = []
    source_urls: set[str] = set()
    for selection in sorted(brief["selections"], key=lambda item: item["id"]):
        target = targets.get(selection["target_id"])
        if target is None:
            raise HandoffError(
                f"brief selects unsupported Identity target: {selection['target_id']}"
            )
        content = target["content"]
        if selection["copy_source"] == "identity-approved":
            identity_copy = content.get("copy")
            if not isinstance(identity_copy, dict) or selection["candidate_copy"] != identity_copy.get(
                "value"
            ):
                raise HandoffError(
                    f"identity-approved copy differs from Identity target: {target['id']}"
                )
        record = records[target["surface"]["id"]]
        source_urls.add(record["source"]["url"])
        required_link = selection["required_link"]
        if required_link is None and isinstance(content.get("link"), dict):
            required_link = content["link"].get("value")
        channels.append(
            {
                "id": selection["id"],
                "target_id": target["id"],
                "surface": deepcopy(target["surface"]),
                "asset": {
                    "id": content["assetId"],
                    "path": content["inputPath"],
                    "sha256": content["sha256"],
                    "media_type": content["mediaType"],
                    "alt_text": content["altText"],
                    "license": deepcopy(content["license"]),
                    "origin": deepcopy(content["origin"]),
                    "identity_approvals": deepcopy(target.get("approvals", {})),
                },
                "copy": {
                    "text": selection["candidate_copy"],
                    "source": selection["copy_source"],
                    "status": "candidate",
                    "approval_id": None,
                    "claims": [
                        {
                            "text": claim["text"],
                            "status": "candidate",
                            "evidence": claim["evidence"],
                            "approval_id": None,
                        }
                        for claim in selection["claims"]
                    ],
                },
                "required_link": required_link,
                "attribution": deepcopy(selection["attribution"]),
                "provenance": {
                    "identity_target_path": f"targets/{target['id']}.json",
                    "catalog_record_id": record["id"],
                    "catalog_source": deepcopy(record["source"]),
                },
            }
        )

    metadata = catalog["catalog"]
    packet = {
        "schema_version": PACKET_SCHEMA,
        "packet": {
            "id": brief["campaign_id"],
            "version": brief["version"],
            "state": "draft",
            "created_at": brief["created_at"],
            "superseded_by": None,
        },
        "intent": {
            field: deepcopy(brief[field]) for field in ("objective", "audience", "context")
        },
        "identity": {
            "artifact_schema": IDENTITY_SCHEMA,
            "artifact_version": identity["source"]["projectionVersion"],
            "project_id": identity["project"]["id"],
            "source_digest": identity["source"]["digest"],
            "package_digest": {
                "algorithm": "sha256-canonical-json",
                "value": canonical_digest(identity),
            },
        },
        "catalog": {
            "id": metadata["id"],
            "version": metadata["version"],
            "digest": {"algorithm": "sha256-utf8-lf", "value": catalog_digest},
            "captured_at": metadata["source_snapshot"]["captured_at"],
            "source_urls": sorted(source_urls),
            "freshness_notice": FRESHNESS_NOTICE,
            "live_verification": {
                "status": "required",
                "required": True,
                "verified_at": None,
                "verified_by": None,
                "evidence": None,
            },
        },
        "channels": channels,
        "review": {
            "status": "pending",
            "reviewed_by": None,
            "reviewed_at": None,
            "notes": None,
            "approval": None,
        },
        "publishing_checklist": [
            {
                "id": identifier,
                "required": True,
                "status": "pending",
                "evidence": None,
                "completed_by": None,
                "completed_at": None,
            }
            for identifier in CHECKLIST_IDS
        ],
        "external_handoff": {
            "authorized": False,
            "allowed_action": "immutable-export-only",
            "authorization_approval_id": None,
            "adapter": None,
        },
        "publication": {"status": "not-published", "receipt": None},
        "lifecycle": {
            "history": [
                {
                    "from": None,
                    "to": "draft",
                    "actor": brief["created_by"],
                    "occurred_at": brief["created_at"],
                    "reason": "Created from locked Identity, catalog, and user-supplied brief inputs.",
                }
            ]
        },
    }
    errors = validate_packet(packet)
    if errors:
        raise HandoffError(errors[0])
    return packet


def validate_packet(packet: dict[str, Any]) -> list[str]:
    """Return deterministic semantic diagnostics for one campaign packet."""

    errors: list[str] = []
    if set(packet) != ROOT_KEYS:
        unknown = sorted(set(packet) - ROOT_KEYS)
        missing = sorted(ROOT_KEYS - set(packet))
        if unknown:
            errors.append(f"packet contains unsupported fields: {', '.join(unknown)}")
        if missing:
            errors.append(f"packet is missing required fields: {', '.join(missing)}")
        return errors
    if packet.get("schema_version") != PACKET_SCHEMA:
        errors.append(f"packet schema must be {PACKET_SCHEMA}")
    unsafe = unsafe_fields(packet)
    errors.extend(unsafe)
    metadata = packet.get("packet")
    if not isinstance(metadata, dict):
        return errors + ["packet metadata must be an object"]
    state = metadata.get("state")
    states = {"draft", "reviewed", "approved-for-export", "published", "superseded"}
    if state not in states:
        errors.append("packet state is unsupported")
    if not isinstance(metadata.get("id"), str) or CAMPAIGN_ID.fullmatch(metadata["id"]) is None:
        errors.append("packet id is invalid")
    if not isinstance(metadata.get("version"), str) or SEMVER.fullmatch(metadata["version"]) is None:
        errors.append("packet version is invalid")
    try:
        require_timestamp(metadata.get("created_at"), "packet.created_at")
    except HandoffError as error:
        errors.append(str(error))
    if state == "superseded":
        if not isinstance(metadata.get("superseded_by"), str) or CAMPAIGN_ID.fullmatch(
            metadata["superseded_by"]
        ) is None:
            errors.append("superseded packet must name a valid replacement")
    elif metadata.get("superseded_by") is not None:
        errors.append("active packet cannot name a superseding packet")

    identity = packet.get("identity")
    if not isinstance(identity, dict) or identity.get("artifact_schema") != IDENTITY_SCHEMA:
        errors.append("packet has no supported Identity artifact lock")
    else:
        for field in ("source_digest",):
            if not isinstance(identity.get(field), str) or SHA256.fullmatch(identity[field]) is None:
                errors.append(f"identity.{field} is invalid")
        package_digest = identity.get("package_digest")
        if (
            not isinstance(package_digest, dict)
            or package_digest.get("algorithm") != "sha256-canonical-json"
            or not isinstance(package_digest.get("value"), str)
            or SHA256.fullmatch(package_digest["value"]) is None
        ):
            errors.append("Identity package digest is invalid")

    catalog = packet.get("catalog")
    if not isinstance(catalog, dict):
        errors.append("packet has no catalog lock")
    else:
        digest = catalog.get("digest")
        if (
            not isinstance(digest, dict)
            or digest.get("algorithm") != "sha256-utf8-lf"
            or not isinstance(digest.get("value"), str)
            or SHA256.fullmatch(digest["value"]) is None
        ):
            errors.append("catalog digest lock is invalid")
        if not isinstance(catalog.get("source_urls"), list) or not catalog["source_urls"]:
            errors.append("catalog source URLs are missing")
        live = catalog.get("live_verification")
        if not isinstance(live, dict) or live.get("status") not in {"required", "verified"}:
            errors.append("catalog live verification state is invalid")
        elif live.get("status") == "verified":
            for field in ("verified_at", "verified_by", "evidence"):
                if not isinstance(live.get(field), str) or not live[field].strip():
                    errors.append(f"verified catalog freshness requires {field}")
        elif any(live.get(field) is not None for field in ("verified_at", "verified_by", "evidence")):
            errors.append("required catalog verification cannot contain partial evidence")

    channels = packet.get("channels")
    if not isinstance(channels, list) or not channels:
        errors.append("packet requires at least one channel")
        channels = []
    channel_ids: set[str] = set()
    target_ids: set[str] = set()
    approval = packet.get("review", {}).get("approval") if isinstance(packet.get("review"), dict) else None
    approval_id = approval.get("id") if isinstance(approval, dict) else None
    for index, channel in enumerate(channels):
        if not isinstance(channel, dict):
            errors.append(f"channels[{index}] must be an object")
            continue
        identifier = channel.get("id")
        target_id = channel.get("target_id")
        if not isinstance(identifier, str) or IDENTIFIER.fullmatch(identifier) is None:
            errors.append(f"channels[{index}].id is invalid")
        elif identifier in channel_ids:
            errors.append(f"duplicate channel id: {identifier}")
        else:
            channel_ids.add(identifier)
        if not isinstance(target_id, str) or not target_id:
            errors.append(f"channels[{index}].target_id is invalid")
        elif target_id in target_ids:
            errors.append(f"duplicate target id: {target_id}")
        else:
            target_ids.add(target_id)
        surface = channel.get("surface")
        if not isinstance(surface, dict) or not isinstance(surface.get("dimensions"), dict):
            errors.append(f"channels[{index}] has no exact surface dimensions")
        else:
            dimensions = surface["dimensions"]
            if any(
                not isinstance(dimensions.get(field), int) or dimensions[field] < 1
                for field in ("widthPx", "heightPx")
            ):
                errors.append(f"channels[{index}] has invalid surface dimensions")
            safe_zone = surface.get("safeZone")
            if not isinstance(safe_zone, dict) or safe_zone.get("state") not in {
                "known",
                "unknown",
            }:
                errors.append(f"channels[{index}] has no valid safe-zone state")
        asset = channel.get("asset")
        if (
            not isinstance(asset, dict)
            or not isinstance(asset.get("sha256"), str)
            or SHA256.fullmatch(asset["sha256"]) is None
        ):
            errors.append(f"channels[{index}] has no asset provenance")
        copy = channel.get("copy")
        if not isinstance(copy, dict):
            errors.append(f"channels[{index}] has no copy record")
            continue
        claims = copy.get("claims")
        if not isinstance(claims, list):
            errors.append(f"channels[{index}] claims must be an array")
            claims = []
        if state in {"draft", "reviewed"}:
            if copy.get("status") != "candidate" or copy.get("approval_id") is not None:
                errors.append(f"channels[{index}] pre-export copy must remain candidate")
            for claim in claims:
                if not isinstance(claim, dict) or claim.get("status") != "candidate" or claim.get(
                    "approval_id"
                ) is not None:
                    errors.append(f"channels[{index}] pre-export claims must remain candidate")
        if state in {"approved-for-export", "published"}:
            if copy.get("status") != "approved" or copy.get("approval_id") != approval_id:
                errors.append(f"channels[{index}] approved copy lacks the packet approval")
            for claim in claims:
                if not isinstance(claim, dict) or claim.get("status") != "approved" or claim.get(
                    "approval_id"
                ) != approval_id:
                    errors.append(f"channels[{index}] approved claim lacks the packet approval")
        attribution = channel.get("attribution")
        if isinstance(attribution, dict) and attribution.get("required") is True:
            if not isinstance(attribution.get("text"), str) or not attribution["text"].strip():
                errors.append(f"channels[{index}] is missing required attribution")
        link = channel.get("required_link")
        if link is not None and (not isinstance(link, str) or HTTPS_URL.fullmatch(link) is None):
            errors.append(f"channels[{index}] required link is not HTTPS")

    review = packet.get("review")
    if not isinstance(review, dict):
        errors.append("packet review must be an object")
    elif state == "draft":
        if review.get("status") != "pending" or review.get("approval") is not None:
            errors.append("draft packet cannot claim review or approval")
        if any(review.get(field) is not None for field in ("reviewed_by", "reviewed_at", "notes")):
            errors.append("draft packet cannot contain partial review evidence")
    elif state == "reviewed":
        if review.get("status") != "reviewed" or review.get("approval") is not None:
            errors.append("reviewed packet must remain unapproved")
        for field in ("reviewed_by", "reviewed_at", "notes"):
            if not isinstance(review.get(field), str) or not review[field].strip():
                errors.append(f"reviewed packet requires review.{field}")
    elif state in {"approved-for-export", "published"}:
        if review.get("status") != "approved-for-export" or not isinstance(approval, dict):
            errors.append("exportable packet requires explicit human approval")
        else:
            if approval.get("schema_version") != APPROVAL_SCHEMA:
                errors.append("campaign approval schema is unsupported")
            if approval.get("packet_id") != metadata.get("id"):
                errors.append("campaign approval belongs to a different packet")
            if approval.get("decision") != "approved-for-export":
                errors.append("campaign approval decision is unsupported")
            if not isinstance(approval.get("id"), str) or APPROVAL_ID.fullmatch(
                approval["id"]
            ) is None:
                errors.append("campaign approval id is invalid")
            for field in ("approved_by", "evidence"):
                if not isinstance(approval.get(field), str) or not approval[field].strip():
                    errors.append(f"campaign approval requires {field}")
            try:
                require_timestamp(approval.get("approved_at"), "approval.approved_at")
            except HandoffError as error:
                errors.append(str(error))
            digest = approval.get("reviewed_packet_digest")
            try:
                expected_reviewed_digest = canonical_digest(reviewed_basis(packet))
            except (AttributeError, KeyError, TypeError):
                expected_reviewed_digest = None
            if (
                not isinstance(digest, dict)
                or digest.get("algorithm") != "sha256-canonical-json"
                or digest.get("value") != expected_reviewed_digest
            ):
                errors.append("campaign approval digest does not match the exact reviewed packet")

    checklist = packet.get("publishing_checklist")
    checklist_index: dict[str, dict[str, Any]] = {}
    if not isinstance(checklist, list):
        errors.append("publishing checklist must be an array")
        checklist = []
    for item in checklist:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            errors.append("checklist item has no stable ID")
            continue
        if item["id"] in checklist_index:
            errors.append(f"duplicate checklist item: {item['id']}")
        checklist_index[item["id"]] = item
        if item.get("status") == "completed":
            for field in ("evidence", "completed_by", "completed_at"):
                if not isinstance(item.get(field), str) or not item[field].strip():
                    errors.append(f"completed checklist item {item['id']} requires {field}")
    if set(checklist_index) != set(CHECKLIST_IDS):
        errors.append("publishing checklist does not match the required v1 checklist")
    if state in {"approved-for-export", "published"}:
        incomplete = sorted(
            identifier
            for identifier, item in checklist_index.items()
            if item.get("required") is True and item.get("status") != "completed"
        )
        if incomplete:
            errors.append(f"required checklist items are incomplete: {', '.join(incomplete)}")
        live = catalog.get("live_verification") if isinstance(catalog, dict) else None
        if isinstance(live, dict) and live.get("required") is True and live.get("status") != "verified":
            errors.append("catalog freshness must be verified before export approval")

    external = packet.get("external_handoff")
    if not isinstance(external, dict):
        errors.append("external handoff must be an object")
    elif state in {"draft", "reviewed"} and external.get("authorized") is not False:
        errors.append("draft or reviewed packet cannot authorize external handoff")
    elif state in {"draft", "reviewed"} and any(
        external.get(field) is not None for field in ("authorization_approval_id", "adapter")
    ):
        errors.append("draft or reviewed packet cannot contain external authorization evidence")
    elif state in {"approved-for-export", "published"}:
        if external.get("authorized") is not True or external.get(
            "authorization_approval_id"
        ) != approval_id:
            errors.append("external export authorization does not match human approval")
        if external.get("allowed_action") != "immutable-export-only":
            errors.append("external handoff may authorize immutable export only")

    publication = packet.get("publication")
    if not isinstance(publication, dict):
        errors.append("publication record must be an object")
    elif state == "published":
        receipt = publication.get("receipt")
        if publication.get("status") != "published" or not isinstance(receipt, dict):
            errors.append("published state requires an external publication receipt")
        else:
            if receipt.get("authorization_approval_id") != approval_id:
                errors.append("publication receipt does not preserve export approval")
            for field in ("adapter", "platform_event_id", "published_at"):
                if not isinstance(receipt.get(field), str) or not receipt[field].strip():
                    errors.append(f"publication receipt requires {field}")
            try:
                require_timestamp(receipt.get("published_at"), "publication receipt published_at")
            except HandoffError as error:
                errors.append(str(error))
            if receipt.get("adapter") != (
                external.get("adapter") if isinstance(external, dict) else None
            ):
                errors.append("publication receipt adapter does not match external handoff")
            exported_digest = receipt.get("exported_packet_digest")
            try:
                expected_exported_digest = canonical_digest(approved_basis(packet))
            except (AttributeError, KeyError, TypeError):
                expected_exported_digest = None
            if (
                not isinstance(exported_digest, dict)
                or exported_digest.get("algorithm") != "sha256-canonical-json"
                or exported_digest.get("value") != expected_exported_digest
            ):
                errors.append("publication receipt digest does not match the exported packet")
    elif publication.get("status") != "not-published" or publication.get("receipt") is not None:
        errors.append("non-published packet cannot contain a publication receipt")

    lifecycle = packet.get("lifecycle")
    history = lifecycle.get("history") if isinstance(lifecycle, dict) else None
    if not isinstance(history, list) or not history:
        errors.append("lifecycle history is missing")
    else:
        previous = None
        allowed_history = {
            "draft": {"reviewed", "superseded"},
            "reviewed": {"approved-for-export", "superseded"},
            "approved-for-export": {"published", "superseded"},
            "published": {"superseded"},
            "superseded": set(),
        }
        for index, event in enumerate(history):
            if not isinstance(event, dict):
                errors.append(f"lifecycle history event {index} must be an object")
                continue
            if event.get("from") != previous:
                errors.append(f"lifecycle history is not contiguous at event {index}")
            if event.get("to") not in states:
                errors.append(f"lifecycle history event {index} has an invalid state")
            if index > 0 and event.get("to") not in allowed_history.get(previous, set()):
                errors.append(f"lifecycle history contains an invalid transition at event {index}")
            for field in ("actor", "occurred_at", "reason"):
                if not isinstance(event.get(field), str) or not event[field].strip():
                    errors.append(f"lifecycle history event {index} requires {field}")
            previous = event.get("to")
        if history[0].get("from") is not None or history[0].get("to") != "draft":
            errors.append("lifecycle history must begin with creation of a draft")
        if previous != state:
            errors.append("lifecycle history does not end in the current packet state")
        if any(event.get("from") == "superseded" for event in history if isinstance(event, dict)):
            errors.append("superseded packet state is terminal")
    return sorted(set(errors))


def complete_check(
    packet: dict[str, Any],
    check_id: str,
    completed_by: str,
    completed_at: str,
    evidence: str,
) -> dict[str, Any]:
    """Record evidence for one checklist item without changing lifecycle state."""

    errors = validate_packet(packet)
    if errors:
        raise HandoffError(errors[0])
    if packet["packet"]["state"] not in {"draft", "reviewed"}:
        raise HandoffError("checklist evidence can be changed only before export approval")
    require_text(completed_by, "completed_by")
    require_timestamp(completed_at, "completed_at")
    require_text(evidence, "evidence")
    updated = deepcopy(packet)
    matches = [item for item in updated["publishing_checklist"] if item["id"] == check_id]
    if len(matches) != 1:
        raise HandoffError(f"unknown checklist item: {check_id}")
    matches[0].update(
        {
            "status": "completed",
            "evidence": evidence,
            "completed_by": completed_by,
            "completed_at": completed_at,
        }
    )
    errors = validate_packet(updated)
    if errors:
        raise HandoffError(errors[0])
    return updated


def record_freshness(
    packet: dict[str, Any],
    verified_by: str,
    verified_at: str,
    evidence: str,
) -> dict[str, Any]:
    """Record an external current-fact check without fetching or changing facts."""

    errors = validate_packet(packet)
    if errors:
        raise HandoffError(errors[0])
    if packet["packet"]["state"] not in {"draft", "reviewed"}:
        raise HandoffError("freshness evidence can be changed only before export approval")
    require_text(verified_by, "verified_by")
    require_timestamp(verified_at, "verified_at")
    require_text(evidence, "evidence")
    updated = deepcopy(packet)
    updated["catalog"]["live_verification"] = {
        "status": "verified",
        "required": True,
        "verified_at": verified_at,
        "verified_by": verified_by,
        "evidence": evidence,
    }
    for item in updated["publishing_checklist"]:
        if item["id"] == "catalog-freshness":
            item.update(
                {
                    "status": "completed",
                    "evidence": evidence,
                    "completed_by": verified_by,
                    "completed_at": verified_at,
                }
            )
    errors = validate_packet(updated)
    if errors:
        raise HandoffError(errors[0])
    return updated


def transition_packet(
    packet: dict[str, Any],
    to_state: str,
    actor: str,
    occurred_at: str,
    reason: str,
    *,
    review_notes: str | None = None,
    approval: dict[str, Any] | None = None,
    superseded_by: str | None = None,
) -> dict[str, Any]:
    """Apply one allowed human-owned lifecycle transition."""

    errors = validate_packet(packet)
    if errors:
        raise HandoffError(errors[0])
    current = packet["packet"]["state"]
    if current == "superseded":
        raise HandoffError("superseded packet state is terminal")
    if to_state == "published":
        raise HandoffError(
            "this skill cannot publish; only a separately authorized adapter may record publication"
        )
    allowed = {
        "draft": {"reviewed", "superseded"},
        "reviewed": {"approved-for-export", "superseded"},
        "approved-for-export": {"superseded"},
        "published": {"superseded"},
    }
    if to_state not in allowed.get(current, set()):
        raise HandoffError(f"unsupported lifecycle transition: {current} -> {to_state}")
    require_text(actor, "actor")
    require_timestamp(occurred_at, "occurred_at")
    require_text(reason, "reason")
    updated = deepcopy(packet)
    if to_state == "reviewed":
        updated["review"] = {
            "status": "reviewed",
            "reviewed_by": actor,
            "reviewed_at": occurred_at,
            "notes": require_text(review_notes, "review_notes"),
            "approval": None,
        }
    elif to_state == "approved-for-export":
        if not isinstance(approval, dict):
            raise HandoffError("approved-for-export transition requires an approval record")
        require_closed(
            approval,
            {
                "schema_version",
                "id",
                "packet_id",
                "reviewed_packet_digest",
                "decision",
                "approved_by",
                "approved_at",
                "evidence",
            },
            "approval record",
        )
        if approval.get("schema_version") != APPROVAL_SCHEMA:
            raise HandoffError(f"approval schema must be {APPROVAL_SCHEMA}")
        if approval.get("packet_id") != packet["packet"]["id"]:
            raise HandoffError("approval record belongs to a different packet")
        digest = approval.get("reviewed_packet_digest")
        if (
            not isinstance(digest, dict)
            or digest.get("algorithm") != "sha256-canonical-json"
            or digest.get("value") != canonical_digest(packet)
        ):
            raise HandoffError("approval digest does not match the exact reviewed packet")
        if approval.get("decision") != "approved-for-export":
            raise HandoffError("approval decision must be approved-for-export")
        for field in ("id", "approved_by", "approved_at", "evidence"):
            require_text(approval.get(field), f"approval.{field}")
        require_timestamp(approval["approved_at"], "approval.approved_at")
        incomplete = [
            item["id"]
            for item in packet["publishing_checklist"]
            if item["required"] and item["status"] != "completed"
        ]
        if incomplete:
            raise HandoffError(f"required checklist items are incomplete: {', '.join(incomplete)}")
        live = packet["catalog"]["live_verification"]
        if live["required"] and live["status"] != "verified":
            raise HandoffError("catalog freshness must be verified before export approval")
        approval_id = approval["id"]
        updated["review"]["status"] = "approved-for-export"
        updated["review"]["approval"] = deepcopy(approval)
        updated["external_handoff"].update(
            {"authorized": True, "authorization_approval_id": approval_id}
        )
        for channel in updated["channels"]:
            channel["copy"]["status"] = "approved"
            channel["copy"]["approval_id"] = approval_id
            for claim in channel["copy"]["claims"]:
                claim["status"] = "approved"
                claim["approval_id"] = approval_id
    elif to_state == "superseded":
        if not isinstance(superseded_by, str) or CAMPAIGN_ID.fullmatch(superseded_by) is None:
            raise HandoffError("superseded transition requires a valid replacement campaign ID")
        if superseded_by == packet["packet"]["id"]:
            raise HandoffError("packet cannot supersede itself")
        updated["packet"]["superseded_by"] = superseded_by
    updated["packet"]["state"] = to_state
    updated["lifecycle"]["history"].append(
        {
            "from": current,
            "to": to_state,
            "actor": actor,
            "occurred_at": occurred_at,
            "reason": reason,
        }
    )
    errors = validate_packet(updated)
    if errors:
        raise HandoffError(errors[0])
    return updated


def write_output(output: Path, value: dict[str, Any], inputs: Sequence[Path]) -> None:
    """Atomically write derived output without mutating an input or symlink."""

    resolved = output.resolve()
    if any(resolved == path.resolve() for path in inputs):
        raise HandoffError("output must not overwrite an input artifact")
    current = output.parent
    while current != current.parent:
        if current.is_symlink():
            raise HandoffError("output path may not traverse a symbolic link")
        if current.exists():
            break
        current = current.parent
    if output.is_symlink():
        raise HandoffError("output path may not be a symbolic link")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_name(f".{output.name}.tmp")
    temporary.write_text(canonical_json(value), encoding="utf-8")
    os.replace(temporary, output)


def build_parser() -> argparse.ArgumentParser:
    """Build the portable command interface."""

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Prepare a new deterministic draft packet.")
    prepare.add_argument("--identity-package", type=Path, required=True)
    prepare.add_argument("--catalog", type=Path, required=True)
    prepare.add_argument("--brief", type=Path, required=True)
    prepare.add_argument("--output", type=Path, required=True)

    validate = subparsers.add_parser("validate", help="Validate one campaign handoff packet.")
    validate.add_argument("--packet", type=Path, required=True)
    validate.add_argument("--output-format", choices=("human", "json"), default="human")

    digest = subparsers.add_parser("digest", help="Print the canonical reviewed packet digest.")
    digest.add_argument("--packet", type=Path, required=True)

    freshness = subparsers.add_parser(
        "record-freshness", help="Record a human current-fact verification."
    )
    freshness.add_argument("--packet", type=Path, required=True)
    freshness.add_argument("--verified-by", required=True)
    freshness.add_argument("--verified-at", required=True)
    freshness.add_argument("--evidence", required=True)
    freshness.add_argument("--output", type=Path, required=True)

    check = subparsers.add_parser("complete-check", help="Complete one reviewed checklist item.")
    check.add_argument("--packet", type=Path, required=True)
    check.add_argument("--check-id", choices=CHECKLIST_IDS, required=True)
    check.add_argument("--completed-by", required=True)
    check.add_argument("--completed-at", required=True)
    check.add_argument("--evidence", required=True)
    check.add_argument("--output", type=Path, required=True)

    transition = subparsers.add_parser("transition", help="Apply an allowed human-owned state change.")
    transition.add_argument("--packet", type=Path, required=True)
    transition.add_argument(
        "--to-state",
        choices=("reviewed", "approved-for-export", "published", "superseded"),
        required=True,
    )
    transition.add_argument("--actor", required=True)
    transition.add_argument("--occurred-at", required=True)
    transition.add_argument("--reason", required=True)
    transition.add_argument("--review-notes")
    transition.add_argument("--approval-record", type=Path)
    transition.add_argument("--superseded-by")
    transition.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run one command and return a stable status."""

    arguments = build_parser().parse_args(argv)
    try:
        if arguments.command == "prepare":
            identity = load_json(arguments.identity_package)
            catalog = load_json(arguments.catalog)
            brief = load_json(arguments.brief)
            packet = prepare_packet(
                identity,
                arguments.identity_package,
                catalog,
                arguments.catalog,
                brief,
            )
            write_output(
                arguments.output,
                packet,
                (arguments.identity_package, arguments.catalog, arguments.brief),
            )
            print(arguments.output)
        elif arguments.command == "validate":
            packet = load_json(arguments.packet)
            errors = validate_packet(packet)
            if arguments.output_format == "json":
                print(canonical_json({"valid": not errors, "errors": errors}), end="")
            elif errors:
                for error in errors:
                    print(f"ERROR: {error}")
            else:
                print(f"VALID {arguments.packet}")
            return 1 if errors else 0
        elif arguments.command == "digest":
            packet = load_json(arguments.packet)
            errors = validate_packet(packet)
            if errors:
                raise HandoffError(errors[0])
            print(canonical_digest(packet))
        elif arguments.command == "record-freshness":
            packet = load_json(arguments.packet)
            updated = record_freshness(
                packet,
                arguments.verified_by,
                arguments.verified_at,
                arguments.evidence,
            )
            write_output(arguments.output, updated, (arguments.packet,))
            print(arguments.output)
        elif arguments.command == "complete-check":
            packet = load_json(arguments.packet)
            updated = complete_check(
                packet,
                arguments.check_id,
                arguments.completed_by,
                arguments.completed_at,
                arguments.evidence,
            )
            write_output(arguments.output, updated, (arguments.packet,))
            print(arguments.output)
        elif arguments.command == "transition":
            packet = load_json(arguments.packet)
            approval = (
                load_json(arguments.approval_record)
                if arguments.approval_record is not None
                else None
            )
            updated = transition_packet(
                packet,
                arguments.to_state,
                arguments.actor,
                arguments.occurred_at,
                arguments.reason,
                review_notes=arguments.review_notes,
                approval=approval,
                superseded_by=arguments.superseded_by,
            )
            inputs = [arguments.packet]
            if arguments.approval_record is not None:
                inputs.append(arguments.approval_record)
            write_output(arguments.output, updated, inputs)
            print(arguments.output)
    except (HandoffError, OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
