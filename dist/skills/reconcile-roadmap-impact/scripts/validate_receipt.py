#!/usr/bin/env python3
"""Read-only draft receipt validation; no strategy, source or authority inference."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import stat

from jsonschema import Draft202012Validator

SCHEMA = Path(__file__).resolve().parents[1] / "references/receipt.schema.json"


def validate_receipt(value):
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    if not Draft202012Validator(schema).is_valid(value):
        return ["Roadmap-impact receipt does not satisfy the draft contract"]
    if value["disposition"] == "updated" and value["changed_paths"] != [value["roadmap"]["path"]]:
        return ["Updated receipt must name exactly its canonical roadmap path"]
    return []


def read_receipt(path):
    if not all(hasattr(os, name) for name in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("safe regular input admission unavailable")
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result: raise ValueError("ambiguous JSON")
            result[key] = value
        return result
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        metadata = os.fstat(stream.fileno())
        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= 1024 * 1024:
            raise ValueError("bounded regular input required")
        raw = stream.read(1024 * 1024 + 1)
    if len(raw) > 1024 * 1024: raise ValueError("bounded input required")
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError("nonfinite JSON")))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path)
    args = parser.parse_args()
    try:
        errors = validate_receipt(read_receipt(args.receipt))
    except (OSError, ValueError, TypeError, KeyError, RecursionError):
        errors = ["Roadmap-impact receipt unavailable or invalid; source details withheld"]
    print("invalid: roadmap-impact receipt" if errors else "valid: receipt structure only; no authority or factual verification")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
