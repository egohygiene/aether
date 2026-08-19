#!/usr/bin/env python3
"""Validate materialized Aether architecture documents in a repository."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

try:
    import jsonschema
except ModuleNotFoundError:  # pragma: no cover - exercised in minimal consumers
    jsonschema = None


CANONICAL_FILES = {
    "AI_CONSTITUTION.md",
    "ARCHITECTURE.md",
    "DECISIONS.md",
    "DESIGN.md",
    "DESIGN_SYSTEM.md",
    "EPISTEMOLOGY.md",
    "FOUNDATIONS.md",
    "MANIFESTO.md",
    "META.md",
    "METHODOLOGY.md",
    "ONTOLOGY.md",
    "PERSONAL_MODEL.md",
    "PILLARS.md",
    "PRINCIPLES.md",
    "PURPOSE.md",
    "ROADMAP.md",
    "SYSTEM.md",
    "VISION.md",
}

FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(?P<yaml>.*?)\n---\s*\n", re.DOTALL)
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\((?P<target>[^)]+)\)")


@dataclass(frozen=True)
class Document:
    path: Path
    metadata: dict[str, Any]
    body: str


def parse_document(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_PATTERN.match(text)
    if match is None:
        raise ValueError("missing YAML frontmatter")
    metadata = yaml.safe_load(match.group("yaml"))
    if not isinstance(metadata, dict):
        raise ValueError("frontmatter must be a mapping")
    for field in ("created", "updated"):
        value = metadata.get(field)
        if hasattr(value, "isoformat"):
            metadata[field] = value.isoformat()
    return Document(path=path, metadata=metadata, body=text[match.end() :])


def discover(repository: Path) -> tuple[list[Document], list[str]]:
    documents: list[Document] = []
    errors: list[str] = []
    for filename in sorted(CANONICAL_FILES):
        path = repository / filename
        if not path.exists():
            continue
        try:
            documents.append(parse_document(path))
        except (OSError, UnicodeError, ValueError, yaml.YAMLError) as error:
            errors.append(f"{filename}: {error}")
    return documents, errors


def validate_schema(documents: list[Document], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if jsonschema is None:
        required = schema.get("required", [])
        for document in documents:
            missing = [field for field in required if field not in document.metadata]
            for field in missing:
                errors.append(f"{document.path.name}: frontmatter: missing required field {field}")
            if document.metadata.get("schema") != "aether.architecture-document/v1":
                errors.append(f"{document.path.name}: schema: invalid architecture schema")
            if document.metadata.get("kind") != "architecture-document":
                errors.append(f"{document.path.name}: kind: expected architecture-document")
            for field in ("owners", "governed_by", "depends_on", "related", "supersedes"):
                if field in document.metadata and not isinstance(document.metadata[field], list):
                    errors.append(f"{document.path.name}: {field}: expected an array")
        return errors
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )
    for document in documents:
        for error in sorted(validator.iter_errors(document.metadata), key=lambda item: list(item.path)):
            location = ".".join(str(part) for part in error.path) or "frontmatter"
            errors.append(f"{document.path.name}: {location}: {error.message}")
    return errors


def validate_markdown(repository: Path, documents: list[Document]) -> list[str]:
    errors: list[str] = []
    for document in documents:
        headings = [line for line in document.body.splitlines() if line.startswith("# ")]
        if len(headings) != 1:
            errors.append(f"{document.path.name}: expected exactly one H1, found {len(headings)}")
        for match in MARKDOWN_LINK_PATTERN.finditer(document.body):
            target = match.group("target").split("#", 1)[0].strip()
            if not target or "://" in target or target.startswith(("mailto:", "#")):
                continue
            resolved = (document.path.parent / target).resolve()
            try:
                resolved.relative_to(repository.resolve())
            except ValueError:
                errors.append(f"{document.path.name}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{document.path.name}: unresolved relative link: {target}")
    return errors


def validate_graph(documents: list[Document]) -> list[str]:
    errors: list[str] = []
    by_id: dict[str, Document] = {}
    for document in documents:
        artifact_id = document.metadata.get("id")
        if not isinstance(artifact_id, str):
            continue
        if artifact_id in by_id:
            errors.append(
                f"duplicate id {artifact_id}: {by_id[artifact_id].path.name}, {document.path.name}"
            )
        by_id[artifact_id] = document

    edges: dict[str, list[str]] = {}
    for artifact_id, document in by_id.items():
        dependencies = document.metadata.get("depends_on", [])
        if not isinstance(dependencies, list):
            continue
        edges[artifact_id] = []
        for dependency in dependencies:
            if dependency not in by_id:
                errors.append(f"{document.path.name}: unresolved dependency id: {dependency}")
            else:
                edges[artifact_id].append(dependency)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, trail: list[str]) -> None:
        if node in visited:
            return
        if node in visiting:
            cycle_start = trail.index(node)
            errors.append("dependency cycle: " + " -> ".join(trail[cycle_start:] + [node]))
            return
        visiting.add(node)
        for dependency in edges.get(node, []):
            visit(dependency, trail + [node])
        visiting.remove(node)
        visited.add(node)

    for node in edges:
        visit(node, [])
    return errors


def validate_meta(documents: list[Document]) -> list[str]:
    errors: list[str] = []
    meta = next((document for document in documents if document.path.name == "META.md"), None)
    if meta is None:
        errors.append("META.md: missing architecture inventory")
        return errors
    for document in documents:
        if document.path.name not in meta.body:
            errors.append(f"META.md: does not inventory {document.path.name}")
        artifact_id = document.metadata.get("id")
        if isinstance(artifact_id, str) and artifact_id not in meta.body:
            errors.append(f"META.md: does not inventory artifact id {artifact_id}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, required=True)
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).with_name("architecture-document.schema.json"),
    )
    parser.add_argument("--require-complete-reference", action="store_true")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repository = args.repository.resolve()
    schema = json.loads(args.schema.read_text(encoding="utf-8"))
    documents, errors = discover(repository)
    errors.extend(validate_schema(documents, schema))
    errors.extend(validate_markdown(repository, documents))
    errors.extend(validate_graph(documents))
    errors.extend(validate_meta(documents))

    discovered_files = {document.path.name for document in documents}
    if args.require_complete_reference:
        for missing in sorted(CANONICAL_FILES - discovered_files):
            errors.append(f"{missing}: missing from complete-reference set")

    result = {
        "repository": str(repository),
        "documents": len(documents),
        "errors": sorted(set(errors)),
        "valid": not errors,
    }
    if args.format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"architecture documents: {result['documents']}")
        if result["errors"]:
            for error in result["errors"]:
                print(f"ERROR: {error}")
        else:
            print("architecture validation passed")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
