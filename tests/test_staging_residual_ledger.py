"""Exercise inventory completeness and the absence of removal authority."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

from catalog import staging_ledger as ledger


class StagingResidualLedgerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q")
        self.write(".staging/instructions/example.md", "Retained synthetic instruction.\n")
        self.write(".staging/hooks/example/support.txt", "Supporting evidence.\n")
        self.commit()

    def git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.PIPE).decode().strip()

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def commit(self):
        self.git("add", ".")
        self.git("-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        return self.git("rev-parse", "HEAD")

    def test_same_immutable_input_is_identical_and_complete(self):
        first = ledger.build(self.root, "HEAD")
        self.assertEqual(first, ledger.build(self.root, first["source"]["revision"]))
        self.assertEqual(first["totals"]["files"], 2)
        members = [path for unit in first["units"] for path in unit["members"]]
        self.assertCountEqual(members, [row["path"] for row in first["files"]])
        self.assertEqual(ledger.validate(first, self.root), [])

    def test_missing_duplicate_dangling_or_cross_unit_members_fail(self):
        original = ledger.build(self.root, "HEAD")
        for kind in ("missing", "duplicate", "dangling", "cross-unit", "digest", "totals"):
            with self.subTest(kind=kind):
                data = copy.deepcopy(original)
                if kind == "missing":
                    data["files"].pop()
                elif kind == "duplicate":
                    data["files"].append(copy.deepcopy(data["files"][0]))
                elif kind == "dangling":
                    data["units"][0]["members"].append(".staging/hooks/unknown/support.txt")
                elif kind == "cross-unit":
                    data["units"][0]["members"] = data["units"][1]["members"]
                elif kind == "digest":
                    data["files"][0]["sha256"] = "0" * 64
                else:
                    data["totals"]["bytes"] += 1
                self.assertTrue(ledger.validate(data, self.root))

    def test_current_nested_supporting_file_addition_requires_reconciliation(self):
        old = ledger.build(self.root, "HEAD")
        self.write(".staging/hooks/example/nested/new-support.txt", "New retained bytes.\n")
        revision = self.commit()
        self.assertTrue(any("current tracked staging" in error for error in ledger.validate(old, self.root)))
        current = ledger.build(self.root, revision)
        self.assertEqual(current["totals"]["files"], 3)
        self.assertEqual(ledger.validate(current, self.root), [])

    def test_shallow_checkout_cannot_invent_the_recorded_source_history(self):
        data = ledger.build(self.root, "HEAD")
        self.write("README.md", "Unrelated synthetic change.\n")
        self.commit()
        with tempfile.TemporaryDirectory() as temporary:
            shallow = Path(temporary) / "consumer"
            subprocess.run(["git", "clone", "--quiet", "--depth", "1", self.root.as_uri(), str(shallow)],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertTrue(ledger.validate(data, shallow))
            subprocess.run(["git", "-C", str(shallow), "fetch", "--quiet", "--unshallow"],
                           check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(ledger.validate(data, shallow), [])
        workflow = (ledger.ROOT / ".github/workflows/pr-validation.yml").read_text()
        self.assertIn("fetch-depth: 0", workflow)

    def test_symlink_is_indexed_as_git_bytes_without_following_its_target(self):
        target = "../../synthetic-outside.txt"
        (self.root / ".staging/instructions/alias").symlink_to(target)
        self.write("synthetic-outside.txt", "Never read through the alias.\n")
        self.commit()
        data = ledger.build(self.root, "HEAD")
        row = next(row for row in data["files"] if row["path"].endswith("/alias"))
        self.assertEqual(row["mode"], "120000")
        self.assertEqual(row["sha256"], hashlib.sha256(target.encode()).hexdigest())
        self.assertEqual(ledger.validate(data, self.root), [])

    def test_canonical_agent_delta_records_tools_and_drift_without_equivalence(self):
        staged = ".staging/agents/example.agent.md"
        canonical = "library/organization/agents/example/AGENT.md"
        self.write(staged, "---\ntools: [read, edit]\n---\nStaged role.\n")
        self.write(canonical, "---\ntools: [read, search]\nmetadata:\n  aether-skills: [maintain-repository-continuity]\n  aether-specs: [repository-continuity]\n---\nCanonical role.\n")
        self.write(ledger.AGENT_LEDGER, json.dumps({"covered": {"example": {"staged-path": staged, "canonical-path": canonical}}, "move-out": {}}))
        self.commit()
        data = ledger.build(self.root, "HEAD")
        unit = next(unit for unit in data["units"] if unit["bucket"] == "agents")
        self.assertEqual(unit["canonical_comparison"]["staged_tools"], ["read", "edit"])
        self.assertEqual(unit["canonical_comparison"]["canonical_tools"], ["read", "search"])
        self.assertEqual(unit["receipt_state"], "local-source-only")
        self.assertFalse(unit["removal_authority"])
        self.write(canonical, "---\ntools: [read]\n---\nChanged canonical role.\n")
        self.commit()
        self.assertTrue(any("current owner/disposition" in error for error in ledger.validate(data, self.root)))

    def test_historical_absence_is_distinct_from_retained_disposition(self):
        inventory = {"entries": [
            {"staging_path": ".staging/skills/old/SKILL.md", "current_staging_state": "removed", "classification": "first-party candidate"},
            {"staging_path": ".staging/skills/retained/SKILL.md", "current_staging_state": "present", "classification": "unknown provenance"},
        ]}
        self.write(ledger.SKILL_INVENTORY, json.dumps(inventory))
        self.write(".staging/skills/retained/SKILL.md", "Retained evidence.\n")
        self.write(ledger.DISPOSITIONS + "/retained.json", json.dumps({"staging_path": ".staging/skills/retained/SKILL.md", "disposition": "preserve-migration-evidence"}))
        self.commit()
        data = ledger.build(self.root, "HEAD")
        self.assertEqual(data["totals"]["current_skill_roots"], 1)
        self.assertEqual(data["totals"]["historical_removed_skill_roots"], 1)
        self.assertEqual(data["historical_removed_skills"][0]["state"], "historical-absent")
        self.assertEqual(ledger.validate(data, self.root), [])

    def test_inventory_and_local_destination_never_grant_removal_authority(self):
        data = ledger.build(self.root, "HEAD")
        data["units"][0]["removal_authority"] = True
        self.assertTrue(ledger.validate(data, self.root))
        with self.assertRaises(ValueError):
            ledger.GitSource(self.root, "--help")

    def test_current_canonical_ledger_covers_all_buckets_and_nine_agent_deltas(self):
        data = json.loads((ledger.ROOT / ledger.LEDGER).read_text())
        self.assertEqual(ledger.validate(data, ledger.ROOT), [])
        self.assertEqual(data["totals"]["files"], 734)
        self.assertEqual(data["totals"]["current_skill_roots"], 186)
        self.assertEqual(data["totals"]["historical_removed_skill_roots"], 6)
        self.assertEqual(set(data["totals"]["by_bucket"]), ledger.BUCKETS)
        self.assertEqual(sum("canonical_comparison" in unit for unit in data["units"]), 9)
        self.assertEqual(sum(unit["disposition"] == "retained-transfer-pending" for unit in data["units"]), 4)


if __name__ == "__main__":
    unittest.main()
