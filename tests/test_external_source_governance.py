"""Tests for the bounded external-source review and allowlist contracts."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import tempfile
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

    @staticmethod
    def _load(path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
