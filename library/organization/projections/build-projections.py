#!/usr/bin/env python3
"""Build deterministic provider projections from canonical Aether agent source.

The provider registry is canonical for adapter support. Provider-native files are
release artifacts only; canonical agent intent remains under
``library/organization/agents/<agent-id>/AGENT.md``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[3]
AGENTS_DIR = REPO_ROOT / "library" / "organization" / "agents"
REGISTRY_PATH = REPO_ROOT / "library" / "organization" / "projections" / "provider-registry.v1.json"
SCHEMA_PATH = REPO_ROOT / "catalog" / "schemas" / "aether.projection-interface.v1.schema.json"
DECISION_IMPACT_PATH = (
    REPO_ROOT
    / "library"
    / "organization"
    / "projections"
    / "templates"
    / "decision-impact.AGENTS.md"
)
GENERATOR_ID = "library/organization/projections/build-projections.py"
INTERFACE_SCHEMA = "aether.projection-interface/v1"
INTERFACE_VERSION = "1.1.0"
MANIFEST_SCHEMA = "aether.projection-manifest/v1"
MANUAL_IMPORT_SCHEMA = "aether.manual-agent-import/v1"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
INSTRUCTION_METADATA_RE = re.compile(r"<!-- aether-instruction (\{.*\}) -->")
DECISION_IMPACT_START = "<!-- BEGIN AETHER DECISION-IMPACT -->"
DECISION_IMPACT_END = "<!-- END AETHER DECISION-IMPACT -->"
_SKILL_LINK_RE = re.compile(r"(?:\.\./){2}skills/[^/]+/([^/]+)/SKILL\.md")
_SPEC_LINK_RE = re.compile(r"(?:\.\./){2}specs/([^\s\)\"']+)")

CLAUDE_TOOL_MAP: dict[str, tuple[str, ...]] = {
    "read": ("Read",),
    "search": ("Glob", "Grep"),
    "edit": ("Edit", "Write"),
    "execute": ("Bash",),
    "web": ("WebFetch", "WebSearch"),
}

OPENCODE_TOOL_MAP: dict[str, tuple[str, ...]] = {
    "read": ("read",),
    "search": ("glob", "grep"),
    "edit": ("edit",),
    "execute": ("bash",),
    "web": ("webfetch", "websearch"),
}


def _canonical_json(value: Any, *, pretty: bool = False) -> str:
    """Return deterministic JSON text."""
    if pretty:
        return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _normalized_text(path: Path) -> str:
    """Read UTF-8 text with LF line endings."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def _sha256_bytes(content: bytes) -> str:
    """Return a lowercase SHA-256 digest."""
    return hashlib.sha256(content).hexdigest()


def _sha256_text(text: str) -> str:
    """Return a SHA-256 digest for normalized UTF-8 text."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    return _sha256_bytes(normalized.encode("utf-8"))


def _repo_relative(path: Path) -> str:
    """Return a repository-relative POSIX path when possible."""
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _load_decision_impact() -> tuple[dict[str, Any], str]:
    """Load and validate the canonical decision-impact instruction module."""
    if not DECISION_IMPACT_PATH.is_file():
        raise ValueError(
            f"decision-impact instruction is missing: {_repo_relative(DECISION_IMPACT_PATH)}"
        )
    text = _normalized_text(DECISION_IMPACT_PATH).strip()
    if text.count(DECISION_IMPACT_START) != 1 or text.count(DECISION_IMPACT_END) != 1:
        raise ValueError("decision-impact instruction must contain exactly one managed marker pair")
    if text.index(DECISION_IMPACT_START) > text.index(DECISION_IMPACT_END):
        raise ValueError("decision-impact instruction markers are out of order")

    match = INSTRUCTION_METADATA_RE.search(text)
    if match is None:
        raise ValueError("decision-impact instruction is missing aether-instruction metadata")
    try:
        metadata = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        raise ValueError(f"decision-impact instruction metadata is invalid JSON: {exc}") from exc
    if not isinstance(metadata, dict):
        raise ValueError("decision-impact instruction metadata must be an object")
    for field in ("id", "version", "status", "inherits"):
        if field not in metadata:
            raise ValueError(f"decision-impact instruction metadata is missing {field}")
    if metadata["id"] != "decision-impact":
        raise ValueError("decision-impact instruction metadata has an unexpected id")
    if not isinstance(metadata["inherits"], list) or not metadata["inherits"]:
        raise ValueError("decision-impact instruction must inherit at least one pinned contract")
    for inherited in metadata["inherits"]:
        if not isinstance(inherited, dict) or not {
            "contract",
            "revision",
            "source_url",
            "status",
        }.issubset(inherited):
            raise ValueError(
                "decision-impact inherited contracts require contract, revision, source_url, and status"
            )
    return metadata, text


def _decision_impact_provenance() -> dict[str, Any]:
    """Return provenance for the shared decision-impact module."""
    metadata, _module = _load_decision_impact()
    source_text = _normalized_text(DECISION_IMPACT_PATH)
    return {
        "id": metadata["id"],
        "version": metadata["version"],
        "status": metadata["status"],
        "source": _repo_relative(DECISION_IMPACT_PATH),
        "source_digest": {
            "algorithm": "sha256-utf8-lf",
            "value": _sha256_text(source_text),
        },
        "inherits": metadata["inherits"],
    }


def _apply_decision_impact(body: str) -> str:
    """Insert or refresh exactly one managed decision-impact block."""
    _metadata, module = _load_decision_impact()
    start_count = body.count(DECISION_IMPACT_START)
    end_count = body.count(DECISION_IMPACT_END)
    if start_count != end_count or start_count > 1:
        raise ValueError("projected guidance contains an invalid decision-impact marker set")
    if start_count == 0:
        return f"{body.rstrip()}\n\n{module}\n"

    start = body.index(DECISION_IMPACT_START)
    end = body.index(DECISION_IMPACT_END, start) + len(DECISION_IMPACT_END)
    parts = [body[:start].rstrip(), module, body[end:].lstrip()]
    return "\n\n".join(part for part in parts if part).rstrip() + "\n"


def load_registry() -> dict[str, Any]:
    """Load and validate the versioned provider registry."""
    registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(registry), key=lambda error: list(error.absolute_path))
    if errors:
        details = "; ".join(
            f"{'.'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ValueError(f"provider registry does not satisfy its schema: {details}")
    if registry["interface_version"] != INTERFACE_VERSION:
        raise ValueError(
            "provider registry interface_version does not match the projection builder"
        )
    return registry


def find_agents() -> list[tuple[str, Path]]:
    """Return canonical agents in deterministic ID order."""
    agents: list[tuple[str, Path]] = []
    for child in sorted(AGENTS_DIR.iterdir()):
        if not child.is_dir():
            continue
        source = child / "AGENT.md"
        if source.is_file():
            agents.append((child.name, source))
    return agents


def _parse_agent(agent_id: str, source: Path) -> tuple[dict[str, Any], str]:
    """Return canonical frontmatter and Markdown body for one agent."""
    text = _normalized_text(source)
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"agent {agent_id} has no YAML frontmatter: {_repo_relative(source)}")
    frontmatter = yaml.safe_load(match.group(1)) or {}
    if not isinstance(frontmatter, dict):
        raise ValueError(f"agent {agent_id} frontmatter must be a mapping")
    if frontmatter.get("aether-id") != agent_id:
        raise ValueError(f"agent {agent_id} does not match aether-id {frontmatter.get('aether-id')!r}")
    for required in ("name", "description", "tools"):
        if required not in frontmatter:
            raise ValueError(f"agent {agent_id} is missing required frontmatter field {required}")
    tools = frontmatter["tools"]
    if not isinstance(tools, list) or any(not isinstance(tool, str) for tool in tools):
        raise ValueError(f"agent {agent_id} tools must be a string list")
    return frontmatter, text[match.end():].lstrip("\n")


def _rewrite_links(body: str, spec_prefix: str) -> str:
    """Rewrite canonical skill/spec paths to consumer-local paths."""
    body = _SKILL_LINK_RE.sub(lambda match: f".agents/skills/{match.group(1)}/SKILL.md", body)
    return _SPEC_LINK_RE.sub(lambda match: f"{spec_prefix}/{match.group(1)}", body)


def _projection_provenance(provider: str, source: Path, source_text: str) -> dict[str, Any]:
    """Return deterministic provenance shared by every projected agent."""
    return {
        "interface": INTERFACE_SCHEMA,
        "interface_version": INTERFACE_VERSION,
        "provider": provider,
        "source": _repo_relative(source),
        "source_digest": {
            "algorithm": "sha256-utf8-lf",
            "value": _sha256_text(source_text),
        },
        "generator": GENERATOR_ID,
        "instruction_modules": [_decision_impact_provenance()],
    }


def _provenance_comment(provider: str, source: Path, source_text: str) -> str:
    """Return a provider-safe Markdown provenance header."""
    payload = _canonical_json(_projection_provenance(provider, source, source_text))
    return f"<!-- aether-projection {payload} -->"


def _render_markdown(frontmatter: dict[str, Any], provenance: str, body: str) -> bytes:
    """Render one Markdown projection deterministically."""
    yaml_text = yaml.safe_dump(
        frontmatter,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip()
    return f"---\n{yaml_text}\n---\n{provenance}\n\n{body.rstrip()}\n".encode("utf-8")


def _agents_guidance_fixture() -> bytes:
    """Render an install-review fixture for repository-root AGENTS.md guidance."""
    _metadata, module = _load_decision_impact()
    provenance = {
        "interface": INTERFACE_SCHEMA,
        "interface_version": INTERFACE_VERSION,
        "kind": "repository-agents-guidance-fixture",
        "instruction_modules": [_decision_impact_provenance()],
        "generator": GENERATOR_ID,
    }
    return (
        "# AGENTS.md\n\n"
        f"<!-- aether-projection {_canonical_json(provenance)} -->\n\n"
        "> Generated integration fixture. Preserve consumer-owned repository commands, "
        "boundaries, and nested instruction precedence when installing this managed module.\n\n"
        f"{module}\n"
    ).encode("utf-8")


def _mapped_tools(canonical_tools: list[str], mapping: dict[str, tuple[str, ...]]) -> list[str]:
    """Map canonical Aether tool intent into a provider allowlist."""
    result: list[str] = []
    for canonical_tool in canonical_tools:
        provider_tools = mapping.get(canonical_tool)
        if provider_tools is None:
            raise ValueError(f"unsupported canonical tool for provider mapping: {canonical_tool}")
        for provider_tool in provider_tools:
            if provider_tool not in result:
                result.append(provider_tool)
    return result


def _github_projection(
    frontmatter: dict[str, Any],
    body: str,
    source: Path,
    source_text: str,
    *,
    organization: bool,
) -> bytes:
    """Render the GitHub Copilot/VS Code shared agent profile."""
    projected_frontmatter = {
        "name": frontmatter["name"],
        "description": frontmatter["description"],
        "tools": frontmatter["tools"],
    }
    spec_prefix = "specs" if organization else ".github/specs"
    return _render_markdown(
        projected_frontmatter,
        _provenance_comment("github-copilot", source, source_text),
        _rewrite_links(body, spec_prefix),
    )


def _claude_projection(
    agent_id: str,
    frontmatter: dict[str, Any],
    body: str,
    source: Path,
    source_text: str,
) -> bytes:
    """Render a Claude Code project subagent."""
    projected_frontmatter = {
        "name": agent_id,
        "description": frontmatter["description"],
        "tools": _mapped_tools(frontmatter["tools"], CLAUDE_TOOL_MAP),
    }
    return _render_markdown(
        projected_frontmatter,
        _provenance_comment("claude-code", source, source_text),
        _rewrite_links(body, ".github/specs"),
    )


def _opencode_permissions(frontmatter: dict[str, Any]) -> dict[str, Any]:
    """Translate canonical least-privilege intent into OpenCode permissions."""
    permission: dict[str, Any] = {"*": "deny"}
    for provider_tool in _mapped_tools(frontmatter["tools"], OPENCODE_TOOL_MAP):
        permission[provider_tool] = "allow"

    metadata = frontmatter.get("metadata")
    skills = metadata.get("aether-skills", []) if isinstance(metadata, dict) else []
    if skills:
        if not isinstance(skills, list) or any(not isinstance(skill, str) for skill in skills):
            raise ValueError("metadata.aether-skills must be a string list")
        permission["skill"] = {"*": "deny", **{skill: "allow" for skill in sorted(skills)}}
    return permission


def _opencode_projection(
    frontmatter: dict[str, Any],
    body: str,
    source: Path,
    source_text: str,
) -> bytes:
    """Render an OpenCode project subagent."""
    projected_frontmatter = {
        "description": frontmatter["description"],
        "mode": "subagent",
        "permission": _opencode_permissions(frontmatter),
    }
    return _render_markdown(
        projected_frontmatter,
        _provenance_comment("opencode", source, source_text),
        _rewrite_links(body, ".github/specs"),
    )


def _manual_zencoder_packet(agent_records: list[dict[str, Any]]) -> bytes:
    """Render an explicit manual-import packet without inventing a native file format."""
    packet = {
        "schema_version": MANUAL_IMPORT_SCHEMA,
        "provider": "zencoder",
        "status": "manual-import",
        "reason": (
            "No repository-native Zencoder custom-agent definition format was verified "
            "during the 2026-08-23 provider review. Use this packet as reviewed input "
            "to Zencoder's custom-agent UI or organization catalog."
        ),
        "agents": agent_records,
    }
    return _canonical_json(packet, pretty=True).encode("utf-8")


def _build_files(registry: dict[str, Any]) -> dict[str, bytes]:
    """Build every provider projection and its deterministic manifest in memory."""
    files: dict[str, bytes] = {}
    zencoder_agents: list[dict[str, Any]] = []
    source_records: dict[str, dict[str, Any]] = {}

    for agent_id, source in find_agents():
        source_text = _normalized_text(source)
        frontmatter, body = _parse_agent(agent_id, source)
        projected_body = _apply_decision_impact(body)
        source_provenance = _projection_provenance("canonical", source, source_text)
        source_records[agent_id] = source_provenance

        files[f"github/repository/.github/agents/{agent_id}.agent.md"] = _github_projection(
            frontmatter,
            projected_body,
            source,
            source_text,
            organization=False,
        )
        files[f"github/organization/agents/{agent_id}.agent.md"] = _github_projection(
            frontmatter,
            projected_body,
            source,
            source_text,
            organization=True,
        )
        files[f"claude/repository/.claude/agents/{agent_id}.md"] = _claude_projection(
            agent_id,
            frontmatter,
            projected_body,
            source,
            source_text,
        )
        files[f"opencode/repository/.opencode/agents/{agent_id}.md"] = _opencode_projection(
            frontmatter,
            projected_body,
            source,
            source_text,
        )

        zencoder_agents.append(
            {
                "id": agent_id,
                "name": frontmatter["name"],
                "description": frontmatter["description"],
                "canonical_tools": list(frontmatter["tools"]),
                "instructions": _rewrite_links(projected_body, ".github/specs").rstrip(),
                "provenance": source_provenance,
            }
        )

    files["fixtures/repository-instructions/AGENTS.md"] = _agents_guidance_fixture()
    files["zencoder/manual-import/agents.json"] = _manual_zencoder_packet(zencoder_agents)

    for template in registry["mcp_templates"]:
        source = REPO_ROOT / template["source"]
        if not source.is_file():
            raise ValueError(f"MCP template source is missing: {template['source']}")
        files[Path(template["output"]).relative_to("dist").as_posix()] = _normalized_text(source).encode("utf-8")

    provider_states = [
        {
            "id": provider["id"],
            "status": provider["status"],
            "adapter": provider["adapter"],
            "shares_output_with": provider["shares_output_with"],
            "unsupported_features": provider["unsupported_features"],
        }
        for provider in registry["providers"]
    ]
    manifest_outputs = [
        {
            "path": f"dist/{path}",
            "sha256": _sha256_bytes(content),
        }
        for path, content in sorted(files.items())
    ]
    manifest = {
        "schema_version": MANIFEST_SCHEMA,
        "interface_version": registry["interface_version"],
        "generator": GENERATOR_ID,
        "provider_registry": _repo_relative(REGISTRY_PATH),
        "provider_registry_sha256": _sha256_text(_normalized_text(REGISTRY_PATH)),
        "providers": provider_states,
        "canonical_sources": source_records,
        "outputs": manifest_outputs,
    }
    files["projections/manifest.v1.json"] = _canonical_json(manifest, pretty=True).encode("utf-8")
    return files


def build(*, check: bool = False, output_directory: Path | None = None) -> int:
    """Build provider projections or verify an existing generated tree."""
    registry = load_registry()
    output_root = output_directory or (REPO_ROOT / "dist")
    expected = _build_files(registry)
    drift = 0

    for relative_path, content in sorted(expected.items()):
        output_path = output_root / relative_path
        display_path = _repo_relative(output_path)
        if check:
            if not output_path.is_file():
                print(f"DRIFT  missing projection: {display_path}")
                drift += 1
            elif output_path.read_bytes() != content:
                print(f"DRIFT  stale projection: {display_path}")
                drift += 1
            else:
                print(f"OK     {display_path}")
            continue

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(content)
        print(f"wrote  {display_path}")

    if check and drift:
        print(f"\n{drift} provider projection(s) are out of date.", file=sys.stderr)
        return 1
    if check:
        print(f"\nAll {len(expected)} provider projection file(s) are current.")
    else:
        print(f"\n{len(expected)} provider projection file(s) written.")
    return 0


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify generated projections without writing files.",
    )
    parser.add_argument(
        "--output-directory",
        default="dist",
        help="Base directory receiving provider projections.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the provider projection builder."""
    arguments = parse_arguments()
    return build(
        check=arguments.check,
        output_directory=(REPO_ROOT / arguments.output_directory),
    )


if __name__ == "__main__":
    raise SystemExit(main())
