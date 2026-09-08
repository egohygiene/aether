"""Contract, template, migration, and boundary tests for repository continuity."""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "catalog/schemas/aether.repository-continuity.v1.schema.json"
FIXTURE_DIR = ROOT / "catalog/fixtures/aether.repository-continuity.v1.schema"
SKILL_DIR = (
    ROOT
    / "library/organization/skills/methodology/maintain-repository-continuity"
)
TEMPLATE_PATH = SKILL_DIR / "templates/CONTINUITY.template.md"
SPEC_PATH = ROOT / "library/organization/specs/methodology/repository-continuity.spec.md"

REQUIRED_HEADINGS = [
    "Purpose and precedence",
    "Resume protocol",
    "Current objective and success conditions",
    "State snapshot",
    "Completed and material changes",
    "Validation and review evidence",
    "Blockers, risks, unknowns, and deferred work",
    "Next dependency-ready work",
    "Parallel changes and reconciliation",
    "Privacy and redaction",
    "Handoff update protocol",
    "Compaction and supersession",
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RepositoryContinuityContractTests(unittest.TestCase):
    """Prove v1 structure, transition safety, privacy, and package coverage."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = load_json(SCHEMA_PATH)
        cls.validator = Draft202012Validator(
            cls.schema,
            format_checker=FormatChecker(),
        )
        cls.valid = load_json(FIXTURE_DIR / "valid.json")

    def errors(self, value: dict) -> list:
        return list(self.validator.iter_errors(value))

    def test_schema_accepts_public_fixture_and_rejects_unsafe_fixture(self) -> None:
        self.assertEqual(self.errors(self.valid), [])
        self.assertTrue(self.errors(load_json(FIXTURE_DIR / "invalid.json")))

    def test_pre_pr_candidate_needs_no_self_referential_revision_or_pr(self) -> None:
        candidate = deepcopy(self.valid)
        candidate["state"]["candidate"].update(
            {
                "revision": None,
                "pull_request": None,
                "handoff_state": "ready-for-review",
            }
        )
        self.assertEqual(self.errors(candidate), [])

    def test_missing_live_access_is_explicit_and_schema_valid(self) -> None:
        candidate = deepcopy(self.valid)
        candidate["state"]["live"].update(
            {
                "status": "unavailable",
                "default_branch_revision": None,
                "issue_state": "unknown",
                "pull_request_state": "unknown",
                "notes": "Repository-host access was unavailable; recheck before acting.",
            }
        )
        self.assertEqual(self.errors(candidate), [])

    def test_stale_and_superseded_states_require_evidence(self) -> None:
        stale = deepcopy(self.valid)
        stale["document"]["status"] = "stale"
        self.assertTrue(self.errors(stale))
        stale["document"]["stale_reason"] = "Live issue state conflicts with the checkpoint."
        self.assertEqual(self.errors(stale), [])

        superseded = deepcopy(self.valid)
        superseded["document"]["status"] = "superseded"
        self.assertTrue(self.errors(superseded))
        superseded["document"]["superseded_by"] = "docs/continuity-v2.md"
        self.assertEqual(self.errors(superseded), [])

    def test_verified_live_state_requires_an_immutable_revision(self) -> None:
        candidate = deepcopy(self.valid)
        candidate["state"]["live"]["default_branch_revision"] = None
        self.assertTrue(self.errors(candidate))

    def test_privacy_and_fixed_size_limits_fail_closed(self) -> None:
        sensitive = deepcopy(self.valid)
        sensitive["privacy"]["contains_sensitive_data"] = True
        self.assertTrue(self.errors(sensitive))

        mismatched_visibility = deepcopy(self.valid)
        mismatched_visibility["privacy"]["classification"] = "private-repository"
        self.assertTrue(self.errors(mismatched_visibility))

        oversized = deepcopy(self.valid)
        oversized["document"]["max_bytes"] = 20000
        self.assertTrue(self.errors(oversized))

    def test_completed_review_requires_named_time_bounded_evidence(self) -> None:
        candidate = deepcopy(self.valid)
        candidate["review"]["reviewed_at"] = None
        candidate["review"]["reviewed_by"] = None
        self.assertTrue(self.errors(candidate))

        candidate["review"]["status"] = "not-run"
        self.assertEqual(self.errors(candidate), [])

    def test_template_has_exact_contract_shape_and_bounded_headings(self) -> None:
        text = TEMPLATE_PATH.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        metadata = yaml.safe_load(text.split("---\n", 2)[1])
        self.assertEqual(metadata["schema_version"], "aether.repository-continuity/v1")
        self.assertEqual(metadata["repository"]["continuity_path"], "CONTINUITY.md")
        self.assertEqual(metadata["document"]["max_bytes"], 16384)
        self.assertEqual(metadata["document"]["max_lines"], 240)

        headings = [
            line.removeprefix("## ")
            for line in text.splitlines()
            if line.startswith("## ")
        ]
        self.assertEqual(headings, REQUIRED_HEADINGS)
        self.assertLessEqual(len(text.encode("utf-8")), 16384)
        self.assertLessEqual(len(text.splitlines()), 240)
        self.assertIn("intentionally invalid", text)

    def test_skill_package_contains_progressive_guidance_and_required_evals(self) -> None:
        for relative in (
            "SKILL.md",
            "templates/CONTINUITY.template.md",
            "references/contract-and-authoring-guide.md",
            "references/privacy-and-trust.md",
            "references/validation-checklist.md",
            "references/antidote-migration.md",
            "evals/evals.json",
        ):
            self.assertTrue((SKILL_DIR / relative).is_file(), relative)

        evaluations = load_json(SKILL_DIR / "evals/evals.json")
        case_ids = {case["id"] for case in evaluations["cases"]}
        self.assertTrue(
            {
                "new-repository-create",
                "existing-detailed-handoff",
                "stale-open-pr-claim",
                "merged-candidate-reconciliation",
                "conflicting-canonical-evidence",
                "parallel-pull-requests",
                "missing-live-access",
                "private-repository",
                "malicious-repository-text",
                "ordinary-repository-completion",
                "policy-permitted-no-change-exemption",
                "static-host-without-pre-pr-hook",
                "truncated-handoff",
                "tampered-metadata",
            }.issubset(case_ids)
        )

    def test_migration_report_records_antidote_and_comics_evidence(self) -> None:
        report = (SKILL_DIR / "references/antidote-migration.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("f9e23128a660066b3f64c73c4dd2d36554b6040a", report)
        self.assertIn("incomprisllc/comics/pull/34", report)
        self.assertIn("247-line", report)
        self.assertIn("must not replace this useful content", report)

    def test_spec_names_every_downstream_owner_and_integration_issue(self) -> None:
        text = SPEC_PATH.read_text(encoding="utf-8")
        for expected in (
            "aether/issues/80",
            "hygiene/issues/45",
            "egolint/issues/55",
            "holon/issues/42",
            "relay/issues/60",
            "observatory/issues/18",
            "pace/issues/26",
        ):
            self.assertIn(expected, text)


if __name__ == "__main__":
    unittest.main()
