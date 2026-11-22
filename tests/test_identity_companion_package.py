"""Portable, read-only controls for the Identity companion's source-lock helper.

All source trees and locks exercised here are synthetic fixtures. Hash checks
do not qualify a real Identity binary, install channel, agent or human approval.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "author-project-identity"
PACKAGE = ROOT / "library/organization/skills/authoring" / SKILL_NAME
SCRIPT_NAME = "scripts/verify_identity_source.py"
REVISION = "a" * 40


def _snapshot(root: Path) -> dict[str, tuple]:
    """Observe content and write timestamps without following fixture links."""
    observed = {}
    for path in sorted(root.rglob("*")):
        name = path.relative_to(root).as_posix()
        if path.is_symlink():
            observed[name] = ("symlink", str(path.readlink()))
        elif path.is_file():
            observed[name] = (
                "file", hashlib.sha256(path.read_bytes()).hexdigest(),
                path.stat().st_mtime_ns,
            )
        elif path.is_dir():
            observed[name] = ("directory",)
    return observed


class IdentityCompanionPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Use the actual distribution builder, not a handwritten package copy."""
        cls._portable = tempfile.TemporaryDirectory(prefix="identity-skill-portable-")
        cls.addClassCleanup(cls._portable.cleanup)
        cls.portable_root = Path(cls._portable.name)
        cls.installed = cls.portable_root / "installed-skill"
        cls.installed.mkdir()
        cls.cwd = cls.portable_root / "outside-aether"
        cls.cwd.mkdir()

        builder_path = ROOT / "library/organization/skills/build-distributions.py"
        spec = importlib.util.spec_from_file_location(
            "identity_companion_distribution_under_test", builder_path,
        )
        assert spec and spec.loader
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        generated = builder._build_skill_dist(SKILL_NAME, PACKAGE)
        prefix = Path("dist/skills") / SKILL_NAME
        for name, content in generated.items():
            relative = Path(name).relative_to(prefix)
            destination = cls.installed / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        cls.script = cls.installed / SCRIPT_NAME
        if not cls.script.is_file():
            raise AssertionError("The actual distribution omitted the source-lock helper")

    def setUp(self):
        self._fixture = tempfile.TemporaryDirectory(prefix="identity-source-fixture-")
        self.addCleanup(self._fixture.cleanup)
        self.fixture = Path(self._fixture.name)
        self.source = self.fixture / "source"
        self.source.mkdir()
        self.contents = {
            "docs/identity contract.md": b"# Synthetic identity contract\n",
            "scripts/check.py": b"# Source inspection only; never execute this file.\n",
        }
        for relative, content in self.contents.items():
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        self.lock = {
            "schema": "aether.identity-source-lock/v1",
            "repository": "egohygiene/identity",
            "revision": REVISION,
            "resources": [
                {
                    "path": relative,
                    "sha256": hashlib.sha256(content).hexdigest(),
                    "size_bytes": len(content),
                }
                for relative, content in self.contents.items()
            ],
            "notes": "Synthetic lock; no actual upstream or release is qualified.",
        }
        self.lock_file = self.fixture / "source-lock.json"

    def run_helper(self, lock: dict | str | None = None, *, expected: int):
        if isinstance(lock, str):
            self.lock_file.write_text(lock, encoding="utf-8")
        else:
            self.lock_file.write_text(
                json.dumps(self.lock if lock is None else lock), encoding="utf-8",
            )
        before_source = _snapshot(self.source)
        before_lock = self.lock_file.read_bytes()
        before_package = _snapshot(self.installed)
        result = subprocess.run(
            [
                sys.executable, "-I", str(self.script),
                "--source-root", str(self.source),
                "--lock", str(self.lock_file),
            ],
            cwd=self.cwd, capture_output=True, text=True, timeout=10,
            check=False,
        )
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        self.assertEqual(_snapshot(self.source), before_source)
        self.assertEqual(self.lock_file.read_bytes(), before_lock)
        self.assertEqual(_snapshot(self.installed), before_package)
        self.assertLess(len(result.stdout), 16_384)
        self.assertNotIn(str(self.source), result.stdout)
        self.assertNotIn(str(self.fixture), result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)
        self.assertEqual(result.stderr, "", result.stderr)
        report = json.loads(result.stdout)
        self.assertIsInstance(report, dict)
        self.assertIn("status", report)
        self.assertIn("scope", report)
        self.assertIsInstance(report.get("findings"), list)
        return report

    def test_actual_distribution_runs_isolated_outside_aether(self):
        self.assertTrue((self.installed / "SKILL.md").is_file())
        self.assertTrue((self.installed / "references/identity-source-lock.json").is_file())
        self.assertTrue(
            (self.installed / "references/project-identity-authoring.spec.md").is_file()
        )
        report = self.run_helper(expected=0)
        self.assertEqual(report["findings"], [])
        scope = json.dumps(report["scope"]).lower()
        for term in ("file", "binary", "approval", "release"):
            self.assertIn(term, scope)

    def test_default_lock_resolves_relative_to_copied_package(self):
        """A host need not run from Aether or pass a checkout-relative lock."""
        with tempfile.TemporaryDirectory(prefix="identity-default-lock-") as temporary:
            # The production builder has already created a complete portable
            # package. Use an independent copy so tests never mutate that copy.
            import shutil

            copied = Path(temporary) / "skill"
            shutil.copytree(self.installed, copied)
            (copied / "references/identity-source-lock.json").write_text(
                json.dumps(self.lock), encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable, "-I", str(copied / SCRIPT_NAME),
                    "--source-root", str(self.source),
                ],
                cwd=self.cwd, capture_output=True, text=True, timeout=10,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual(json.loads(result.stdout)["findings"], [])

    def test_changed_resource_is_a_finding_without_repair(self):
        (self.source / "scripts/check.py").write_bytes(b"changed source\n")
        report = self.run_helper(expected=1)
        self.assertTrue(report["findings"])

    def test_missing_resource_is_a_finding_without_generation(self):
        (self.source / "scripts/check.py").unlink()
        report = self.run_helper(expected=1)
        self.assertTrue(report["findings"])
        self.assertFalse((self.source / "scripts/check.py").exists())

    def test_unlisted_files_do_not_become_whole_source_verification(self):
        unlisted = self.source / "unlisted.py"
        unlisted.write_text("raise RuntimeError('must not execute')\n", encoding="utf-8")
        report = self.run_helper(expected=0)
        self.assertEqual(report["findings"], [])
        scope = json.dumps(report["scope"]).lower()
        self.assertIn("file", scope)
        self.assertIn("binary", scope)
        self.assertIn("release", scope)

    def test_oversized_resource_is_refused_without_dumping_content(self):
        marker = b"PRIVATE_FIXTURE_CONTENT_MUST_NOT_APPEAR"
        path = self.source / "scripts/check.py"
        path.write_bytes(marker * 40_000)
        report = self.run_helper(expected=1)
        self.assertTrue(report["findings"])
        self.assertNotIn(marker.decode(), json.dumps(report))

    def test_symlink_resource_and_parent_do_not_escape_source(self):
        outside = self.fixture / "outside-secret.txt"
        outside.write_text("PRIVATE_OUTSIDE_VALUE", encoding="utf-8")
        original = self.source / "scripts/check.py"
        original.unlink()
        try:
            original.symlink_to(outside)
        except (OSError, NotImplementedError):
            self.skipTest("This host cannot create the disposable symlink fixture")
        report = self.run_helper(expected=1)
        self.assertNotIn(str(outside), json.dumps(report))
        self.assertNotIn("PRIVATE_OUTSIDE_VALUE", json.dumps(report))
        original.unlink()
        (self.source / "scripts").rmdir()
        external_directory = self.fixture / "outside-directory"
        external_directory.mkdir()
        (external_directory / "check.py").write_bytes(self.contents["scripts/check.py"])
        (self.source / "scripts").symlink_to(external_directory, target_is_directory=True)
        report = self.run_helper(expected=1)
        self.assertNotIn(str(external_directory), json.dumps(report))

    def test_invalid_lock_paths_are_input_errors(self):
        for unsafe in ("../outside.txt", "/absolute.txt", "docs\\outside.txt", "C:/outside.txt"):
            with self.subTest(path=unsafe):
                lock = deepcopy(self.lock)
                lock["resources"][0]["path"] = unsafe
                report = self.run_helper(lock, expected=2)
                self.assertTrue(report["findings"])

    def test_duplicate_resource_paths_are_input_errors(self):
        lock = deepcopy(self.lock)
        lock["resources"].append(deepcopy(lock["resources"][0]))
        self.assertTrue(self.run_helper(lock, expected=2)["findings"])

    def test_invalid_revision_digest_and_bounds_are_input_errors(self):
        mutations = (
            lambda lock: lock.update(revision="main"),
            lambda lock: lock["resources"][0].update(sha256="z" * 64),
            lambda lock: lock["resources"][0].update(size_bytes=0),
            lambda lock: lock["resources"][0].update(size_bytes=1_048_577),
            lambda lock: lock["resources"][0].update(size_bytes=True),
        )
        for mutate in mutations:
            with self.subTest(mutation=mutate):
                lock = deepcopy(self.lock)
                mutate(lock)
                self.assertTrue(self.run_helper(lock, expected=2)["findings"])

    def test_malformed_lock_is_an_input_error_with_json_diagnostics(self):
        self.assertTrue(self.run_helper("{not-json", expected=2)["findings"])


if __name__ == "__main__":
    unittest.main()
