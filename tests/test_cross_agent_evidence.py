"""Contract, lifecycle, and adversarial tests for cross-agent public evidence."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "catalog" / "evidence-packets"
FIXTURES = CONTRACT / "fixtures"
SCRIPT = CONTRACT / "validate.py"


def load_module():
    spec = importlib.util.spec_from_file_location("evidence_packet_validator", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


validator = load_module()


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def set_pointer(data: dict, pointer: str, value) -> None:
    target = data
    parts = pointer.lstrip("/").split("/")
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    final = parts[-1]
    if isinstance(target, list):
        target[int(final)] = value
    else:
        target[final] = value


def redigest_packet(packet: dict) -> None:
    packet["integrity"]["envelope_digest"]["value"] = validator.canonical_envelope_digest(
        packet, "packet"
    )


class CrossAgentEvidenceTests(unittest.TestCase):
    """Prove public-only, exact-evidence, and least-authority boundaries."""

    def test_all_three_schemas_accept_their_synthetic_examples(self) -> None:
        cases = (
            ("aether.cross-agent-evidence-packet.v1.schema.json", "legal-source-packet.json"),
            ("aether.cross-agent-evidence-packet.v1.schema.json", "software-research-packet.json"),
            ("aether.sanitized-research-request.v1.schema.json", "sanitized-request.json"),
            ("aether.evidence-projection.v1.schema.json", "filesystem-projection.json"),
        )
        for schema_name, fixture_name in cases:
            with self.subTest(fixture=fixture_name):
                schema = json.loads(
                    (ROOT / "catalog" / "schemas" / schema_name).read_text(encoding="utf-8")
                )
                errors = list(
                    Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(
                        load(fixture_name)
                    )
                )
                self.assertEqual(errors, [])

    def test_legal_and_software_packets_validate_with_exact_local_spans(self) -> None:
        for name in ("legal-source-packet.json", "software-research-packet.json"):
            with self.subTest(packet=name):
                self.assertEqual(
                    validator.validate_packet(load(name), FIXTURES),
                    [],
                )

    def test_sanitized_request_is_separate_and_double_review_bound(self) -> None:
        request = load("sanitized-request.json")
        self.assertEqual(validator.validate_request(request), [])
        request["payload"]["public_queries"][0] = "a confidentially derived query"
        request["integrity"]["envelope_digest"]["value"] = validator.canonical_envelope_digest(
            request, "request"
        )
        errors = validator.validate_request(request)
        self.assertTrue(any("not bound to the exact public request" in error for error in errors))

    def test_every_projection_kind_preserves_the_packet_authority_ceiling(self) -> None:
        packet = load("legal-source-packet.json")
        for kind in ("provider", "mcp", "a2a", "filesystem", "queue"):
            with self.subTest(kind=kind):
                projection = load("filesystem-projection.json")
                projection["projection"]["adapter_kind"] = kind
                self.assertEqual(validator.validate_projection(projection, packet), [])

        projection = load("filesystem-projection.json")
        projection["authority"]["required_session_capabilities"].append("credential-access")
        errors = validator.validate_projection(projection, packet)
        self.assertTrue(any("may not broaden" in error for error in errors))

    def test_adversarial_fixture_cases_fail_closed_for_the_named_reason(self) -> None:
        fixture = load("adversarial-cases.json")
        for case in fixture["cases"]:
            with self.subTest(case=case["id"]):
                packet = load(fixture["base_packet"])
                set_pointer(packet, case["pointer"], case["value"])
                redigest_packet(packet)
                errors = validator.validate_packet(packet, FIXTURES)
                self.assertTrue(
                    any(case["expected_error"] in error for error in errors),
                    errors,
                )

    def test_exact_span_and_source_references_are_verified(self) -> None:
        packet = load("legal-source-packet.json")
        excerpt = packet["payload"]["evidence"]["sources"][0]["excerpts"][0]
        excerpt["end_byte"] -= 1
        redigest_packet(packet)
        errors = validator.validate_packet(packet, FIXTURES)
        self.assertTrue(any("exact-span digest mismatch" in error for error in errors))

        packet = load("legal-source-packet.json")
        packet["payload"]["findings"]["items"][0]["evidence_refs"] = ["source/missing"]
        redigest_packet(packet)
        errors = validator.validate_packet(packet, FIXTURES)
        self.assertTrue(any("unknown evidence" in error for error in errors))

    def test_lifecycle_states_require_explicit_failure_information(self) -> None:
        packet = load("legal-source-packet.json")
        packet["payload"]["lifecycle"]["state"] = "superseded"
        redigest_packet(packet)
        errors = validator.validate_packet(packet, FIXTURES)
        self.assertTrue(any("must name its replacement" in error for error in errors))

        packet = load("legal-source-packet.json")
        packet["payload"]["lifecycle"]["state"] = "revoked"
        redigest_packet(packet)
        errors = validator.validate_packet(packet, FIXTURES)
        self.assertTrue(any("revocation evidence" in error for error in errors))

        packet = load("legal-source-packet.json")
        packet["payload"]["lifecycle"]["state"] = "incompatible"
        redigest_packet(packet)
        errors = validator.validate_packet(packet, FIXTURES)
        self.assertTrue(any("name the incompatibility" in error for error in errors))

    def test_import_requires_explicit_attachment_root_and_never_fetches(self) -> None:
        errors = validator.validate_packet(load("legal-source-packet.json"), None)
        self.assertTrue(any("explicit attachment root" in error for error in errors))

        packet = load("legal-source-packet.json")
        attachment = packet["payload"]["evidence"]["attachments"][0]
        attachment.update(
            {
                "kind": "immutable-reference",
                "path": None,
                "url": "https://example.invalid/immutable/legal-source.txt",
            }
        )
        redigest_packet(packet)
        self.assertEqual(validator.validate_packet(packet, None), [])

    def test_admission_fails_closed_without_policy_and_capability_context(self) -> None:
        packet = load("legal-source-packet.json")
        errors = validator.admit_packet(packet, FIXTURES, None, set(), set())
        self.assertTrue(any("explicit destination" in error for error in errors))
        self.assertTrue(any("policy admission is missing" in error for error in errors))
        self.assertTrue(any("session capabilities are missing" in error for error in errors))

        self.assertEqual(
            validator.admit_packet(
                packet,
                FIXTURES,
                "egohygiene/realm#25",
                {"egohygiene/hygiene#39"},
                {"public-evidence-import"},
            ),
            [],
        )

    def test_unsigned_and_unverified_signature_states_are_explicit(self) -> None:
        packet = load("legal-source-packet.json")
        packet["integrity"]["signature"]["value"] = "not-allowed"
        errors = validator.validate_packet(packet, FIXTURES)
        self.assertTrue(any("must not contain signature material" in error for error in errors))

        packet = load("software-research-packet.json")
        packet["integrity"]["signature"]["key_id"] = None
        errors = validator.validate_packet(packet, FIXTURES)
        self.assertTrue(any("must contain algorithm" in error for error in errors))

    def test_cli_returns_structured_model_independent_result(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--packet",
                str(FIXTURES / "legal-source-packet.json"),
                "--attachments-root",
                str(FIXTURES),
                "--format",
                "json",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), {"errors": [], "kind": "packet", "valid": True})


if __name__ == "__main__":
    unittest.main()
