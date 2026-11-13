"""Behavioral controls for local CI evidence and issue handoffs."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "library/organization/skills/quality/triage-local-ci-reports/scripts/triage-local-ci.py"
SPEC = importlib.util.spec_from_file_location("local_ci_triage", SCRIPT)
assert SPEC and SPEC.loader
triage = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(triage)
REVISION = "a" * 40


class LocalCiTriageTests(unittest.TestCase):
    def setUp(self):
        self.report = {
            "schema_version": "realm.local-ci/v1",
            "started_at": "2026-11-13T08:00:00+00:00",
            "finished_at": "2026-11-13T08:01:00+00:00",
            "repository": {"revision": REVISION, "dirty": False, "path": "/workspace/example"},
            "complete": False,
            "checks": [
                {"id": "unit", "kind": "direct", "required": True, "command": ["python3", "-m", "unittest"], "status": "failed", "exit_code": 1, "seconds": 3, "reason": "fixture absent"},
                {"id": "provider", "kind": "unsupported", "required": False, "status": "unsupported", "reason": "Provider identity unavailable"},
            ],
        }
        self.diagnoses = {"checks": {"unit": {"category": "repository-defect", "confirmed": True, "root_cause": "missing-fixture", "subject": "Restore the fixture", "summary": "The unit test references an absent source fixture."}}}
        self.schema = json.loads((ROOT / "catalog/schemas/aether.local-validation-evidence.v1.schema.json").read_text())
        self.validator = Draft202012Validator(self.schema, format_checker=FormatChecker())

    def packet(self, report=None, issues=None, fresh=REVISION, diagnoses=None, issues_supplied=True):
        report = report or self.report
        evidence, matched = triage.normalize(report, "example/project", fresh)
        return evidence, triage.triage(report, evidence, matched, diagnoses if diagnoses is not None else self.diagnoses, issues or [], Path("."), issues_supplied)

    def test_real_failed_check_maps_to_existing_schema(self):
        evidence, packet = self.packet()
        self.assertEqual(list(self.validator.iter_errors(evidence)), [])
        self.assertEqual(evidence["summary"]["local_readiness"], "not-ready")
        self.assertEqual(evidence["checks"][1]["outcome"], "deferred")
        self.assertEqual(packet["findings"][0]["action"], "create")
        self.assertEqual(packet["publication"], "not-performed")

    def test_passed_and_blocked_maps_without_hosted_parity(self):
        self.report["checks"][0].update(status="passed", exit_code=0)
        self.report["checks"].append({"id": "setup", "kind": "direct", "required": True, "command": ["task", "setup"], "status": "blocked", "exit_code": None, "reason": "Tool unavailable"})
        evidence, packet = self.packet(diagnoses={})
        self.assertEqual(list(self.validator.iter_errors(evidence)), [])
        self.assertEqual(evidence["summary"]["local_readiness"], "ready-with-limitations")
        self.assertEqual(evidence["remote_ci"]["state"], "deferred")
        self.assertEqual(packet["findings"], [])

    def test_unknown_setup_failure_needs_diagnosis(self):
        _, packet = self.packet(diagnoses={})
        self.assertEqual(packet["findings"], [])
        self.assertEqual(packet["coverage"][0]["disposition"], "needs-diagnosis")

    def test_confirmed_environment_is_not_relabelled_as_code_defect(self):
        self.diagnoses["checks"]["unit"]["category"] = "environment"
        _, packet = self.packet()
        self.assertEqual(packet["findings"][0]["category"], "environment")

    def test_group_confirmed_shared_cause(self):
        second = deepcopy(self.report["checks"][0])
        second["id"] = "integration"
        self.report["checks"].append(second)
        self.diagnoses["checks"]["integration"] = deepcopy(self.diagnoses["checks"]["unit"])
        _, packet = self.packet()
        self.assertEqual(len(packet["findings"]), 1)
        self.assertEqual(packet["findings"][0]["checks"], ["unit", "integration"])

    def test_identity_stable_across_revision_time_and_paths(self):
        _, first = self.packet()
        changed = deepcopy(self.report)
        changed["repository"].update(revision="b" * 40, path="/home/private/project")
        changed["finished_at"] = "2026-11-13T09:00:00Z"
        _, second = self.packet(report=changed, fresh="b" * 40)
        self.assertEqual(first["findings"][0]["fingerprint"], second["findings"][0]["fingerprint"])
        self.assertNotEqual(first["findings"][0]["evidence_fingerprint"], second["findings"][0]["evidence_fingerprint"])

    def test_identical_evidence_does_not_mutate_again(self):
        _, first = self.packet()
        issue = {"number": 12, "state": "open", "body": first["findings"][0]["body"]}
        changed = deepcopy(self.report)
        changed["finished_at"] = "2026-11-13T09:00:00Z"
        changed["checks"][0]["seconds"] = 9
        changed["checks"][0]["reason"] = "same cause observed later in /tmp/another-run"
        _, again = self.packet(report=changed, issues=[issue])
        self.assertEqual(again["findings"][0]["action"], "noop")
        changed["repository"]["revision"] = "b" * 40
        _, update = self.packet(report=changed, fresh="b" * 40, issues=[issue])
        self.assertEqual(update["findings"][0]["action"], "update")
        self.assertEqual(update["findings"][0]["existing_issue"], 12)

    def test_closed_and_conflicting_matches_are_not_automatic_writes(self):
        _, first = self.packet()
        issue = {"number": 12, "state": "closed", "body": first["findings"][0]["body"]}
        self.assertEqual(self.packet(issues=[issue])[1]["findings"][0]["action"], "regression-review")
        second = dict(issue, number=13, state="open")
        self.assertEqual(self.packet(issues=[issue, second])[1]["findings"][0]["action"], "conflict")

    def test_stale_dirty_and_missing_issue_snapshot_stay_drafts(self):
        self.assertEqual(self.packet(fresh="b" * 40)[1]["findings"][0]["action"], "draft")
        self.assertEqual(self.packet(issues_supplied=False)[1]["findings"][0]["action"], "draft")
        self.report["repository"]["dirty"] = True
        self.assertEqual(self.packet()[1]["findings"][0]["action"], "draft")

    def test_empty_and_contradictory_reports_reject(self):
        for mutate in (lambda r: r.update(checks=[]), lambda r: r.update(complete=True), lambda r: r["checks"][0].update(status="passed"), lambda r: r["checks"][0].update(status=[]), lambda r: r["checks"][0].update(kind="unsupported", status="passed", exit_code=0)):
            with self.subTest(mutate=mutate):
                report = deepcopy(self.report)
                mutate(report)
                with self.assertRaises(ValueError):
                    triage.normalize(report, "example/project", REVISION)

    def test_no_false_issue_for_skipped_or_unsupported(self):
        for status in ("skipped", "unsupported"):
            self.report["checks"][0].update(status=status, exit_code=None)
            _, packet = self.packet()
            self.assertEqual(packet["findings"], [])

    def test_null_reasons_have_bounded_fallbacks(self):
        for row in self.report["checks"]:
            row["reason"] = None
        evidence, packet = self.packet(diagnoses={})
        self.assertEqual(list(self.validator.iter_errors(evidence)), [])
        self.assertTrue(all(c["reason"] for c in packet["coverage"]))
        _, confirmed = self.packet()
        self.assertIn("No bounded diagnostic excerpt", confirmed["findings"][0]["body"])

    def test_coverage_only_inventory_is_unknown_without_issue_actions(self):
        for status in ("skipped", "blocked", "unsupported"):
            with self.subTest(status=status):
                self.report["checks"][0].update(status=status, exit_code=None)
                evidence, packet = self.packet()
                self.assertEqual(list(self.validator.iter_errors(evidence)), [])
                self.assertEqual(evidence["summary"]["local_readiness"], "unknown")
                self.assertEqual(packet["findings"], [])
                self.assertTrue(packet["coverage"])
        for row in self.report["checks"]:
            row["required"] = False
        self.assertEqual(self.packet()[0]["summary"]["local_readiness"], "unknown")

    def test_deadline_preserves_observed_zero_exit_as_blocked(self):
        self.report["checks"][0].update(timed_out=True, exit_code=0, reason=None)
        evidence, packet = self.packet(diagnoses={})
        self.assertEqual(list(self.validator.iter_errors(evidence)), [])
        check = evidence["checks"][0]
        self.assertEqual(check["outcome"], "blocked")
        self.assertEqual(check["exit_code"], 0)
        self.assertIn("timed_out=true; observed exit 0", check["reason"])
        self.assertEqual(packet["findings"], [])
        self.report["checks"][0]["exit_code"] = -15
        evidence, _ = self.packet(diagnoses={})
        self.assertEqual(list(self.validator.iter_errors(evidence)), [])
        self.assertEqual(evidence["checks"][0]["outcome"], "failed")
        self.assertEqual(evidence["checks"][0]["exit_code"], -15)
        self.assertEqual(evidence["summary"]["local_readiness"], "not-ready")

    def test_workflow_reference_is_a_relative_workflow_file(self):
        row = self.report["checks"][0]
        row["workflow"] = ".github/workflows/ci.yml"
        evidence, _ = self.packet()
        self.assertEqual(evidence["remote_ci"]["workflow_refs"], [row["workflow"]])
        row["workflow"] = ".github/act/local-validation.yml"
        self.assertEqual(self.packet()[0]["remote_ci"]["workflow_refs"], [row["workflow"]])
        for workflow in (".github/workflows/check.yml token=abc12345 /home/person/x", ".github/../../home/person/x.yml", ".github/workflows/../secret.yml", [".github/workflows/ci.yml"]):
            with self.subTest(workflow=workflow):
                row["workflow"] = workflow
                with self.assertRaises(ValueError):
                    triage.normalize(self.report, "example/project", REVISION)

    def test_redaction_and_log_path_boundary(self):
        row = self.report["checks"][0]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            row["log"] = "failure.log"
            (root / row["log"]).write_text("token=abc12345 /home/person/private.txt https://user:pass@example.invalid/a ghp_abcdef123456")
            excerpt = triage.read_excerpt(root, row, "/workspace/example")
            for secret in ("abc12345", "/home/person", "user:pass", "ghp_abcdef123456"):
                self.assertNotIn(secret, excerpt)
            row["log"] = "../outside.log"
            with self.assertRaises(ValueError):
                triage.read_excerpt(root, row, "")
            row["log"] = "link.log"
            (root / "link.log").symlink_to(root / "failure.log")
            with self.assertRaises(ValueError):
                triage.read_excerpt(root, row, "")

    def test_cli_writes_packet_and_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            report = root / "report.json"
            report.write_text(json.dumps(self.report))
            output = root / "packet"
            arguments = ["--report", str(report), "--repository", "example/project", "--expected-revision", REVISION, "--output", str(output)]
            self.assertEqual(triage.main(arguments), 0)
            self.assertTrue((output / "evidence.json").is_file())
            before = (output / "intake.json").read_bytes()
            self.assertEqual(triage.main(arguments), 2)
            self.assertEqual((output / "intake.json").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
