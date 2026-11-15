#!/usr/bin/env python3
"""Bounded optional note authoring checks and create-only scaffold; no promotion."""
from __future__ import annotations

import argparse
from datetime import date
import json
import os
from pathlib import Path
import re
import stat
from urllib.parse import urlsplit

import yaml

MAX_BYTES = 32768


class UniqueLoader(yaml.SafeLoader):
    """Reject ambiguous duplicate metadata rather than choose the last value."""


def _mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise ValueError("duplicate note metadata")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def _reference(value):
    if not isinstance(value, str) or not value or "\\" in value or any(ord(c) < 32 for c in value):
        return False
    parsed = urlsplit(value)
    if parsed.scheme:
        return (parsed.scheme == "https" and bool(parsed.hostname)
                and parsed.username is None and parsed.password is None)
    return bool(parsed.path) and not parsed.path.startswith("/") and all(
        part not in {"", ".", ".."} for part in parsed.path.split("/"))


def inspect_note(text, repository=None):
    """Return mechanical diagnostics only; never infer authority or usefulness."""
    if not isinstance(text, str) or len(text.encode()) > MAX_BYTES or not text.startswith("---\n"):
        raise ValueError("bounded Markdown front matter required")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("front matter unavailable")
    metadata = yaml.load(parts[1], Loader=UniqueLoader)
    if not isinstance(metadata, dict):
        raise ValueError("note metadata unavailable")
    required = {"id", "title", "status", "authority", "visibility", "sources", "related", "next_step"}
    if not required <= metadata.keys() or metadata.keys() - required - {"created", "updated", "extensions"}:
        raise ValueError("minimal note metadata missing")
    if (not isinstance(metadata["id"], str) or not re.fullmatch(r"exp-[a-z0-9]+(?:-[a-z0-9]+)*", metadata["id"])
            or not isinstance(metadata["title"], str) or not 0 < len(metadata["title"]) <= 140
            or metadata["status"] not in {"draft", "superseded"}
            or metadata["authority"] != "exploratory-only"
            or metadata["visibility"] not in {"public", "private"}):
        raise ValueError("invalid identity, tentative status, visibility or authority")
    for key in ("created", "updated"):
        if metadata.get(key) is not None:
            if not isinstance(metadata[key], (str, date)):
                raise ValueError("unknown dates must be null")
            date.fromisoformat(str(metadata[key]))
    if metadata["next_step"] is not None and (not isinstance(metadata["next_step"], str)
                                               or not 0 < len(metadata["next_step"]) <= 400):
        raise ValueError("next step must be an optional bounded proposal")
    if not isinstance(metadata["related"], list) or not all(_reference(ref) for ref in metadata["related"]):
        raise ValueError("invalid relationship reference")
    if metadata["status"] == "superseded" and not metadata["related"]:
        raise ValueError("superseded note requires a replacement relationship")
    sources = metadata["sources"]
    if not isinstance(sources, list) or len(sources) > 16:
        raise ValueError("bounded source references required")
    missing = not sources
    for source in sources:
        if (not isinstance(source, dict) or set(source) != {"reference", "visibility"}
                or not _reference(source["reference"]) or source["visibility"] not in {"public", "private"}):
            raise ValueError("invalid classified source reference")
        if metadata["visibility"] == "public" and source["visibility"] != "public":
            raise ValueError("private source cannot enter public note")
        parsed = urlsplit(source["reference"])
        if repository is not None and not parsed.scheme:
            path = Path(repository) / parsed.path
            if not path.is_file() or path.is_symlink() or Path(repository).resolve() not in path.resolve().parents:
                missing = True
    if not parts[2].strip():
        raise ValueError("authored exploratory body required")
    return {"status": "partial" if missing else "valid", "id": metadata["id"],
            "parked": metadata["next_step"] is None, "authority": "exploratory-only",
            "source_gap": missing, "external_references": "not-fetched",
            "meaning_review": "not-authenticated", "metadata": metadata}


def read_note(path):
    if not all(hasattr(os, option) for option in ("O_NOFOLLOW", "O_NONBLOCK")):
        raise ValueError("safe regular-file admission unavailable")
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(descriptor, "rb") as stream:
        metadata = os.fstat(stream.fileno())
        if not stat.S_ISREG(metadata.st_mode) or not 0 < metadata.st_size <= MAX_BYTES:
            raise ValueError("bounded regular input required")
        content = stream.read(MAX_BYTES + 1)
    if len(content) > MAX_BYTES:
        raise ValueError("bounded regular input required")
    return content.decode("utf-8")


def create_note(path, text):
    """Only a caller-selected new file; identical repetition is a no-op."""
    inspect_note(text)
    path = Path(path).absolute()
    if path.suffix != ".md" or not path.parent.is_dir() or any(parent.is_symlink() for parent in path.parents):
        raise ValueError("select an ordinary Markdown path in an existing approved directory")
    try:
        with path.open("x", encoding="utf-8", newline="") as stream:
            stream.write(text)
    except FileExistsError:
        if read_note(path) == text:
            return "unchanged"
        raise ValueError("existing authored content differs; scaffold refuses overwrite") from None
    return "created"


def inspect_collection(paths, repository=None):
    seen = set()
    results = []
    for path in paths:
        result = inspect_note(read_note(path), repository)
        if result["id"] in seen:
            raise ValueError("duplicate stable note identity; preserve and reconcile authored contributions")
        seen.add(result["id"])
        results.append(result)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", type=Path, nargs="+")
    group.add_argument("--create", type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--repository", type=Path)
    args = parser.parse_args()
    if bool(args.create) != bool(args.template):
        parser.error("--template is required only with --create")
    try:
        if args.create:
            print(json.dumps({"result": create_note(args.create, read_note(args.template)),
                              "authority": "exploratory-only", "promotion": "not-performed"}))
        else:
            results = inspect_collection(args.check, args.repository)
            print(json.dumps({"checked": len(results), "partial": sum(r["status"] == "partial" for r in results),
                              "scope": "structure/local references only; source content withheld",
                              "external_references": "not-fetched", "meaning_review": "not-authenticated"}))
    except (OSError, ValueError, TypeError, KeyError, RecursionError, yaml.YAMLError):
        print("note unavailable, invalid or conflicting; source content withheld")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
