#!/usr/bin/env python3
"""Read-only bounded ledger checks; stored discussion has no instruction authority."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime
import json
import os
from pathlib import Path, PurePosixPath
import stat
from urllib.parse import urlsplit

from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = Path(__file__).resolve().parents[1] / "references/ledger.schema.json"
MAX_BYTES = 1024 * 1024


def _safe_reference(value):
    if any(ord(c) < 32 or ord(c) == 127 for c in value) or "\\" in value:
        return False
    parsed = urlsplit(value)
    if parsed.scheme:
        return (parsed.scheme == "https" and bool(parsed.hostname)
                and parsed.username is None and parsed.password is None)
    return (not value.startswith("/") and bool(value)
            and all(part not in {"", ".", ".."} for part in value.split("/"))
            and PurePosixPath(value).as_posix() == value)


def validate_ledger(value):
    """Admission checks; cannot classify prose or verify source/review authenticity."""
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if not Draft202012Validator(schema, format_checker=FormatChecker()).is_valid(value):
        raise ValueError("ledger structure does not satisfy the draft contract")
    if len(json.dumps(value, ensure_ascii=False).encode()) > MAX_BYTES:
        raise ValueError("ledger exceeds bounded segment size")
    if not _safe_reference(value["onboarding"]) or urlsplit(value["onboarding"]).scheme:
        raise ValueError("unsafe onboarding reference")
    by_id = {}
    public = value["visibility"] == "public"
    for entry in value["entries"]:
        if entry["id"] in by_id:
            raise ValueError("duplicate stable checkpoint identity")
        by_id[entry["id"]] = entry
        if public and entry["visibility"] != "public":
            raise ValueError("private checkpoint cannot enter a public ledger")
        if entry["kind"] == "correction" and not entry["corrects"]:
            raise ValueError("correction requires a prior checkpoint")
        if entry["state"] in {"validated", "merged", "published", "provider-submitted"} and not entry["state_evidence"]:
            raise ValueError("completed lifecycle claim requires evidence references")
        sources = entry["provenance"] + entry["state_evidence"]
        for source in sources:
            if not _safe_reference(source["reference"]):
                raise ValueError("unsafe source reference")
            if public and source["visibility"] != "public":
                raise ValueError("private source cannot enter a public ledger")
    for source in value["prior_segments"]:
        if not _safe_reference(source["reference"]) or source["revision"] is None:
            raise ValueError("prior segment requires a safe immutable reference")
        if public and source["visibility"] != "public":
            raise ValueError("private prior segment cannot enter a public ledger")
    edges = {}
    for identity, entry in by_id.items():
        targets = entry["reply_to"] + entry["corrects"] + entry["supersedes"]
        if any(target not in by_id or target == identity for target in targets):
            raise ValueError("missing/self checkpoint link; reconcile required prior context")
        if any(datetime.fromisoformat(by_id[target]["recorded_at"].replace("Z", "+00:00"))
               > datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00")) for target in targets):
            raise ValueError("checkpoint cannot reply to or correct a future entry")
        edges[identity] = set(targets)
    visited, pending = set(), set()
    def visit(identity):
        if identity in pending:
            raise ValueError("checkpoint relationship cycle")
        if identity not in visited:
            pending.add(identity)
            for target in edges[identity]:
                visit(target)
            pending.remove(identity)
            visited.add(identity)
    for identity in by_id:
        visit(identity)
    return value


def reconcile(current, incoming_entries):
    """Pure append/union; never mutate, overwrite or delete caller-owned entries."""
    validate_ledger(current)
    if not isinstance(incoming_entries, list):
        raise ValueError("incoming entries must be a list")
    result = copy.deepcopy(current)
    by_id = {entry["id"]: entry for entry in result["entries"]}
    for entry in incoming_entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("id"), str):
            raise ValueError("incoming checkpoint identity unavailable")
        previous = by_id.get(entry["id"])
        if previous is not None and previous != entry:
            raise ValueError("stable identity collision; preserve contributions for explicit correction")
        by_id[entry["id"]] = copy.deepcopy(entry)
    result["entries"] = list(by_id.values())
    validate_ledger(result)
    result["entries"].sort(key=lambda entry: (datetime.fromisoformat(entry["recorded_at"].replace("Z", "+00:00")), entry["id"]))
    return result


def read_ledger(path):
    if not all(hasattr(os, option) for option in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("safe regular-file admission unavailable")
    def unique(pairs):
        value = {}
        for key, item in pairs:
            if key in value:
                raise ValueError("ambiguous JSON")
            value[key] = item
        return value
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        metadata = os.fstat(stream.fileno())
        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= MAX_BYTES:
            raise ValueError("bounded regular input required")
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("bounded input required")
    value = json.loads(raw, object_pairs_hook=unique,
                       parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))
    return validate_ledger(value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--validate", required=True, type=Path)
    args = parser.parse_args()
    try:
        read_ledger(args.validate)
    except (OSError, ValueError, TypeError, KeyError, RecursionError):
        print("invalid or unavailable: bounded conversation ledger; source content withheld")
        return 1
    print("valid: ledger structure only; source truth, review, privacy and authority require independent verification")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
