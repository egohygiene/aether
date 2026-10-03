#!/usr/bin/env python3
"""Verify a pinned source bundle and, optionally, Egolint report provenance.

This offline check does not classify issues, format titles, or authorize writes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

DEFAULT_SELECTION = (
    Path(__file__).resolve().parents[1]
    / "references/issue-title-contract/selection.v1.json"
)
SOURCE_PATHS = {
    ".github/issues/title-contract.v1.json",
    ".github/issues/schema/title-contract.v1.schema.json",
    ".github/labels/catalog.v1.json",
    "docs/issue-titles.md",
    "fixtures/issue-titles/cases.v1.json",
}


def load_selection(path: Path = DEFAULT_SELECTION) -> dict:
    """Read one immutable selection and verify all cached source bytes."""
    selection = json.loads(path.read_text(encoding="utf-8"))
    if selection["schema_version"] != 1:
        raise ValueError("unsupported selection schema")
    contract = selection["contract"]
    if not re.fullmatch(r"[0-9a-f]{40}", contract["revision"]):
        raise ValueError("contract revision must be an immutable full commit SHA")
    if contract["authority"] not in {"candidate", "accepted"}:
        raise ValueError("contract authority must be explicit")
    if selection["adoption"] != "explicit-repository-selection-observe":
        raise ValueError("selection does not authorize automatic repository adoption")
    files = selection["files"]
    digests = contract["source_digests"]
    if set(files) != SOURCE_PATHS or set(digests) != SOURCE_PATHS:
        raise ValueError("selection must include exactly the five contract sources")
    if len(set(files.values())) != len(files):
        raise ValueError("source cache paths must be distinct")
    root = path.resolve().parent
    sources = {}
    for source_path, relative_path in files.items():
        relative = PurePosixPath(relative_path)
        if relative.is_absolute() or ".." in relative.parts or "\\" in relative_path:
            raise ValueError("source cache path must stay within the selection directory")
        local = (root / relative_path).resolve()
        if not local.is_relative_to(root):
            raise ValueError("source cache path escapes the selection directory")
        raw = local.read_bytes()
        if hashlib.sha256(raw).hexdigest() != digests[source_path]:
            raise ValueError(f"source digest mismatch: {source_path}")
        sources[source_path] = raw
    title_contract = json.loads(sources[".github/issues/title-contract.v1.json"])
    cases = json.loads(sources["fixtures/issue-titles/cases.v1.json"])
    for field in ("contract_id", "contract_version"):
        if title_contract[field] != contract[field] or cases[field] != contract[field]:
            raise ValueError(f"source identity mismatch: {field}")
    if title_contract["owner"] != contract["repository"]:
        raise ValueError("contract owner does not match selected repository")
    catalog = json.loads(sources[".github/labels/catalog.v1.json"])
    if catalog["catalog_version"] != title_contract["label_catalog"]["version"]:
        raise ValueError("label catalog version does not match contract")
    consumer = selection["consumer"]
    if not re.fullmatch(r"[0-9a-f]{40}", consumer["revision"]):
        raise ValueError("consumer revision must be an immutable full commit SHA")
    if consumer["authority"] not in {"candidate", "accepted"}:
        raise ValueError("consumer authority must be explicit")
    return selection


def verify_report(selection: dict, report: dict) -> None:
    """Reject a proposal/report from a missing, stale, or mixed source selection."""
    if report.get("schema_version") != 1 or report.get("contract") != selection["contract"]:
        raise ValueError("report contract provenance does not match the local selection")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--report", type=Path, help="Egolint proposal or validation JSON")
    args = parser.parse_args()
    try:
        selection = load_selection(args.selection)
        if args.report is not None:
            verify_report(selection, json.loads(args.report.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(json.dumps({"status": "unavailable", "reason": str(exc)}))
        return 2
    print(json.dumps({"status": "verified", "contract": selection["contract"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
