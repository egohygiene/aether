"""Pinned discovery checks plus an opt-in, real Egolint consumer exercise."""

from __future__ import annotations

import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "library/organization/skills/authoring/github-issue-authoring"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sources = load_module("title_sources", SKILL / "scripts/verify_title_contract.py")
projections = load_module(
    "title_projections", ROOT / "library/organization/projections/build-projections.py"
)


class IssueTitleSourceTests(unittest.TestCase):
    def test_selected_bytes_and_contract_schema(self):
        selection = sources.load_selection()
        cache = sources.DEFAULT_SELECTION.parent
        contract = json.loads((cache / selection["files"][".github/issues/title-contract.v1.json"]).read_text())
        schema = json.loads((cache / selection["files"][".github/issues/schema/title-contract.v1.schema.json"]).read_text())
        Draft202012Validator(schema).validate(contract)
        self.assertEqual(selection["contract"]["authority"], "candidate")
        self.assertEqual(selection["adoption"], "explicit-repository-selection-observe")

    def test_portable_selection_matches_canonical_bytes(self):
        portable = ROOT / "dist/skills/github-issue-authoring"
        selection = sources.load_selection(portable / "references/issue-title-contract/selection.v1.json")
        self.assertEqual(selection, sources.load_selection())
        self.assertEqual(
            (portable / "scripts/verify_title_contract.py").read_bytes(),
            (SKILL / "scripts/verify_title_contract.py").read_bytes(),
        )

    def test_missing_or_corrupt_sources_are_unavailable(self):
        for mode in ("missing", "corrupt"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as directory:
                cache = Path(directory) / "cache"
                shutil.copytree(sources.DEFAULT_SELECTION.parent, cache)
                source = cache / "semantics.txt"
                if mode == "missing":
                    source.unlink()
                else:
                    source.write_text(source.read_text() + "\nchanged")
                result = subprocess.run(
                    [sys.executable, str(SKILL / "scripts/verify_title_contract.py"),
                     "--selection", str(cache / "selection.v1.json")],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, 2)
                self.assertEqual(json.loads(result.stdout)["status"], "unavailable")

    def test_mutable_pin_wrong_identity_and_escaping_paths_are_rejected(self):
        for field in ("revision", "contract_id", "path"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as directory:
                cache = Path(directory) / "cache"
                shutil.copytree(sources.DEFAULT_SELECTION.parent, cache)
                path = cache / "selection.v1.json"
                selection = json.loads(path.read_text())
                if field == "path":
                    selection["files"]["docs/issue-titles.md"] = "../outside.txt"
                else:
                    selection["contract"][field] = "main" if field == "revision" else "other/v1"
                path.write_text(json.dumps(selection))
                with self.assertRaises(ValueError):
                    sources.load_selection(path)

    def test_report_missing_stale_or_mixed_provenance_is_rejected(self):
        selection = sources.load_selection()
        good = {"schema_version": 1, "contract": selection["contract"]}
        sources.verify_report(selection, good)
        for field in ("revision", "authority", "source_digests"):
            report = copy.deepcopy(good)
            report["contract"][field] = "stale"
            with self.subTest(field=field), self.assertRaises(ValueError):
                sources.verify_report(selection, report)
        with self.assertRaises(ValueError):
            sources.verify_report(selection, {"schema_version": 1})

    def test_managed_block_update_and_removal_preserve_local_guidance(self):
        before = "# Consumer instructions\n\nKeep local commands here.\n"
        after = "\n## Nested scope\n\nRespect our extra constraints.\n"
        once = projections._apply_issue_authoring(before) + after
        twice = projections._apply_issue_authoring(once)
        self.assertEqual(twice, projections._apply_issue_authoring(twice))
        self.assertIn(before.strip(), twice)
        self.assertIn(after.strip(), twice)
        removed = projections._remove_issue_authoring(twice)
        self.assertEqual(removed, before + after)
        for broken in (once + once, before + projections.ISSUE_AUTHORING_START,
                       projections.ISSUE_AUTHORING_END + projections.ISSUE_AUTHORING_START):
            with self.subTest(broken=broken), self.assertRaises(ValueError):
                projections._apply_issue_authoring(broken)

    def test_module_cannot_silently_drift_from_selection(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "module.md"
            path.write_text(projections.ISSUE_AUTHORING_PATH.read_text().replace('"selection_sha256":"', '"selection_sha256":"bad'))
            with patch.object(projections, "ISSUE_AUTHORING_PATH", path):
                with self.assertRaisesRegex(ValueError, "does not match"):
                    projections._load_issue_authoring()

    def test_discovery_projection_does_not_expand_agent_permissions(self):
        path = ROOT / "library/organization/agents/github-issue-creator/AGENT.md"
        frontmatter, _body = projections._parse_agent("github-issue-creator", path)
        self.assertEqual(frontmatter["tools"], ["read", "search", "web"])
        files = projections._build_files(projections.load_registry())
        for path in ("fixtures/repository-instructions/AGENTS.md", "codex/repository/AGENTS.md",
                     "github/repository/.github/copilot-instructions.md", "claude/repository/CLAUDE.md",
                     "github/repository/.github/agents/github-issue-creator.agent.md"):
            self.assertEqual(files[path].decode().count(projections.ISSUE_AUTHORING_START), 1)
        claude = files["claude/repository/.claude/agents/github-issue-creator.md"].decode()
        metadata = yaml.safe_load(claude.split("---", 2)[1])
        self.assertNotIn("Bash", metadata["tools"])
        self.assertNotIn("Write", metadata["tools"])
        for path, data in files.items():
            if path.endswith(".agent.md") and "github-issue-creator" not in path:
                self.assertNotIn(projections.ISSUE_AUTHORING_START, data.decode())


@unittest.skipUnless(os.environ.get("AETHER_EGOLINT_BINARY"), "set AETHER_EGOLINT_BINARY for real consumer evidence")
class EgolintConsumerTests(unittest.TestCase):
    """Exercise the existing validator, never a second title implementation."""

    def setUp(self):
        self.binary = str(Path(os.environ["AETHER_EGOLINT_BINARY"]).resolve(strict=True))
        self.selection = sources.load_selection()

    def run_egolint(self, *arguments, expected=0):
        result = subprocess.run([self.binary, "issue-title", *arguments], capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        sources.verify_report(self.selection, report)
        return report

    def validate(self, snapshot, expected=0):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issue.json"
            data = json.dumps(snapshot)
            path.write_text(data)
            report = self.run_egolint("validate", "--input", str(path), expected=expected)
            self.assertEqual(path.read_text(), data)
            return report

    def test_fresh_consumer_discovers_portable_skill_and_validates_proposal(self):
        with tempfile.TemporaryDirectory() as directory:
            consumer = Path(directory)
            installed = consumer / ".agents/skills/github-issue-authoring"
            shutil.copytree(ROOT / "dist/skills/github-issue-authoring", installed)
            guidance = projections._repository_guidance_projection("codex-compatible", "AGENTS.md").decode()
            guidance += "\nThis synthetic consumer explicitly selects the issue-title policy in observe mode.\n"
            (consumer / "AGENTS.md").write_text(guidance)
            self.assertIn(".agents/skills/github-issue-authoring/SKILL.md", guidance)
            self.assertIn("references/canonical-issue-titles.md", (installed / "SKILL.md").read_text())
            subject = "[FLO-OBS-01] Checkpoint 2: Export reports"
            proposal = self.run_egolint("format", "--type", "feature", "--reviewed-subject", subject)
            self.assertTrue(proposal["title"].endswith(subject))
            self.assertEqual(proposal, self.run_egolint("format", "--type", "feature", "--reviewed-subject", subject))
            snapshot = {"schema_version": 1, "complete": True, "title": proposal["title"], "labels": [proposal["required_label"]]}
            report = self.validate(snapshot)
            self.assertEqual(report["status"], "conformant")
            (consumer / "report.json").write_text(json.dumps(report))
            checked = subprocess.run(
                [sys.executable, str(installed / "scripts/verify_title_contract.py"), "--report", "report.json"],
                cwd=consumer, capture_output=True, text=True, check=False,
            )
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertEqual(json.loads(checked.stdout)["status"], "verified")

    def test_upstream_cases_without_duplicating_semantics(self):
        cases = json.loads((sources.DEFAULT_SELECTION.parent / "cases.v1.json").read_text())
        for case in cases["cases"]:
            with self.subTest(case=case["id"]):
                expected = case["expected"]
                snapshot = {"schema_version": 1, "complete": True, **case["input"]}
                report = self.validate(snapshot, expected=0 if expected["status"] == "conformant" else 1)
                self.assertEqual(report["status"], expected["status"])
                self.assertEqual(report["type"], expected["type"])
        for migration in cases["migrations"]:
            with self.subTest(migration=migration["id"]):
                primary_type = migration["after"]["labels"][0].removeprefix("type:")
                proposal = self.run_egolint(
                    "format", "--type", primary_type,
                    "--reviewed-subject", migration["reviewed_subject"],
                )
                self.assertEqual(proposal["title"], migration["after"]["title"])
                self.assertIn(proposal["required_label"], migration["after"]["labels"])

    def test_incomplete_provider_evidence_and_changed_labels_do_not_pass(self):
        proposal = self.run_egolint("format", "--type", "feature", "--reviewed-subject", "Preserve IDs")
        snapshot = {"schema_version": 1, "complete": False, "title": proposal["title"], "labels": []}
        self.assertEqual(self.validate(snapshot, expected=2)["status"], "unavailable")
        snapshot.update(complete=True, labels=[proposal["required_label"]])
        self.assertEqual(self.validate(snapshot)["status"], "conformant")
        snapshot["labels"].append("type:bug")
        self.assertEqual(self.validate(snapshot, expected=1)["status"], "conflict")


if __name__ == "__main__":
    unittest.main()
