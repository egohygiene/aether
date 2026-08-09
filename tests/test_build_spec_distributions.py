"""Tests for library/organization/specs/build-distributions.py."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


def _load_build_distributions():
    spec_path = (
        Path(__file__).resolve().parents[1]
        / "library"
        / "organization"
        / "specs"
        / "build-distributions.py"
    )
    spec = importlib.util.spec_from_file_location("build_spec_distributions", spec_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bd = _load_build_distributions()


class TestBuildSpecDistributions(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp(prefix="aether-spec-dist-"))
        self._orig_repo_root = bd.REPO_ROOT
        self._orig_specs_dir = bd.SPECS_DIR
        bd.REPO_ROOT = self._tmp
        bd.SPECS_DIR = self._tmp / "library" / "organization" / "specs"

    def tearDown(self):
        bd.REPO_ROOT = self._orig_repo_root
        bd.SPECS_DIR = self._orig_specs_dir

    def _write_spec(self, name: str, body: str = "# Spec\n") -> Path:
        path = bd.SPECS_DIR / "architecture" / f"{name}.spec.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            f"id: architecture-{name}\n"
            "title: Example\n"
            "schema: aether.specification/v1\n"
            "---\n\n"
            f"{body}",
            encoding="utf-8",
        )
        return path

    def test_build_writes_expected_distribution_file(self):
        self._write_spec("example")
        rc = bd.build(check=False)
        self.assertEqual(rc, 0)
        self.assertTrue((self._tmp / "dist" / "specs" / "architecture-example.spec.md").exists())

    def test_build_honors_custom_output_directory(self):
        self._write_spec("example")
        output_directory = self._tmp / "custom-dist"
        rc = bd.build(check=False, output_directory=output_directory)
        self.assertEqual(rc, 0)
        self.assertTrue((output_directory / "specs" / "architecture-example.spec.md").exists())

    def test_check_detects_drift(self):
        self._write_spec("example")
        bd.build(check=False)
        (self._tmp / "dist" / "specs" / "architecture-example.spec.md").write_text("stale\n", encoding="utf-8")
        rc = bd.build(check=True)
        self.assertNotEqual(rc, 0)


if __name__ == "__main__":
    unittest.main()
