#!/usr/bin/env python3
"""Reference validation for `egohygiene.repository-release/v1` declarations.

This validates a declaration and its local changelog/source paths. It is a
portable contract aid, not a publishing command or an organization conformance
gate; Relay and Egolint own those downstream concerns.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any

try:
    from jsonschema import Draft202012Validator
except ImportError:  # The distributed skill intentionally has a stdlib fallback.
    Draft202012Validator = None  # type: ignore[assignment,misc]


REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
CANONICAL_SCHEMA_PATH = REPOSITORY_ROOT / "catalog" / "schemas" / "aether.repository-release.v1.schema.json"
PACKAGED_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "references" / "aether.repository-release.v1.schema.json"
DEFAULT_DECLARATION = Path(".egohygiene/release.json")
SEMVER_TAG = re.compile(r"^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


class ReleaseContractError(ValueError):
    """Raised when a declaration cannot support a reviewable release plan."""


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseContractError(f"cannot read JSON object {path}: {error}") from error
    if not isinstance(value, dict):
        raise ReleaseContractError(f"{path} must contain a JSON object")
    return value


def _schema_path() -> Path:
    """Locate the canonical schema or the self-contained packaged copy."""

    for candidate in (CANONICAL_SCHEMA_PATH, PACKAGED_SCHEMA_PATH):
        if candidate.is_file():
            return candidate
    raise ReleaseContractError(
        "repository-release v1 schema is unavailable; install the complete skill package "
        "or run from an Aether checkout"
    )


def _basic_schema_errors(data: dict[str, Any]) -> list[str]:
    """Check the portable validator's minimum contract without dependencies.

    The bundled JSON Schema remains the full normative contract. This fallback
    preserves safe, useful local validation when an installed skill has only
    the Python standard library available.
    """

    errors: list[str] = []
    required = {"schema_version", "repository", "release", "changelog", "components", "delivery", "evidence", "automation"}
    missing = sorted(required - data.keys())
    if missing:
        errors.append(f"missing required top-level fields: {', '.join(missing)}")
        return errors
    if data.get("schema_version") != "egohygiene.repository-release/v1":
        errors.append("schema_version must be egohygiene.repository-release/v1")
    if not isinstance(data["repository"], dict) or data["repository"].get("release_profile") not in {
        "contract", "cli-library", "python-package", "npm-package", "container-image", "static-site", "publication", "workspace", "internal-only",
    }:
        errors.append("repository.release_profile is invalid")
    if not isinstance(data["release"], dict) or data["release"].get("tag_prefix") != "v" or data["release"].get("immutable_tags") is not True:
        errors.append("release requires tag_prefix v and immutable_tags true")
    if not isinstance(data["changelog"], dict) or data["changelog"].get("format") != "keep-a-changelog/1.1" or data["changelog"].get("unreleased_heading") != "Unreleased":
        errors.append("changelog must use keep-a-changelog/1.1 and Unreleased")
    if not isinstance(data["components"], list) or not data["components"]:
        errors.append("components must contain at least one component")
    if not isinstance(data["delivery"], dict) or not isinstance(data["delivery"].get("channels"), list) or not data["delivery"]["channels"]:
        errors.append("delivery.channels must contain at least one channel")
    if not isinstance(data["evidence"], dict) or not isinstance(data["evidence"].get("rollback"), dict):
        errors.append("evidence.rollback is required")
    elif any(key not in data["evidence"] for key in ("source", "change", "provenance", "sbom", "signature")):
        errors.append("evidence requires source, change, provenance, sbom, and signature states")
    if not isinstance(data["automation"], dict) or data["automation"].get("github", {}).get("manual_dispatch_required") is not True:
        errors.append("automation.github.manual_dispatch_required must be true")
    return errors


def _repository_path(repository: Path, value: str, label: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts or value in {"", "."}:
        raise ReleaseContractError(f"{label} is not a safe repository-relative path: {value!r}")
    resolved = (repository / candidate).resolve()
    try:
        resolved.relative_to(repository.resolve())
    except ValueError as error:
        raise ReleaseContractError(f"{label} escapes the repository: {value!r}") from error
    return resolved


def validate_release_declaration(
    repository: Path,
    declaration_path: Path = DEFAULT_DECLARATION,
    release_version: str | None = None,
) -> dict[str, Any]:
    """Validate one declaration, its local sources, and an optional release tag."""

    repository = repository.resolve()
    declaration = _repository_path(repository, declaration_path.as_posix(), "declaration path")
    data = _load_json(declaration)
    if Draft202012Validator is not None:
        schema = _load_json(_schema_path())
        validation_errors = sorted(Draft202012Validator(schema).iter_errors(data), key=str)
        details = "; ".join(
            f"{'/'.join(map(str, error.path)) or '<root>'}: {error.message}"
            for error in validation_errors
        )
    else:
        details = "; ".join(_basic_schema_errors(data))
    if details:
        raise ReleaseContractError(f"release declaration violates v1 schema: {details}")

    changelog = _repository_path(repository, data["changelog"]["path"], "changelog path")
    if not changelog.is_file():
        raise ReleaseContractError(f"required changelog is missing: {data['changelog']['path']}")
    changelog_text = changelog.read_text(encoding="utf-8")
    heading = re.escape(data["changelog"]["unreleased_heading"])
    if not re.search(rf"^## \[{heading}\]\s*$", changelog_text, re.MULTILINE):
        raise ReleaseContractError("changelog does not contain the required exact Unreleased heading")

    taskfile = _repository_path(repository, data["automation"]["taskfile_path"], "Taskfile path")
    workflow = _repository_path(repository, data["automation"]["github"]["workflow_path"], "workflow path")
    for label, path in (("Taskfile", taskfile), ("manual release workflow", workflow)):
        if not path.is_file():
            raise ReleaseContractError(f"declared {label} is missing: {path.relative_to(repository)}")

    taskfile_texts = [taskfile.read_text(encoding="utf-8")]
    # Taskfiles often expose the standard handoffs through a local include.
    # Follow simple repository-relative includes without parsing provider-specific
    # Taskfile extensions or executing any task.
    for included_value in re.findall(
        r"^\s*taskfile:\s*[\"']?([^\"'\s#]+)", taskfile_texts[0], re.MULTILINE
    ):
        included = _repository_path(repository, included_value, "Taskfile include")
        if included.is_file():
            taskfile_texts.append(included.read_text(encoding="utf-8"))
    taskfile_text = "\n".join(taskfile_texts)
    for task_name in data["automation"]["tasks"].values():
        if f"{task_name}:" not in taskfile_text:
            raise ReleaseContractError(f"declared Taskfile handoff is missing: {task_name}")
    workflow_text = workflow.read_text(encoding="utf-8")
    if "workflow_dispatch:" not in workflow_text:
        raise ReleaseContractError("declared release workflow must be manually dispatchable")
    if re.search(r"^\s*push:\s*$", workflow_text, re.MULTILINE):
        raise ReleaseContractError("declared release workflow must not publish automatically on push")

    component_ids: set[str] = set()
    for component in data["components"]:
        component_id = component["id"]
        if component_id in component_ids:
            raise ReleaseContractError(f"duplicate component id: {component_id}")
        component_ids.add(component_id)
        authority = component["version_authority"]
        path_value = authority.get("path")
        if path_value is not None:
            authority_path = _repository_path(repository, path_value, f"version authority for {component_id}")
            if not authority_path.is_file():
                raise ReleaseContractError(
                    f"version authority source is missing for {component_id}: {path_value}"
                )

    if release_version is not None:
        if not SEMVER_TAG.fullmatch(release_version):
            raise ReleaseContractError("release version must be an exact vMAJOR.MINOR.PATCH tag")
        if data["release"]["state"] == "frozen":
            raise ReleaseContractError("a frozen repository must not prepare a new release")

    return data


def render_plan(data: dict[str, Any], release_version: str | None) -> str:
    """Render deterministic, non-authoritative planning output."""

    channels = [
        {"kind": channel["kind"], "state": channel["state"]}
        for channel in data["delivery"]["channels"]
    ]
    plan = {
        "schema_version": "egohygiene.repository-release-plan/v1",
        "repository": data["repository"]["id"],
        "release_profile": data["repository"]["release_profile"],
        "requested_release_version": release_version,
        "release_state": data["release"]["state"],
        "components": [component["id"] for component in data["components"]],
        "delivery": channels,
        "evidence": data["evidence"],
        "next_step": "Create or review a release PR; this command does not tag, publish, or deploy.",
    }
    return json.dumps(plan, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", default=".", help="Repository containing the declaration.")
    parser.add_argument(
        "--declaration",
        default=DEFAULT_DECLARATION.as_posix(),
        help="Repository-relative release declaration path.",
    )
    parser.add_argument(
        "--release-version",
        help="Optional exact vMAJOR.MINOR.PATCH candidate to preflight.",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    try:
        data = validate_release_declaration(
            Path(args.repository), Path(args.declaration), args.release_version
        )
    except ReleaseContractError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(render_plan(data, args.release_version), end="")
    else:
        print(
            "VALID: "
            f"{data['repository']['id']} ({data['repository']['release_profile']}); "
            "reviewed release preparation remains required."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
