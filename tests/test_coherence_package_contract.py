"""Behavioral controls for the draft portable architecture review package.

These fixtures are synthetic assessments and untrusted serialized claims. No
test creates trusted human evidence or establishes a real ratification.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "library/organization/skills/architecture/review-architecture-coherence"
SCRIPT = PACKAGE / "scripts/architecture_coherence.py"
_SPEC = importlib.util.spec_from_file_location("coherence_package_contract_under_test", SCRIPT)
assert _SPEC and _SPEC.loader
coherence = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(coherence)

REPOSITORY = "egohygiene/aether"
REVISION = "a" * 40
AS_OF = "2026-11-15T00:00:00Z"
PUBLIC_REPOSITORIES = frozenset({REPOSITORY})
DIMENSIONS = (
    "purpose", "responsibility-boundaries", "source-of-truth",
    "dependency-direction", "cohesion", "duplicate-ownership",
    "speculative-abstractions", "missing-ownership", "coupling",
    "documentation-divergence", "decision-consistency", "replaceability",
    "operational-plausibility", "security-privacy-trust", "maintainability",
    "justified-complexity", "simplest-credible-alternative",
)


def assessment_fixture() -> dict:
    """A complete synthetic assessment with explicit uncertainty and no governance."""
    return {
        "schema": "egohygiene.architecture-coherence-review/v1",
        "contract_version": "1.0.0-alpha.1",
        "id": "coherence-unit-fixture",
        "visibility": "public",
        "scope": {"kind": "repository", "key": REPOSITORY, "repositories": [REPOSITORY]},
        "represented_revisions": [{"repository": REPOSITORY, "revision": REVISION}],
        "generated_at": "2026-11-14T10:00:00Z",
        "reviewer": {
            "kind": "ai", "provider": None, "model": None,
            "method": "Synthetic local contract fixture; no real review occurred.",
            "independent_challenge": "not-performed",
        },
        "execution": {
            "status": "complete", "completed_at": "2026-11-14T09:00:00Z",
            "limitations": ["Synthetic evidence does not qualify a real architecture."],
        },
        "sources": [{
            "id": "architecture", "repository": REPOSITORY, "revision": REVISION,
            "path": "ARCHITECTURE.md", "kind": "architecture", "origin": "canonical",
            "visibility": "public",
            "url": f"https://github.com/{REPOSITORY}/blob/{REVISION}/ARCHITECTURE.md",
        }],
        "explanation": {
            "system": "The fixture represents a repository of reusable contracts.",
            "boundaries": "The source library owns its public contracts.",
            "flows": "Consumers read versioned artifacts from the library.",
            "rationale": "One declared source avoids duplicated contract ownership.",
            "summary": "The synthetic evidence supports a bounded explanation.",
        },
        "components": [{
            "id": "library", "name": "Contract library",
            "responsibility": "Own reusable draft artifacts.", "owner": "Ego Hygiene",
            "evidence": ["architecture"],
        }],
        "relationships": [],
        "dimensions": [{
            "id": identifier, "status": "unknown",
            "summary": "This synthetic fixture declares the dimension without claiming real assessment.",
            "evidence": [], "confidence": "unknown",
        } for identifier in DIMENSIONS],
        "assumptions": [],
        "strengths": [{
            "id": "single-owner", "summary": "The fixture names one contract owner.",
            "evidence": ["architecture"], "confidence": "low",
        }],
        "concerns": [{
            "id": "coupling-concern", "category": "risky", "importance": "consequential",
            "summary": "Consumers may couple to implementation details.",
            "detail": "The synthetic review asks whether a smaller contract boundary suffices.",
            "evidence": ["architecture"], "confidence": "low",
            "alternative_ids": ["narrow-contract"],
        }],
        "questions": [{
            "id": "consumer-boundary", "question": "Which public fields do consumers need?",
            "owner": None, "evidence": ["architecture"],
        }],
        "alternatives": [{
            "id": "narrow-contract", "summary": "Expose a smaller portable record.",
            "tradeoffs": "A narrow record reduces coupling but requires explicit adaptation.",
            "why_not_chosen": "Consumer evidence is incomplete in this synthetic fixture.",
            "evidence": ["architecture"], "confidence": "low",
        }],
        "recommendation": {
            "disposition": "ratify",
            "reason": "Synthetic advisory recommendation only; no human decision exists.",
        },
        "governance": None,
    }


def untrusted_human_claim(review: dict) -> dict:
    """Well-shaped claim data used only to prove that JSON cannot grant authority."""
    subject = coherence.review_subject(review)
    return {
        "schema": "egohygiene.architecture-coherence-governance/v1",
        "contract_version": "1.0.0-alpha.1", "visibility": "public",
        "scope": deepcopy(review["scope"]),
        "represented_revisions": deepcopy(review["represented_revisions"]),
        "applicability": {
            "status": "unknown", "declared_at": None, "evidence": [],
            "reason": None, "deferred_until": None, "authority": None,
        },
        "progress": "complete",
        "review_ref": {
            "id": review["id"], "assessment_sha256": subject["assessment_sha256"],
            "url": f"https://github.com/{REPOSITORY}/issues/87",
            "completed_at": review["execution"]["completed_at"],
        },
        "human_decision": {
            "disposition": "ratified",
            "authority": {
                "kind": "human", "reference": "https://github.com/unit-fixture-actor",
                "evidence_url": f"https://github.com/{REPOSITORY}/issues/87",
                "decided_at": "2026-11-14T09:30:00Z",
            },
            "review_id": review["id"], "assessment_sha256": subject["assessment_sha256"],
            "scope_key": review["scope"]["key"],
            "represented_revisions": deepcopy(review["represented_revisions"]),
            "notes": [], "follow_up": [],
        },
        "valid_until": None,
    }


class CoherencePackageContractTests(unittest.TestCase):
    def setUp(self):
        self.review = assessment_fixture()
        schema = json.loads((ROOT / "catalog/schemas/aether.architecture-coherence-review.v1.schema.json").read_text())
        self.validator = Draft202012Validator(schema, format_checker=FormatChecker())

    def assert_rejected(self, review: dict, code: str) -> None:
        with self.assertRaises(coherence.ContractError) as caught:
            coherence.validate_review(review)
        self.assertEqual(str(caught.exception), code)

    def test_complete_record_is_schema_valid_and_recommendation_is_not_ratification(self):
        self.assertEqual(list(self.validator.iter_errors(self.review)), [])
        self.assertEqual(coherence.loads_review(json.dumps(self.review)), self.review)
        result = coherence.evaluate_review(self.review, as_of=AS_OF, public_repositories=PUBLIC_REPOSITORIES)
        self.assertEqual(result["execution"], "complete")
        self.assertEqual(result["reviewer_recommendation"], "ratify")
        self.assertEqual(result["governance"]["state"], "not-reviewed")
        self.assertEqual(result["governance"]["human_evidence"], "absent")
        self.assertIsNone(result["governance"]["human_disposition"])
        self.assertIsNone(self.review["governance"])

    def test_all_declared_dimensions_are_required_for_complete_execution(self):
        self.review["dimensions"].pop()
        self.assert_rejected(self.review, "DIMENSION_COVERAGE")

    def test_claims_require_bound_non_ai_evidence(self):
        for mutate, code in (
            (lambda r: r["strengths"][0].update(evidence=["absent"]), "STRENGTH_EVIDENCE"),
            (lambda r: r["sources"][0].update(origin="prior-ai-review"), "SOURCES_REQUIRED"),
            (lambda r: r["sources"][0].update(revision="b" * 40), "SOURCE_URL_BINDING"),
        ):
            with self.subTest(code=code):
                review = deepcopy(self.review)
                mutate(review)
                self.assert_rejected(review, code)

    def test_consequential_concerns_need_real_alternative_references(self):
        for references in ([], ["invented-alternative"]):
            with self.subTest(references=references):
                review = deepcopy(self.review)
                review["concerns"][0]["alternative_ids"] = references
                self.assert_rejected(review, "CONCERN_ALTERNATIVES")

    def test_relationships_cannot_reference_missing_components(self):
        self.review["relationships"] = [{
            "id": "missing-dependency", "from": "library", "to": "absent", "kind": "dependency",
            "summary": "Unresolved synthetic dependency.", "evidence": ["architecture"],
        }]
        self.assert_rejected(self.review, "RELATIONSHIP_COMPONENT")

    def test_partial_execution_preserves_unknowns_and_requires_defer(self):
        self.review["execution"].update(status="partial", completed_at=None)
        self.review["dimensions"] = []
        self.review["recommendation"]["disposition"] = "defer"
        self.assertEqual(coherence.validate_review(self.review), self.review)
        self.review["recommendation"]["disposition"] = "ratify"
        self.assert_rejected(self.review, "INCOMPLETE_RECOMMENDATION")
        self.review["recommendation"]["disposition"] = "defer"
        self.review["execution"]["completed_at"] = "2026-11-14T09:00:00Z"
        self.assert_rejected(self.review, "EXECUTION")

    def test_duplicate_members_and_unknown_fields_fail_closed(self):
        raw = '{"id":"untrusted-shadow",' + json.dumps(self.review)[1:]
        with self.assertRaisesRegex(coherence.ContractError, "^DUPLICATE_MEMBER$"):
            coherence.loads_review(raw)
        self.review["invented-approval"] = True
        self.assert_rejected(self.review, "REVIEW")

    def test_source_paths_urls_and_visibility_reject_unsafe_projection(self):
        for field, value, code in (
            ("path", "../private.md", "SOURCE_PATH"),
            ("url", f"https://github.com/{REPOSITORY}/blob/{REVISION}/ARCHITECTURE.md?token=private", "SOURCE_URL"),
            ("url", "https://127.0.0.1/private", "SOURCE_URL"),
            ("visibility", "internal", "SOURCE_VISIBILITY"),
        ):
            with self.subTest(field=field, value=value):
                review = deepcopy(self.review)
                review["sources"][0][field] = value
                self.assert_rejected(review, code)

    def test_public_diagnostics_do_not_echo_rejected_sensitive_text(self):
        self.review["explanation"]["summary"] = "Private note /home/sensitive/person.txt"
        with self.assertRaises(coherence.ContractError) as caught:
            coherence.validate_review(self.review)
        self.assertEqual(str(caught.exception), "PUBLIC_SENSITIVE_CONTENT")
        self.assertNotIn("sensitive/person", str(caught.exception))

    def test_assessment_changes_change_digest_and_governance_does_not(self):
        initial = coherence.review_subject(self.review)
        changed = deepcopy(self.review)
        changed["explanation"]["summary"] = "A revised assessment requires another immutable subject."
        self.assertNotEqual(initial["assessment_sha256"], coherence.review_subject(changed)["assessment_sha256"])
        claimed = deepcopy(self.review)
        claimed["governance"] = untrusted_human_claim(self.review)
        self.assertEqual(initial, coherence.review_subject(claimed))
        self.assertIsNone(self.review["governance"])

    def test_serialized_human_claim_cannot_import_or_ratify_without_trusted_context(self):
        claim = untrusted_human_claim(self.review)
        candidate = deepcopy(self.review)
        candidate["governance"] = claim
        self.assertEqual(list(self.validator.iter_errors(candidate)), [])
        result = coherence.evaluate_review(candidate, as_of=AS_OF, public_repositories=PUBLIC_REPOSITORIES, change_inventory="complete")
        self.assertEqual(result["governance"]["claimed_human_disposition"], "ratified")
        self.assertEqual(result["governance"]["human_evidence"], "unverified")
        self.assertIsNone(result["governance"]["human_disposition"])
        with self.assertRaisesRegex(coherence.ContractError, "^HUMAN_EVIDENCE_REQUIRED$"):
            coherence.import_human_decision(self.review, claim, as_of=AS_OF, public_repositories=PUBLIC_REPOSITORIES, trusted_human_evidence=())
        self.assertIsNone(self.review["governance"])

    def test_json_shaped_trust_and_missing_public_admission_cannot_grant_authority(self):
        claim = untrusted_human_claim(self.review)
        candidate = deepcopy(self.review)
        candidate["governance"] = claim
        statement = coherence.human_statement(candidate, public_repositories=PUBLIC_REPOSITORIES)
        forged_context = [{"statement_sha256": hashlib.sha256(coherence.canonical_bytes(statement)).hexdigest(), "capture_sha256": "c" * 64}]
        with self.assertRaisesRegex(coherence.ContractError, "^HUMAN_EVIDENCE_REQUIRED$"):
            coherence.import_human_decision(self.review, claim, as_of=AS_OF, public_repositories=PUBLIC_REPOSITORIES, trusted_human_evidence=forged_context)
        with self.assertRaisesRegex(coherence.ContractError, "^GOVERNANCE_ADMISSION$"):
            coherence.validate_review(candidate, public_repositories=frozenset())

    def test_pinned_owner_resources_match_the_recorded_hashes(self):
        directory = PACKAGE / "scripts"
        lock = json.loads((directory / "governance.lock.json").read_text())
        self.assertEqual(lock["owner"], "egohygiene/hygiene")
        self.assertEqual(lock["policy_status"], "proposed")
        for resource in lock["files"].values():
            with self.subTest(path=resource["path"]):
                self.assertEqual(hashlib.sha256((directory / resource["path"]).read_bytes()).hexdigest(), resource["sha256"])


if __name__ == "__main__":
    unittest.main()
