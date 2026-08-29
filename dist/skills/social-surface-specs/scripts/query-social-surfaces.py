#!/usr/bin/env python3
"""Query a pinned social-surface catalog without a network connection."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


def _default_catalog() -> Path:
    """Resolve canonical source locally or the packaged offline catalog."""
    canonical = Path(__file__).with_name("catalog.v1.json")
    if canonical.exists():
        return canonical
    return Path(__file__).resolve().parents[1] / "references" / "social-surface-catalog.v1.json"


DEFAULT_CATALOG = _default_catalog()


def _normalized_bytes(path: Path) -> bytes:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def _matches(record: dict[str, Any], args: argparse.Namespace) -> bool:
    exact_filters = {
        "platform": args.platform,
        "use": args.use,
        "media_format": args.media_format,
        "content_type": args.content_type,
    }
    for field, value in exact_filters.items():
        if value is not None and str(record.get(field, "")).casefold() != value.casefold():
            return False
    if args.placement is not None and args.placement.casefold() not in str(record.get("placement", "")).casefold():
        return False
    return True


def query(catalog_path: Path, args: argparse.Namespace) -> dict[str, Any]:
    content = _normalized_bytes(catalog_path)
    catalog = json.loads(content.decode("utf-8"))
    metadata = catalog["catalog"]
    matches = [record for record in catalog["records"] if _matches(record, args)]
    matches.sort(key=lambda record: record["id"])
    return {
        "schema_version": "aether.social-surface-query-result/v1",
        "catalog": {
            "id": metadata["id"],
            "version": metadata["version"],
            "digest": {"algorithm": "sha256-utf8-lf", "value": hashlib.sha256(content).hexdigest()},
            "lifecycle": metadata["lifecycle"]["state"],
            "rights_review": metadata["rights_review"]["state"],
        },
        "freshness_warning": "This is a dated, offline catalog snapshot. Verify consequential or changed requirements against the linked live official source before production use.",
        "matches": matches,
    }


def render_markdown(result: dict[str, Any]) -> str:
    catalog = result["catalog"]
    lines = [
        f"# {catalog['id']} @ {catalog['version']}",
        "",
        f"Catalog digest: `{catalog['digest']['value']}`",
        "",
        f"> {result['freshness_warning']}",
        "",
    ]
    if not result["matches"]:
        lines.append("No matching surfaces in this pinned catalog.")
    for record in result["matches"]:
        dimensions = record["dimensions"]
        dimensions_text = "unknown" if dimensions is None else f"{dimensions['width_px']}×{dimensions['height_px']} px"
        lines.extend([
            f"## {record['platform']} — {record['placement']}",
            "",
            f"- Use: {record['use']}",
            f"- Format: {record['media_format'] or 'unknown'}",
            f"- Dimensions: {dimensions_text}",
            f"- Aspect ratio: {record['aspect_ratio'] or 'unknown'}",
            f"- Safe zone: {record['safe_zone']['state']}",
            f"- Verification: {record['verification']['state']}",
            f"- Source: [{record['source']['label']}]({record['source']['url']})",
            "",
        ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG, help="Pinned catalog JSON path.")
    parser.add_argument("--platform")
    parser.add_argument("--use", choices=["organic", "advertising"])
    parser.add_argument("--placement")
    parser.add_argument("--media-format")
    parser.add_argument("--content-type")
    parser.add_argument("--output-format", choices=["json", "markdown"], default="json")
    args = parser.parse_args()
    try:
        result = query(args.catalog, args)
    except (OSError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: unable to query catalog: {exc}", file=sys.stderr)
        return 2
    if args.output_format == "markdown":
        print(render_markdown(result))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
