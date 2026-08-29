#!/usr/bin/env python3
"""Build and validate Aether's normalized artifact provenance model."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
FIRST_PARTY_CATALOG = ROOT / "catalog" / "first-party" / "catalog.v1.json"
EXTERNAL_CATALOGS = (
    ROOT / "catalog" / "external" / "approved-skills.v1.json",
    ROOT / "catalog" / "external" / "source-candidates.v1.json",
)
AGENT_CATALOG = ROOT / "library" / "organization" / "agents" / "catalog.json"
SCHEMA_PATH = ROOT / "catalog" / "schemas" / "aether.provenance-catalog.v1.schema.json"
REPOSITORY_LICENSE = "MIT"
SCHEMA_VERSION = "aether.provenance-catalog/v1"
LIFECYCLE_STATES = {"draft", "experimental", "stable", "deprecated", "retired"}
TRUST_STATES = {"first-party", "trusted", "restricted", "untrusted", "unknown"}
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
HEX_64_RE = re.compile(r"^[a-f0-9]{64}$")
REVISION_RE = re.compile(
    r"^(?:[a-f0-9]{7,64}|v?[0-9]+\.[0-9]+\.[0-9]+(?:[-+][0-9A-Za-z.-]+)?)$"
)


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def normalized_text(path: Path) -> str:
    """Read UTF-8 text with canonical LF line endings."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def source_digest(path: Path) -> str:
    """Return the canonical sha256-utf8-lf digest for a source file."""
    return hashlib.sha256(normalized_text(path).encode("utf-8")).hexdigest()


def parse_frontmatter(path: Path) -> dict[str, Any]:
    """Parse a Markdown YAML frontmatter mapping."""
    match = FRONTMATTER_RE.match(normalized_text(path))
    if match is None:
        raise ValueError(f"{path} is missing YAML frontmatter")
    value = yaml.safe_load(match.group(1))
    if not isinstance(value, dict):
        raise ValueError(f"{path} frontmatter must be a mapping")
    return value


def canonical_bytes(value: Any) -> bytes:
    """Serialize JSON deterministically for reproducibility checks."""
    return json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")


def normalize_lifecycle(value: Any, *, source_state: str | None = None) -> dict[str, str]:
    """Map source lifecycle vocabulary into the canonical lifecycle states."""
    state = str(value or "draft").lower()
    mapping = {
        "approved": "stable",
        "pending": "draft",
        "reviewed": "experimental",
        "rejected": "retired",
        "unknown": "draft",
    }
    normalized = mapping.get(state, state)
    if normalized not in LIFECYCLE_STATES:
        normalized = "draft"
    result = {"state": normalized}
    original = source_state or state
    if original != normalized:
        result["source_state"] = original
    return result


def _publishability(record: dict[str, Any]) -> tuple[bool, list[str]]:
    """Return whether a record may enter stable publication and why not."""
    reasons: list[str] = []
    source = record.get("source") if isinstance(record.get("source"), dict) else {}
    digest = source.get("digest") if isinstance(source.get("digest"), dict) else {}
    revision = str(source.get("revision", ""))
    license_value = str(record.get("license", "")).strip()
    trust = str(record.get("trust", "unknown"))
    maintainers = record.get("maintainers")

    if not revision or revision == "unknown" or REVISION_RE.fullmatch(revision) is None:
        reasons.append("source revision is not an immutable commit or semantic version")
    if digest.get("algorithm") not in {"sha256-utf8-lf", "sha256-tree", "sha256-bytes"}:
        reasons.append("source digest algorithm is unsupported")
    if not isinstance(digest.get("value"), str) or HEX_64_RE.fullmatch(digest["value"]) is None:
        reasons.append("source digest is missing or invalid")
    if not license_value or license_value.lower() in {"unknown", "tbd", "unverified"}:
        reasons.append("license is unresolved")
    if trust in {"unknown", "untrusted", "restricted"}:
        reasons.append(f"trust classification '{trust}' is not eligible for stable publication")
    if not isinstance(maintainers, list) or not maintainers:
        reasons.append("maintainer ownership is missing")

    lifecycle = record.get("lifecycle") if isinstance(record.get("lifecycle"), dict) else {}
    if lifecycle.get("state") != "stable":
        reasons.append("lifecycle is not stable")

    return not reasons, sorted(set(reasons))


def _first_party_record(artifact: dict[str, Any]) -> dict[str, Any]:
    """Normalize an existing first-party v1 catalog artifact."""
    source_path = str(artifact.get("source_path", ""))
    kind = str(artifact.get("kind", "other"))
    if kind not in {"specification", "skill", "agent", "prompt", "instruction"}:
        raise ValueError(f"unsupported first-party artifact kind: {kind}")
    lifecycle = normalize_lifecycle((artifact.get("lifecycle") or {}).get("state"))
    record = {
        "id": str(artifact.get("id", "")),
        "kind": kind,
        "party": "first-party",
        "source": {
            "repository": "egohygiene/aether",
            "path": source_path,
            "revision": str(artifact.get("artifact_version", "unknown")),
            "digest": dict(artifact.get("source_digest") or {}),
        },
        "license": str(artifact.get("license", "unknown")),
        "trust": "first-party",
        "lifecycle": lifecycle,
        "compatibility": dict(artifact.get("compatibility") or {"required_tools": []}),
        "maintainers": sorted(set((artifact.get("owner") or {}).get("maintainers") or [])),
        "publishable": False,
        "blocked_reasons": [],
    }
    publishable, reasons = _publishability(record)
    record["publishable"] = publishable
    record["blocked_reasons"] = reasons
    return record


def _agent_records() -> list[dict[str, Any]]:
    """Normalize canonical organization agents without making provider projections canonical."""
    catalog = load_json(AGENT_CATALOG)
    agents = catalog.get("agents")
    if not isinstance(agents, dict):
        raise ValueError(f"{AGENT_CATALOG} agents must be an object")

    records: list[dict[str, Any]] = []
    for agent_id in sorted(agents):
        catalog_entry = agents[agent_id]
        if not isinstance(catalog_entry, dict):
            raise ValueError(f"agent {agent_id} catalog entry must be an object")
        path = ROOT / "library" / "organization" / "agents" / agent_id / "AGENT.md"
        if not path.exists():
            raise ValueError(f"agent {agent_id} is missing {path.relative_to(ROOT)}")
        frontmatter = parse_frontmatter(path)
        metadata = frontmatter.get("metadata") if isinstance(frontmatter.get("metadata"), dict) else {}
        declared_id = str(frontmatter.get("aether-id", ""))
        if declared_id != agent_id:
            raise ValueError(f"agent {agent_id} frontmatter id is {declared_id!r}")

        owners_value = metadata.get("aether-owners", "egohygiene")
        if isinstance(owners_value, list):
            maintainers = sorted({str(value) for value in owners_value if str(value)})
        else:
            maintainers = [str(owners_value)] if str(owners_value) else ["egohygiene"]

        tools = catalog_entry.get("tools") if isinstance(catalog_entry.get("tools"), list) else []
        lifecycle = normalize_lifecycle(metadata.get("aether-status", catalog_entry.get("status", "draft")))
        record = {
            "id": f"agent/{agent_id}",
            "kind": "agent",
            "party": "first-party",
            "source": {
                "repository": "egohygiene/aether",
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "revision": str(metadata.get("aether-version", catalog_entry.get("version", "unknown"))),
                "digest": {
                    "algorithm": "sha256-utf8-lf",
                    "value": source_digest(path),
                },
            },
            "license": REPOSITORY_LICENSE,
            "trust": "first-party",
            "lifecycle": lifecycle,
            "compatibility": {
                "required_tools": sorted({str(tool) for tool in tools if str(tool)}),
                "notes": "Agent tool capabilities are recorded as compatibility requirements; provider projections remain generated adapters.",
            },
            "maintainers": maintainers,
            "publishable": False,
            "blocked_reasons": [],
        }
        publishable, reasons = _publishability(record)
        record["publishable"] = publishable
        record["blocked_reasons"] = reasons
        records.append(record)
    return records


def _generic_markdown_records(kind: str, directory_name: str, filename: str) -> list[dict[str, Any]]:
    """Normalize future canonical prompt/instruction records when their source directories exist."""
    root = ROOT / "library" / "organization" / directory_name
    if not root.exists():
        return []
    records: list[dict[str, Any]] = []
    for path in sorted(root.rglob(filename)):
        frontmatter = parse_frontmatter(path)
        artifact_id = str(frontmatter.get("aether-id") or frontmatter.get("id") or path.parent.name)
        metadata = frontmatter.get("metadata") if isinstance(frontmatter.get("metadata"), dict) else {}
        status = metadata.get("aether-status", frontmatter.get("status", "draft"))
        version = metadata.get("aether-version", frontmatter.get("version", "unknown"))
        owners = metadata.get("aether-owners", frontmatter.get("owners", ["egohygiene"]))
        if isinstance(owners, list):
            maintainers = sorted({str(owner) for owner in owners if str(owner)})
        else:
            maintainers = [str(owners)] if str(owners) else ["egohygiene"]
        license_value = str(frontmatter.get("license", REPOSITORY_LICENSE))
        record = {
            "id": f"{kind}/{artifact_id}",
            "kind": kind,
            "party": "first-party",
            "source": {
                "repository": "egohygiene/aether",
                "path": str(path.relative_to(ROOT)).replace("\\", "/"),
                "revision": str(version),
                "digest": {"algorithm": "sha256-utf8-lf", "value": source_digest(path)},
            },
            "license": license_value,
            "trust": "first-party",
            "lifecycle": normalize_lifecycle(status),
            "compatibility": {"required_tools": []},
            "maintainers": maintainers,
            "publishable": False,
            "blocked_reasons": [],
        }
        publishable, reasons = _publishability(record)
        record["publishable"] = publishable
        record["blocked_reasons"] = reasons
        records.append(record)
    return records


def build_first_party() -> dict[str, Any]:
    """Build the normalized first-party provenance catalog."""
    source_catalog = load_json(FIRST_PARTY_CATALOG)
    artifacts = source_catalog.get("artifacts")
    if not isinstance(artifacts, list):
        raise ValueError(f"{FIRST_PARTY_CATALOG} artifacts must be an array")

    records = [_first_party_record(artifact) for artifact in artifacts if isinstance(artifact, dict)]
    records.extend(_agent_records())
    records.extend(_generic_markdown_records("prompt", "prompts", "PROMPT.md"))
    records.extend(_generic_markdown_records("instruction", "instructions", "INSTRUCTION.md"))
    records.sort(key=lambda record: record["id"])
    return {"schema_version": SCHEMA_VERSION, "records": records}


def _external_lifecycle(entry: dict[str, Any]) -> dict[str, str]:
    """Map external review status to the shared lifecycle vocabulary."""
    state = str(entry.get("review_state", "unknown"))
    return normalize_lifecycle(state, source_state=state)


def build_external() -> dict[str, Any]:
    """Build the normalized external provenance catalog."""
    entries: list[dict[str, Any]] = []
    for catalog_path in EXTERNAL_CATALOGS:
        source_catalog = load_json(catalog_path)
        candidate_entries = source_catalog.get("entries")
        if not isinstance(candidate_entries, list):
            raise ValueError(f"{catalog_path} entries must be an array")
        for entry in candidate_entries:
            if not isinstance(entry, dict):
                raise ValueError(f"{catalog_path} entries must be objects")
            entries.append(entry)

    records: list[dict[str, Any]] = []
    for entry in entries:
        source_type = str(entry.get("source_type", "other"))
        if source_type not in {"skill", "specification", "agent", "prompt", "instruction"}:
            raise ValueError(f"unsupported external source_type: {source_type}")
        upstream_ref = entry.get("upstream_ref") if isinstance(entry.get("upstream_ref"), dict) else {}
        revision = str(upstream_ref.get("commit") or upstream_ref.get("tag") or "unknown")
        if revision == "unknown" and str(upstream_ref.get("tag", "")) != "unknown":
            revision = str(upstream_ref["tag"])
        license_info = entry.get("upstream_license") if isinstance(entry.get("upstream_license"), dict) else {}
        compatibility = entry.get("compatibility") if isinstance(entry.get("compatibility"), dict) else {"required_tools": []}
        trust = str(entry.get("trust_classification", "unknown"))
        if trust not in TRUST_STATES:
            trust = "unknown"
        record = {
            "id": str(entry.get("id", "")),
            "kind": source_type,
            "party": "external",
            "source": {
                "repository": str(entry.get("upstream_repository", "unknown")),
                "path": str(entry.get("upstream_skill_path", "unknown")),
                "revision": revision,
                "digest": dict(entry.get("content_hash") or {}),
            },
            "license": str(license_info.get("spdx_or_unknown", "unknown")),
            "trust": trust,
            "lifecycle": _external_lifecycle(entry),
            "compatibility": {
                "required_tools": sorted({str(tool) for tool in compatibility.get("required_tools", []) if str(tool)})
            },
            "maintainers": ["egohygiene"],
            "publishable": False,
            "blocked_reasons": [],
        }
        publishable, reasons = _publishability(record)
        if entry.get("redistribution_permission") != "allowed":
            reasons.append("redistribution permission is not allowed")
        if entry.get("redistribution_status") != "verified":
            reasons.append("redistribution status is not verified")
        record["publishable"] = publishable and not reasons
        record["blocked_reasons"] = sorted(set(reasons))
        records.append(record)

    records.sort(key=lambda record: record["id"])
    return {"schema_version": SCHEMA_VERSION, "records": records}


def validate_catalog(catalog: dict[str, Any]) -> list[str]:
    """Validate schema, uniqueness, lifecycle semantics, and stable-publication gates."""
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)
    errors = [
        f"schema violation at {'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
        for error in validator.iter_errors(catalog)
    ]

    records = catalog.get("records", [])
    identifiers = [record.get("id") for record in records if isinstance(record, dict)]
    if identifiers != sorted(identifiers):
        errors.append("records must be sorted by id")
    if len(identifiers) != len(set(identifiers)):
        errors.append("record ids must be unique")

    for record in records:
        if not isinstance(record, dict):
            continue
        publishable, reasons = _publishability(record)
        if bool(record.get("publishable")) != publishable:
            errors.append(f"{record.get('id')}: publishable flag does not match provenance policy")
        expected_reasons = reasons
        if record.get("party") == "external":
            # External redistribution gates are added by build_external and remain
            # visible as blocked reasons even though they are not part of the core
            # source-provenance gate.
            expected_reasons = [
                reason for reason in record.get("blocked_reasons", [])
                if isinstance(reason, str)
            ]
            if publishable and expected_reasons:
                publishable = False
        if record.get("lifecycle", {}).get("state") == "stable" and not record.get("publishable"):
            errors.append(
                f"{record.get('id')}: stable artifact is blocked from publication: "
                + "; ".join(record.get("blocked_reasons", []))
            )
        if record.get("party") == "first-party" and record.get("trust") != "first-party":
            errors.append(f"{record.get('id')}: first-party artifact must use first-party trust")

    return sorted(set(errors))


def build_scope(scope: str) -> dict[str, Any]:
    """Build one requested provenance view."""
    if scope == "first-party":
        return build_first_party()
    if scope == "external":
        return build_external()
    first_party = build_first_party()["records"]
    external = build_external()["records"]
    return {"schema_version": SCHEMA_VERSION, "records": sorted(first_party + external, key=lambda record: record["id"])}


def check(scope: str) -> list[str]:
    """Run validation and deterministic two-build comparison."""
    first = build_scope(scope)
    second = build_scope(scope)
    errors = validate_catalog(first)
    if canonical_bytes(first) != canonical_bytes(second):
        errors.append("determinism failure: consecutive provenance builds differ")

    if scope in {"first-party", "all"}:
        agent_catalog = load_json(AGENT_CATALOG)
        expected_agents = {
            f"agent/{agent_id}" for agent_id in (agent_catalog.get("agents") or {})
        }
        present = {
            record["id"] for record in first["records"] if record.get("party") == "first-party"
        }
        missing = sorted(expected_agents - present)
        if missing:
            errors.append(f"missing canonical agent records: {missing}")

    if scope in {"external", "all"}:
        expected_external = set()
        for catalog_path in EXTERNAL_CATALOGS:
            external_catalog = load_json(catalog_path)
            expected_external.update(
                str(entry.get("id"))
                for entry in external_catalog.get("entries", [])
                if isinstance(entry, dict)
            )
        present = {
            record["id"] for record in first["records"] if record.get("party") == "external"
        }
        missing = sorted(expected_external - present)
        if missing:
            errors.append(f"missing external provenance records: {missing}")

    return sorted(set(errors))


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=["check", "generate"],
        help="Validate the model or generate a normalized catalog.",
    )
    parser.add_argument(
        "--scope",
        choices=["first-party", "external", "all"],
        default="all",
        help="Select which catalog sources to normalize.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Write generated JSON to this path instead of stdout.",
    )
    return parser


def main() -> int:
    """Run the provenance command."""
    arguments = build_parser().parse_args()
    try:
        errors = check(arguments.scope)
        if errors:
            for error in errors:
                print(f"error: {error}", file=sys.stderr)
            return 1
        catalog = build_scope(arguments.scope)
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    if arguments.command == "check":
        counts: dict[str, int] = {}
        for record in catalog["records"]:
            key = f"{record['party']}:{record['kind']}"
            counts[key] = counts.get(key, 0) + 1
        summary = ", ".join(f"{key}={counts[key]}" for key in sorted(counts))
        print(f"provenance validation passed: {summary}")
        return 0

    rendered = json.dumps(catalog, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        sys.stdout.write(rendered)
    else:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
