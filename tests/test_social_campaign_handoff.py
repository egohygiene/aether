"""Deterministic and adversarial evidence for campaign handoff packets."""

from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - the repository dev environment installs it
    Draft202012Validator = None

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "library/organization/skills/marketing/prepare-social-campaign-handoff"
SCRIPT = SKILL / "scripts/campaign-handoff.py"
FIXTURE = ROOT / "tests/fixtures/social-campaign-handoff"


def load_module():
    """Load the portable script as a test module."""

    spec = importlib.util.spec_from_file_location("campaign_handoff", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


handoff = load_module()


def load(name: str) -> dict:
    """Load one campaign fixture."""

    return json.loads((FIXTURE / name).read_text(encoding="utf-8"))


def prepare(brief_name: str = "product-release-brief.json") -> dict:
    """Build one in-memory draft from the synthetic approved inputs."""

    return handoff.prepare_packet(
        load("identity-social-surfaces.json"),
        FIXTURE / "identity-social-surfaces.json",
        load("catalog.v1.json"),
        FIXTURE / "catalog.v1.json",
        load(brief_name),
    )


def complete_review(packet: dict) -> dict:
    """Record freshness and every remaining required checklist item."""

    updated = handoff.record_freshness(
        packet,
        "example-reviewer",
        "2026-08-29T12:00:00Z",
        "https://example.invalid/reviews/freshness",
    )
    for identifier in handoff.CHECKLIST_IDS:
        if identifier == "catalog-freshness":
            continue
        updated = handoff.complete_check(
            updated,
            identifier,
            "example-reviewer",
            "2026-08-29T12:05:00Z",
            f"https://example.invalid/reviews/{identifier}",
        )
    return handoff.transition_packet(
        updated,
        "reviewed",
        "example-reviewer",
        "2026-08-29T12:10:00Z",
        "Human inspection completed; export approval remains pending.",
        review_notes="Reviewed the exact surfaces, copy, claims, links, and attribution.",
    )


def approve(packet: dict) -> dict:
    """Approve one exact reviewed packet through a digest-bound record."""

    approval = {
        "schema_version": handoff.APPROVAL_SCHEMA,
        "id": "approval/example-product-release",
        "packet_id": packet["packet"]["id"],
        "reviewed_packet_digest": {
            "algorithm": "sha256-canonical-json",
            "value": handoff.canonical_digest(packet),
        },
        "decision": "approved-for-export",
        "approved_by": "example-approver",
        "approved_at": "2026-08-29T12:20:00Z",
        "evidence": "https://example.invalid/reviews/export-approval",
    }
    return handoff.transition_packet(
        packet,
        "approved-for-export",
        "example-approver",
        "2026-08-29T12:20:00Z",
        "Exact reviewed packet approved for immutable export.",
        approval=approval,
    )


class SocialCampaignHandoffTests(unittest.TestCase):
    """Prove source locks, review gates, and publishing separation."""

    def test_examples_prepare_deterministically_with_exact_surface_facts(self) -> None:
        first = prepare("organization-announcement-brief.json")
        second = prepare("organization-announcement-brief.json")
        self.assertEqual(first, second)
        self.assertEqual(first["packet"]["state"], "draft")
        self.assertEqual(first["review"]["status"], "pending")
        self.assertFalse(first["external_handoff"]["authorized"])
        self.assertEqual(
            first["channels"][0]["surface"]["dimensions"],
            {"widthPx": 1500, "heightPx": 500},
        )
        product = prepare()
        channel = product["channels"][0]
        self.assertEqual(channel["surface"]["dimensions"], {"widthPx": 1080, "heightPx": 1080})
        self.assertEqual(channel["surface"]["safeZone"]["state"], "unknown")
        self.assertEqual(channel["copy"]["status"], "candidate")
        self.assertIsNone(channel["copy"]["claims"][0]["approval_id"])
        self.assertEqual(handoff.validate_packet(product), [])

    def test_catalog_tampering_and_unsupported_surfaces_fail_closed(self) -> None:
        identity = load("identity-social-surfaces.json")
        catalog = load("catalog.v1.json")
        catalog["records"][0]["dimensions"]["width_px"] = 999
        with tempfile.TemporaryDirectory() as temporary:
            catalog_path = Path(temporary) / "catalog.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            with self.assertRaisesRegex(handoff.HandoffError, "digest"):
                handoff.prepare_packet(
                    identity,
                    FIXTURE / "identity-social-surfaces.json",
                    catalog,
                    catalog_path,
                    load("product-release-brief.json"),
                )

        brief = load("product-release-brief.json")
        brief["selections"][0]["target_id"] = "unapproved-video-ad"
        with self.assertRaisesRegex(handoff.HandoffError, "unsupported Identity target"):
            handoff.prepare_packet(
                identity,
                FIXTURE / "identity-social-surfaces.json",
                load("catalog.v1.json"),
                FIXTURE / "catalog.v1.json",
                brief,
            )

    def test_missing_attribution_and_identity_copy_drift_are_rejected(self) -> None:
        brief = load("organization-announcement-brief.json")
        brief["selections"][0]["attribution"] = {"required": True, "text": None}
        with self.assertRaisesRegex(handoff.HandoffError, "attribution.text"):
            handoff.validate_brief(brief)

        brief = load("organization-announcement-brief.json")
        brief["selections"][0]["candidate_copy"] = "Invented identity statement"
        with self.assertRaisesRegex(handoff.HandoffError, "differs from Identity target"):
            handoff.prepare_packet(
                load("identity-social-surfaces.json"),
                FIXTURE / "identity-social-surfaces.json",
                load("catalog.v1.json"),
                FIXTURE / "catalog.v1.json",
                brief,
            )

    def test_credentials_and_direct_publish_requests_are_rejected(self) -> None:
        brief = load("product-release-brief.json")
        brief["access_token"] = "ghp_abcdefghijklmnopqrstuvwxyz1234567890"
        with self.assertRaisesRegex(handoff.HandoffError, "unsupported fields"):
            handoff.validate_brief(brief)

        brief = load("product-release-brief.json")
        brief["selections"][0]["claims"][0]["evidence"] = (
            "Bearer abcdefghijklmnopqrstuvwxyz123456"
        )
        with self.assertRaisesRegex(handoff.HandoffError, "credential-like"):
            handoff.validate_brief(brief)

        packet = prepare()
        with self.assertRaisesRegex(handoff.HandoffError, "cannot publish"):
            handoff.transition_packet(
                packet,
                "published",
                "example-user",
                "2026-08-29T12:00:00Z",
                "Unsafe direct-publish attempt.",
            )

    def test_draft_cannot_claim_approved_copy_or_claims(self) -> None:
        packet = prepare()
        packet["channels"][0]["copy"]["status"] = "approved"
        packet["channels"][0]["copy"]["approval_id"] = "approval/invented"
        packet["channels"][0]["copy"]["claims"][0]["status"] = "approved"
        packet["channels"][0]["copy"]["claims"][0]["approval_id"] = "approval/invented"
        errors = handoff.validate_packet(packet)
        self.assertTrue(any("pre-export copy" in error for error in errors))
        self.assertTrue(any("pre-export claims" in error for error in errors))

    def test_review_and_digest_bound_approval_are_explicit(self) -> None:
        reviewed = complete_review(prepare())
        self.assertEqual(reviewed["packet"]["state"], "reviewed")
        self.assertFalse(reviewed["external_handoff"]["authorized"])
        bad_approval = {
            "schema_version": handoff.APPROVAL_SCHEMA,
            "id": "approval/wrong-digest",
            "packet_id": reviewed["packet"]["id"],
            "reviewed_packet_digest": {
                "algorithm": "sha256-canonical-json",
                "value": "0" * 64,
            },
            "decision": "approved-for-export",
            "approved_by": "example-approver",
            "approved_at": "2026-08-29T12:20:00Z",
            "evidence": "https://example.invalid/reviews/export-approval",
        }
        with self.assertRaisesRegex(handoff.HandoffError, "exact reviewed packet"):
            handoff.transition_packet(
                reviewed,
                "approved-for-export",
                "example-approver",
                "2026-08-29T12:20:00Z",
                "Attempted approval with stale evidence.",
                approval=bad_approval,
            )

        approved = approve(reviewed)
        self.assertEqual(approved["packet"]["state"], "approved-for-export")
        self.assertTrue(approved["external_handoff"]["authorized"])
        self.assertEqual(approved["external_handoff"]["allowed_action"], "immutable-export-only")
        self.assertEqual(approved["channels"][0]["copy"]["status"], "approved")
        self.assertEqual(handoff.validate_packet(approved), [])
        approved["channels"][0]["copy"]["text"] = "Edited after human approval"
        self.assertTrue(
            any("exact reviewed packet" in error for error in handoff.validate_packet(approved))
        )

    def test_stale_catalog_cannot_be_approved_for_export(self) -> None:
        reviewed = complete_review(prepare())
        reviewed["catalog"]["live_verification"] = {
            "status": "required",
            "required": True,
            "verified_at": None,
            "verified_by": None,
            "evidence": None,
        }
        for item in reviewed["publishing_checklist"]:
            if item["id"] == "catalog-freshness":
                item.update(
                    {
                        "status": "pending",
                        "evidence": None,
                        "completed_by": None,
                        "completed_at": None,
                    }
                )
        with self.assertRaisesRegex(handoff.HandoffError, "catalog-freshness"):
            approve(reviewed)

    def test_published_state_requires_separate_adapter_receipt(self) -> None:
        approved = approve(complete_review(prepare()))
        published = deepcopy(approved)
        approval_id = published["review"]["approval"]["id"]
        exported_digest = handoff.canonical_digest(approved)
        published["packet"]["state"] = "published"
        published["external_handoff"]["adapter"] = "adapter/example-scheduler"
        published["publication"] = {
            "status": "published",
            "receipt": {
                "adapter": "adapter/example-scheduler",
                "authorization_approval_id": approval_id,
                "platform_event_id": "example-event-123",
                "published_at": "2026-08-29T13:00:00Z",
                "exported_packet_digest": {
                    "algorithm": "sha256-canonical-json",
                    "value": exported_digest,
                },
            },
        }
        published["lifecycle"]["history"].append(
            {
                "from": "approved-for-export",
                "to": "published",
                "actor": "adapter/example-scheduler",
                "occurred_at": "2026-08-29T13:00:00Z",
                "reason": "External adapter recorded an authorized publication receipt.",
            }
        )
        self.assertEqual(handoff.validate_packet(published), [])
        published["publication"]["receipt"]["exported_packet_digest"]["value"] = "0" * 64
        self.assertTrue(
            any("exported packet" in error for error in handoff.validate_packet(published))
        )
        published["publication"]["receipt"] = None
        self.assertTrue(any("receipt" in error for error in handoff.validate_packet(published)))

    @unittest.skipIf(Draft202012Validator is None, "jsonschema is not installed")
    def test_json_schema_accepts_examples_and_rejects_unsafe_fixture(self) -> None:
        schema = json.loads(
            (ROOT / "catalog/schemas/aether.social-campaign-handoff.v1.schema.json").read_text(
                encoding="utf-8"
            )
        )
        validator = Draft202012Validator(schema)
        valid = json.loads(
            (
                ROOT
                / "catalog/fixtures/aether.social-campaign-handoff.v1.schema/valid.json"
            ).read_text(encoding="utf-8")
        )
        invalid = json.loads(
            (
                ROOT
                / "catalog/fixtures/aether.social-campaign-handoff.v1.schema/invalid.json"
            ).read_text(encoding="utf-8")
        )
        self.assertEqual(list(validator.iter_errors(valid)), [])
        self.assertNotEqual(list(validator.iter_errors(invalid)), [])

    def test_superseded_is_terminal_and_preserves_history(self) -> None:
        packet = handoff.transition_packet(
            prepare(),
            "superseded",
            "example-maintainer",
            "2026-08-29T12:00:00Z",
            "Campaign replaced before review.",
            superseded_by="campaign/replacement",
        )
        self.assertEqual(packet["packet"]["superseded_by"], "campaign/replacement")
        self.assertEqual(handoff.validate_packet(packet), [])
        with self.assertRaisesRegex(handoff.HandoffError, "terminal"):
            handoff.transition_packet(
                packet,
                "reviewed",
                "example-maintainer",
                "2026-08-29T12:10:00Z",
                "Invalid reopening attempt.",
                review_notes="Should not work.",
            )

    def test_cli_is_deterministic_and_never_overwrites_input(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "campaign.json"
            command = [
                sys.executable,
                str(SCRIPT),
                "prepare",
                "--identity-package",
                str(FIXTURE / "identity-social-surfaces.json"),
                "--catalog",
                str(FIXTURE / "catalog.v1.json"),
                "--brief",
                str(FIXTURE / "product-release-brief.json"),
                "--output",
                str(output),
            ]
            subprocess.run(command, check=True, capture_output=True, text=True)
            first = output.read_bytes()
            subprocess.run(command, check=True, capture_output=True, text=True)
            self.assertEqual(first, output.read_bytes())
            validation = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "validate",
                    "--packet",
                    str(output),
                    "--output-format",
                    "json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(json.loads(validation.stdout)["valid"])

            brief_path = FIXTURE / "product-release-brief.json"
            result = subprocess.run(
                [*command[:-1], str(brief_path)],
                capture_output=True,
                text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must not overwrite", result.stderr)


if __name__ == "__main__":
    unittest.main()
