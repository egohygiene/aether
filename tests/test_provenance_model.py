"""Tests for the normalized Aether provenance model."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "catalog"))

from provenance_model import (  # noqa: E402
    build_external,
    build_first_party,
    canonical_bytes,
    check,
    validate_catalog,
)


class ProvenanceModelTests(unittest.TestCase):
    def test_repository_provenance_model_is_valid(self) -> None:
        self.assertEqual(check("all"), [])

    def test_schema_uses_absolute_resolvable_identifier(self) -> None:
        schema = json.loads(
            (ROOT / "catalog/schemas/aether.provenance-catalog.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            schema["$id"],
            "https://egohygiene.io/schemas/aether/provenance-catalog/v1.json",
        )

    def test_first_party_includes_agents(self) -> None:
        catalog = build_first_party()
        identifiers = {record["id"] for record in catalog["records"]}
        self.assertIn("agent/architect", identifiers)
        self.assertIn("agent/auditor", identifiers)
        self.assertTrue(any(record["kind"] == "skill" for record in catalog["records"]))
        self.assertTrue(
            any(record["kind"] == "specification" for record in catalog["records"])
        )

    def test_external_entries_preserve_external_trust(self) -> None:
        catalog = build_external()
        self.assertTrue(catalog["records"])
        for record in catalog["records"]:
            self.assertEqual(record["party"], "external")
            self.assertIn(record["trust"], {"trusted", "restricted", "untrusted", "unknown"})
            self.assertNotEqual(record["trust"], "first-party")

    def test_stable_artifact_with_unknown_license_is_rejected(self) -> None:
        catalog = build_first_party()
        record = copy.deepcopy(catalog["records"][0])
        record["lifecycle"] = {"state": "stable"}
        record["license"] = "unknown"
        record["publishable"] = False
        record["blocked_reasons"] = ["license is unresolved"]
        candidate = {"schema_version": catalog["schema_version"], "records": [record]}
        errors = validate_catalog(candidate)
        self.assertTrue(any("stable artifact is blocked" in error for error in errors))

    def test_normalized_output_is_deterministic(self) -> None:
        first = build_first_party()
        second = build_first_party()
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))


if __name__ == "__main__":
    unittest.main()
