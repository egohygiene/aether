"""Admit authored checkpoint examples and reject unsupported evidence claims."""

from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

from tests.test_audit_package_contract import audit, PACKAGE, ROOT


EXAMPLES = PACKAGE / "references/examples"


class AuditReportContractTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((PACKAGE / "references/audit-profiles.v1.json").read_text())
        self.examples = {path.stem: json.loads(path.read_text()) for path in EXAMPLES.glob("*.json")}
        self.report = deepcopy(self.examples["repository-complete"])

    def rejects(self, value):
        with self.assertRaises(audit.AuditContractError):
            audit.validate_report(value, self.registry)

    def test_all_examples_satisfy_both_schema_and_reference_semantics(self):
        self.assertEqual(len(self.examples), 7)
        for name in ("audit-profile-registry", "repository-audit-report"):
            schema = json.loads((ROOT / f"catalog/schemas/aether.{name}.v1.schema.json").read_text())
            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema, format_checker=FormatChecker())
            values = [self.registry] if name == "audit-profile-registry" else self.examples.values()
            for value in values:
                validator.validate(value)
        for name, value in self.examples.items():
            with self.subTest(name=name):
                self.assertEqual(audit.validate_report(value, self.registry), value)

    def test_canonical_report_hashes_bind_actual_synthetic_markdown(self):
        for name, value in self.examples.items():
            with self.subTest(name=name):
                path = EXAMPLES / Path(value["canonical_report"]["path"]).name
                self.assertIn("fictional contract-fixture", path.read_text())
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), value["canonical_report"]["sha256"])

    def test_stale_capture_is_preserved_as_partial_and_not_current_execution(self):
        value = self.examples["organization-stale-partial"]
        summary = audit.report_summary(value, self.registry)
        self.assertEqual(summary["scope"]["kind"], "organization")
        self.assertEqual(len(summary["scope"]["repositories"]), 2)
        self.assertEqual(summary["completion"]["state"], "partial")
        self.assertLess(value["evidence"][0]["observed_at"], value["started_at"])
        self.assertEqual(value["provenance"]["commands"][0]["state"], "not_run")
        changed = deepcopy(value)
        changed["completion"].update(state="complete", reason=None)
        changed["completion"]["profiles"][0].update(state="complete", reason=None)
        self.rejects(changed)

    def test_missing_provenance_and_missing_observed_source_identity_reject(self):
        for key in ("provenance", "canonical_report"):
            value = deepcopy(self.report)
            del value[key]
            self.rejects(value)
        for key in ("repository", "revision", "observed_at"):
            value = deepcopy(self.report)
            value["evidence"][0][key] = None
            self.rejects(value)

    def test_malformed_and_duplicate_findings_or_dangling_evidence_reject(self):
        for kind in ("duplicate", "invalid-id", "unresolved-reference", "unknown-field"):
            with self.subTest(kind=kind):
                value = deepcopy(self.report)
                if kind == "duplicate":
                    value["findings"].append(deepcopy(value["findings"][0]))
                elif kind == "invalid-id":
                    value["findings"][0]["id"] = "arbitrary-finding"
                elif kind == "unresolved-reference":
                    value["findings"][0]["evidence_refs"] = ["EVIDENCE-999"]
                else:
                    value["findings"][0]["implicitly_resolved"] = True
                self.rejects(value)

    def test_confirmed_finding_requires_observed_evidence(self):
        value = deepcopy(self.report)
        value["evidence"][0]["classification"] = "recommended"
        self.rejects(value)
        value = deepcopy(self.report)
        value["findings"][0]["evidence_refs"] = []
        self.rejects(value)

    def test_policy_conformance_requires_observed_policy_evidence(self):
        value = deepcopy(self.report)
        finding = value["findings"][0]
        finding.update(nature="policy-conformance", source_profile={"id": "contract-drift", "version": "1.0.0"})
        value["profiles"] = audit.resolve_profiles(["contract-drift"], self.registry)
        value["completion"]["profiles"][0]["profile"] = finding["source_profile"]
        self.rejects(value)
        value["evidence"][0]["kind"] = "policy"
        audit.validate_report(value, self.registry)

    def test_experimental_opportunity_cannot_become_a_confirmed_blocking_defect(self):
        for field, replacement in (("severity", "high"), ("status", "confirmed"), ("classification", "confirmed-defect"), ("evidence_classification", "observed")):
            with self.subTest(field=field):
                value = deepcopy(self.examples["experimental"])
                value["findings"][0][field] = replacement
                self.rejects(value)

    def test_declared_profile_versions_and_digest_cannot_drift(self):
        for field in ("registry_sha256", "resolved"):
            value = deepcopy(self.report)
            if field == "registry_sha256":
                value["profiles"][field] = "0" * 64
            else:
                value["profiles"][field][0]["version"] = "99.0.0"
            self.rejects(value)

    def test_blocked_and_not_applicable_are_retained_without_passing_projection(self):
        for name, state in (("blocked", "blocked"), ("not-applicable", "not_applicable"), ("holistic-partial", "partial")):
            summary = audit.report_summary(self.examples[name], self.registry)
            self.assertEqual(summary["completion"]["state"], state)
            self.assertNotIn("passed", summary)
        value = deepcopy(self.report)
        value["completion"]["state"] = "passed"
        self.rejects(value)

    def test_successful_command_requires_actual_observed_command_class_evidence(self):
        value = deepcopy(self.report)
        value["provenance"]["commands"] = [{"command": "synthetic-read-only-check", "state": "success", "exit_code": 0, "evidence_refs": ["EVIDENCE-1"], "reason": None}]
        self.rejects(value)
        value["evidence"][0]["kind"] = "command"
        audit.validate_report(value, self.registry)
        value["evidence"][0]["classification"] = "recommended"
        self.rejects(value)

    def test_unrun_command_cannot_claim_exit_success(self):
        value = deepcopy(self.examples["organization-stale-partial"])
        value["provenance"]["commands"][0]["exit_code"] = 0
        self.rejects(value)

    def test_resolution_requires_bound_prior_and_distinct_current_evidence(self):
        for mutation in ("prior-hash", "prior-uri", "current-revision", "prior-label", "no-current-proof"):
            with self.subTest(mutation=mutation):
                value = deepcopy(self.examples["resolved"])
                if mutation == "prior-hash":
                    value["evidence"][1]["sha256"] = "3" * 64
                elif mutation == "prior-uri":
                    value["evidence"][1]["uri"] = "https://example.org/unrelated.md"
                elif mutation == "current-revision":
                    value["evidence"][0]["revision"] = "c" * 40
                elif mutation == "prior-label":
                    value["prior_audits"][0]["evidence_classification"] = "unverified"
                else:
                    value["findings"][0]["history"]["evidence_refs"] = ["EVIDENCE-2"]
                self.rejects(value)

    def test_disappearance_does_not_create_resolution_or_provider_issue_state(self):
        value = deepcopy(self.examples["blocked"])
        self.assertEqual(audit.report_summary(value, self.registry)["findings"], [])
        self.assertEqual(value["prior_audits"], [])
        value = deepcopy(self.report)
        value["candidate_issues"][0]["status"] = "created"
        self.rejects(value)

    def test_public_roster_refuses_private_members_and_exposes_external_owners_for_admission(self):
        value = deepcopy(self.report)
        value["scope"]["repositories"][0]["visibility"] = "private"
        self.rejects(value)
        with self.assertRaises(audit.AuditContractError):
            audit.referenced_repositories(value)
        value = deepcopy(self.report)
        value["evidence"][0]["uri"] = "https://github.com/another-owner/tool/blob/" + "a" * 40 + "/README.md"
        self.assertEqual(audit.referenced_repositories(value), ["another-owner/tool", "example-org/library"])

    def test_unsafe_uri_and_machine_local_path_reject_without_echoing_supplied_value(self):
        for key, supplied in (("uri", "https://user:synthetic@example.org/evidence"), ("path", "/tmp/private/input.json"), ("uri", "https://example.org/../evidence")):
            with self.subTest(key=key, supplied=supplied):
                value = deepcopy(self.report)
                value["evidence"][0][key] = supplied
                with self.assertRaises(audit.AuditContractError) as failure:
                    audit.validate_report(value, self.registry)
                self.assertNotIn(supplied, str(failure.exception))

    def test_future_observation_and_reversed_run_clock_reject(self):
        value = deepcopy(self.report)
        value["evidence"][0]["observed_at"] = "2026-12-01T00:00:00Z"
        self.rejects(value)
        value = deepcopy(self.report)
        value["completed_at"] = "2026-11-14T00:00:00Z"
        self.rejects(value)

    def test_summary_is_deterministic_typed_metadata_with_no_narrative_or_issue_mutations(self):
        summary = audit.report_summary(self.report, self.registry)
        self.assertEqual(summary, audit.report_summary(audit.parse(audit.canonical_bytes(self.report)), self.registry))
        self.assertEqual(summary["report_sha256"], audit.digest(self.report))
        self.assertNotIn("candidate_issues", summary)
        self.assertNotIn("evidence", summary)
        for key in ("observation", "recommendation", "why_it_matters"):
            self.assertNotIn(key, summary["findings"][0])


if __name__ == "__main__":
    unittest.main()
