"""Contract tests for provider-neutral Aether projections."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
BUILDER_PATH = ROOT / "library" / "organization" / "projections" / "build-projections.py"
SPEC = importlib.util.spec_from_file_location("aether_provider_projections", BUILDER_PATH)
assert SPEC is not None
assert SPEC.loader is not None
projections = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(projections)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def read_frontmatter(path: Path) -> dict[str, object]:
    """Load YAML frontmatter from a generated Markdown projection."""
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if match is None:
        raise AssertionError(f"missing frontmatter: {path}")
    value = yaml.safe_load(match.group(1))
    if not isinstance(value, dict):
        raise AssertionError(f"frontmatter is not an object: {path}")
    return value


class ProviderProjectionTests(unittest.TestCase):
    """Keep provider adapters deterministic, explicit, and least privilege."""

    def test_registry_is_versioned_and_resolves_provider_states(self) -> None:
        registry = projections.load_registry()
        providers = {provider["id"]: provider for provider in registry["providers"]}

        self.assertEqual(registry["schema_version"], "aether.projection-interface/v1")
        self.assertEqual(registry["interface_version"], "1.0.0")
        self.assertEqual(
            set(providers),
            {"github-copilot", "vscode-copilot", "claude-code", "opencode", "zencoder"},
        )
        self.assertEqual(providers["vscode-copilot"]["status"], "native-shared")
        self.assertEqual(providers["vscode-copilot"]["shares_output_with"], "github-copilot")
        self.assertEqual(providers["zencoder"]["status"], "manual-import")
        self.assertIn(
            "verified-repository-native-agent-file",
            providers["zencoder"]["unsupported_features"],
        )

    def test_build_emits_native_manual_and_mcp_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "dist"
            self.assertEqual(projections.build(output_directory=output), 0)

            agents = projections.find_agents()
            self.assertGreaterEqual(len(agents), 1)
            expected_count = (len(agents) * 4) + 3
            generated_files = sorted(path for path in output.rglob("*") if path.is_file())
            self.assertEqual(len(generated_files), expected_count)

            for agent_id, _source in agents:
                self.assertTrue((output / "github/repository/.github/agents" / f"{agent_id}.agent.md").is_file())
                self.assertTrue((output / "github/organization/agents" / f"{agent_id}.agent.md").is_file())
                self.assertTrue((output / "claude/repository/.claude/agents" / f"{agent_id}.md").is_file())
                self.assertTrue((output / "opencode/repository/.opencode/agents" / f"{agent_id}.md").is_file())

            self.assertTrue((output / "zencoder/manual-import/agents.json").is_file())
            self.assertTrue((output / "mcp/github/.mcp.json").is_file())
            self.assertTrue((output / "projections/manifest.v1.json").is_file())

    def test_markdown_outputs_include_source_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "dist"
            projections.build(output_directory=output)

            github = (output / "github/repository/.github/agents/architect.agent.md").read_text(encoding="utf-8")
            claude = (output / "claude/repository/.claude/agents/architect.md").read_text(encoding="utf-8")
            opencode = (output / "opencode/repository/.opencode/agents/architect.md").read_text(encoding="utf-8")

            for provider_name, text in (
                ("github-copilot", github),
                ("claude-code", claude),
                ("opencode", opencode),
            ):
                self.assertIn("<!-- aether-projection ", text)
                self.assertIn(f'\"provider\":\"{provider_name}\"', text)
                self.assertIn("library/organization/agents/architect/AGENT.md", text)
                self.assertIn("sha256-utf8-lf", text)

    def test_claude_projection_maps_tools_without_gaining_execute(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "dist"
            projections.build(output_directory=output)
            frontmatter = read_frontmatter(output / "claude/repository/.claude/agents/architect.md")

            self.assertEqual(frontmatter["name"], "architect")
            self.assertEqual(
                frontmatter["tools"],
                ["Read", "Glob", "Grep", "Edit", "Write", "WebFetch", "WebSearch"],
            )
            self.assertNotIn("Bash", frontmatter["tools"])

    def test_opencode_projection_is_explicitly_deny_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "dist"
            projections.build(output_directory=output)
            frontmatter = read_frontmatter(output / "opencode/repository/.opencode/agents/architect.md")
            permission = frontmatter["permission"]

            self.assertEqual(frontmatter["mode"], "subagent")
            self.assertEqual(permission["*"], "deny")
            self.assertEqual(permission["read"], "allow")
            self.assertEqual(permission["glob"], "allow")
            self.assertEqual(permission["grep"], "allow")
            self.assertEqual(permission["edit"], "allow")
            self.assertEqual(permission["webfetch"], "allow")
            self.assertEqual(permission["websearch"], "allow")
            self.assertNotIn("bash", permission)
            self.assertEqual(
                permission["skill"],
                {"*": "deny", "architecture-authoring": "allow"},
            )

    def test_zencoder_packet_is_explicitly_manual_import(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "dist"
            projections.build(output_directory=output)
            packet = json.loads((output / "zencoder/manual-import/agents.json").read_text(encoding="utf-8"))

            self.assertEqual(packet["schema_version"], "aether.manual-agent-import/v1")
            self.assertEqual(packet["provider"], "zencoder")
            self.assertEqual(packet["status"], "manual-import")
            self.assertIn("No repository-native Zencoder", packet["reason"])
            self.assertEqual(
                {agent["id"] for agent in packet["agents"]},
                {agent_id for agent_id, _source in projections.find_agents()},
            )

    def test_github_mcp_template_contains_no_credential_value(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "dist"
            projections.build(output_directory=output)
            template_text = (output / "mcp/github/.mcp.json").read_text(encoding="utf-8")
            template = json.loads(template_text)
            github = template["mcpServers"]["github"]

            self.assertEqual(github["command"], "docker")
            self.assertIn("GITHUB_PERSONAL_ACCESS_TOKEN", github["args"])
            self.assertNotIn("ghp_", template_text)
            self.assertNotIn("github_pat_", template_text)
            self.assertNotIn("<YOUR_TOKEN>", template_text)

    def test_two_builds_are_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            first = root / "first"
            second = root / "second"
            projections.build(output_directory=first)
            projections.build(output_directory=second)

            first_files = {
                path.relative_to(first): path.read_bytes()
                for path in first.rglob("*")
                if path.is_file()
            }
            second_files = {
                path.relative_to(second): path.read_bytes()
                for path in second.rglob("*")
                if path.is_file()
            }
            self.assertEqual(first_files, second_files)

    def test_check_mode_detects_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "dist"
            projections.build(output_directory=output)
            self.assertEqual(projections.build(check=True, output_directory=output), 0)

            target = output / "github/repository/.github/agents/architect.agent.md"
            target.write_text(target.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
            self.assertEqual(projections.build(check=True, output_directory=output), 1)

    def test_manifest_records_provider_states_and_output_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "dist"
            projections.build(output_directory=output)
            manifest = json.loads((output / "projections/manifest.v1.json").read_text(encoding="utf-8"))

            self.assertEqual(manifest["schema_version"], "aether.projection-manifest/v1")
            states = {provider["id"]: provider for provider in manifest["providers"]}
            self.assertEqual(states["zencoder"]["status"], "manual-import")
            self.assertEqual(states["vscode-copilot"]["shares_output_with"], "github-copilot")
            self.assertTrue(all(len(output_record["sha256"]) == 64 for output_record in manifest["outputs"]))


if __name__ == "__main__":
    unittest.main()
