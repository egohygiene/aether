"""Qualify optional authored exploration output without promotion or overwrite."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "library/organization/skills/authoring/author-exploration-note"
SPEC = importlib.util.spec_from_file_location("exploration_note", SKILL / "scripts/note.py")
note = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(note)


class ExplorationNoteTests(unittest.TestCase):
    def setUp(self):
        self.cases = json.loads((SKILL / "evals/fixtures/notes.json").read_text())

    def render(self, metadata, body="A tentative idea; no architecture or task is accepted."):
        return "---\n" + yaml.safe_dump(metadata, sort_keys=False) + "---\n\n# Synthetic exploration\n\n" + body + "\n"

    def test_create_repeat_and_authored_revision_never_overwrite(self):
        text = self.cases["create"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "note.md"
            self.assertEqual("created", note.create_note(path, text))
            self.assertEqual("unchanged", note.create_note(path, text))
            revised = self.cases["revise"]
            path.write_text(revised)
            with self.assertRaisesRegex(ValueError, "refuses overwrite"):
                note.create_note(path, text)
            self.assertEqual(revised, path.read_text())
            self.assertEqual(note.inspect_note(text)["id"], note.inspect_note(revised)["id"])
            self.assertIn("Correction", revised)

    def test_park_and_graduate_links_keep_tentative_authority(self):
        parked = note.inspect_note(self.cases["park"])
        linked = note.inspect_note(self.cases["graduate-link"])
        self.assertTrue(parked["parked"])
        self.assertEqual(("draft", "draft"), (parked["metadata"]["status"], linked["metadata"]["status"]))
        self.assertTrue(linked["metadata"]["related"])
        self.assertEqual("exploratory-only", linked["authority"])
        self.assertEqual("not-authenticated", linked["meaning_review"])

    def test_duplicate_identity_preserves_both_contributions(self):
        with tempfile.TemporaryDirectory() as directory:
            a, b = Path(directory) / "a.md", Path(directory) / "b.md"
            a.write_text(self.cases["create"]); b.write_text(self.cases["revise"])
            before = (a.read_bytes(), b.read_bytes())
            with self.assertRaisesRegex(ValueError, "duplicate stable"):
                note.inspect_collection([a, b])
            self.assertEqual(before, (a.read_bytes(), b.read_bytes()))

    def test_conflicting_decision_and_missing_sources_remain_explicit(self):
        conflict = note.inspect_note(self.cases["conflicting-decision"])
        self.assertEqual("draft", conflict["metadata"]["status"])
        self.assertIn("Hypothesis conflicts with the canonical decision", self.cases["conflicting-decision"])
        with tempfile.TemporaryDirectory() as directory:
            partial = note.inspect_note(self.cases["missing-source"], directory)
            self.assertEqual("partial", partial["status"])
            self.assertTrue(partial["source_gap"])
        metadata = copy.deepcopy(conflict["metadata"])
        for field, value in (("status", "accepted"), ("authority", "approved-decision")):
            with self.subTest(field=field), self.assertRaises(ValueError):
                note.inspect_note(self.render({**metadata, field: value}))

    def test_public_private_and_ambiguous_metadata_fail_closed(self):
        private = note.inspect_note(self.cases["private"])
        self.assertEqual("private", private["metadata"]["visibility"])
        with self.assertRaisesRegex(ValueError, "private source"):
            note.inspect_note(self.cases["private-to-public"])
        duplicate = self.cases["create"].replace("status: draft", "status: draft\nstatus: accepted")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            note.inspect_note(duplicate)
        metadata = private["metadata"]
        for reference in ("/private/synthetic", "../outside.md", "file:///synthetic", "https://:secret@example.invalid/source"):
            unsafe = {**metadata, "sources": [{"reference": reference, "visibility": "private"}]}
            with self.subTest(reference=reference), self.assertRaises(ValueError):
                note.inspect_note(self.render(unsafe))

    def test_create_refuses_symlink_missing_directory_and_cli_withholds_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            existing = root / "authored.md"; existing.write_text(self.cases["create"])
            link = root / "link.md"; link.symlink_to(existing)
            with self.assertRaises((OSError, ValueError)):
                note.create_note(link, self.cases["create"])
            with self.assertRaises(ValueError):
                note.create_note(root / "not-selected-directory/note.md", self.cases["create"])
            self.assertFalse((root / "not-selected-directory").exists())
            bad = root / "bad.md";bad.write_text("synthetic content that diagnostics must not echo")
            result = subprocess.run([sys.executable, str(SKILL / "scripts/note.py"), "--check", str(bad)],
                                    text=True, capture_output=True, timeout=5)
            self.assertEqual(1, result.returncode)
            self.assertNotIn("synthetic content", result.stdout + result.stderr)

    def test_reviewed_repository_canary_stays_local_owned_parked_and_source_linked(self):
        canary = ROOT / "docs/explorations/2026-11-15-opt-in-onboarding-discovery.md"
        result = note.inspect_note(note.read_note(canary), ROOT)
        self.assertEqual("valid", result["status"])
        self.assertEqual("exp-opt-in-onboarding-discovery", result["id"])
        self.assertTrue(result["parked"])
        self.assertEqual("draft", result["metadata"]["status"])
        self.assertEqual("public", result["metadata"]["visibility"])
        self.assertIn("Canonical source stays in this repository", canary.read_text())
        self.assertIn("No architecture is accepted", canary.read_text())

    def test_declared_examples_cover_optional_authoring_without_ingestion(self):
        data = json.loads((SKILL / "evals/evals.json").read_text())
        self.assertEqual(11, len(data["cases"]))
        self.assertEqual({"create", "revise", "park", "graduate-link", "duplicate", "conflicting-decision",
                          "missing-source", "public", "private", "private-to-public", "non-exploration-task"},
                         {case["id"] for case in data["cases"]})


if __name__ == "__main__":
    unittest.main()
