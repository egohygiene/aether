"""Inventory, composition, and fresh-session routing tests for continuity."""

from __future__ import annotations

import json
from pathlib import Path
import re
import unittest

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[1]
INSTRUCTION_DIR = (
    ROOT / "library/organization/instructions/repository-continuity"
)
INVENTORY_PATH = INSTRUCTION_DIR / "continuity-dispositions.v1.json"
INVENTORY_SCHEMA_PATH = (
    ROOT / "catalog/schemas/aether.continuity-dispositions.v1.schema.json"
)
ROUTING_FIXTURE_PATH = (
    ROOT
    / "library/organization/skills/methodology/maintain-repository-continuity"
    / "evals/fixtures/repository-routing.v1.json"
)
AGENT_CATALOG_PATH = ROOT / "library/organization/agents/catalog.json"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def load_json(path: Path) -> dict:
    """Read one JSON object."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise AssertionError(f"expected object: {path}")
    return value


def frontmatter(path: Path) -> dict:
    """Read YAML frontmatter from one canonical Markdown source."""
    match = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if match is None:
        raise AssertionError(f"missing frontmatter: {path}")
    value = yaml.safe_load(match.group(1))
    if not isinstance(value, dict):
        raise AssertionError(f"frontmatter is not an object: {path}")
    return value


def resolve_fresh_session(case: dict) -> dict[str, str | None]:
    """Apply the fixture's minimum v1 evidence-precedence routing rules."""
    continuity = case["continuity"]
    live = case["live"]
    if live["status"] != "verified":
        return {"action": "partial-blocked", "next_work": None}
    if (
        continuity["status"] != "current"
        or continuity["base_revision"] != live["default_branch_revision"]
        or live["parallel_pull_requests"]
        or live["next_work_state"] != "open"
    ):
        return {"action": "reconcile-before-selection", "next_work": None}
    return {"action": "continue", "next_work": continuity["next_work"]}


class ContinuityIntegrationTests(unittest.TestCase):
    """Keep every canonical disposition complete, bounded, and executable."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.inventory = load_json(INVENTORY_PATH)

    def test_inventory_satisfies_schema_and_has_unique_sorted_ids(self) -> None:
        schema = load_json(INVENTORY_SCHEMA_PATH)
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.assertEqual(list(validator.iter_errors(self.inventory)), [])

        for key in ("skills", "agents"):
            identifiers = [record["id"] for record in self.inventory[key]]
            self.assertEqual(identifiers, sorted(identifiers))
            self.assertEqual(len(identifiers), len(set(identifiers)))

    def test_inventory_covers_every_canonical_skill_and_agent_exactly_once(self) -> None:
        expected_skills = {
            path.parent.name
            for path in (ROOT / "library/organization/skills").glob("*/*/SKILL.md")
        }
        expected_agents = {
            path.parent.name
            for path in (ROOT / "library/organization/agents").glob("*/AGENT.md")
        }
        actual_skills = {record["id"] for record in self.inventory["skills"]}
        actual_agents = {record["id"] for record in self.inventory["agents"]}

        self.assertEqual(actual_skills, expected_skills)
        self.assertEqual(actual_agents, expected_agents)
        self.assertEqual(len(actual_skills), 36)
        self.assertEqual(len(actual_agents), 9)

        for record in self.inventory["skills"] + self.inventory["agents"]:
            source = ROOT / record["source"]
            self.assertTrue(source.is_file(), record["source"])
            self.assertEqual(source.parent.name, record["id"])
            self.assertNotIn(".staging", source.parts)

    def test_applicable_skills_declare_compact_domain_handoffs(self) -> None:
        for record in self.inventory["skills"]:
            source = ROOT / record["source"]
            text = source.read_text(encoding="utf-8")
            metadata = frontmatter(source).get("metadata", {})
            evals = load_json(source.parent / "evals/evals.json")

            if record["disposition"] == "not-applicable":
                self.assertNotIn("aether-continuity-disposition", text, record["id"])
                continue

            self.assertEqual(metadata["aether-version"], evals["version"], record["id"])
            self.assertEqual(metadata["aether-version"], "1.1.0", record["id"])

            if record["id"] == "maintain-repository-continuity":
                self.assertIn("## Perform the pre-PR handoff", text)
                continue

            marker = f"<!-- aether-continuity-disposition: {record['disposition']} -->"
            self.assertEqual(text.count(marker), 1, record["id"])
            self.assertIn("`maintain-repository-continuity`", text, record["id"])
            self.assertIn(f"- **Contribute:** {record['domain_evidence'][0]}", text)
            self.assertIn(f"- **Never claim:** {record['never_claim'][0]}", text)

            start = text.index("## Repository continuity composition")
            later_heading = text.find("\n## ", start + 4)
            block = text[start:] if later_heading == -1 else text[start:later_heading]
            self.assertLess(len(block.encode("utf-8")), 1800, record["id"])
            self.assertNotIn("## Resume safely", block, record["id"])
            self.assertNotIn("## Compact and supersede", block, record["id"])

            if record["pre_pr_write"]:
                self.assertIn("**Refresh** and **Verify**", block, record["id"])
            else:
                self.assertIn("continuity read-only", block, record["id"])

    def test_agents_compose_the_skill_without_gaining_authority(self) -> None:
        catalog = load_json(AGENT_CATALOG_PATH)["agents"]
        for record in self.inventory["agents"]:
            source = ROOT / record["source"]
            text = source.read_text(encoding="utf-8")
            fm = frontmatter(source)
            metadata = fm["metadata"]
            marker = f"<!-- aether-continuity-disposition: {record['disposition']} -->"

            self.assertEqual(text.count(marker), 1, record["id"])
            self.assertIn("maintain-repository-continuity", metadata["aether-skills"])
            self.assertIn("repository-continuity", metadata["aether-specs"])
            self.assertIn(f"- **Contribute:** {record['domain_evidence'][0]}", text)
            self.assertIn(f"- **Never claim:** {record['never_claim'][0]}", text)
            self.assertEqual(metadata["aether-version"], "1.1.0")
            self.assertEqual(catalog[record["id"]]["version"], "1.1.0")
            self.assertIn(
                "maintain-repository-continuity",
                catalog[record["id"]]["skills"],
            )
            self.assertIn("repository-continuity", catalog[record["id"]]["specs"])

            if record["pre_pr_write"]:
                self.assertIn("**Refresh** and **Verify**", text, record["id"])
            else:
                self.assertIn("continuity read-only", text, record["id"])

        self.assertNotIn("edit", frontmatter(ROOT / "library/organization/agents/auditor/AGENT.md")["tools"])
        self.assertNotIn(
            "edit",
            frontmatter(
                ROOT / "library/organization/agents/github-issue-creator/AGENT.md"
            )["tools"],
        )

    def test_fresh_session_routes_three_repository_classes_without_chat_history(self) -> None:
        fixture = load_json(ROUTING_FIXTURE_PATH)
        self.assertFalse(fixture["prior_conversation_provided"])
        repositories = fixture["repositories"]
        self.assertEqual(
            {case["repository_class"] for case in repositories},
            {"application", "library", "publication"},
        )
        self.assertGreaterEqual(len({case["host"] for case in repositories}), 2)

        for case in repositories:
            self.assertTrue(case["instructions_available"])
            self.assertTrue(case["canonical_documents_available"])
            self.assertEqual(resolve_fresh_session(case), case["expected"], case["id"])

        library = next(case for case in repositories if case["id"] == "library-fresh-resume")
        self.assertEqual(library["expected"]["next_work"], "example/library#142")


if __name__ == "__main__":
    unittest.main()
