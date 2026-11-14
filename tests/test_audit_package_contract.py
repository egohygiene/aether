"""Bounded executable controls for the existing draft audit package."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "library/organization/skills/quality/audit-repository"
SPEC = importlib.util.spec_from_file_location("audit_package_contract", PACKAGE / "scripts/audit_contract.py")
assert SPEC and SPEC.loader
audit = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(audit)


def frontmatter(path):
    return yaml.safe_load(path.read_text().split("---", 2)[1])


class AuditPackageContractTests(unittest.TestCase):
    def setUp(self):
        self.registry = json.loads((PACKAGE / "references/audit-profiles.v1.json").read_text())

    def test_package_identity_resources_and_draft_are_consistent(self):
        source = frontmatter(PACKAGE / "SKILL.md")
        suite = json.loads((PACKAGE / "evals/evals.json").read_text())
        self.assertEqual(source["metadata"]["aether-version"], "1.2.0")
        self.assertEqual(suite["version"], source["metadata"]["aether-version"])
        self.assertEqual(suite["skill"], source["name"])
        self.assertEqual(source["metadata"]["aether-status"], "draft")
        self.assertEqual(source["metadata"]["aether-executable-resources"], ["scripts/audit_contract.py"])
        self.assertEqual(self.registry["status"], "draft")

    def test_read_only_agent_and_approved_policy_remain_distinct(self):
        agent = frontmatter(ROOT / "library/organization/agents/auditor/AGENT.md")
        self.assertNotIn("edit", agent["tools"])
        self.assertNotIn("execute", agent["tools"])
        policy = frontmatter(ROOT / "library/organization/specs/quality/auditor.spec.md")
        self.assertEqual((policy["status"], str(policy["version"])), ("approved", "2.0.0"))

    def test_single_profile_preserves_exact_registry_identity(self):
        resolved = audit.resolve_profiles(["contract-drift"], self.registry)
        self.assertEqual(resolved["resolved"], [{"id": "contract-drift", "version": "1.0.0"}])
        self.assertEqual(resolved["requested"], resolved["resolved"])
        self.assertEqual(resolved["registry_sha256"], audit.digest(self.registry))

    def test_holistic_excludes_experiments_until_explicit_selection(self):
        holistic = audit.resolve_profiles(["holistic"], self.registry)
        self.assertEqual({x["id"] for x in holistic["resolved"]}, {"contract-drift", "feature-opportunity", "implementation-quality"})
        selected = audit.resolve_profiles(["holistic", "experimental-opportunity"], self.registry)
        self.assertIn({"id": "experimental-opportunity", "version": "1.0.0"}, selected["resolved"])

    def test_overlapping_composition_deduplicates_and_is_order_independent(self):
        first = audit.resolve_profiles(["holistic", "contract-drift"], self.registry)
        second = audit.resolve_profiles(["contract-drift", "holistic"], self.registry)
        self.assertEqual(first, second)
        self.assertEqual(len(first["resolved"]), 3)
        with self.assertRaises(audit.AuditContractError):
            audit.resolve_profiles(["contract-drift", "contract-drift"], self.registry)

    def test_unknown_profile_and_wrong_version_reject(self):
        for requested in (["unknown-profile"], [{"id": "contract-drift", "version": "9.9.9"}]):
            with self.subTest(requested=requested), self.assertRaises(audit.AuditContractError):
                audit.resolve_profiles(requested, self.registry)

    def test_cycles_and_implicit_experimental_composition_reject(self):
        for child in ("holistic", "experimental-opportunity"):
            registry = deepcopy(self.registry)
            holistic = next(x for x in registry["profiles"] if x["id"] == "holistic")
            holistic["includes"].append({"id": child, "version": "1.0.0"})
            with self.subTest(child=child), self.assertRaises(audit.AuditContractError):
                audit.validate_registry(registry)

    def test_completion_retains_unknown_blocked_and_not_applicable(self):
        for states, expected in ((["unknown"], "unknown"), (["blocked"], "blocked"), (["not_applicable"], "not_applicable"), (["complete", "not_applicable"], "complete"), (["complete", "blocked"], "partial"), (["failed", "complete"], "failed")):
            with self.subTest(states=states):
                self.assertEqual(audit.completion_state([{"state": state} for state in states]), expected)
        with self.assertRaises(audit.AuditContractError):
            audit.completion_state([{"state": "passed"}])

    def test_duplicate_members_and_nonfinite_json_reject_without_echoing_input(self):
        for raw in ('{"secret":"synthetic-value","secret":"second"}', '{"value":NaN}', '[]'):
            with self.subTest(raw=raw), self.assertRaises(audit.AuditContractError) as failure:
                audit.parse(raw)
            self.assertNotIn("synthetic-value", str(failure.exception))

    def test_canonical_digest_ignores_object_key_order(self):
        self.assertEqual(audit.digest({"a": 1, "b": 2}), audit.digest({"b": 2, "a": 1}))
        self.assertEqual(audit.parse(audit.canonical_bytes(self.registry)), self.registry)


if __name__ == "__main__":
    unittest.main()
