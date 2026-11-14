"""Tests for the bounded external-source review and allowlist contracts."""

from __future__ import annotations

import copy
from datetime import date, datetime
import importlib.util
import json
from pathlib import Path
import tempfile
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "catalog" / "external" / "validate.py"
SPEC = importlib.util.spec_from_file_location("external_source_validator", VALIDATOR_PATH)
assert SPEC is not None and SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validator)


class ExternalSourceGovernanceTests(unittest.TestCase):
    def test_canonical_external_source_governance_is_valid(self) -> None:
        self.assertEqual(validator.validate(), [])

    def test_allowlist_is_bounded_to_the_reviewed_design_source(self) -> None:
        allowlist = self._load(ROOT / "catalog/external/initial-allowlist.v1.json")
        self.assertEqual(allowlist["default_disposition"], "deny")
        self.assertEqual(len(allowlist["entries"]), 7)
        self.assertEqual(
            {entry["source_id"] for entry in allowlist["entries"]},
            {"external-source/emilkowalski-skill"},
        )
        self.assertTrue(all(entry["requires_human_review"] for entry in allowlist["entries"]))

    def test_rejects_a_digest_that_does_not_match_the_reviewed_record(self) -> None:
        allowlist = self._load(ROOT / "catalog/external/initial-allowlist.v1.json")
        allowlist["entries"][0]["content_hash"]["value"] = "0" * 64
        with tempfile.TemporaryDirectory() as directory:
            candidate_path = Path(directory) / "allowlist.json"
            candidate_path.write_text(json.dumps(allowlist), encoding="utf-8")
            errors = validator.validate(allowlist_path=candidate_path)
        self.assertTrue(any("allowlist digest does not match" in error for error in errors))

    def test_rejects_a_deferred_source_in_the_allowlist(self) -> None:
        allowlist = self._load(ROOT / "catalog/external/initial-allowlist.v1.json")
        approved = self._load(ROOT / "catalog/external/approved-skills.v1.json")
        deferred = next(entry for entry in approved["entries"] if entry["id"] == "external/ab-testing")
        candidate = copy.deepcopy(allowlist["entries"][0])
        candidate.update(
            {
                "artifact_id": deferred["id"],
                "source_id": "external-source/coreyhaines31-marketingskills",
                "upstream_ref": deferred["upstream_ref"],
                "content_hash": deferred["content_hash"],
            }
        )
        allowlist["entries"].append(candidate)
        allowlist["entries"].sort(key=lambda entry: entry["artifact_id"])
        with tempfile.TemporaryDirectory() as directory:
            candidate_path = Path(directory) / "allowlist.json"
            candidate_path.write_text(json.dumps(allowlist), encoding="utf-8")
            errors = validator.validate(allowlist_path=candidate_path)
        self.assertTrue(any("source decision must be allowlisted" in error for error in errors))

    def validate_register(self, register):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "register.json"
            path.write_text(json.dumps(register), encoding="utf-8")
            return validator.validate(register_path=path)

    def test_real_calendar_dates_are_required(self):
        original = self._load(validator.REGISTER_PATH)
        for invalid in ("2026-99-99", "2027-02-29", "2026-04-31", "2026-1-01"):
            with self.subTest(invalid=invalid):
                register = copy.deepcopy(original)
                register["sources"][0]["next_review"]["not_after"] = invalid
                self.assertTrue(any("real ISO calendar date" in error for error in self.validate_register(register)))
        original["reviewed_at"] = "2026-02-30T23:00:00Z"
        self.assertTrue(any("UTC RFC 3339" in error for error in self.validate_register(original)))

    def test_deadlines_and_allowlist_cannot_precede_source_review(self):
        register = self._load(validator.REGISTER_PATH)
        register["sources"][0]["next_review"]["not_after"] = "2026-08-29"
        self.assertTrue(any("next review cannot precede" in error for error in self.validate_register(register)))
        register = self._load(validator.REGISTER_PATH)
        register["reviewed_at"] = "2026-08-31T00:00:00Z"
        self.assertTrue(any("allowlist reviewed_at cannot precede" in error for error in self.validate_register(register)))

    def test_frozen_deadline_boundary_keeps_decision_and_freshness_separate(self):
        register = self._load(validator.REGISTER_PATH)
        for day, expected in ((date(2026, 9, 29), "current"), (date(2026, 9, 30), "current"),
                              (date(2026, 10, 1), "overdue")):
            with self.subTest(day=day):
                rows = validator.assess_freshness(register, day)
                self.assertEqual(rows[0]["decision"], "deferred")
                self.assertEqual(rows[0]["use_boundary"], "deny")
                self.assertEqual(rows[1]["decision"], "allowlisted")
                self.assertEqual(rows[1]["use_boundary"], "agent-assisted-reference-only")
                self.assertEqual(rows[0]["freshness"], expected)
                self.assertEqual(rows[1]["freshness"], expected)
                self.assertIsNone(rows[0]["followup_state"], "Future followups cannot leak into historical assessment")

    def test_missing_dates_or_assessment_before_review_stay_unknown(self):
        register = self._load(validator.REGISTER_PATH)
        self.assertTrue(all(row["freshness"] == "unknown" for row in
                            validator.assess_freshness(register, date(2026, 8, 29))))
        del register["sources"][0]["next_review"]
        self.assertEqual(validator.assess_freshness(register, date(2026, 11, 14))[0]["freshness"], "unknown")

    def test_assessment_is_explicit_deterministic_and_never_mutates_authority(self):
        register = self._load(validator.REGISTER_PATH)
        before = copy.deepcopy(register)
        first = validator.assess_freshness(register, date(2026, 11, 14))
        self.assertEqual(first, validator.assess_freshness(register, date(2026, 11, 14)))
        self.assertEqual(register, before)
        self.assertEqual(sum(row["freshness"] == "overdue" for row in first), 3)
        self.assertEqual([row["followup_state"] for row in first], ["unknown", "blocked", None, "unknown"])
        for invalid in (None, "2026-11-14", datetime(2026, 11, 14)):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                validator.assess_freshness(register, invalid)

    def test_followups_cannot_renew_or_fabricate_a_completed_review(self):
        original = self._load(validator.REGISTER_PATH)
        for field, invalid in (("renews_review", True), ("state", "verified"), ("evidence", []),
                               ("next_action", ""), ("assessed_at", "2026-99-99T00:00:00Z"),
                               ("assessed_at", "2026-01-01T00:00:00Z")):
            with self.subTest(field=field, invalid=invalid):
                register = copy.deepcopy(original)
                register["sources"][0]["followups"][0][field] = invalid
                self.assertTrue(any("followup" in error for error in self.validate_register(register)))

    def test_followups_preserve_all_three_overdue_deadlines_and_restrictions(self):
        register = self._load(validator.REGISTER_PATH)
        overdue = [source for source in register["sources"] if source["next_review"]["not_after"] == "2026-09-30"]
        self.assertEqual(len(overdue), 3)
        self.assertEqual(register["reviewed_at"], "2026-08-30T23:00:00Z")
        for source in overdue:
            self.assertIs(source["followups"][0]["renews_review"], False)
            self.assertTrue(source["constraints"])
            self.assertTrue(source["followups"][0]["next_action"])

    def test_cli_freshness_gate_is_nonzero_and_reports_each_dimension(self):
        result = subprocess.run([sys.executable, str(VALIDATOR_PATH), "--as-of", "2026-11-14", "--format", "json"],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 1)
        report = json.loads(result.stdout)
        self.assertEqual(report["structural_status"], "pass")
        self.assertFalse(report["complete"])
        self.assertEqual(sum(row["freshness"] == "overdue" for row in report["freshness"]), 3)

    def test_cli_structural_check_does_not_claim_freshness(self):
        result = subprocess.run([sys.executable, str(VALIDATOR_PATH), "--format", "json"],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertIsNone(report["assessment_date"])
        self.assertEqual(report["freshness"], [])
        invalid = subprocess.run([sys.executable, str(VALIDATOR_PATH), "--as-of", "2026-99-99"],
                                 capture_output=True, text=True, check=False)
        self.assertEqual(invalid.returncode, 2)

    @staticmethod
    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
