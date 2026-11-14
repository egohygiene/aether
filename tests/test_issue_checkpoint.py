"""Qualify published checkpoint examples and actual provider composition."""
from __future__ import annotations

from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "library/organization/skills/methodology/execute-issue-checkpoint"
SPEC = importlib.util.spec_from_file_location("checkpoint_projections", ROOT / "library/organization/projections/build-projections.py")
projections = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(projections)


class IssueCheckpointTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((SKILL / "evals/fixtures/cases.json").read_text())["cases"]
        self.by_id = {row["id"]: row for row in self.cases}

    def test_declared_examples_preserve_complete_scope_and_real_dependency_graph(self):
        self.assertEqual(9, len(self.cases))
        for case in self.cases:
            with self.subTest(case=case["id"]):
                covered = {criterion for values in case["scope_coverage"].values() for criterion in values}
                self.assertEqual(set(case["original_criteria"]), covered)
                nodes = set(case["scope_coverage"])
                edges = {node: set() for node in nodes}
                for dependent, prerequisite in case["prerequisite_edges"]:
                    self.assertIn(dependent, nodes); self.assertIn(prerequisite, nodes)
                    self.assertNotEqual(dependent, prerequisite)
                    edges[dependent].add(prerequisite)
                visited, pending = set(), set()
                def visit(node):
                    self.assertNotIn(node, pending)
                    if node not in visited:
                        pending.add(node)
                        for target in edges[node]: visit(target)
                        pending.remove(node); visited.add(node)
                for node in nodes: visit(node)
                self.assertFalse(set(case["existing_checkpoint_ids"]) & set(case["proposed_checkpoint_ids"]))

    def test_unsplit_and_already_checkpointed_examples_create_no_duplicate_structure(self):
        small = self.by_id["small-unsplit"]
        self.assertEqual("execute-unchanged", small["decision"])
        self.assertEqual([], small["proposed_checkpoint_ids"])
        existing = self.by_id["existing-checkpoints-noop"]
        self.assertEqual(set(existing["existing_checkpoint_ids"]), set(existing["scope_coverage"]))
        self.assertEqual([], existing["proposed_checkpoint_ids"])
        self.assertEqual(2, len(self.by_id["two-useful-checkpoints"]["proposed_checkpoint_ids"]))
        independent = self.by_id["group-without-blocker"]
        self.assertEqual(2, len(independent["existing_checkpoint_ids"]))
        self.assertEqual([], independent["prerequisite_edges"])

    def test_example_evidence_does_not_strengthen_saved_or_unavailable_work(self):
        for case in self.cases:
            self.assertEqual("not-run", case["hosted_checks"])
            self.assertFalse(case["merged"])
            self.assertFalse(case["delivered"])
        saved = self.by_id["saved-draft-resume"]
        self.assertEqual("draft", saved["pr_state"])
        self.assertTrue(saved["prepared"])
        self.assertFalse(saved["validated"])
        stale = self.by_id["stale-concurrent-state"]
        self.assertNotEqual(stale["recorded_head"], stale["current_head"])
        self.assertTrue(stale["preserve_concurrent_work"])
        self.assertEqual("unavailable", self.by_id["provider-unavailable"]["pr_state"])
        self.assertEqual(0, self.by_id["read-only-session"]["remote_mutations"])

    def test_fresh_process_recovers_saved_work_and_actual_git_without_prior_chat(self):
        # Mechanical file/Git recovery, not a model/host effectiveness claim.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def git(*args):
                return subprocess.check_output(["git", "-C", str(root), *args], stderr=subprocess.PIPE, text=True).strip()
            git("init", "-q")
            (root / "implementation.txt").write_text("Synthetic prepared implementation.\n")
            git("add", ".")
            git("-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "prepared")
            implementation = git("rev-parse", "HEAD")
            handoff = dict(self.by_id["saved-draft-resume"], recorded_head=implementation,
                           instruction_sources=["AGENTS.md", "CONTINUITY.md"], next_action="Inspect the deferred native check and its available runtime.")
            (root / "HANDOFF.json").write_text(json.dumps(handoff))
            git("add", ".")
            git("-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid", "-c", "commit.gpgsign=false", "commit", "-qm", "saved handoff")
            actual = git("rev-parse", "HEAD")
            program = """import json,pathlib,subprocess,sys
root=pathlib.Path(sys.argv[1]);saved=json.loads((root/'HANDOFF.json').read_text())
head=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
print(json.dumps({'recorded':saved['recorded_head'],'actual':head,'hosted':saved['hosted_checks'],'pr':saved['pr_state'],'next':saved['next_action'],'instructions':saved['instruction_sources']}))
"""
            result = subprocess.run([sys.executable, "-I", "-c", program, str(root)], capture_output=True, text=True, check=True)
            recovered = json.loads(result.stdout)
            self.assertEqual((implementation, actual), (recovered["recorded"], recovered["actual"]))
            self.assertEqual(("not-run", "draft"), (recovered["hosted"], recovered["pr"]))
            self.assertEqual(handoff["next_action"], recovered["next"])
            self.assertEqual(["AGENTS.md", "CONTINUITY.md"], recovered["instructions"])

    def test_shared_entrypoint_is_singular_idempotent_and_keeps_consumer_text(self):
        body = "Consumer-owned scope and commands stay here.\n"
        once = projections._apply_worker_strategy(body)
        self.assertEqual(once, projections._apply_worker_strategy(once))
        self.assertIn(body.strip(), once)
        with self.assertRaises(ValueError): projections._apply_worker_strategy(once + once)
        metadata, _text = projections._load_worker_strategy()
        self.assertEqual("0.2.0", metadata["spec_version"])

    def test_actual_provider_outputs_compose_checkpoint_entrypoint_without_new_tools(self):
        with tempfile.TemporaryDirectory() as directory, redirect_stdout(io.StringIO()):
            output = Path(directory)
            self.assertEqual(0, projections.build(output_directory=output))
            for identity, source in projections.find_agents():
                canonical = yaml.safe_load(source.read_text().split("---", 2)[1])
                self.assertIn("execute-issue-checkpoint", canonical["metadata"]["aether-skills"])
                path = output / "opencode/repository/.opencode/agents" / (identity + ".md")
                text = path.read_text()
                self.assertEqual(1, text.count(projections.WORKER_STRATEGY_START))
                permission = yaml.safe_load(text.split("---", 2)[1])["permission"]
                if "edit" not in canonical["tools"]: self.assertNotIn("edit", permission)
                if "execute" not in canonical["tools"]: self.assertNotIn("bash", permission)
            for path in output.rglob("*.md"):
                if path.name == "CLAUDE.md" or path.name == "AGENTS.md" or path.name.endswith(".agent.md"):
                    self.assertEqual(1, path.read_text().count(projections.WORKER_STRATEGY_START), str(path))
            packet = json.loads((output / "zencoder/manual-import/agents.json").read_text())
            self.assertTrue(all(agent["instructions"].count(projections.WORKER_STRATEGY_START) == 1 for agent in packet["agents"]))


if __name__ == "__main__":
    unittest.main()
