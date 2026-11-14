"""Prove fail-closed source/receipt binding using synthetic Git and provider data."""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from catalog import staging_guard as guard


class StagingGuardTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.run_git("init", "-q")
        self.staged = ".staging/skills/example/SKILL.md"
        self.canonical = "library/organization/skills/example/SKILL.md"
        self.specification = "library/organization/specs/example.spec.md"
        self.write(self.staged, b"Synthetic retained prototype.\n")
        self.write(self.canonical, b"Synthetic canonical replacement.\n")
        self.write(self.specification, b"Synthetic review specification.\n")
        self.write_json(guard.INTAKES, {"schema_version": "aether.staging-intakes/v1", "records": []})
        self.write_json(guard.APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": []})
        self.write_json(guard.POLICY, {"schema_version": "aether.staging-guard-policy/v1", "repository": guard.REPOSITORY,
                                       "approvers": [{"id": 10001, "login": "fixture-maintainer"}], "adr": "ADR-0005"})
        self.write_json(guard.LEDGER, {"files": [{"path": self.staged, "sha256": self.hash(self.staged)}]})
        self.initial = self.commit()

    def run_git(self, *args):
        return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.PIPE).decode().strip()

    def write(self, path, content):
        selected = self.root / path
        selected.parent.mkdir(parents=True, exist_ok=True)
        selected.write_bytes(content)

    def write_json(self, path, content):
        self.write(path, (json.dumps(content, indent=2) + "\n").encode())

    def hash(self, path):
        return hashlib.sha256((self.root / path).read_bytes()).hexdigest()

    def commit(self):
        self.run_git("add", ".")
        self.run_git("-c", "user.name=Synthetic Fixture", "-c", "user.email=fixture@example.invalid",
                     "-c", "commit.gpgsign=false", "commit", "-qm", "fixture")
        return self.run_git("rev-parse", "HEAD")

    def plan(self):
        mode, blob = guard.tree(self.root, self.initial, self.staged)[self.staged]
        return {"id": "STG-synthetic", "source": {"revision": self.initial, "path": self.staged, "mode": mode, "blob": blob},
                "specification": self.specification, "disposition": {"kind": "canonical", "revision": self.initial,
                "path": self.canonical, "sha256": self.hash(self.canonical)}, "attestation": None}

    def admit(self, row=None):
        self.row = row or self.plan()
        self.write_json(guard.APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": [self.row]})
        reviewed = self.commit()
        self.assertEqual(guard.check_diff(self.root, self.initial, reviewed)["changed_paths"], [])
        self.row["attestation"] = {"pull_request": 1, "comment_id": 7, "review_commit": reviewed}
        self.write_json(guard.APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": [self.row]})
        self.base = self.commit()
        # Preparing the plan, attaching the provider reference, and removing the
        # source must each pass the real gate as separate changes.
        self.assertEqual(guard.check_diff(self.root, reviewed, self.base)["changed_paths"], [])
        (self.root / self.staged).unlink()
        self.head = self.commit()
        self.comment = {"user": {"type": "User", "id": 10001, "login": "fixture-maintainer"},
                        "issue_url": "https://api.github.com/repos/" + guard.REPOSITORY + "/issues/1",
                        "body": "AETHER-STAGING-APPROVE STG-synthetic sha256:" + guard.payload_digest(self.row) + " source:" + reviewed}

    def provider(self, suffix):
        if suffix == "pulls/2":
            return {"head": {"sha": self.head}, "base": {"sha": self.base, "repo": {"full_name": guard.REPOSITORY}}, "body": "Refs ADR-0005"}
        if suffix == "issues/comments/7":
            return self.comment
        raise AssertionError("Unexpected synthetic provider endpoint: " + suffix)

    def test_unrelated_change_needs_no_evacuations_or_provider(self):
        self.write("README.md", b"An unrelated change.\n")
        head = self.commit()
        def denied(_):
            self.fail("Unrelated changes must not request provider approval")
        self.assertEqual(guard.check_diff(self.root, self.initial, head, provider=denied)["changed_paths"], [])
        self.assertEqual(guard.check_worktree(self.root), [])

    def test_nested_untracked_supporting_intake_is_rejected_then_recorded(self):
        added = ".staging/skills/example/nested/support.txt"
        self.write(added, b"New synthetic supporting bytes.\n")
        self.assertTrue(any(added in item for item in guard.check_worktree(self.root)))
        intake = {"id": "INT-synthetic", "path": added, "sha256": self.hash(added), "owner": "fixture curator",
                  "classification": "unknown-provenance", "reason": "Retain for review", "authority": "quarantine-only"}
        self.write_json(guard.INTAKES, {"schema_version": "aether.staging-intakes/v1", "records": [intake]})
        self.assertEqual(guard.check_worktree(self.root), [])
        head = self.commit()
        self.assertEqual(guard.check_diff(self.root, self.initial, head)["changed_paths"], [added])
        intake["sha256"] = "0" * 64
        self.write_json(guard.INTAKES, {"schema_version": "aether.staging-intakes/v1", "records": [intake]})
        with self.assertRaisesRegex(ValueError, "exact intake"):
            guard.check_diff(self.root, self.initial, self.commit())

    def test_missing_approval_and_same_head_fabrication_fail_before_provider(self):
        row = self.plan()
        row["attestation"] = {"pull_request": 1, "comment_id": 7, "review_commit": self.initial}
        self.write_json(guard.APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": [row]})
        (self.root / self.staged).unlink()
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "base-admitted exact preimage"):
            guard.check_diff(self.root, self.initial, head)

    def test_exact_base_admitted_synthetic_removal_and_account_attestation_pass(self):
        self.admit()
        result = guard.check_diff(self.root, self.base, self.head, 2, self.provider)
        self.assertEqual(result["verified_attestations"], ["STG-synthetic"])
        self.assertEqual(result["changed_paths"], [self.staged])
        self.comment["user"]["login"] = "renamed-synthetic-maintainer"
        self.assertEqual(guard.check_diff(self.root, self.base, self.head, 2, self.provider)["verified_attestations"], ["STG-synthetic"])

    def test_attestation_completion_cannot_change_payload_or_authorize_same_diff(self):
        row = self.plan()
        self.write_json(guard.APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": [row]})
        reviewed = self.commit()
        row["attestation"] = {"pull_request": 1, "comment_id": 7, "review_commit": reviewed}
        self.write_json(guard.APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": [row]})
        (self.root / self.staged).unlink()
        with self.assertRaisesRegex(ValueError, "base-admitted exact preimage"):
            guard.check_diff(self.root, reviewed, self.commit())
        self.write(self.staged, b"Synthetic retained prototype.\n")
        row["specification"] = "out-of-scope: altered review scope"
        self.write_json(guard.APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": [row]})
        with self.assertRaisesRegex(ValueError, "immutable"):
            guard.check_diff(self.root, reviewed, self.commit())

    def test_forged_bot_wrong_account_conversation_or_digest_attestations_fail(self):
        self.admit()
        original = copy.deepcopy(self.comment)
        for mutation in ("bot", "account", "conversation", "digest", "quoted"):
            with self.subTest(mutation=mutation):
                self.comment = copy.deepcopy(original)
                if mutation == "bot": self.comment["user"]["type"] = "Bot"
                elif mutation == "account": self.comment["user"]["id"] = 10002
                elif mutation == "conversation": self.comment["issue_url"] += "9"
                elif mutation == "quoted": self.comment["body"] = "Not approved; example only:\n```\n" + original["body"] + "\n```"
                else: self.comment["body"] = "AETHER-STAGING-APPROVE STG-synthetic sha256:" + "0" * 64
                with self.assertRaises(ValueError):
                    guard.check_diff(self.root, self.base, self.head, 2, self.provider)

    def test_changed_preimage_and_rename_cannot_reuse_an_old_approval(self):
        self.admit()
        self.run_git("checkout", "-q", self.base)
        self.write(self.staged, b"A different current preimage.\n")
        base = self.commit()
        destination = self.root / ".staging/skills/example/renamed.md"
        (self.root / self.staged).rename(destination)
        head = self.commit()
        with self.assertRaisesRegex(ValueError, "base-admitted exact preimage"):
            guard.check_diff(self.root, base, head)

    def test_changed_or_symlink_destination_and_removed_evidence_fail(self):
        for mutation in ("bytes", "symlink", "approval"):
            with self.subTest(mutation=mutation):
                if not hasattr(self, "row"):
                    self.admit()
                self.run_git("checkout", "-q", self.head)
                if mutation == "bytes": self.write(self.canonical, b"Replacement changed after review.\n")
                elif mutation == "symlink":
                    (self.root / self.canonical).unlink()
                    (self.root / self.canonical).symlink_to("../../unrelated")
                else: self.write_json(guard.APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": []})
                head = self.commit()
                previous = self.head
                self.head = head
                with self.assertRaises(ValueError):
                    guard.check_diff(self.root, self.base, head, 2, self.provider)
                self.head = previous

    def test_actual_pr_source_and_adr_reference_are_required(self):
        self.admit()
        for mutation in ("base", "head", "repository", "adr"):
            with self.subTest(mutation=mutation):
                def provider(suffix):
                    data = copy.deepcopy(self.provider(suffix))
                    if suffix.startswith("pulls/"):
                        if mutation in {"base", "head"}: data[mutation]["sha"] = "0" * 40
                        elif mutation == "repository": data["base"]["repo"]["full_name"] = "example/other"
                        else: data["body"] = "Unrelated request"
                    return data
                with self.assertRaises(ValueError): guard.check_diff(self.root, self.base, self.head, 2, provider)

    def test_retained_flat_and_plural_hook_records_keep_their_own_shapes(self):
        records = list((guard.ROOT / guard.DISPOSITIONS).glob("*.json"))
        self.assertEqual(len(records), 16)
        for record in records: guard.disposition_record(json.loads(record.read_text()))
        hook = json.loads((guard.ROOT / guard.DISPOSITIONS / "hooks-github-copilot-integration.json").read_text())
        self.assertIn("staging_paths", hook)
        hook["reviewed_date"] = "2026-02-30"
        with self.assertRaises(ValueError): guard.disposition_record(hook)

    def test_intake_is_not_a_rights_or_removal_grant_and_json_is_unambiguous(self):
        row = {"id": "INT-synthetic", "path": self.staged, "sha256": self.hash(self.staged), "owner": "fixture",
               "classification": "unknown-provenance", "reason": "retain", "authority": "human-approved-removal"}
        with self.assertRaises(ValueError): guard.intake_records({"schema_version": "aether.staging-intakes/v1", "records": [row]})
        with self.assertRaises(ValueError): guard.document(b'{"records":[],"records":[]}')
        with self.assertRaises(ValueError): guard.path(".staging/../outside", staged=True)
        self.assertEqual(guard.check_worktree(guard.ROOT), [])

    def test_extracted_base_controller_runs_while_proposed_controller_is_poisoned(self):
        controller = "catalog/staging_guard.py"
        self.write(controller, Path(guard.__file__).read_bytes())
        base = self.commit()
        self.write(controller, b'raise SystemExit("untrusted proposed controller executed")\n')
        head = self.commit()
        with tempfile.TemporaryDirectory() as temporary:
            trusted = Path(temporary) / "base-controller.py"
            trusted.write_bytes(guard.blob(self.root, base, controller))
            command = [sys.executable, str(trusted), "diff", "--repository-root", str(self.root),
                       "--base", base, "--head", head, "--controller-revision", base]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["controller_revision"], base)
            trusted.write_bytes(trusted.read_bytes() + b"\n# changed controller bytes\n")
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, 1)
            self.assertIn("immutable base", json.loads(result.stdout)["errors"][0])

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX special-file admission control")
    def test_special_files_and_control_aliases_fail_without_blocking_or_following(self):
        fifo = self.root / ".staging/skills/example/fifo"
        os.mkfifo(fifo)
        result = subprocess.run([sys.executable, guard.__file__, "intake", "--repository-root", str(self.root)],
                                capture_output=True, text=True, timeout=3, check=False)
        self.assertEqual(result.returncode, 1)
        fifo.unlink()
        original = self.root / guard.INTAKES
        original.unlink()
        original.symlink_to(self.root / guard.POLICY)
        self.assertTrue(guard.check_worktree(self.root))


if __name__ == "__main__":
    unittest.main()
