#!/usr/bin/env python3
"""Check selected local Identity source bytes without execution or acquisition."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys


MAX_BYTES = 1_048_576
SCOPE = (
    "Declared source-file hashes only; this does not verify Git HEAD, a binary, "
    "installation, approval, release, or complete project identity."
)


def read_lock(path: Path) -> dict:
    if path.is_symlink() or not path.is_file():
        raise ValueError("Lock must be a regular non-symlink file.")
    with path.open("rb") as stream:
        payload = stream.read(MAX_BYTES + 1)
    if len(payload) > MAX_BYTES:
        raise ValueError("Lock exceeds its byte budget.")
    try:
        lock = json.loads(payload)
    except (UnicodeError, ValueError) as error:
        raise ValueError("Lock must contain valid UTF-8 JSON.") from error
    if not isinstance(lock, dict):
        raise ValueError("Lock must be an object.")
    if lock.get("schema") != "aether.identity-source-lock/v1":
        raise ValueError("Unsupported lock schema.")
    if lock.get("repository") != "egohygiene/identity":
        raise ValueError("Lock must identify egohygiene/identity.")
    if not isinstance(lock.get("revision"), str) or not re.fullmatch(
        r"[0-9a-f]{40}", lock["revision"]
    ):
        raise ValueError("Lock requires a full lowercase Git revision.")
    resources = lock.get("resources")
    if not isinstance(resources, list) or not 1 <= len(resources) <= 64:
        raise ValueError("Lock requires between one and 64 resources.")
    seen = set()
    for resource in resources:
        if not isinstance(resource, dict):
            raise ValueError("Each locked resource must be an object.")
        name = resource.get("path")
        if not isinstance(name, str) or not name or "\\" in name or ":" in name:
            raise ValueError("Resource paths must be portable relative POSIX paths.")
        relative = PurePosixPath(name)
        if not relative.parts or relative.is_absolute() or str(relative) != name or any(
            part in {".", ".."} for part in relative.parts
        ):
            raise ValueError("Resource path escapes or is not normalized.")
        if name in seen:
            raise ValueError("Resource paths must be unique.")
        seen.add(name)
        digest = resource.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
            raise ValueError("Each resource requires a lowercase SHA256.")
        size = resource.get("size_bytes")
        if type(size) is not int or not 1 <= size <= MAX_BYTES:
            raise ValueError("Each resource requires a bounded positive byte count.")
    return lock


def check_source(source_root: Path, lock: dict) -> list[dict]:
    if source_root.is_symlink() or not source_root.is_dir():
        raise ValueError("Source root must be a non-symlink directory.")
    root = source_root.resolve(strict=True)
    findings = []
    for resource in lock["resources"]:
        name = resource["path"]
        candidate = root
        try:
            for part in PurePosixPath(name).parts:
                candidate = candidate / part
                if candidate.is_symlink():
                    raise ValueError("symlink")
            if not stat.S_ISREG(candidate.stat().st_mode):
                raise ValueError("not-regular")
            with candidate.open("rb") as stream:
                payload = stream.read(resource["size_bytes"] + 1)
            if len(payload) != resource["size_bytes"]:
                findings.append({"path": name, "reason": "size-mismatch"})
            elif hashlib.sha256(payload).hexdigest() != resource["sha256"]:
                findings.append({"path": name, "reason": "sha256-mismatch"})
        except ValueError as error:
            findings.append({"path": name, "reason": str(error)})
        except FileNotFoundError:
            findings.append({"path": name, "reason": "missing"})
        except OSError:
            findings.append({"path": name, "reason": "unreadable"})
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument(
        "--lock", type=Path,
        default=Path(__file__).resolve().parents[1] / "references/identity-source-lock.json",
    )
    args = parser.parse_args(argv)
    try:
        lock = read_lock(args.lock)
        findings = check_source(args.source_root, lock)
    except (OSError, ValueError) as error:
        message = str(error) if isinstance(error, ValueError) else "Input could not be read."
        print(json.dumps({"status": "invalid-input", "scope": SCOPE,
                          "findings": [{"reason": message}]}, sort_keys=True))
        return 2
    report = {
        "status": "mismatch" if findings else "verified",
        "scope": SCOPE,
        "source_repository": lock["repository"],
        "selected_revision": lock["revision"],
        "checked_files": len(lock["resources"]),
        "findings": findings,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
