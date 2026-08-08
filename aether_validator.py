#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import unittest
from datetime import date, datetime
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

EXIT_OK = 0
EXIT_VALIDATION_FAILED = 1
EXIT_INVALID_INVOCATION = 2
EXIT_INTERNAL_ERROR = 3

SKILL_ALLOWED_TOP = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}
SKILL_REQUIRED_TOP = {"name", "description"}
SKILL_NAME_RE = re.compile(r"^[a-z](?:[a-z0-9-]*[a-z0-9])?$")
SPEC_SCHEMA = "aether.specification/v1"
SPEC_REQUIRED_TOP = {
    "schema", "id", "title", "kind", "version", "status", "owners", "created", "updated", "domain", "tags",
}
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
SPEC_STATUS = {"draft", "stable", "deprecated", "retired", "approved"}
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


@dataclass
class Diagnostic:
    rule_id: str
    severity: str
    message: str
    guidance: str
    artifact_id: str | None = None
    file: str | None = None
    line: int | None = None
    context: dict[str, Any] = field(default_factory=dict)


class ValidationError(Exception):
    pass


def _rel(path: Path, root: Path) -> str:
    return str(path.relative_to(root)).replace("\\", "/")


def _canonical_json_bytes(data: Any) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _normalized_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _sha256_utf8_lf(path: Path) -> str:
    return hashlib.sha256(_normalized_text(path).encode("utf-8")).hexdigest()


def _parse_frontmatter(path: Path) -> tuple[dict[str, Any] | None, Diagnostic | None]:
    text = _normalized_text(path)
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, Diagnostic(
            rule_id="AETHER_FRONTMATTER_001",
            severity="error",
            message="Missing YAML frontmatter block.",
            guidance="Add a YAML frontmatter block delimited by --- at the top of the file.",
            file=str(path),
            line=1,
        )
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, Diagnostic(
            rule_id="AETHER_FRONTMATTER_002",
            severity="error",
            message=f"Malformed YAML frontmatter: {exc}",
            guidance="Fix YAML syntax in frontmatter.",
            file=str(path),
            line=1,
        )
    if not isinstance(data, dict):
        return None, Diagnostic(
            rule_id="AETHER_FRONTMATTER_003",
            severity="error",
            message="Frontmatter must be a mapping.",
            guidance="Use YAML key/value mappings in frontmatter.",
            file=str(path),
            line=1,
        )
    return data, None


class AetherValidator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.skills_root = repo_root / "library" / "organization" / "skills"
        self.specs_root = repo_root / "library" / "organization" / "specs"
        self.catalog_path = repo_root / "catalog" / "first-party" / "catalog.v1.json"
        self.catalog_schema_path = repo_root / "catalog" / "schemas" / "aether.artifact-catalog.v1.schema.json"

    def _skill_dirs(self) -> list[Path]:
        return sorted({p.parent for p in self.skills_root.rglob("SKILL.md")})

    def _spec_files(self) -> list[Path]:
        return sorted(self.specs_root.rglob("*.spec.md"))

    def _skill_identity_maps(self) -> tuple[dict[str, str], dict[str, str], dict[str, Path]]:
        bare_to_prefixed: dict[str, str] = {}
        prefixed_to_bare: dict[str, str] = {}
        path_by_prefixed: dict[str, Path] = {}
        for skill_dir in self._skill_dirs():
            skill_path = skill_dir / "SKILL.md"
            fm, _ = _parse_frontmatter(skill_path)
            if not fm:
                continue
            name = str(fm.get("name", skill_dir.name))
            prefixed = f"skill/{name}"
            bare_to_prefixed[name] = prefixed
            prefixed_to_bare[prefixed] = name
            path_by_prefixed[prefixed] = skill_path
        return bare_to_prefixed, prefixed_to_bare, path_by_prefixed

    def validate_skills(self) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        for skill_dir in self._skill_dirs():
            skill_path = skill_dir / "SKILL.md"
            rel = _rel(skill_path, self.repo_root)
            artifact_id = f"skill/{skill_dir.name}"
            fm, err = _parse_frontmatter(skill_path)
            if err:
                err.file = rel
                err.artifact_id = artifact_id
                diagnostics.append(err)
                continue
            assert fm is not None

            for key in SKILL_REQUIRED_TOP:
                if key not in fm:
                    diagnostics.append(Diagnostic(
                        rule_id="AETHER_SKILL_001",
                        severity="error",
                        message=f"Missing required skill field '{key}'.",
                        guidance="Add required 'name' and 'description' fields to SKILL.md frontmatter.",
                        artifact_id=artifact_id,
                        file=rel,
                        line=1,
                        context={"field": key},
                    ))

            name = str(fm.get("name", ""))
            if name:
                if name != skill_dir.name:
                    diagnostics.append(Diagnostic(
                        rule_id="AETHER_SKILL_002",
                        severity="error",
                        message=f"Skill name '{name}' does not match directory '{skill_dir.name}'.",
                        guidance="Rename the skill directory or the 'name' field so they match exactly.",
                        artifact_id=artifact_id,
                        file=rel,
                        line=1,
                    ))
                if len(name) > 64 or not SKILL_NAME_RE.match(name):
                    diagnostics.append(Diagnostic(
                        rule_id="AETHER_SKILL_003",
                        severity="error",
                        message="Skill name must be lowercase kebab-case and <= 64 characters.",
                        guidance="Use a lowercase kebab-case identifier up to 64 characters.",
                        artifact_id=artifact_id,
                        file=rel,
                        line=1,
                    ))

            desc = fm.get("description")
            if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SKILL_004",
                    severity="error",
                    message="Skill description must be a non-empty string <= 1024 characters.",
                    guidance="Provide a concise non-empty description no longer than 1024 characters.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                ))
            elif "use when" not in desc.lower():
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SKILL_005",
                    severity="error",
                    message="Skill description must state when the skill should be loaded.",
                    guidance="Include wording such as 'Use when ...' in the description.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                ))

            unsupported = [k for k in fm if k not in SKILL_ALLOWED_TOP]
            for key in unsupported:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SKILL_006",
                    severity="error",
                    message=f"Unsupported top-level skill key '{key}'.",
                    guidance="Move Aether metadata under the 'metadata' mapping.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                    context={"field": key},
                ))

            metadata = fm.get("metadata")
            if metadata is not None and not isinstance(metadata, dict):
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SKILL_007",
                    severity="error",
                    message="Skill metadata must be a mapping.",
                    guidance="Use YAML mapping syntax for metadata.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                ))
            if "allowed-tools" in fm and not isinstance(fm["allowed-tools"], list):
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SKILL_008",
                    severity="error",
                    message="allowed-tools must be a list of strings.",
                    guidance="Declare allowed-tools as a YAML list of tool names.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                ))

            for required_path in [
                skill_dir / "evals" / "evals.json",
                skill_dir / "references",
                skill_dir / "templates",
            ]:
                if not required_path.exists():
                    diagnostics.append(Diagnostic(
                        rule_id="AETHER_SKILL_009",
                        severity="error",
                        message=f"Missing required skill package content: {_rel(required_path, self.repo_root)}",
                        guidance="Ensure each canonical skill has references/, templates/, and evals/evals.json.",
                        artifact_id=artifact_id,
                        file=rel,
                        line=1,
                    ))

            size = sum(p.stat().st_size for p in skill_dir.rglob("*") if p.is_file())
            if size > 2 * 1024 * 1024:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SKILL_010",
                    severity="warning",
                    message=f"Skill package size is {size} bytes; keep packages lightweight.",
                    guidance="Reduce bulky assets or move large assets out of canonical skill packages.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                ))

            executable_files = [
                p for p in skill_dir.rglob("*")
                if p.is_file() and (os.access(p, os.X_OK) or p.suffix in {".sh", ".py", ".mjs", ".js"})
            ]
            declared_exec = []
            if isinstance(metadata, dict):
                maybe = metadata.get("aether-executable-resources", [])
                if isinstance(maybe, list):
                    declared_exec = [str(x) for x in maybe if isinstance(x, str)]
            if executable_files and not declared_exec:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SKILL_011",
                    severity="error",
                    message="Skill has executable resources but none are declared in metadata.aether-executable-resources.",
                    guidance="Declare executable resources in metadata.aether-executable-resources.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                    context={"executables": [_rel(p, self.repo_root) for p in executable_files[:10]]},
                ))

        return diagnostics

    def _collect_specs(self) -> tuple[list[Diagnostic], dict[str, dict[str, Any]], dict[str, Path]]:
        diagnostics: list[Diagnostic] = []
        by_id: dict[str, dict[str, Any]] = {}
        path_by_id: dict[str, Path] = {}
        for spec_path in self._spec_files():
            rel = _rel(spec_path, self.repo_root)
            fm, err = _parse_frontmatter(spec_path)
            if err:
                err.file = rel
                diagnostics.append(err)
                continue
            assert fm is not None
            spec_id = str(fm.get("id", ""))
            artifact_id = f"specification/{spec_id}" if spec_id else None

            if fm.get("schema") != SPEC_SCHEMA:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SPEC_001",
                    severity="error",
                    message=f"Invalid spec schema '{fm.get('schema')}'.",
                    guidance=f"Set schema to '{SPEC_SCHEMA}'.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                ))

            for key in sorted(SPEC_REQUIRED_TOP):
                if key not in fm:
                    diagnostics.append(Diagnostic(
                        rule_id="AETHER_SPEC_002",
                        severity="error",
                        message=f"Missing required spec field '{key}'.",
                        guidance="Add all required aether.specification/v1 frontmatter fields.",
                        artifact_id=artifact_id,
                        file=rel,
                        line=1,
                        context={"field": key},
                    ))

            version = fm.get("version")
            if not isinstance(version, str) or not SEMVER_RE.match(version):
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SPEC_003",
                    severity="error",
                    message="Specification version must be semver (x.y.z).",
                    guidance="Use semantic version strings like 1.0.0.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                ))

            status = fm.get("status")
            if status not in SPEC_STATUS:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SPEC_004",
                    severity="error",
                    message=f"Invalid specification lifecycle status '{status}'.",
                    guidance=f"Use one of: {', '.join(sorted(SPEC_STATUS))}.",
                    artifact_id=artifact_id,
                    file=rel,
                    line=1,
                ))

            for date_field in ("created", "updated"):
                value = fm.get(date_field)
                if isinstance(value, (date, datetime)):
                    value = value.isoformat()[:10]
                if not isinstance(value, str) or not DATE_RE.match(value):
                    diagnostics.append(Diagnostic(
                        rule_id="AETHER_SPEC_005",
                        severity="error",
                        message=f"Field '{date_field}' must be YYYY-MM-DD.",
                        guidance="Use ISO date format YYYY-MM-DD.",
                        artifact_id=artifact_id,
                        file=rel,
                        line=1,
                        context={"field": date_field},
                    ))

            if spec_id:
                if spec_id in by_id:
                    diagnostics.append(Diagnostic(
                        rule_id="AETHER_SPEC_006",
                        severity="error",
                        message=f"Duplicate specification id '{spec_id}'.",
                        guidance="Assign unique stable IDs to each specification.",
                        artifact_id=f"specification/{spec_id}",
                        file=rel,
                        line=1,
                        context={"first_seen": _rel(path_by_id[spec_id], self.repo_root)},
                    ))
                else:
                    by_id[spec_id] = fm
                    path_by_id[spec_id] = spec_path

        return diagnostics, by_id, path_by_id

    def validate_specs(self) -> tuple[list[Diagnostic], dict[str, dict[str, Any]], dict[str, Path]]:
        diagnostics, by_id, path_by_id = self._collect_specs()
        return diagnostics, by_id, path_by_id

    def validate_graph(self, specs_by_id: dict[str, dict[str, Any]], spec_paths: dict[str, Path] | None = None) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        bare_skill, _prefixed_skill, _skill_paths = self._skill_identity_maps()
        spec_paths = spec_paths or {}

        graph: dict[str, list[str]] = {sid: [] for sid in specs_by_id}

        for spec_id, fm in specs_by_id.items():
            artifact_id = f"specification/{spec_id}"
            source_path = spec_paths.get(spec_id, self.specs_root)
            rel_file = _rel(source_path, self.repo_root)

            for rel_field in ("depends_on", "supersedes"):
                raw = fm.get(rel_field) or []
                refs = raw if isinstance(raw, list) else [raw]
                for ref in refs:
                    if not isinstance(ref, str):
                        continue
                    graph[spec_id].append(ref)
                    if ref not in specs_by_id:
                        diagnostics.append(Diagnostic(
                            rule_id="AETHER_GRAPH_001",
                            severity="error",
                            message=f"Unresolved {rel_field} target '{ref}'.",
                            guidance="Use existing specification IDs in relationship fields.",
                            artifact_id=artifact_id,
                            file=rel_file,
                            line=1,
                            context={"field": rel_field, "target": ref},
                        ))

            raw_related = fm.get("related") or []
            related_refs = raw_related if isinstance(raw_related, list) else [raw_related]
            for ref in related_refs:
                if not isinstance(ref, str):
                    continue
                if ref in specs_by_id:
                    continue
                if ref.startswith("specification/") and ref.removeprefix("specification/") in specs_by_id:
                    continue
                if ref in bare_skill:
                    continue
                if ref.startswith("skill/") and ref.removeprefix("skill/") in bare_skill:
                    continue
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_GRAPH_002",
                    severity="error",
                    message=f"Unresolved related target '{ref}'.",
                    guidance="Reference an existing spec ID or skill name/ID.",
                    artifact_id=artifact_id,
                    file=rel_file,
                    line=1,
                    context={"field": "related", "target": ref},
                ))

        visited: set[str] = set()
        stack: list[str] = []

        def dfs(node: str):
            visited.add(node)
            stack.append(node)
            for nxt in graph.get(node, []):
                if nxt not in graph:
                    continue
                if nxt in stack:
                    cycle = stack[stack.index(nxt):] + [nxt]
                    diagnostics.append(Diagnostic(
                        rule_id="AETHER_GRAPH_003",
                        severity="error",
                        message=f"Dependency cycle detected: {' -> '.join(cycle)}",
                        guidance="Remove at least one depends_on edge to keep the spec graph acyclic.",
                        artifact_id=f"specification/{node}",
                        context={"cycle": cycle},
                    ))
                    continue
                if nxt not in visited:
                    dfs(nxt)
            stack.pop()

        for node in sorted(graph):
            if node not in visited:
                dfs(node)

        return diagnostics

    def generate_catalog(self) -> dict[str, Any]:
        specs_diags, specs_by_id, _ = self._collect_specs()
        if any(d.severity == "error" for d in specs_diags):
            raise ValidationError("Cannot generate catalog while specification frontmatter is invalid.")

        bare_skill, _prefixed, _skill_paths = self._skill_identity_maps()
        known_spec_ids = {f"specification/{x}" for x in specs_by_id}
        known_skill_ids = {f"skill/{x}" for x in bare_skill}

        existing_catalog: dict[str, Any] = {}
        existing_by_path: dict[str, dict[str, Any]] = {}
        if self.catalog_path.exists():
            existing_catalog = json.loads(self.catalog_path.read_text(encoding="utf-8"))
            for artifact in existing_catalog.get("artifacts", []):
                src = artifact.get("source_path")
                if isinstance(src, str):
                    existing_by_path[src] = json.loads(json.dumps(artifact))

        artifacts: list[dict[str, Any]] = []

        for spec_path in self._spec_files():
            fm, _ = _parse_frontmatter(spec_path)
            if fm is None:
                continue
            spec_id = str(fm["id"])
            source_path = _rel(spec_path, self.repo_root)
            source_digest = _sha256_utf8_lf(spec_path)
            if source_path in existing_by_path:
                record = existing_by_path[source_path]
                record["source_digest"] = {"algorithm": "sha256-utf8-lf", "value": source_digest}
                artifacts.append(record)
                continue

            related_ids = []
            for ref in fm.get("related") or []:
                if ref in specs_by_id:
                    related_ids.append(f"specification/{ref}")
                elif ref.startswith("specification/") and ref in known_spec_ids:
                    related_ids.append(ref)
                elif ref in bare_skill:
                    related_ids.append(f"skill/{ref}")
                elif ref.startswith("skill/") and ref in known_skill_ids:
                    related_ids.append(ref)

            dependencies = [
                f"specification/{x}" if not str(x).startswith("specification/") else str(x)
                for x in (fm.get("depends_on") or [])
            ]
            supersedes_ids = [
                f"specification/{x}" if not str(x).startswith("specification/") else str(x)
                for x in (fm.get("supersedes") or [])
            ]
            description = ""
            body = _normalized_text(spec_path)
            after_frontmatter = body.split("---\n", 2)[-1]
            for line in after_frontmatter.splitlines():
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    description = stripped
                    break

            artifacts.append({
                "artifact_version": str(fm.get("version", "1.0.0")),
                "compatibility": {"required_tools": []},
                "dependencies": dependencies,
                "deprecation": {"replacement_id": None},
                "description": description,
                "domain": str(fm.get("domain", "unknown")),
                "generated_distribution_paths": [f"dist/specs/{spec_id}.spec.md"],
                "id": f"specification/{spec_id}",
                "implements_specification_id": None,
                "kind": "specification",
                "license": "MIT",
                "lifecycle": {"state": str(fm.get("status", "draft"))},
                "owner": {
                    "maintainers": [str(x) for x in (fm.get("owners") or ["egohygiene"])],
                    "primary": str((fm.get("owners") or ["egohygiene"])[0]),
                },
                "related_ids": sorted(set(related_ids)),
                "release": {
                    "included": str(fm.get("status", "draft")) == "stable",
                    "reason": "Only stable artifacts are releasable under catalog policy." if str(fm.get("status", "draft")) != "stable" else "Stable artifact is eligible for release manifests.",
                },
                "scope": "organization",
                "source_digest": {"algorithm": "sha256-utf8-lf", "value": source_digest},
                "source_path": source_path,
                "supersedes_ids": supersedes_ids,
                "tags": [str(x) for x in (fm.get("tags") or [])],
                "title": str(fm.get("title", spec_id)),
            })

        for skill_dir in self._skill_dirs():
            skill_path = skill_dir / "SKILL.md"
            fm, _ = _parse_frontmatter(skill_path)
            if fm is None:
                continue
            name = str(fm.get("name", skill_dir.name))
            source_path = _rel(skill_path, self.repo_root)
            source_digest = _sha256_utf8_lf(skill_path)
            if source_path in existing_by_path:
                record = existing_by_path[source_path]
                record["source_digest"] = {"algorithm": "sha256-utf8-lf", "value": source_digest}
                artifacts.append(record)
                continue

            metadata = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
            spec_ref = str(metadata.get("aether-spec-id", "")).strip()
            implements = f"specification/{spec_ref}" if spec_ref else None
            dependencies = [implements] if implements else []

            artifacts.append({
                "artifact_version": str(metadata.get("aether-version", "1.0.0")),
                "compatibility": {"required_tools": [str(x) for x in (fm.get("allowed-tools") or []) if isinstance(x, str)]},
                "dependencies": dependencies,
                "deprecation": {"replacement_id": None},
                "description": str(fm.get("description", "")),
                "domain": str(metadata.get("aether-domain", "unknown")),
                "generated_distribution_paths": [f"dist/skills/{name}/SKILL.md"],
                "id": f"skill/{name}",
                "implements_specification_id": implements,
                "kind": "skill",
                "license": str(fm.get("license", "MIT")),
                "lifecycle": {"state": str(metadata.get("aether-status", "draft"))},
                "owner": {
                    "maintainers": [str(metadata.get("aether-owners", "egohygiene"))],
                    "primary": str(metadata.get("aether-owners", "egohygiene")),
                },
                "related_ids": [],
                "release": {
                    "included": str(metadata.get("aether-status", "draft")) == "stable",
                    "reason": "Only stable artifacts are releasable under catalog policy." if str(metadata.get("aether-status", "draft")) != "stable" else "Stable artifact is eligible for release manifests.",
                },
                "scope": str(metadata.get("aether-scope", "organization")),
                "source_digest": {"algorithm": "sha256-utf8-lf", "value": source_digest},
                "source_path": source_path,
                "supersedes_ids": [],
                "tags": [str(metadata.get("aether-domain", "skill")), "skill"],
                "title": " ".join(piece.capitalize() for piece in name.split("-")),
            })

        authority = existing_catalog.get("authority") if existing_catalog else None
        lifecycle_policy = existing_catalog.get("lifecycle_policy") if existing_catalog else None
        serialization = existing_catalog.get("serialization") if existing_catalog else None
        versioning = existing_catalog.get("versioning") if existing_catalog else None

        catalog = {
            "schema_version": "aether.artifact-catalog/v1",
            "artifacts": sorted(artifacts, key=lambda item: item["id"]),
            "authority": authority or {
                "source_of_truth": [
                    "library/organization/specs/**/*.spec.md",
                    "library/organization/skills/**/SKILL.md",
                ],
                "resolution_policy": "frontmatter-overrides-catalog",
            },
            "versioning": versioning or {
                "artifact_version_policy": "semver",
                "repository_release_policy": "stable-only",
            },
            "serialization": serialization or {
                "json_canonicalization": "json.dumps(sort_keys=True,separators=(\",\",\":\"))",
                "source_digest_algorithm": "sha256-utf8-lf",
            },
            "lifecycle_policy": lifecycle_policy or {
                "allowed_states": ["draft", "experimental", "stable", "deprecated", "retired"],
            },
        }
        return catalog

    def validate_catalog(self, check_only: bool = True) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        generated = self.generate_catalog()

        if self.catalog_schema_path.exists():
            schema = json.loads(self.catalog_schema_path.read_text(encoding="utf-8"))
            validator = Draft202012Validator(schema)
            for err in validator.iter_errors(generated):
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_CATALOG_001",
                    severity="error",
                    message=f"Generated catalog fails schema at {'/'.join(map(str, err.path)) or '<root>'}: {err.message}",
                    guidance="Fix generator mappings to satisfy catalog schema contracts.",
                    file=_rel(self.catalog_schema_path, self.repo_root),
                    context={"path": list(err.path)},
                ))

        if self.catalog_path.exists():
            current = json.loads(self.catalog_path.read_text(encoding="utf-8"))
            if current != generated:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_CATALOG_002",
                    severity="error",
                    message="Catalog drift detected between catalog.v1.json and generated output.",
                    guidance="Run `aether catalog generate` to rewrite catalog or fix source metadata.",
                    file=_rel(self.catalog_path, self.repo_root),
                    context={
                        "current_digest": hashlib.sha256(_canonical_json_bytes(current)).hexdigest(),
                        "generated_digest": hashlib.sha256(_canonical_json_bytes(generated)).hexdigest(),
                        "check_mode": check_only,
                    },
                ))
        elif check_only:
            diagnostics.append(Diagnostic(
                rule_id="AETHER_CATALOG_003",
                severity="error",
                message="Missing canonical catalog file.",
                guidance="Run `aether catalog generate` to create catalog/first-party/catalog.v1.json.",
                file=_rel(self.catalog_path, self.repo_root),
            ))

        return diagnostics

    def write_catalog(self) -> None:
        generated = self.generate_catalog()
        self.catalog_path.parent.mkdir(parents=True, exist_ok=True)
        self.catalog_path.write_text(json.dumps(generated, indent=2, sort_keys=False) + "\n", encoding="utf-8")

    def validate_json_files(self) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        for path in sorted(self.repo_root.rglob("*.json")):
            if ".git" in path.parts:
                continue
            if "dist" in path.parts:
                continue
            rel = _rel(path, self.repo_root)
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_JSON_001",
                    severity="error",
                    message=f"Malformed JSON: {exc.msg}",
                    guidance="Fix JSON syntax.",
                    file=rel,
                    line=exc.lineno,
                ))
        return diagnostics

    def validate_shell_syntax(self) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        shell_files = []
        for path in sorted(self.repo_root.rglob("*")):
            if not path.is_file() or ".git" in path.parts:
                continue
            if path.suffix == ".sh":
                shell_files.append(path)
                continue
            try:
                first = path.read_text(encoding="utf-8").splitlines()[0]
            except (UnicodeDecodeError, IndexError):
                continue
            if first.startswith("#!") and re.search(r"(^|/)(bash|sh)(\s|$)", first.strip()):
                shell_files.append(path)

        for path in shell_files:
            rel = _rel(path, self.repo_root)
            proc = subprocess.run(["bash", "-n", str(path)], capture_output=True, text=True)
            if proc.returncode != 0:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_SHELL_001",
                    severity="error",
                    message=(proc.stderr or proc.stdout or "shell syntax error").strip(),
                    guidance="Fix shell syntax errors reported by `bash -n`.",
                    file=rel,
                ))
        return diagnostics

    def validate_markdown_links(self) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        markdown_files = sorted((self.repo_root / "library" / "organization").rglob("*.md"))
        for path in markdown_files:
            rel = _rel(path, self.repo_root)
            text = path.read_text(encoding="utf-8")
            skill_root = None
            if "library/organization/skills/" in rel:
                parts = path.parts
                idx = parts.index("skills")
                if len(parts) >= idx + 3:
                    skill_root = Path(*parts[:idx + 3])
            for line_no, line in enumerate(text.splitlines(), start=1):
                for raw in MARKDOWN_LINK_RE.findall(line):
                    target = raw.split("#", 1)[0].strip()
                    if not target or target.startswith(("http://", "https://", "mailto:", "tel:")):
                        continue
                    if target.startswith("/"):
                        diagnostics.append(Diagnostic(
                            rule_id="AETHER_LINK_002",
                            severity="error",
                            message=f"Absolute markdown path '{target}' is not allowed.",
                            guidance="Use repository-relative links with ./ or ../ where possible.",
                            file=rel,
                            line=line_no,
                            context={"link": target},
                        ))
                        continue
                    resolved = (path.parent / target).resolve()
                    if skill_root is not None:
                        skill_root_resolved = skill_root.resolve()
                        if not str(resolved).startswith(str(skill_root_resolved)):
                            diagnostics.append(Diagnostic(
                                rule_id="AETHER_LINK_003",
                                severity="error",
                                message=f"Link escapes skill package boundary: '{target}'.",
                                guidance="Keep skill-local links within the skill package directory.",
                                file=rel,
                                line=line_no,
                                context={"link": target},
                            ))
                            continue
                    if not resolved.exists():
                        diagnostics.append(Diagnostic(
                            rule_id="AETHER_LINK_001",
                            severity="error",
                            message=f"Broken local markdown link target '{target}'.",
                            guidance="Fix the link path or add the referenced file.",
                            file=rel,
                            line=line_no,
                            context={"link": target},
                        ))
        return diagnostics

    def validate_provenance(self) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        lock_path = self.repo_root / ".staging" / "manifests" / "skills-lock.json"
        if not lock_path.exists():
            diagnostics.append(Diagnostic(
                rule_id="AETHER_PROVENANCE_001",
                severity="warning",
                message="No .staging/manifests/skills-lock.json provenance file found.",
                guidance="If staging provenance exists, keep skills-lock.json committed for migration traceability.",
            ))
            return diagnostics

        try:
            lock = json.loads(lock_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            diagnostics.append(Diagnostic(
                rule_id="AETHER_PROVENANCE_002",
                severity="error",
                message=f"Malformed provenance lock JSON: {exc.msg}",
                guidance="Fix JSON in .staging/manifests/skills-lock.json.",
                file=_rel(lock_path, self.repo_root),
                line=exc.lineno,
            ))
            return diagnostics

        skills = lock.get("skills", {})
        if not isinstance(skills, dict):
            diagnostics.append(Diagnostic(
                rule_id="AETHER_PROVENANCE_003",
                severity="error",
                message="skills-lock.json 'skills' must be an object map.",
                guidance="Use a mapping from skill key to provenance record.",
                file=_rel(lock_path, self.repo_root),
            ))
            return diagnostics

        for key, record in skills.items():
            if not isinstance(record, dict):
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_PROVENANCE_004",
                    severity="error",
                    message=f"Provenance entry '{key}' must be an object.",
                    guidance="Store provenance entries as JSON objects.",
                    file=_rel(lock_path, self.repo_root),
                ))
                continue

            source = record.get("source", "")
            source_type = record.get("sourceType", "")
            skill_path = record.get("skillPath", "")
            digest = record.get("computedHash", "")

            if source_type not in {"github"}:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_PROVENANCE_005",
                    severity="error",
                    message=f"Unknown external provenance sourceType '{source_type}'.",
                    guidance="Use a supported sourceType (currently: github).",
                    file=_rel(lock_path, self.repo_root),
                    context={"entry": key},
                ))
            if not isinstance(source, str) or "/" not in source:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_PROVENANCE_006",
                    severity="error",
                    message=f"Invalid provenance source '{source}'.",
                    guidance="Set source to '<owner>/<repo>' format.",
                    file=_rel(lock_path, self.repo_root),
                    context={"entry": key},
                ))
            if not isinstance(skill_path, str) or ".." in Path(skill_path).parts:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_PROVENANCE_007",
                    severity="error",
                    message=f"Invalid skillPath '{skill_path}'.",
                    guidance="Keep skillPath relative and disallow parent traversal segments.",
                    file=_rel(lock_path, self.repo_root),
                    context={"entry": key},
                ))
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_PROVENANCE_008",
                    severity="error",
                    message=f"Invalid computedHash for '{key}'.",
                    guidance="Use 64-char lowercase hex digests.",
                    file=_rel(lock_path, self.repo_root),
                    context={"entry": key},
                ))

        diagnostics.append(Diagnostic(
            rule_id="AETHER_PROVENANCE_009",
            severity="warning",
            message="skills-lock computedHash values are preserved provenance and are not validated against a reconstructed historical algorithm.",
            guidance="Keep existing lock hashes unchanged unless migration policy provides a documented algorithm update.",
            file=_rel(lock_path, self.repo_root),
        ))

        return diagnostics

    def validate_distribution(self) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        dist_dir = self.repo_root / "dist"
        if not dist_dir.exists():
            diagnostics.append(Diagnostic(
                rule_id="AETHER_DIST_001",
                severity="warning",
                message="Distribution validation skipped because dist/ does not exist (issue 011 not yet landed).",
                guidance="Once distribution generation exists, run with dist artifacts present.",
            ))
            return diagnostics

        for record in self.generate_catalog().get("artifacts", []):
            for rel_path in record.get("generated_distribution_paths", []):
                p = self.repo_root / rel_path
                if not p.exists():
                    diagnostics.append(Diagnostic(
                        rule_id="AETHER_DIST_002",
                        severity="error",
                        message=f"Missing generated distribution artifact '{rel_path}'.",
                        guidance="Generate distribution artifacts or correct generated_distribution_paths entries.",
                        artifact_id=record.get("id"),
                    ))
        return diagnostics

    def validate_staging(self, strict: bool = False) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        staging = self.repo_root / ".staging"
        if not staging.exists():
            return diagnostics
        allowed = {"agents", "hooks", "instructions", "integrations", "manifests", "scripts", "skills", "specs"}
        for child in sorted(staging.iterdir(), key=lambda p: p.name):
            if child.name not in allowed:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_STAGING_001",
                    severity="error" if strict else "warning",
                    message=f"Unclassified top-level staging unit '{child.name}'.",
                    guidance="Classify staging content under a known top-level bucket or remove it.",
                    file=_rel(child, self.repo_root),
                    context={"strict_mode": strict},
                ))
        return diagnostics

    def validate_skill_spec_mapping(self, specs_by_id: dict[str, dict[str, Any]]) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        for skill_dir in self._skill_dirs():
            skill_path = skill_dir / "SKILL.md"
            rel = _rel(skill_path, self.repo_root)
            fm, _ = _parse_frontmatter(skill_path)
            if not fm:
                continue
            metadata = fm.get("metadata") if isinstance(fm.get("metadata"), dict) else {}
            spec_id = metadata.get("aether-spec-id")
            if spec_id and spec_id not in specs_by_id:
                diagnostics.append(Diagnostic(
                    rule_id="AETHER_MAPPING_001",
                    severity="error",
                    message=f"Skill maps to missing specification id '{spec_id}'.",
                    guidance="Set metadata.aether-spec-id to an existing specification ID.",
                    artifact_id=f"skill/{skill_dir.name}",
                    file=rel,
                    line=1,
                ))
        return diagnostics

    def run_validation(self, scopes: set[str], strict_staging: bool = False, catalog_check: bool = True) -> list[Diagnostic]:
        diagnostics: list[Diagnostic] = []
        specs_diags, specs_by_id, spec_paths = ([], {}, {})

        if "skills" in scopes:
            diagnostics.extend(self.validate_skills())
        if "specifications" in scopes:
            specs_diags, specs_by_id, spec_paths = self.validate_specs()
            diagnostics.extend(specs_diags)
        if "graph" in scopes:
            if not specs_by_id:
                _specs_diags, specs_by_id, spec_paths = self.validate_specs()
            diagnostics.extend(self.validate_graph(specs_by_id, spec_paths))
            diagnostics.extend(self.validate_skill_spec_mapping(specs_by_id))
        if "catalog" in scopes:
            diagnostics.extend(self.validate_catalog(check_only=catalog_check))
        if "distribution" in scopes:
            diagnostics.extend(self.validate_distribution())
        if "provenance" in scopes:
            diagnostics.extend(self.validate_provenance())
        if "staging" in scopes:
            diagnostics.extend(self.validate_staging(strict=strict_staging))
        if "json" in scopes:
            diagnostics.extend(self.validate_json_files())
        if "shell" in scopes:
            diagnostics.extend(self.validate_shell_syntax())
        if "links" in scopes:
            diagnostics.extend(self.validate_markdown_links())

        return diagnostics


def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "library" / "organization").exists() and (candidate / "catalog").exists():
            return candidate
    raise ValidationError("Unable to locate repository root containing library/organization and catalog directories.")


def format_text(diagnostics: list[Diagnostic]) -> str:
    lines = []
    for d in diagnostics:
        location = ""
        if d.file:
            location = d.file
            if d.line:
                location = f"{location}:{d.line}"
        lines.append(
            f"[{d.severity.upper()}] {d.rule_id}"
            + (f" ({d.artifact_id})" if d.artifact_id else "")
            + (f" @ {location}" if location else "")
            + f"\n  Problem: {d.message}\n  Fix: {d.guidance}"
        )
    if not lines:
        return "Validation passed with 0 diagnostics."
    return "\n".join(lines)


def format_json(diagnostics: list[Diagnostic]) -> str:
    payload = {
        "schema_version": "aether.validation-diagnostics/v1",
        "diagnostics": [asdict(d) for d in diagnostics],
    }
    return json.dumps(payload, indent=2, sort_keys=True)


def command_validate(args: argparse.Namespace) -> int:
    root = find_repo_root(Path(args.repo_root).resolve() if args.repo_root else Path.cwd())
    validator = AetherValidator(root)

    scopes = set()
    if args.skills:
        scopes.add("skills")
    if args.specifications:
        scopes.add("specifications")
    if args.graph:
        scopes.add("graph")
    if args.catalog:
        scopes.add("catalog")
    if args.distribution:
        scopes.add("distribution")
    if args.provenance:
        scopes.add("provenance")
    if args.staging:
        scopes.add("staging")
    if args.json_files:
        scopes.add("json")
    if args.shell:
        scopes.add("shell")
    if args.links:
        scopes.add("links")

    if not scopes:
        scopes = {"skills", "specifications", "graph", "catalog", "distribution", "provenance", "staging", "json", "shell", "links"}

    diagnostics = validator.run_validation(
        scopes=scopes,
        strict_staging=args.strict_staging,
        catalog_check=True,
    )

    if args.format == "json":
        print(format_json(diagnostics))
    else:
        print(format_text(diagnostics))

    has_errors = any(d.severity == "error" for d in diagnostics)
    return EXIT_VALIDATION_FAILED if has_errors else EXIT_OK


def command_catalog_generate(args: argparse.Namespace) -> int:
    root = find_repo_root(Path(args.repo_root).resolve() if args.repo_root else Path.cwd())
    validator = AetherValidator(root)
    generated = validator.generate_catalog()
    if args.check:
        existing = json.loads(validator.catalog_path.read_text(encoding="utf-8")) if validator.catalog_path.exists() else None
        if existing != generated:
            print("Catalog drift detected.")
            return EXIT_VALIDATION_FAILED
        print("Catalog is up to date.")
        return EXIT_OK

    validator.write_catalog()
    print(f"Wrote {validator.catalog_path}")
    return EXIT_OK


def command_test(_args: argparse.Namespace) -> int:
    root = find_repo_root(Path(_args.repo_root).resolve() if _args.repo_root else Path.cwd())
    suite = unittest.defaultTestLoader.discover(str(root / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return EXIT_OK if result.wasSuccessful() else EXIT_VALIDATION_FAILED


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="aether", description="Canonical deterministic Aether validation and catalog tooling.")
    parser.add_argument("--repo-root", help="Explicit repository root path. Defaults to auto-detected from current working directory.")

    subparsers = parser.add_subparsers(dest="command", required=True)

    validate = subparsers.add_parser("validate", help="Run deterministic validation checks.")
    validate.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    validate.add_argument("--skills", action="store_true", help="Run only skill validation rules.")
    validate.add_argument("--specifications", action="store_true", help="Run only specification schema/content validation rules.")
    validate.add_argument("--graph", action="store_true", help="Run only relationship graph and mapping validation rules.")
    validate.add_argument("--catalog", action="store_true", help="Run only catalog generation/check validation rules.")
    validate.add_argument("--distribution", action="store_true", help="Run only distribution validation rules.")
    validate.add_argument("--provenance", action="store_true", help="Run only external provenance validation rules.")
    validate.add_argument("--staging", action="store_true", help="Run only staging disposition validation rules.")
    validate.add_argument("--strict-staging", action="store_true", help="Treat unclassified staging units as errors.")
    validate.add_argument("--json-files", action="store_true", help="Run only JSON syntax validation rules.")
    validate.add_argument("--shell", action="store_true", help="Run only shebang-aware shell syntax validation rules.")
    validate.add_argument("--links", action="store_true", help="Run only markdown link/path traversal validation rules.")
    validate.set_defaults(handler=command_validate)

    catalog = subparsers.add_parser("catalog", help="Catalog generation commands.")
    catalog_sub = catalog.add_subparsers(dest="catalog_command", required=True)
    catalog_generate = catalog_sub.add_parser("generate", help="Generate or check deterministic first-party catalog.")
    catalog_generate.add_argument("--check", action="store_true", help="Check for drift without rewriting files.")
    catalog_generate.set_defaults(handler=command_catalog_generate)

    test = subparsers.add_parser("test", help="Run validator test suite.")
    test.set_defaults(handler=command_test)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        return args.handler(args)
    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return EXIT_INVALID_INVOCATION
    except SystemExit as exc:
        if isinstance(exc.code, int):
            return exc.code
        return EXIT_INVALID_INVOCATION
    except Exception as exc:  # pragma: no cover
        print(f"INTERNAL ERROR: {exc}", file=sys.stderr)
        return EXIT_INTERNAL_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
