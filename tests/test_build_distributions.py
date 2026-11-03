"""Tests for library/organization/skills/build-distributions.py."""

from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


# ---------------------------------------------------------------------------
# Load the module under test without relying on installed packages
# ---------------------------------------------------------------------------

def _load_build_distributions():
    spec_path = (
        Path(__file__).resolve().parents[1]
        / "library"
        / "organization"
        / "skills"
        / "build-distributions.py"
    )
    spec = importlib.util.spec_from_file_location("build_distributions", spec_path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


try:
    bd = _load_build_distributions()
except Exception as exc:
    raise ImportError(f"Cannot load build-distributions.py: {exc}") from exc


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _make_skill(root: Path, skill_name: str, domain: str = "domain") -> Path:
    """Create a minimal canonical skill tree in *root* and return its directory."""
    skill_dir = root / "library" / "organization" / "skills" / domain / skill_name
    _write(
        skill_dir / "SKILL.md",
        f"""\
---
name: {skill_name}
description: Test skill for {skill_name}. Use when validating distributions.
license: MIT
metadata:
  aether-version: "1.2.3"
  aether-status: "draft"
  aether-spec-id: "example-spec"
  aether-scope: "organization"
  aether-domain: "architecture"
  aether-owners: "egohygiene"
  aether-created: "2026-08-01"
  aether-updated: "2026-08-01"
---

# {skill_name}

A test skill.
""",
    )
    _write(skill_dir / "evals" / "evals.json", '{"version": 1, "cases": []}\n')
    _write(skill_dir / "references" / "guide.md", "# Guide\n")
    _write(skill_dir / "templates" / "output.template.md", "# Template\n")
    return skill_dir


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestFindSkills(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp(prefix="aether-bd-test-"))
        # Monkey-patch SKILLS_DIR so the module uses our temp tree
        self._orig_skills_dir = bd.SKILLS_DIR
        self._orig_dist_dir = bd.DIST_DIR
        bd.SKILLS_DIR = self._tmp / "library" / "organization" / "skills"
        bd.DIST_DIR = self._tmp / "dist" / "skills"
        bd.REPO_ROOT = self._tmp

    def tearDown(self):
        bd.SKILLS_DIR = self._orig_skills_dir
        bd.DIST_DIR = self._orig_dist_dir
        bd.REPO_ROOT = Path(__file__).resolve().parents[1]

    def test_finds_skills_sorted(self):
        _make_skill(self._tmp, "beta-skill")
        _make_skill(self._tmp, "alpha-skill")
        skills = bd.find_skills()
        names = [n for n, _ in skills]
        self.assertEqual(names, sorted(names))

    def test_ignores_non_skill_dirs(self):
        # Create a directory without SKILL.md
        (self._tmp / "library" / "organization" / "skills" / "domain" / "no-skill").mkdir(
            parents=True, exist_ok=True
        )
        _make_skill(self._tmp, "real-skill")
        skills = bd.find_skills()
        names = [n for n, _ in skills]
        self.assertIn("real-skill", names)
        self.assertNotIn("no-skill", names)


class TestSourceDigest(unittest.TestCase):
    def test_lf_normalised(self):
        tmp = Path(tempfile.mkdtemp(prefix="aether-bd-digest-"))
        lf_file = tmp / "lf.md"
        crlf_file = tmp / "crlf.md"
        content = "---\nname: test\n---\n\nBody\n"
        lf_file.write_text(content, encoding="utf-8")
        crlf_file.write_bytes(content.replace("\n", "\r\n").encode("utf-8"))
        self.assertEqual(bd._source_digest(lf_file), bd._source_digest(crlf_file))

    def test_digest_is_64_hex_chars(self):
        tmp = Path(tempfile.mkdtemp(prefix="aether-bd-digest2-"))
        f = tmp / "file.md"
        f.write_text("hello\n", encoding="utf-8")
        digest = bd._source_digest(f)
        self.assertRegex(digest, r"^[a-f0-9]{64}$")


class TestBuildManifest(unittest.TestCase):
    def _make_source(self) -> Path:
        tmp = Path(tempfile.mkdtemp(prefix="aether-bd-manifest-"))
        src = tmp / "SKILL.md"
        src.write_text(
            "---\nname: test-skill\ndescription: x\nmetadata:\n  aether-version: \"2.3.4\"\n---\nbody\n",
            encoding="utf-8",
        )
        return src

    def test_manifest_schema_version(self):
        src = self._make_source()
        fm = {"metadata": {"aether-version": "2.3.4"}}
        manifest = bd._build_manifest("test-skill", fm, src, ["dist/skills/test-skill/SKILL.md"])
        self.assertEqual(manifest["schema_version"], "aether.distribution-manifest/v1")

    def test_manifest_artifact_id(self):
        src = self._make_source()
        fm = {}
        manifest = bd._build_manifest("my-skill", fm, src, [])
        self.assertEqual(manifest["artifact_id"], "skill/my-skill")

    def test_manifest_distribution_id(self):
        src = self._make_source()
        fm = {}
        manifest = bd._build_manifest("my-skill", fm, src, [])
        self.assertEqual(manifest["distribution_id"], "distribution/my-skill")

    def test_manifest_source_digest_algorithm(self):
        src = self._make_source()
        fm = {}
        manifest = bd._build_manifest("my-skill", fm, src, [])
        self.assertEqual(manifest["source_digest"]["algorithm"], "sha256-utf8-lf")

    def test_manifest_source_digest_value_matches(self):
        src = self._make_source()
        fm = {}
        manifest = bd._build_manifest("my-skill", fm, src, [])
        expected = bd._source_digest(src)
        self.assertEqual(manifest["source_digest"]["value"], expected)

    def test_manifest_version_from_frontmatter(self):
        src = self._make_source()
        fm = {"metadata": {"aether-version": "3.1.0"}}
        manifest = bd._build_manifest("x", fm, src, [])
        self.assertEqual(manifest["artifact_version"], "3.1.0")

    def test_manifest_compatibility_default(self):
        src = self._make_source()
        fm = {}
        manifest = bd._build_manifest("x", fm, src, [])
        self.assertEqual(manifest["compatibility"], {"required_tools": []})

    def test_manifest_generator_field(self):
        src = self._make_source()
        fm = {}
        manifest = bd._build_manifest("x", fm, src, [])
        self.assertEqual(manifest["generator"], bd.GENERATOR_ID)


class TestBuildSkillDist(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp(prefix="aether-bd-dist-"))
        self._orig_repo_root = bd.REPO_ROOT
        bd.REPO_ROOT = self._tmp

    def tearDown(self):
        bd.REPO_ROOT = self._orig_repo_root

    def test_outputs_skill_md(self):
        skill_dir = _make_skill(self._tmp, "my-skill")
        file_map = bd._build_skill_dist("my-skill", skill_dir)
        self.assertIn("dist/skills/my-skill/SKILL.md", file_map)

    def test_outputs_companion_files(self):
        skill_dir = _make_skill(self._tmp, "my-skill")
        file_map = bd._build_skill_dist("my-skill", skill_dir)
        self.assertIn("dist/skills/my-skill/evals/evals.json", file_map)
        self.assertIn("dist/skills/my-skill/references/guide.md", file_map)
        self.assertIn("dist/skills/my-skill/templates/output.template.md", file_map)

    def test_python_execution_caches_do_not_change_distribution(self):
        skill_dir = _make_skill(self._tmp, "my-skill")
        scripts = skill_dir / "scripts"
        scripts.mkdir()
        (scripts / "check.py").write_text("print('check')\n")
        before = bd._build_skill_dist("my-skill", skill_dir)
        (scripts / "__pycache__").mkdir()
        (scripts / "__pycache__/check.cpython-312.pyc").write_bytes(b"generated cache")
        (scripts / "check.pyc").write_bytes(b"legacy cache")
        self.assertEqual(before, bd._build_skill_dist("my-skill", skill_dir))

    def test_outputs_manifest(self):
        skill_dir = _make_skill(self._tmp, "my-skill")
        file_map = bd._build_skill_dist("my-skill", skill_dir)
        manifest_key = "dist/skills/my-skill/distribution-manifest.v1.json"
        self.assertIn(manifest_key, file_map)
        manifest = json.loads(file_map[manifest_key].decode("utf-8"))
        self.assertEqual(manifest["schema_version"], "aether.distribution-manifest/v1")

    def test_skill_md_content_matches_canonical(self):
        skill_dir = _make_skill(self._tmp, "my-skill")
        canonical = (skill_dir / "SKILL.md").read_bytes()
        file_map = bd._build_skill_dist("my-skill", skill_dir)
        # Normalized bytes
        normalized = canonical.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        self.assertEqual(file_map["dist/skills/my-skill/SKILL.md"], normalized)

    def test_manifest_generated_paths_includes_all_files(self):
        skill_dir = _make_skill(self._tmp, "my-skill")
        file_map = bd._build_skill_dist("my-skill", skill_dir)
        manifest = json.loads(
            file_map["dist/skills/my-skill/distribution-manifest.v1.json"].decode("utf-8")
        )
        for path_key in file_map:
            self.assertIn(path_key, manifest["generated_paths"])

    def test_deterministic_across_two_calls(self):
        skill_dir = _make_skill(self._tmp, "my-skill")
        map1 = bd._build_skill_dist("my-skill", skill_dir)
        map2 = bd._build_skill_dist("my-skill", skill_dir)
        self.assertEqual(map1, map2)

    def test_packages_declared_repository_resource(self):
        skill_dir = _make_skill(self._tmp, "my-skill")
        resource = self._tmp / "catalog" / "example.v1.json"
        _write(resource, '{"version": 1}\n')
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8").replace(
                "  aether-updated: \"2026-08-01\"\n",
                "  aether-updated: \"2026-08-01\"\n"
                "  aether-distribution-resources:\n"
                "    - source: \"catalog/example.v1.json\"\n"
                "      destination: \"references/example.v1.json\"\n",
            ),
            encoding="utf-8",
        )
        file_map = bd._build_skill_dist("my-skill", skill_dir)
        self.assertEqual(
            file_map["dist/skills/my-skill/references/example.v1.json"],
            b'{"version": 1}\n',
        )

    def test_rejects_distribution_resource_path_escape(self):
        skill_dir = _make_skill(self._tmp, "my-skill")
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8").replace(
                "  aether-updated: \"2026-08-01\"\n",
                "  aether-updated: \"2026-08-01\"\n"
                "  aether-distribution-resources:\n"
                "    - source: \"../outside.json\"\n"
                "      destination: \"references/example.v1.json\"\n",
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(ValueError, "escapes repository"):
            bd._build_skill_dist("my-skill", skill_dir)


class TestBuildIntegration(unittest.TestCase):
    """End-to-end: build() writes correct files to a temp dist dir."""

    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp(prefix="aether-bd-e2e-"))
        self._orig_skills_dir = bd.SKILLS_DIR
        self._orig_dist_dir = bd.DIST_DIR
        self._orig_repo_root = bd.REPO_ROOT
        bd.SKILLS_DIR = self._tmp / "library" / "organization" / "skills"
        bd.DIST_DIR = self._tmp / "dist" / "skills"
        bd.REPO_ROOT = self._tmp

    def tearDown(self):
        bd.SKILLS_DIR = self._orig_skills_dir
        bd.DIST_DIR = self._orig_dist_dir
        bd.REPO_ROOT = self._orig_repo_root

    def test_build_creates_dist_files(self):
        _make_skill(self._tmp, "alpha-skill")
        _make_skill(self._tmp, "beta-skill")
        rc = bd.build(check=False)
        self.assertEqual(rc, 0)
        self.assertTrue((self._tmp / "dist" / "skills" / "alpha-skill" / "SKILL.md").exists())
        self.assertTrue((self._tmp / "dist" / "skills" / "beta-skill" / "SKILL.md").exists())

    def test_check_passes_after_build(self):
        _make_skill(self._tmp, "alpha-skill")
        bd.build(check=False)
        rc = bd.build(check=True)
        self.assertEqual(rc, 0)

    def test_check_detects_missing_file(self):
        _make_skill(self._tmp, "alpha-skill")
        bd.build(check=False)
        # Remove a generated file to simulate drift
        (self._tmp / "dist" / "skills" / "alpha-skill" / "SKILL.md").unlink()
        rc = bd.build(check=True)
        self.assertNotEqual(rc, 0)

    def test_check_detects_stale_content(self):
        _make_skill(self._tmp, "alpha-skill")
        bd.build(check=False)
        # Corrupt the distribution
        stale = self._tmp / "dist" / "skills" / "alpha-skill" / "SKILL.md"
        stale.write_text("stale content\n", encoding="utf-8")
        rc = bd.build(check=True)
        self.assertNotEqual(rc, 0)

    def test_idempotent_rebuild(self):
        _make_skill(self._tmp, "alpha-skill")
        bd.build(check=False)
        contents_before = {}
        for f in (self._tmp / "dist" / "skills").rglob("*"):
            if f.is_file():
                contents_before[str(f)] = f.read_bytes()
        self.assertEqual(0, bd.build(check=False))
        contents_after = {}
        for f in (self._tmp / "dist" / "skills").rglob("*"):
            if f.is_file():
                contents_after[str(f)] = f.read_bytes()
        self.assertEqual(contents_before, contents_after)
        self.assertEqual(0, bd.build(check=True))

    def test_build_honors_custom_output_directory(self):
        _make_skill(self._tmp, "alpha-skill")
        custom_output = self._tmp / "custom-dist"
        rc = bd.build(check=False, output_directory=custom_output)
        self.assertEqual(rc, 0)
        self.assertTrue((custom_output / "skills" / "alpha-skill" / "SKILL.md").exists())

    def test_required_resource_failure_is_nonzero_even_with_partial_success(self):
        _make_skill(self._tmp, "alpha-skill")
        broken = _make_skill(self._tmp, "broken-skill") / "SKILL.md"
        broken.write_text(broken.read_text().replace(
            "metadata:\n",
            "metadata:\n  aether-distribution-resources:\n"
            "    - source: missing-resource.json\n"
            "      destination: references/resource.json\n",
        ))
        for check in (False, True):
            with self.subTest(check=check):
                output = io.StringIO()
                with contextlib.redirect_stderr(output):
                    self.assertNotEqual(0, bd.build(check=check))
                self.assertIn("broken-skill generation", output.getvalue())
                self.assertIn("1/2 artifact(s) generated", output.getvalue())
                self.assertTrue((self._tmp / "dist/skills/alpha-skill/SKILL.md").is_file())

    def test_unknown_inventory_is_detected_and_retained_in_custom_output(self):
        _make_skill(self._tmp, "alpha-skill")
        output = self._tmp / "custom-dist"
        self.assertEqual(0, bd.build(output_directory=output))
        _write(output / "skills/removed-skill/SKILL.md", "obsolete\n")
        _write(output / "skills/alpha-skill/references/user-note.md", "keep me\n")
        (output / "skills/empty-package").mkdir()
        _write(output / "personal-note.txt", "outside generator ownership\n")
        before = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
        for check in (True, False):
            with self.subTest(check=check):
                self.assertNotEqual(0, bd.build(check=check, output_directory=output))
                after = {p.relative_to(output): p.read_bytes() for p in output.rglob("*") if p.is_file()}
                self.assertEqual(before, after)
                self.assertTrue((output / "skills/empty-package").is_dir())

    def test_removing_last_skill_does_not_bypass_inventory_check(self):
        skill = _make_skill(self._tmp, "alpha-skill")
        self.assertEqual(0, bd.build())
        shutil.rmtree(skill)
        self.assertNotEqual(0, bd.build(check=True))
        self.assertTrue((self._tmp / "dist/skills/alpha-skill/SKILL.md").is_file())

    def test_missing_source_directory_and_output_io_failures_are_nonzero(self):
        self.assertNotEqual(0, bd.build())
        self.assertNotEqual(0, bd.build(check=True))
        _make_skill(self._tmp, "alpha-skill")
        (self._tmp / "dist/skills/alpha-skill/SKILL.md").mkdir(parents=True)
        self.assertNotEqual(0, bd.build())
        self.assertNotEqual(0, bd.build(check=True))

    def test_companion_file_and_directory_symlinks_do_not_read_external_bytes(self):
        for directory_link in (False, True):
            with self.subTest(directory_link=directory_link), tempfile.TemporaryDirectory() as foreign:
                skill = _make_skill(self._tmp, "linked-skill")
                sentinel = Path(foreign) / "sentinel.txt"
                sentinel.write_text("harmless outside-source sentinel\n", encoding="utf-8")
                link = skill / "references" / "linked"
                link.symlink_to(Path(foreign) if directory_link else sentinel, target_is_directory=directory_link)
                original = Path.read_bytes
                outside_reads = []
                def guarded_read(path):
                    if path.resolve() == sentinel.resolve():
                        outside_reads.append(path)
                        raise AssertionError("outside-source bytes must not be read")
                    return original(path)
                try:
                    with mock.patch.object(Path, "read_bytes", guarded_read):
                        for check in (False, True):
                            self.assertNotEqual(0, bd.build(check=check))
                    self.assertEqual([], outside_reads)
                    self.assertEqual("harmless outside-source sentinel\n", sentinel.read_text())
                finally:
                    link.unlink()

    def test_output_symlinks_are_rejected_without_reading_or_replacing_their_targets(self):
        _make_skill(self._tmp, "linked-skill")
        with tempfile.TemporaryDirectory() as foreign:
            sentinel = Path(foreign) / "sentinel.txt"
            sentinel.write_text("keep outside output unchanged\n", encoding="utf-8")
            output = self._tmp / "custom-dist"
            link = output / "skills/linked-skill/SKILL.md"
            link.parent.mkdir(parents=True)
            link.symlink_to(sentinel)
            for check in (False, True):
                self.assertNotEqual(0, bd.build(check=check, output_directory=output))
                self.assertEqual("keep outside output unchanged\n", sentinel.read_text())
            link.unlink()
            shutil.rmtree(output / "skills")
            (output / "skills").symlink_to(Path(foreign), target_is_directory=True)
            for check in (False, True):
                self.assertNotEqual(0, bd.build(check=check, output_directory=output))
            self.assertEqual([sentinel], list(Path(foreign).iterdir()))

    def test_symlinked_skill_source_is_rejected_before_reading(self):
        skill = _make_skill(self._tmp, "linked-skill")
        with tempfile.TemporaryDirectory() as foreign:
            target = Path(foreign) / "SKILL.md"
            target.write_text((skill / "SKILL.md").read_text(), encoding="utf-8")
            (skill / "SKILL.md").unlink()
            (skill / "SKILL.md").symlink_to(target)
            for check in (False, True):
                self.assertNotEqual(0, bd.build(check=check))


if __name__ == "__main__":
    unittest.main()
