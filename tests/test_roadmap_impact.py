"""Exercise receipt/role refusals and real shared-provider composition."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "library/organization/skills/architecture/reconcile-roadmap-impact"


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


receipt = module("roadmap_receipt", SKILL / "scripts/validate_receipt.py")
projections = module("roadmap_projections", ROOT / "library/organization/projections/build-projections.py")


class RoadmapImpactTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((SKILL / "evals/fixtures/cases.json").read_text())["cases"]
        self.by_id = {row["id"]: row["receipt"] for row in self.cases}

    def test_synthetic_receipts_cover_all_dispositions_and_match_goldens(self):
        self.assertEqual(10, len(self.cases))
        self.assertEqual({"updated", "proposed", "not-affected", "blocked"},
                         {row["receipt"]["disposition"] for row in self.cases})
        for row in self.cases:
            self.assertEqual([], receipt.validate_receipt(row["receipt"]), row["id"])
            golden = json.loads((SKILL / "evals/goldens" / (row["id"] + ".golden.txt")).read_text())
            self.assertEqual(row["receipt"], golden)

    def test_every_mutating_agent_declares_skill_and_projected_shared_hook(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            self.assertEqual(0, projections.build(output_directory=output))
            manifest = json.loads((output / "projections/manifest.v1.json").read_text())
            for identity, source in projections.find_agents():
                data = yaml.safe_load(source.read_text().split("---", 2)[1])
                self.assertIn("reconcile-roadmap-impact", data["metadata"]["aether-skills"])
                self.assertIn("architecture-roadmap", data["metadata"]["aether-specs"])
                for prefix, suffix in (("github/repository/.github/agents", ".agent.md"),
                                       ("github/organization/agents", ".agent.md"),
                                       ("claude/repository/.claude/agents", ".md"),
                                       ("opencode/repository/.opencode/agents", ".md")):
                    text = (output / prefix / (identity + suffix)).read_text()
                    self.assertEqual(1, text.count(projections.ROADMAP_IMPACT_START), (identity, prefix))
                    self.assertEqual(1, text.count(projections.ROADMAP_IMPACT_END), (identity, prefix))
                    self.assertIn("Read-only roles never mutate", text)
                modules = manifest["canonical_sources"][identity]["instruction_modules"]
                self.assertEqual(1, sum(item["id"] == "roadmap-impact" for item in modules))
                permission = yaml.safe_load((output / "opencode/repository/.opencode/agents" / (identity + ".md")).read_text().split("---", 2)[1])["permission"]
                self.assertEqual("allow", permission["skill"]["reconcile-roadmap-impact"])
                if "edit" not in data["tools"]: self.assertNotIn("edit", permission)
                if "execute" not in data["tools"]: self.assertNotIn("bash", permission)
            packet = json.loads((output / "zencoder/manual-import/agents.json").read_text())
            for agent in packet["agents"]:
                self.assertEqual(1, agent["instructions"].count(projections.ROADMAP_IMPACT_START))
            for path in ("fixtures/repository-instructions/AGENTS.md", "codex/repository/AGENTS.md",
                         "github/repository/.github/copilot-instructions.md", "claude/repository/CLAUDE.md"):
                self.assertEqual(1, (output / path).read_text().count(projections.ROADMAP_IMPACT_START))

    def test_shared_block_is_idempotent_preserves_consumer_text_and_rejects_duplicates(self):
        body = "Consumer-owned commands and scoped restrictions remain here.\n"
        once = projections._apply_roadmap_impact(body)
        self.assertEqual(once, projections._apply_roadmap_impact(once))
        self.assertIn(body.strip(), once)
        with self.assertRaises(ValueError): projections._apply_roadmap_impact(once + once)
        with self.assertRaises(ValueError): projections._apply_roadmap_impact(projections.ROADMAP_IMPACT_START)

    def test_read_only_role_cannot_claim_a_roadmap_update(self):
        for role in ("reader", "read-only"):
            value = copy.deepcopy(self.by_id["complete-factual-step"]); value["role"] = role
            self.assertTrue(receipt.validate_receipt(value))
        auditor = yaml.safe_load((ROOT / "library/organization/agents/auditor/AGENT.md").read_text().split("---", 2)[1])
        self.assertEqual(["read", "search"], auditor["tools"])

    def test_no_change_needs_reason_and_forbids_fabricated_edits(self):
        for mutation in ("reason", "edit", "proposal", "intent"):
            value = copy.deepcopy(self.by_id["routine-maintenance"])
            if mutation == "reason": value["reason"] = ""
            elif mutation == "edit": value["changed_paths"] = ["ROADMAP.md"]
            elif mutation == "proposal": value["proposed_changes"] = ["An unreviewed change"]
            else: value["intent_change"] = True
            self.assertTrue(receipt.validate_receipt(value), mutation)

    def test_updated_receipt_requires_exact_path_current_source_and_review_reference_for_intent(self):
        for mutation in ("path", "stale", "revision", "evidence", "intent"):
            value = copy.deepcopy(self.by_id["complete-factual-step"])
            if mutation == "path": value["changed_paths"] = ["unrelated.md"]
            elif mutation == "stale": value["roadmap"]["availability"] = "stale"
            elif mutation == "revision": value["roadmap"]["revision"] = None
            elif mutation == "evidence": value["evidence"] = []
            else: value["intent_change"] = True
            self.assertTrue(receipt.validate_receipt(value), mutation)
        # A declaration can be structurally valid; actual review authentication
        # is intentionally outside this validator and cannot grant permission.
        value["evidence"].append(dict(kind="human-review", reference="docs/decisions/synthetic-reviewed-intent.md"))
        self.assertEqual([], receipt.validate_receipt(value))

    def test_blocked_context_cannot_be_strengthened_into_no_change_or_completion(self):
        for disposition in ("not-affected", "updated", "proposed"):
            value = copy.deepcopy(self.by_id["missing-source"]); value["disposition"] = disposition
            self.assertTrue(receipt.validate_receipt(value))

    def test_organization_signal_is_inferred_owner_specific_and_never_private_export(self):
        for mutation in ("authority", "owner", "private"):
            value = copy.deepcopy(self.by_id["organization-proposal"])
            if mutation == "authority": value["organization_signals"][0]["assertion"] = "authoritative"
            elif mutation == "owner": value["organization_signals"][0]["owner"] = "egohygiene/aether"
            else: value["visibility"] = "private"
            self.assertTrue(receipt.validate_receipt(value))

    def test_portable_schema_matches_canonical_source_and_cli_refuses_ambiguous_private_input(self):
        canonical = ROOT / "catalog/schemas/aether.roadmap-impact.v1.schema.json"
        self.assertEqual(canonical.read_bytes(), receipt.SCHEMA.read_bytes())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "receipt.json"
            path.write_text('{"reason":"SYNTHETIC-PRIVATE-SENTINEL","reason":"duplicate"}')
            result = subprocess.run([sys.executable, str(SKILL / "scripts/validate_receipt.py"), str(path)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(1, result.returncode)
            self.assertNotIn("SYNTHETIC-PRIVATE-SENTINEL", result.stdout + result.stderr)
            path.write_text(json.dumps(self.by_id["routine-maintenance"]))
            result = subprocess.run([sys.executable, str(SKILL / "scripts/validate_receipt.py"), str(path)],
                                    capture_output=True, text=True, check=False)
            self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
