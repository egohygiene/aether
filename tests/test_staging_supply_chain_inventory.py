from __future__ import annotations

import copy
import json
import subprocess
import tempfile
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
        by_id = {entry["id"]: entry for entry in entries}
        self.assertEqual(len(by_id), len(entries))
        self.assertGreaterEqual(len(entries), len(lock))

        for skill_name, lock_record in sorted(lock.items()):
            rec = by_id[f"external/{skill_name}"]
            self.assertEqual(rec["upstream_repository"], f"https://github.com/{lock_record['source']}")
            self.assertEqual(rec["upstream_skill_path"], lock_record["skillPath"])
            self.assertTrue(rec["pinned_install_example"].startswith("gh skill install "))
            self.assertEqual(list(validator.iter_errors(rec)), [])

    def test_inventory_covers_current_and_historical_staged_skill_copies(self):
        inventory = self._load_json(INVENTORY_REPORT)

        current_paths = self._tracked_skill_paths(ROOT)
        self.assertTrue(all((ROOT / path).is_file() for path in current_paths))
        records = [self._load_json(p) for p in sorted(FIRST_PARTY_DISP_DIR.glob("*.json"))]
        retained_paths, historical_paths = self._classify_dispositions(records, current_paths)
        self.assertIn(".staging/skills/repository-audit/SKILL.md", retained_paths)
        self._assert_inventory(inventory, current_paths, historical_paths)

    def _assert_inventory(self, inventory: dict, current_paths: set[str], historical_paths: set[str]) -> None:
        entries = inventory["entries"]
        entry_paths = {entry["staging_path"] for entry in entries}
        self.assertEqual(len(entry_paths), len(entries), "inventory paths must be unique")
        self.assertEqual(entry_paths, current_paths | historical_paths)
        self.assertFalse(current_paths & historical_paths)
        for entry in entries:
            expected_state = "present" if entry["staging_path"] in current_paths else "removed"
            self.assertEqual(entry["current_staging_state"], expected_state, entry["staging_path"])

        totals = inventory["inventory_totals"]
        self.assertEqual(totals["direct_staged_skill_directories_current"], len(current_paths))
        self.assertEqual(totals["historical_removed_staged_skill_copies"], len(historical_paths))
        self.assertEqual(
            totals["total_copied_staged_skills_accounted_for"],
            len(current_paths) + len(historical_paths),
        )

        allowed = set(inventory["classification_categories"])
        self.assertTrue(all(entry["classification"] in allowed for entry in entries))

    def _tracked_skill_paths(self, root: Path) -> set[str]:
        tracked = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z", "--", ".staging/skills"])
        paths = (path.decode("utf-8") for path in tracked.split(b"\0") if path)
        return {path for path in paths if len(Path(path).parts) == 4 and Path(path).name == "SKILL.md"}

    def _classify_dispositions(self, records: list[dict], current_paths: set[str]) -> tuple[set[str], set[str]]:
        disposition_paths = {path for record in records for path in self._disposition_staging_paths(record)}
        # Dispositions preserve provenance for present and absent sources. The
        # recorded disposition name alone does not establish physical removal.
        return disposition_paths & current_paths, disposition_paths - current_paths

    def _disposition_staging_paths(self, record: dict) -> list[str]:
        if "staging_path" in record:
            paths = [record["staging_path"]]
        elif "staging_paths" in record:
            paths = list(record["staging_paths"])
        else:
            self.fail("staging disposition record must define staging_path or staging_paths")
        return [path for path in paths if path.startswith(".staging/skills/")]

    def test_retained_dispositions_do_not_count_as_removals(self):
        retained = ".staging/skills/retained/SKILL.md"
        removed = ".staging/skills/removed/SKILL.md"
        records = [
            {"staging_paths": [retained, removed], "disposition": "preserve-migration-evidence"},
            {"staging_path": retained, "disposition": "preserve-migration-evidence"},
        ]
        current, historical = self._classify_dispositions(records, {retained})
        self.assertEqual(current, {retained})
        self.assertEqual(historical, {removed})

    def test_untracked_skill_files_do_not_change_inventory_membership(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            for name in ("tracked", "untracked"):
                path = root / ".staging/skills" / name / "SKILL.md"
                path.parent.mkdir(parents=True)
                path.write_text("retained evidence\n")
            subprocess.run(["git", "-C", str(root), "add", ".staging/skills/tracked/SKILL.md"], check=True)
            self.assertEqual(self._tracked_skill_paths(root), {".staging/skills/tracked/SKILL.md"})

    def test_duplicate_dangling_and_misclassified_inventory_rows_fail(self):
        inventory = self._load_json(INVENTORY_REPORT)
        current = self._tracked_skill_paths(ROOT)
        records = [self._load_json(p) for p in sorted(FIRST_PARTY_DISP_DIR.glob("*.json"))]
        _, historical = self._classify_dispositions(records, current)
        for mutation in ("duplicate", "dangling", "retained-as-removed", "removed-as-present"):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(inventory)
                if mutation == "duplicate":
                    changed["entries"].append(copy.deepcopy(changed["entries"][0]))
                elif mutation == "dangling":
                    row = copy.deepcopy(changed["entries"][0])
                    row["staging_path"] = ".staging/skills/unrecorded/SKILL.md"
                    changed["entries"].append(row)
                else:
                    path = ".staging/skills/repository-audit/SKILL.md" if mutation == "retained-as-removed" else sorted(historical)[0]
                    row = next(entry for entry in changed["entries"] if entry["staging_path"] == path)
                    row["current_staging_state"] = "removed" if mutation == "retained-as-removed" else "present"
                with self.assertRaises(AssertionError):
                    self._assert_inventory(changed, current, historical)


if __name__ == "__main__":
    unittest.main()
