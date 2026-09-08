"""Tests for the diagnosis-record metadata and authoring contract."""

from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "catalog" / "schemas" / "aether.diagnosis-record.v1.schema.json"
TEMPLATE_PATH = (
    ROOT
    / "library"
    / "organization"
    / "skills"
    / "quality"
    / "create-diagnosis-record"
    / "templates"
    / "DIAGNOSIS_RECORD.template.md"
)
SKILL_PATH = TEMPLATE_PATH.parents[1] / "SKILL.md"


def valid_record() -> dict:
    return {
        "schema": "aether.diagnosis-record/v1",
        "id": "diag-20260904-symlink-launcher",
        "title": "Symlinked launcher resolves the installation directory",
        "status": "resolved",
        "created": "2026-09-04T17:00:00Z",
        "updated": "2026-09-04T18:00:00Z",
        "authors": ["egohygiene"],
        "scope": ["research-lab launcher"],
        "context": {
            "repository": "example/repository",
            "environment": "local dev container",
            "component": "headroom-lab",
            "artifact_version": "0123456789abcdef",
            "correlation_ids": [],
        },
        "symptom_summary": "The installed launcher searched beside its symlink.",
        "reproduction": {"status": "reproduced"},
        "root_cause": {"status": "confirmed", "hypothesis_id": "H-001"},
        "remediation": {"status": "implemented"},
        "validation": {"status": "partial"},
        "sensitivity": "internal",
        "redactions": "none",
        "related": [],
        "supersedes": [],
        "superseded_by": [],
    }


class DiagnosisRecordContractTests(unittest.TestCase):
    def setUp(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.validator = Draft202012Validator(schema, format_checker=FormatChecker())

    def errors(self, record: dict) -> list:
        return list(self.validator.iter_errors(record))

    def test_schema_accepts_independent_partial_validation(self) -> None:
        self.assertEqual(self.errors(valid_record()), [])

    def test_confirmed_root_cause_requires_hypothesis_id(self) -> None:
        record = deepcopy(valid_record())
        record["root_cause"]["hypothesis_id"] = None
        self.assertTrue(self.errors(record))

    def test_schema_rejects_unknown_state_and_unbounded_extra_fields(self) -> None:
        record = deepcopy(valid_record())
        record["validation"]["status"] = "probably-good"
        record["automatic_publication"] = True
        self.assertGreaterEqual(len(self.errors(record)), 2)

    def test_template_preserves_required_heading_order(self) -> None:
        template = TEMPLATE_PATH.read_text(encoding="utf-8")
        headings = [
            "## 1. Fault Symptom",
            "## 2. Environment and Scope",
            "## 3. Evidence Register",
            "## 4. Investigation Trail",
            "## 5. Hypotheses",
            "## 6. Root Cause",
            "## 7. Remediation",
            "## 8. Validation",
            "## 9. Residual Risk and Unknowns",
            "## 10. Related Artifacts",
        ]
        positions = [template.index(heading) for heading in headings]
        self.assertEqual(positions, sorted(positions))

    def test_skill_preserves_evidence_and_authorization_boundaries(self) -> None:
        skill = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("Do not fabricate a run", skill)
        self.assertIn("not-authorized", skill)
        self.assertIn("coding-agent quality", skill)


if __name__ == "__main__":
    unittest.main()
