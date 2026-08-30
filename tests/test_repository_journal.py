"""Tests for the deterministic repository-journal skill renderer."""
from __future__ import annotations
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "library/organization/skills/quality/create-repository-journal/scripts/repository-journal.py"
spec = importlib.util.spec_from_file_location("repository_journal", SCRIPT)
journal = importlib.util.module_from_spec(spec)
spec.loader.exec_module(journal)

class RepositoryJournalTests(unittest.TestCase):
    def test_render_is_deterministic_and_marks_missing_evidence(self):
        data = {"schema_version":"aether.repository-journal-input/v1", "repository":"egohygiene/example", "interval":{"start":"2026-08-01T00:00:00Z", "end":"2026-08-02T00:00:00Z"}, "evidence":{"merged_work":["PR #1 merged"], "ci":[]}}
        first, machine = journal.render(data)
        second, _ = journal.render(data)
        self.assertEqual(first, second)
        self.assertIn("merged work: observed: PR #1 merged", first)
        self.assertIn("ci: observed: none", first)
        self.assertIn("releases: not available", first)
        self.assertEqual(machine["contract_id"], "repository-journal")
    def test_rejects_unstructured_or_non_utc_input(self):
        with self.assertRaises(ValueError): journal._load(_write('{"schema_version":"bad"}'))
        with self.assertRaises(ValueError): journal._load(_write('{"schema_version":"aether.repository-journal-input/v1","repository":"x/y","interval":{"start":"2026-01-01","end":"2026-01-02"},"evidence":{}}'))

def _write(content: str) -> Path:
    path = Path(tempfile.mkdtemp()) / "input.json"
    path.write_text(content, encoding="utf-8")
    return path
