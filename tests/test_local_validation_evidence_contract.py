"""Contract tests for adaptive local-validation evidence."""

from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = (
    ROOT / "catalog" / "schemas" / "aether.local-validation-evidence.v1.schema.json"
)
FIXTURE_ROOT = (
    ROOT
    / "catalog"
    / "fixtures"
    / "aether.local-validation-evidence.v1.schema"
)
SKILL_ROOT = (
    ROOT
    / "library"
    / "organization"
    / "skills"
    / "quality"
    / "validate-repository-locally"
)


class LocalValidationEvidenceContractTests(unittest.TestCase):
    def setUp(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.validator = Draft202012Validator(schema, format_checker=FormatChecker())
        self.valid = json.loads(
            (FIXTURE_ROOT / "valid.json").read_text(encoding="utf-8")
        )

    def errors(self, report: dict) -> list:
        return list(self.validator.iter_errors(report))

    def test_constrained_environment_fixture_is_valid(self) -> None:
        self.assertEqual(self.errors(self.valid), [])

    def test_unavailable_check_cannot_be_reported_as_passed(self) -> None:
        report = deepcopy(self.valid)
        check = report["checks"][0]
        check["availability"] = "unavailable"
        check["selection"] = "not-selected"
        self.assertTrue(self.errors(report))

    def test_failed_check_requires_a_nonzero_exit(self) -> None:
        report = deepcopy(self.valid)
        check = report["checks"][0]
        check["outcome"] = "failed"
        self.assertTrue(self.errors(report))

    def test_remote_pass_requires_observed_run_evidence(self) -> None:
        report = deepcopy(self.valid)
        report["remote_ci"]["state"] = "passed"
        self.assertTrue(self.errors(report))

    def test_ready_requires_every_applicable_required_check_to_pass(self) -> None:
        report = deepcopy(self.valid)
        report["checks"][2]["requirement"] = "required"
        report["summary"]["local_readiness"] = "ready"
        self.assertTrue(self.errors(report))

    def test_required_failure_forces_not_ready(self) -> None:
        report = deepcopy(self.valid)
        check = report["checks"][0]
        check["outcome"] = "failed"
        check["exit_code"] = 1
        report["summary"]["local_readiness"] = "ready-with-limitations"
        self.assertTrue(self.errors(report))

    def test_published_invalid_fixture_is_rejected(self) -> None:
        invalid = json.loads(
            (FIXTURE_ROOT / "invalid.json").read_text(encoding="utf-8")
        )
        self.assertTrue(self.errors(invalid))

    def test_skill_preserves_runtime_and_ci_boundaries(self) -> None:
        skill = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        adapters = (SKILL_ROOT / "references" / "execution-adapters.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("aether-continuity-disposition: reader-writer", skill)
        self.assertIn("Do not trigger remote Actions", skill)
        self.assertIn("Docker Engine API", adapters)
        self.assertIn("--platform", adapters)
        self.assertIn("never an automatic fallback", adapters)


if __name__ == "__main__":
    unittest.main()
