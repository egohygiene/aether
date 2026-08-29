#!/usr/bin/env python3
"""Build the deterministic social-surface catalog distribution."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / "catalog" / "social-surfaces" / "catalog.v1.json"
GENERATOR = "catalog/social-surfaces/build-distribution.py"


def normalized_bytes(path: Path) -> bytes:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def build_files() -> dict[str, bytes]:
    catalog_bytes = normalized_bytes(CATALOG_PATH)
    catalog = json.loads(catalog_bytes.decode("utf-8"))
    metadata = catalog["catalog"]
    catalog_name = metadata["id"].split("/", 1)[1]
    prefix = f"dist/catalogs/{catalog_name}"
    release = metadata["release"]
    paths = [f"{prefix}/catalog.v1.json", f"{prefix}/distribution-manifest.v1.json"]
    manifest = {
        "schema_version": "aether.catalog-distribution-manifest/v1",
        "catalog_id": metadata["id"],
        "catalog_version": metadata["version"],
        "catalog_digest": {"algorithm": "sha256-utf8-lf", "value": hashlib.sha256(catalog_bytes).hexdigest()},
        "generated_paths": paths,
        "generator": GENERATOR,
        "publication": {"state": "eligible" if release["included"] else "blocked", "reason": release["reason"]}
    }
    return {
        f"catalogs/{catalog_name}/catalog.v1.json": catalog_bytes,
        f"catalogs/{catalog_name}/distribution-manifest.v1.json": (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8")
    }


def build(check: bool = False, output_directory: Path | None = None) -> int:
    output_root = output_directory or REPO_ROOT / "dist"
    files = build_files()
    drift = 0
    written = 0
    for relative, content in files.items():
        path = output_root / relative
        if check:
            if not path.exists():
                print(f"DRIFT  missing: {path}")
                drift += 1
            elif path.read_bytes() != content:
                print(f"DRIFT  stale:   {path}")
                drift += 1
            else:
                print(f"OK     {path}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            print(f"wrote  {path}")
            written += 1
    if check:
        if drift:
            print(f"{drift} social-surface distribution file(s) are out of date.", file=sys.stderr)
            return 1
        print("Social-surface catalog distribution is up to date.")
        return 0
    print(f"{written} social-surface distribution file(s) written.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Check generated output without writing it.")
    parser.add_argument("--output-directory", default="dist", help="Base output directory.")
    args = parser.parse_args()
    return build(check=args.check, output_directory=REPO_ROOT / args.output_directory)


if __name__ == "__main__":
    raise SystemExit(main())
