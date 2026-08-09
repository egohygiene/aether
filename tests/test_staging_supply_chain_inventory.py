from __future__ import annotations

import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
EXTERNAL_CATALOG = ROOT / "catalog" / "external" / "approved-skills.v1.json"
INVENTORY_REPORT = ROOT / "catalog" / "reports" / "staged-skills-inventory.v1.json"
LOCK_PATH = ROOT / ".staging" / "manifests" / "skills-lock.json"
EXTERNAL_SCHEMA_PATH = ROOT / "catalog" / "schemas" / "aether.external-source-record.v1.schema.json"
FIRST_PARTY_DISP_DIR = ROOT / "catalog" / "first-party" / "staging-dispositions"


class TestExternalCatalogAndStagingInventory(unittest.TestCase):
    def _load_json(self, path: Path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_external_catalog_entries_match_lock_and_schema(self):
        lock = self._load_json(LOCK_PATH)["skills"]
        external = self._load_json(EXTERNAL_CATALOG)
        schema = self._load_json(EXTERNAL_SCHEMA_PATH)
        validator = Draft202012Validator(schema)

        entries = external["entries"]
        self.assertEqual(len(entries), len(lock))

        by_id = {entry["id"]: entry for entry in entries}
        self.assertEqual(len(by_id), len(entries))

        for skill_name, lock_record in sorted(lock.items()):
            rec = by_id[f"external/{skill_name}"]
            self.assertEqual(rec["upstream_repository"], f"https://github.com/{lock_record['source']}")
            self.assertEqual(rec["upstream_skill_path"], lock_record["skillPath"])
            self.assertTrue(rec["pinned_install_example"].startswith("gh skill install "))
            self.assertEqual(list(validator.iter_errors(rec)), [])

    def test_inventory_covers_current_and_historical_staged_skill_copies(self):
        inventory = self._load_json(INVENTORY_REPORT)
        entries = inventory["entries"]

        current_paths = {
            f".staging/skills/{d.name}/SKILL.md"
            for d in sorted((ROOT / ".staging" / "skills").iterdir())
            if d.is_dir() and (d / "SKILL.md").exists()
        }
        historical_paths = {
            self._load_json(p)["staging_path"]
            for p in sorted(FIRST_PARTY_DISP_DIR.glob("*.json"))
        }

        entry_paths = {entry["staging_path"] for entry in entries}
        self.assertTrue(current_paths.issubset(entry_paths))
        self.assertTrue(historical_paths.issubset(entry_paths))

        totals = inventory["inventory_totals"]
        self.assertEqual(totals["direct_staged_skill_directories_current"], len(current_paths))
        self.assertEqual(totals["historical_removed_staged_skill_copies"], len(historical_paths))
        self.assertEqual(
            totals["total_copied_staged_skills_accounted_for"],
            len(current_paths) + len(historical_paths),
        )

        allowed = set(inventory["classification_categories"])
        self.assertTrue(all(entry["classification"] in allowed for entry in entries))


if __name__ == "__main__":
    unittest.main()
