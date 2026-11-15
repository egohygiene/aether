"""Authored architecture scenarios preserve uncertainty and the human boundary."""

from copy import deepcopy
import json
import unittest

from jsonschema import Draft202012Validator, FormatChecker

from tests.test_coherence_package_contract import (
    AS_OF,
    PACKAGE,
    PUBLIC_REPOSITORIES,
    ROOT,
    coherence,
)


class CoherenceReviewExampleTests(unittest.TestCase):
    def setUp(self):
        self.examples = {p.stem: json.loads(p.read_text()) for p in (PACKAGE / "references/examples").glob("*.json")}

    def evaluate(self, value, **options):
        return coherence.evaluate_review(value, as_of=AS_OF, public_repositories=PUBLIC_REPOSITORIES, change_inventory="complete", **options)

    def test_all_six_scenarios_are_schema_and_semantically_valid(self):
        self.assertEqual(set(self.examples), {"coherent", "over-engineered", "contradictory", "incomplete", "stale", "insufficient-evidence"})
        schema = json.loads((ROOT / "catalog/schemas/aether.architecture-coherence-review.v1.schema.json").read_text())
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for name, review in self.examples.items():
            with self.subTest(name=name):
                validator.validate(review)
                self.assertEqual(coherence.loads_review(json.dumps(review), public_repositories=PUBLIC_REPOSITORIES), review)
                self.assertIsNone(self.evaluate(review)["governance"]["human_disposition"])

    def test_coherent_recommendation_is_not_certification_or_human_ratification(self):
        review = self.examples["coherent"]
        self.assertEqual({row["status"] for row in review["dimensions"]}, {"coherent"})
        result = self.evaluate(review)
        self.assertEqual(result["reviewer_recommendation"], "ratify")
        self.assertEqual(result["governance"]["state"], "not-reviewed")
        self.assertEqual(result["governance"]["human_evidence"], "absent")

    def test_over_engineering_and_contradiction_retain_evidence_and_real_counterarguments(self):
        for name, category in (("over-engineered", "risky"), ("contradictory", "wrong")):
            with self.subTest(name=name):
                review = self.examples[name]
                self.assertEqual(review["concerns"][0]["category"], category)
                self.assertEqual(self.evaluate(review)["reviewer_recommendation"], "revise")
                self.assertTrue(review["concerns"][0]["evidence"])
                self.assertTrue(review["alternatives"][0]["tradeoffs"])
                altered = deepcopy(review)
                altered["concerns"][0]["alternative_ids"] = []
                with self.assertRaisesRegex(coherence.ContractError, "^CONCERN_ALTERNATIVES$"):
                    coherence.validate_review(altered)

    def test_incomplete_or_insufficient_evidence_cannot_recommend_completion(self):
        for name, execution in (("incomplete", "partial"), ("insufficient-evidence", "blocked")):
            with self.subTest(name=name):
                review = self.examples[name]
                result = self.evaluate(review)
                self.assertEqual(result["execution"], execution)
                self.assertEqual(result["reviewer_recommendation"], "defer")
                self.assertIsNone(review["execution"]["completed_at"])
                altered = deepcopy(review)
                altered["recommendation"]["disposition"] = "ratify"
                with self.assertRaisesRegex(coherence.ContractError, "^INCOMPLETE_RECOMMENDATION$"):
                    coherence.validate_review(altered)
        concern = self.examples["insufficient-evidence"]["concerns"][0]
        self.assertEqual((concern["category"], concern["confidence"], concern["evidence"]), ("unverified", "unknown", []))

    def test_expired_supplied_claim_stays_stale_and_unauthenticated(self):
        review = self.examples["stale"]
        result = self.evaluate(review)
        self.assertEqual(result["governance"]["freshness"], "stale")
        self.assertEqual(result["governance"]["claimed_human_disposition"], "ratified")
        self.assertEqual(result["governance"]["human_evidence"], "unverified")
        self.assertIsNone(result["governance"]["human_disposition"])
        self.assertNotIn(result["governance"]["state"], {"ratified", "ratified-with-notes"})

    def test_routine_revision_difference_does_not_invent_material_change_or_trust(self):
        review = deepcopy(self.examples["stale"])
        review["governance"]["valid_until"] = None
        current = deepcopy(review["represented_revisions"])
        current[0]["revision"] = "b" * 40
        result = self.evaluate(review, current_revisions=current)
        self.assertEqual(result["governance"]["freshness"], "current")
        self.assertEqual(result["governance"]["revision_match"], "different")
        self.assertEqual(result["governance"]["material_change_ids"], [])
        self.assertEqual(result["governance"]["human_evidence"], "unverified")
        self.assertIsNone(result["governance"]["human_disposition"])


if __name__ == "__main__":
    unittest.main()
