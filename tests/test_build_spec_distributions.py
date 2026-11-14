"""Tests for library/organization/specs/build-distributions.py."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
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

    def test_malformed_required_spec_fails_both_modes_with_partial_output(self):
        self._write_spec("alpha")
        broken = self._write_spec("broken")
        broken.write_text("# Missing frontmatter\n", encoding="utf-8")
        for check in (False, True):
            with self.subTest(check=check):
                error = io.StringIO()
                with contextlib.redirect_stderr(error):
                    self.assertNotEqual(0, bd.build(check=check))
                self.assertIn("broken.spec.md generation", error.getvalue())
                self.assertIn("1/2 artifact(s) generated", error.getvalue())
                self.assertTrue((self._tmp / "dist/specs/architecture-alpha.spec.md").is_file())

    def test_obsolete_files_and_empty_directories_are_reported_without_deletion(self):
        self._write_spec("example")
        output = self._tmp / "custom-dist"
        self.assertEqual(0, bd.build(output_directory=output))
        obsolete = output / "specs/obsolete.spec.md"
        obsolete.write_text("obsolete\n", encoding="utf-8")
        (output / "specs/empty").mkdir()
        note = output / "user.txt"
        note.write_text("outside generator ownership\n", encoding="utf-8")
        before = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
        for check in (True, False):
            with self.subTest(check=check):
                self.assertNotEqual(0, bd.build(check=check, output_directory=output))
                after = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
                self.assertEqual(before, after)
                self.assertTrue((output / "specs/empty").is_dir())

    def test_removing_last_spec_does_not_bypass_inventory_check(self):
        source = self._write_spec("example")
        self.assertEqual(0, bd.build())
        source.unlink()
        self.assertNotEqual(0, bd.build(check=True))
        self.assertTrue((self._tmp / "dist/specs/architecture-example.spec.md").is_file())

    def test_missing_source_directory_and_output_io_failures_are_nonzero(self):
        self.assertNotEqual(0, bd.build())
        self.assertNotEqual(0, bd.build(check=True))
        self._write_spec("example")
        (self._tmp / "dist/specs/architecture-example.spec.md").mkdir(parents=True)
        self.assertNotEqual(0, bd.build())
        self.assertNotEqual(0, bd.build(check=True))

    def test_custom_clean_build_check_and_rebuild_have_identical_inventory(self):
        self._write_spec("example")
        output = self._tmp / "custom-dist"
        self.assertEqual(0, bd.build(output_directory=output))
        before = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
        self.assertEqual(0, bd.build(check=True, output_directory=output))
        self.assertEqual(0, bd.build(output_directory=output))
        after = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
        self.assertEqual(before, after)

    def test_colliding_spec_outputs_fail_instead_of_silently_overwriting(self):
        first = self._write_spec("alpha")
        second = self._write_spec("beta")
        second.write_text(first.read_text(), encoding="utf-8")
        self.assertNotEqual(0, bd.build())
        self.assertNotEqual(0, bd.build(check=True))

    def test_quoted_identifier_is_parsed_semantically_from_one_source_snapshot(self):
        source = self._write_spec("quoted")
        source.write_text(source.read_text().replace("id: architecture-quoted", 'id: "architecture-quoted" # supported comment'))
        self.assertEqual(0, bd.build())
        output = self._tmp / "dist/specs/architecture-quoted.spec.md"
        self.assertEqual(source.read_bytes(), output.read_bytes())
        self.assertEqual(0, bd.build(check=True))

    def test_unsafe_identifiers_fail_before_writing_an_escaping_path(self):
        source = self._write_spec("invalid")
        template = source.read_text()
        output = self._tmp / "custom-dist"
        for value in ["../../escaped", "/absolute", "C:\\escaped", "drive:name", "bad/id", "bad space", ".", "tail-", 7, None]:
            with self.subTest(value=value):
                source.write_text(template.replace("id: architecture-invalid", "id: " + json.dumps(value)))
                self.assertNotEqual(0, bd.build(output_directory=output))
                self.assertNotEqual(0, bd.build(check=True, output_directory=output))
                self.assertFalse(output.exists())
                self.assertFalse((self._tmp / "escaped.spec.md").exists())

    def test_source_and_output_symlinks_fail_without_mutating_external_sentinels(self):
        source = self._write_spec("example")
        with tempfile.TemporaryDirectory() as foreign:
            sentinel = Path(foreign) / "sentinel.spec.md"
            sentinel.write_text(source.read_text(), encoding="utf-8")
            source.unlink()
            source.symlink_to(sentinel)
            for check in (False, True):
                self.assertNotEqual(0, bd.build(check=check))
            source.unlink()
            self._write_spec("example")
            output = self._tmp / "custom-dist"
            output.mkdir()
            (output / "specs").symlink_to(Path(foreign), target_is_directory=True)
            before = sentinel.read_bytes()
            for check in (False, True):
                self.assertNotEqual(0, bd.build(check=check, output_directory=output))
                self.assertEqual(before, sentinel.read_bytes())
            self.assertEqual([sentinel], list(Path(foreign).iterdir()))


if __name__ == "__main__":
    unittest.main()
