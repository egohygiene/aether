from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = ROOT / "catalog" / "social-surfaces"
FIXTURE = ROOT / "tests" / "fixtures" / "social-surfaces" / "query-catalog.v1.json"


def _load(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


builder = _load("social_surface_builder", "catalog/social-surfaces/build-distribution.py")
validator = _load("social_surface_validator", "catalog/social-surfaces/validate.py")


class SocialSurfaceCatalogTests(unittest.TestCase):
    def test_canonical_catalog_passes_contract_and_rights_gate(self):
        self.assertEqual(validator.validate(CATALOG_DIR / "catalog.v1.json"), [])

    def test_source_candidate_is_registered_without_raw_archive_or_templates(self):
        candidate_catalog = json.loads(
            (ROOT / "catalog/external/source-candidates.v1.json").read_text(encoding="utf-8")
        )
        candidate = candidate_catalog["entries"][0]
        self.assertEqual(candidate["id"], "external/media-cheat-sheet-social-surface-snapshot")
        self.assertEqual(candidate["review_state"], "reviewed")
        self.assertEqual(candidate["trust_classification"], "restricted")
        self.assertEqual(candidate["redistribution_permission"], "disallowed")
        self.assertEqual(candidate["redistribution_status"], "verified")
        catalog = json.loads((CATALOG_DIR / "catalog.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(catalog["catalog"]["rights_review"]["state"], "rejected")
        self.assertEqual(catalog["records"], [])
        self.assertFalse(any(path.suffix.lower() == ".svg" for path in CATALOG_DIR.rglob("*")))
        self.assertFalse((ROOT / "catalog/social-surfaces/social-media-specs.zip").exists())

    def test_query_separates_organic_and_advertising(self):
        command = [
            sys.executable,
            str(CATALOG_DIR / "query.py"),
            "--catalog",
            str(FIXTURE),
            "--platform",
            "Example Network",
            "--use",
            "organic",
        ]
        first = subprocess.check_output(command, text=True)
        second = subprocess.check_output(command, text=True)
        self.assertEqual(first, second)
        result = json.loads(first)
        self.assertEqual([record["id"] for record in result["matches"]], ["surface/example-network-organic-image"])
        self.assertIn("dated, offline catalog snapshot", result["freshness_warning"])

    def test_catalog_distribution_is_deterministic_and_lockable(self):
        with tempfile.TemporaryDirectory(prefix="aether-social-surface-") as temp_dir:
            output = Path(temp_dir) / "dist"
            self.assertEqual(builder.build(output_directory=output), 0)
            self.assertEqual(builder.build(check=True, output_directory=output), 0)
            manifest = json.loads(
                (output / "catalogs/social-surface-specs/distribution-manifest.v1.json").read_text(encoding="utf-8")
            )
        self.assertEqual(manifest["catalog_id"], "catalog/social-surface-specs")
        self.assertEqual(manifest["catalog_version"], "1.0.1")
        self.assertRegex(manifest["catalog_digest"]["value"], r"^[a-f0-9]{64}$")
        self.assertEqual(manifest["publication"]["state"], "blocked")

    def test_packaged_skill_queries_its_own_pinned_catalog_by_default(self):
        with tempfile.TemporaryDirectory(prefix="aether-social-surface-skill-") as temp_dir:
            output = Path(temp_dir) / "dist"
            skill_builder = ROOT / "library/organization/skills/build-distributions.py"
            subprocess.run(
                [sys.executable, str(skill_builder), "--output-directory", str(output)],
                check=True,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            result = subprocess.check_output(
                [
                    sys.executable,
                    str(output / "skills/social-surface-specs/scripts/query-social-surfaces.py"),
                    "--output-format",
                    "json",
                ],
                cwd=output / "skills/social-surface-specs",
                text=True,
            )
        self.assertEqual(json.loads(result)["catalog"]["id"], "catalog/social-surface-specs")


if __name__ == "__main__":
    unittest.main()
