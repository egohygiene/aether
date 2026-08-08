#!/usr/bin/env python3
"""
Deterministic specification graph validation script.

Verifies that all canonical specifications in library/organization/specs/:
  - parse as YAML frontmatter
  - use the accepted schema (aether.specification/v1)
  - contain all required fields
  - have unique IDs
  - have resolvable dependency targets (depends_on, supersedes)
  - satisfy the dependency acyclicity rule
  - no canonical skill references a nonexistent specification ID

Note on relationship semantics:
  - depends_on / supersedes: must resolve to a known spec ID (normative)
  - related: may reference spec IDs or skill IDs (non-normative; validated against combined catalog)
  - applies_to: descriptive artifact categories -- not validated against the ID catalog

Replace this script with `aether validate --format text` once issue 007
delivers the canonical validator.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[3]
SPECS_DIR = REPO_ROOT / "library" / "organization" / "specs"
SKILLS_DIR = REPO_ROOT / "library" / "organization" / "skills"

ACCEPTED_SCHEMA = "aether.specification/v1"
REQUIRED_FIELDS = [
    "schema", "id", "title", "kind", "version", "status",
    "owners", "created", "updated", "domain", "tags",
]
# These fields must resolve to known spec IDs.
SPEC_ID_FIELDS = ("depends_on", "supersedes")
# These fields may resolve to spec IDs or skill IDs (non-normative cross-refs).
CATALOG_FIELDS = ("related",)


def parse_frontmatter(path):
    """Return the YAML frontmatter dict or None on parse failure."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return None


def collect_ids(directory, filename):
    """Return mapping of id -> file path for all matching files under directory."""
    id_map = {}
    for path in sorted(directory.rglob(filename)):
        fm = parse_frontmatter(path)
        if fm and "id" in fm:
            id_map[fm["id"]] = path
    return id_map


def is_path_reference(ref):
    """Return True if ref looks like a file path rather than a stable spec ID."""
    return (
        ref.startswith("library/")
        or ref.startswith("./")
        or ref.startswith("../")
        or ref.startswith("/")
        or os.sep in ref
        or "." in Path(ref).suffix and Path(ref).suffix != ""
    )


def find_cycles(graph):
    """Return a list of cycles found via DFS (each cycle as a node list)."""
    visited = set()
    stack = set()
    cycles = []

    def dfs(node, path):
        if node in stack:
            idx = path.index(node)
            cycles.append(path[idx:] + [node])
            return
        if node in visited:
            return
        visited.add(node)
        stack.add(node)
        for neighbour in graph.get(node, []):
            dfs(neighbour, path + [node])
        stack.discard(node)

    for node in list(graph):
        dfs(node, [])
    return cycles


def main():
    errors = []

    # Collect all specs and skills
    spec_files = sorted(SPECS_DIR.rglob("*.spec.md"))
    if not spec_files:
        print("ERROR: No specification files found.", file=sys.stderr)
        return 1

    skill_ids = collect_ids(SKILLS_DIR, "SKILL.md")

    frontmatters = {}
    for path in spec_files:
        fm = parse_frontmatter(path)
        if fm is None:
            errors.append("YAML parse error: {}".format(path.relative_to(REPO_ROOT)))
        else:
            frontmatters[path] = fm

    # Validate schema and required fields; collect IDs
    id_to_path = {}
    for path, fm in frontmatters.items():
        rel = path.relative_to(REPO_ROOT)
        schema = fm.get("schema", "")
        if schema != ACCEPTED_SCHEMA:
            errors.append(
                "Wrong schema in {}: got '{}', expected '{}'".format(rel, schema, ACCEPTED_SCHEMA)
            )
        for field in REQUIRED_FIELDS:
            if field not in fm:
                errors.append("Missing required field '{}' in {}".format(field, rel))
        spec_id = fm.get("id")
        if spec_id:
            if spec_id in id_to_path:
                errors.append(
                    "Duplicate ID '{}' in {} and {}".format(
                        spec_id, rel, id_to_path[spec_id].relative_to(REPO_ROOT)
                    )
                )
            else:
                id_to_path[spec_id] = path

    catalog_ids = {}
    catalog_ids.update(id_to_path)
    catalog_ids.update(skill_ids)

    # Validate relationship targets
    dep_graph = {sid: [] for sid in id_to_path}
    for path, fm in frontmatters.items():
        rel = path.relative_to(REPO_ROOT)
        spec_id = fm.get("id", "")
        for field in SPEC_ID_FIELDS:
            targets = fm.get(field) or []
            if isinstance(targets, str):
                targets = [targets]
            for target in targets:
                dep_graph.setdefault(spec_id, []).append(target)
                if target not in id_to_path:
                    errors.append(
                        "Unresolved {} target '{}' in {}".format(field, target, rel)
                    )
        for field in CATALOG_FIELDS:
            targets = fm.get(field) or []
            if isinstance(targets, str):
                targets = [targets]
            for target in targets:
                if target not in catalog_ids:
                    errors.append(
                        "Unresolved {} target '{}' in {}".format(field, target, rel)
                    )

    # Check dependency graph acyclicity
    cycles = find_cycles(dep_graph)
    for cycle in cycles:
        errors.append("Dependency cycle detected: {}".format(" -> ".join(cycle)))

    # Validate skill spec references
    for skill_path in sorted(SKILLS_DIR.rglob("SKILL.md")):
        text = skill_path.read_text(encoding="utf-8")
        match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not match:
            continue
        try:
            skill_fm = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError:
            continue
        refs = skill_fm.get("specs") or []
        implements = skill_fm.get("implements") or []
        if isinstance(implements, str):
            implements = [implements]
        for ref in refs + implements:
            if not isinstance(ref, str):
                continue
            if is_path_reference(ref):
                errors.append(
                    "Skill {} uses path reference '{}' -- use stable spec ID instead".format(
                        skill_path.relative_to(REPO_ROOT), ref
                    )
                )
            elif ref not in id_to_path:
                errors.append(
                    "Skill {} references nonexistent spec ID '{}'".format(
                        skill_path.relative_to(REPO_ROOT), ref
                    )
                )

    # Report
    if errors:
        print("VALIDATION FAILED -- {} error(s):\n".format(len(errors)))
        for err in errors:
            print("  x  {}".format(err))
        return 1

    print("VALIDATION PASSED -- {} specification(s) checked, 0 errors.".format(len(frontmatters)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
