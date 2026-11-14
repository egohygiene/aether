"""Tests for the normalized Aether provenance model."""

from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "catalog"))

from provenance_model import (  # noqa: E402
    _agent_records,
    _first_party_record,
    build_external,
    build_first_party,
    canonical_bytes,
    check,
    validate_catalog,
)


class ProvenanceModelTests(unittest.TestCase):
    def test_agent_source_overrides_stale_catalog_capability_and_maturity(self) -> None:
        catalog = {"agents": {"auditor": {"tools": ["read", "execute"], "version": "9.9.9", "status": "stable"}}}
        source = {"aether-id": "auditor", "tools": ["read"], "metadata": {"aether-version": "1.2.0", "aether-status": "draft", "aether-owners": "egohygiene"}}
        with mock.patch("provenance_model.load_json", return_value=catalog), mock.patch("provenance_model.parse_frontmatter", return_value=source):
            record = _agent_records()[0]
        self.assertEqual(record["source"]["revision"], "1.2.0")
        self.assertEqual(record["lifecycle"], {"state": "draft"})
        self.assertEqual(record["compatibility"]["required_tools"], ["read"])
        self.assertFalse(record["publishable"])

    def test_missing_agent_source_metadata_cannot_inherit_catalog_maturity(self) -> None:
        catalog = {"agents": {"auditor": {"tools": ["read", "execute"], "version": "9.9.9", "status": "stable"}}}
        for metadata in ({}, {"aether-version": "1.0.0"}, {"aether-version": "invalid", "aether-status": "stable"}):
            with self.subTest(metadata=metadata), mock.patch("provenance_model.load_json", return_value=catalog), mock.patch("provenance_model.parse_frontmatter", return_value={"aether-id": "auditor", "tools": ["read"], "metadata": metadata}):
                with self.assertRaisesRegex(ValueError, "agent auditor source must declare"):
                    _agent_records()

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

    def test_first_party_normalization_retains_approved_source_state(self) -> None:
        catalog = json.loads((ROOT / "catalog/first-party/catalog.v1.json").read_text(encoding="utf-8"))
        artifact = copy.deepcopy(next(item for item in catalog["artifacts"] if item["id"] == "specification/auditor"))
        artifact["lifecycle"] = {"state": "stable", "source_state": "approved"}
        record = _first_party_record(artifact)
        self.assertEqual(record["lifecycle"], {"state": "stable", "source_state": "approved"})


if __name__ == "__main__":
    unittest.main()
