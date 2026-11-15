"""Tests for release metadata and distribution CLI helpers."""

from __future__ import annotations

import importlib.util
import hashlib
import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock


def _load_module(name: str, relative_path: str):
    repo_root = Path(__file__).resolve().parents[1]
    module_path = repo_root / relative_path
    spec = importlib.util.spec_from_file_location(name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


av = _load_module("aether_validator_module", "aether_validator.py")
bp = _load_module(
    "build_projections_module",
    "library/organization/agents/build-projections.py",
)
br = _load_module(
    "build_release_artifacts_module",
    "library/organization/skills/build-release-artifacts.py",
)


class TestDistributionBuildCommand(unittest.TestCase):
    def test_generator_failure_survives_later_successful_generators(self):
        for check in (False, True):
            for failed_generator in (0, 1):
                with self.subTest(check=check, failed_generator=failed_generator):
                    args = type("Args", (), {
                        "repo_root": "/tmp/example-repo",
                        "output_directory": "custom-dist",
                        "check": check,
                    })()
                    results = [0, 0, 0, 0]
                    results[failed_generator] = 1
                    with mock.patch.object(av, "find_repo_root", return_value=Path("/tmp/example-repo")):
                        with mock.patch.object(av, "_run_python_script", side_effect=results) as run_script:
                            self.assertNotEqual(0, av.command_distribution_build(args))
                    self.assertEqual(4, run_script.call_count)
                    self.assertTrue(all(call.kwargs["check"] == check for call in run_script.call_args_list))

    def test_distribution_build_runs_all_generators(self):
        args = type(
            "Args",
            (),
            {
                "repo_root": "/tmp/example-repo",
                "output_directory": "dist-out",
                "check": True,
            },
        )()
        with mock.patch.object(av, "find_repo_root", return_value=Path("/tmp/example-repo")):
            with mock.patch.object(av, "_run_python_script", return_value=0) as run_script:
                rc = av.command_distribution_build(args)

        self.assertEqual(rc, 0)
        self.assertEqual(run_script.call_count, 4)
        calls = run_script.call_args_list
        self.assertTrue(str(calls[0].args[0]).endswith("specs/build-distributions.py"))
        self.assertTrue(str(calls[1].args[0]).endswith("skills/build-distributions.py"))
        self.assertTrue(str(calls[2].args[0]).endswith("build-projections.py"))
        self.assertTrue(str(calls[3].args[0]).endswith("social-surfaces/build-distribution.py"))
        self.assertTrue(all(call.kwargs["check"] for call in calls))
        self.assertTrue(all(call.kwargs["output_directory"] == "dist-out" for call in calls))


class TestBuildProjections(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp(prefix="aether-bp-test-"))
        self._orig_agents_dir = bp.AGENTS_DIR
        self._orig_repo_root = bp.REPO_ROOT
        bp.AGENTS_DIR = self._tmp / "library" / "organization" / "agents"
        bp.REPO_ROOT = self._tmp

    def tearDown(self):
        bp.AGENTS_DIR = self._orig_agents_dir
        bp.REPO_ROOT = self._orig_repo_root

    def test_writes_to_custom_output_directory(self):
        agent_dir = bp.AGENTS_DIR / "test-agent"
        agent_dir.mkdir(parents=True, exist_ok=True)
        (agent_dir / "AGENT.md").write_text(
            "---\n"
            "name: Test agent\n"
            "description: Example\n"
            "tools:\n"
            "  - read\n"
            "aether-id: test-agent\n"
            "metadata:\n"
            "  aether-version: 1.0.0\n"
            "---\n"
            "\n## Mission\n\n"
            "Use [skill](../../skills/quality/test-engineering/SKILL.md) and "
            "[spec](../../specs/quality/auditor.spec.md).\n",
            encoding="utf-8",
        )

        output_directory = self._tmp / "custom-dist"
        rc = bp.build(check=False, output_directory=output_directory)

        self.assertEqual(rc, 0)
        self.assertTrue(
            (
                output_directory
                / "github"
                / "repository"
                / ".github"
                / "agents"
                / "test-agent.agent.md"
            ).exists()
        )
        projected = (
            output_directory
            / "github"
            / "repository"
            / ".github"
            / "agents"
            / "test-agent.agent.md"
        ).read_text(encoding="utf-8")
        self.assertIn(".agents/skills/test-engineering/SKILL.md", projected)
        self.assertIn(".github/specs/quality/auditor.spec.md", projected)
        self.assertTrue(
            (
                output_directory
                / "github"
                / "organization"
                / "agents"
                / "test-agent.agent.md"
            ).exists()
        )


class TestBuildReleaseArtifacts(unittest.TestCase):
    def setUp(self):
        self._tmp = Path(tempfile.mkdtemp(prefix="aether-release-test-"))
        self.addCleanup(__import__("shutil").rmtree, self._tmp)
        self.output_directory = self._tmp / "dist"
        skill_dir = self.output_directory / "skills" / "example-skill"
        skill_dir.mkdir(parents=True, exist_ok=True)
        manifest = {
            "schema_version": "aether.distribution-manifest/v1",
            "distribution_id": "distribution/example-skill",
            "artifact_id": "skill/example-skill",
            "artifact_version": "1.2.3",
            "source_digest": {
                "algorithm": "sha256-utf8-lf",
                "value": "a" * 64,
            },
            "generated_paths": [
                "dist/skills/example-skill/SKILL.md",
                "dist/skills/example-skill/distribution-manifest.v1.json",
            ],
            "generator": "test",
            "compatibility": {"required_tools": []},
        }
        (skill_dir / "SKILL.md").write_text("# Example\n", encoding="utf-8")
        (skill_dir / "distribution-manifest.v1.json").write_text(
            json.dumps(manifest, indent=2) + "\n",
            encoding="utf-8",
        )

        catalog = {
            "schema_version": "aether.artifact-catalog/v1",
            "artifacts": [
                {
                    "id": "skill/example-skill",
                    "kind": "skill",
                    "artifact_version": "1.2.3",
                    "license": "MIT",
                    "lifecycle": {"state": "stable"},
                    "release": {"included": True},
                    "source_digest": {
                        "algorithm": "sha256-utf8-lf",
                        "value": "a" * 64,
                    },
                }
            ],
        }

        self.catalog_path = self._tmp / "catalog.json"
        self.catalog_path.write_text(json.dumps(catalog, indent=2) + "\n", encoding="utf-8")
        self.license_path = self._tmp / "LICENSE"
        self.license_path.write_text("MIT License\n", encoding="utf-8")
        self.changelog_path = self._tmp / "CHANGELOG.md"
        self.changelog_path.write_text(
            "# Changelog\n\n## [Unreleased]\n\n- Example release notes.\n\n## [1.0.0] - 2026-01-01\n\n- Done.\n",
            encoding="utf-8",
        )

        repo_root = Path(__file__).resolve().parents[1]
        self.schema_path = (
            repo_root / "catalog" / "schemas" / "aether.release-manifest.v1.schema.json"
        )

        self._orig_catalog_path = br.CATALOG_PATH
        self._orig_license_path = br.LICENSE_PATH
        self._orig_changelog_path = br.CHANGELOG_PATH
        self._orig_schema_path = br.RELEASE_SCHEMA_PATH
        self._orig_social_catalog_path = br.SOCIAL_SURFACE_CATALOG_PATH
        br.CATALOG_PATH = self.catalog_path
        br.LICENSE_PATH = self.license_path
        br.CHANGELOG_PATH = self.changelog_path
        br.RELEASE_SCHEMA_PATH = self.schema_path
        br.SOCIAL_SURFACE_CATALOG_PATH = self._tmp / "social-catalog.json"
        br.SOCIAL_SURFACE_CATALOG_PATH.write_text(
            json.dumps(
                {
                    "catalog": {
                        "id": "catalog/social-surface-specs",
                        "version": "1.0.0",
                        "lifecycle": {"state": "experimental"},
                        "rights_review": {"state": "pending"},
                        "release": {"included": False}
                    }
                }
            ) + "\n",
            encoding="utf-8",
        )

    def tearDown(self):
        br.CATALOG_PATH = self._orig_catalog_path
        br.LICENSE_PATH = self._orig_license_path
        br.CHANGELOG_PATH = self._orig_changelog_path
        br.RELEASE_SCHEMA_PATH = self._orig_schema_path
        br.SOCIAL_SURFACE_CATALOG_PATH = self._orig_social_catalog_path

    def test_build_release_artifacts_writes_expected_files(self):
        release_dir = br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)

        manifest = json.loads((release_dir / "release-manifest.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["repository_release_tag"], "v1.2.3")
        self.assertEqual(manifest["artifacts"][0]["artifact_id"], "skill/example-skill")
        self.assertTrue((release_dir / "checksums.txt").exists())
        self.assertTrue((release_dir / "release-provenance.v1.json").exists())
        self.assertIn("Example release notes.", (release_dir / "release-notes.md").read_text(encoding="utf-8"))
        self.assertIn("MIT License", (release_dir / "LICENSE.notices.txt").read_text(encoding="utf-8"))

    def test_build_release_artifacts_requires_release_eligible_skills(self):
        self.catalog_path.write_text(
            json.dumps({"schema_version": "aether.artifact-catalog/v1", "artifacts": []}, indent=2) + "\n",
            encoding="utf-8",
        )

        with self.assertRaises(ValueError):
            br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)

    def test_stable_rights_approved_catalog_is_included(self):
        catalog_dir = self.output_directory / "catalogs" / "social-surface-specs"
        catalog_dir.mkdir(parents=True, exist_ok=True)
        (catalog_dir / "distribution-manifest.v1.json").write_text(
            json.dumps(
                {
                    "catalog_id": "catalog/social-surface-specs",
                    "catalog_version": "1.0.0",
                    "catalog_digest": {"algorithm": "sha256-utf8-lf", "value": "b" * 64},
                    "generated_paths": ["dist/catalogs/social-surface-specs/distribution-manifest.v1.json",
                                        "dist/catalogs/social-surface-specs/catalog.v1.json"]
                }
            ) + "\n",
            encoding="utf-8",
        )
        (catalog_dir / "catalog.v1.json").write_text('{"synthetic": true}\n', encoding="utf-8")
        br.SOCIAL_SURFACE_CATALOG_PATH.write_text(
            json.dumps(
                {
                    "catalog": {
                        "id": "catalog/social-surface-specs",
                        "version": "1.0.0",
                        "lifecycle": {"state": "stable"},
                        "rights_review": {"state": "approved"},
                        "release": {"included": True}
                    }
                }
            ) + "\n",
            encoding="utf-8",
        )

        release_dir = br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)
        manifest = json.loads((release_dir / "release-manifest.v1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["catalogs"][0]["catalog_id"], "catalog/social-surface-specs")
        payload = self._tmp / "catalog-payload"
        archive = self._tmp / "catalog.tar.gz"
        br.build_release_payload(self.output_directory, payload, archive)
        with tarfile.open(archive) as bundle:
            self.assertIn("catalogs/social-surface-specs/catalog.v1.json", bundle.getnames())

    def test_metadata_and_archive_repeat_exactly_without_prior_self_hashes(self):
        first = br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)
        before = {p.name: p.read_bytes() for p in first.iterdir()}
        (first / "prior-unselected.tar.gz").write_bytes(b"old output must not become input")
        br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)
        self.assertEqual(before, {name: (first / name).read_bytes() for name in before})
        provenance = json.loads((first / "release-provenance.v1.json").read_text())
        self.assertEqual("d" * 40, provenance["commit_sha"])
        provenance_paths = {item["path"] for item in provenance["output_files"]}
        self.assertNotIn("release/release-provenance.v1.json", provenance_paths)
        self.assertNotIn("release/checksums.txt", provenance_paths)
        for entry in provenance["output_files"]:
            self.assertEqual(entry["sha256"], hashlib.sha256(
                (self.output_directory / entry["path"]).read_bytes()).hexdigest())
        checksums = {}
        for line in (first / "checksums.txt").read_text().splitlines():
            digest, path = line.split("  ", 1)
            checksums[path] = digest
            self.assertEqual(digest, hashlib.sha256((self.output_directory / path).read_bytes()).hexdigest())
        self.assertIn("release/release-provenance.v1.json", checksums)
        self.assertNotIn("release/checksums.txt", checksums)
        archives = []
        for index in (1, 2):
            payload = self._tmp / f"payload-{index}"
            archive = self._tmp / f"archive-{index}.tar.gz"
            br.build_release_payload(self.output_directory, payload, archive)
            archives.append(archive.read_bytes())
            with tarfile.open(archive) as bundle:
                names = set(bundle.getnames())
                self.assertEqual(set(checksums) | {"release/checksums.txt"}, names)
                for member in bundle.getmembers():
                    self.assertEqual((0, 0, 0, "", ""),
                                     (member.mtime, member.uid, member.gid, member.uname, member.gname))
        self.assertEqual(*archives)

    def test_unselected_drafts_projections_and_extra_files_never_enter_channel(self):
        for relative in ("skills/draft-skill/SKILL.md", "github/repository/draft.agent.md",
                         "skills/example-skill/unlisted-secret.txt"):
            path = self.output_directory / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("synthetic excluded fixture\n")
        br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)
        payload, archive = self._tmp / "selected", self._tmp / "selected.tar.gz"
        br.build_release_payload(self.output_directory, payload, archive)
        with tarfile.open(archive) as bundle:
            names = bundle.getnames()
            self.assertEqual(7, len(names))
            self.assertTrue(all(name.startswith(("release/", "skills/example-skill/")) for name in names))
            self.assertFalse(any("draft" in name or "secret" in name for name in names))
        self.assertTrue((self.output_directory / "skills/draft-skill/SKILL.md").exists())

    def test_manifest_escape_symlink_and_special_file_fail_closed(self):
        manifest_path = self.output_directory / "skills/example-skill/distribution-manifest.v1.json"
        original = json.loads(manifest_path.read_text())
        for bad in ("dist/skills/example-skill/../draft/SKILL.md", "/tmp/private",
                    "dist/skills/draft/SKILL.md", "dist/skills/example-skill/./SKILL.md"):
            manifest = {**original, "generated_paths": [*original["generated_paths"], bad]}
            manifest_path.write_text(json.dumps(manifest))
            with self.subTest(path=bad), self.assertRaises(ValueError):
                br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)
        manifest_path.write_text(json.dumps(original))
        entry = manifest_path.parent / "SKILL.md"
        entry.unlink()
        private = self._tmp / "private.txt"
        private.write_text("synthetic private fixture")
        entry.symlink_to(private)
        with self.assertRaises(ValueError):
            br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)
        entry.unlink()
        __import__("os").mkfifo(entry)
        with self.assertRaises(ValueError):
            br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)

    def test_destinations_do_not_overwrite_existing_data(self):
        br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)
        for payload, archive in ((self.output_directory / "nested", self._tmp / "nested.tar.gz"),
                                 (self._tmp / "existing", self._tmp / "existing/archive.tar.gz")):
            with self.assertRaises(ValueError):
                br.build_release_payload(self.output_directory, payload, archive)
        payload, archive = self._tmp / "unused", self._tmp / "existing.tar.gz"
        archive.write_bytes(b"caller-owned")
        with self.assertRaises(ValueError):
            br.build_release_payload(self.output_directory, payload, archive)
        self.assertEqual(b"caller-owned", archive.read_bytes())
        self.assertFalse(payload.exists())

    def test_changelog_boundaries_and_full_source_identity(self):
        self.assertEqual("## [Unreleased]\n\n- Example release notes.",
                         br._extract_unreleased_changelog(self.changelog_path))
        for tag, commit in (("main", "d" * 40), ("v01.2.3", "d" * 40), ("v1.2.3", "unknown")):
            with self.subTest(tag=tag, commit=commit), self.assertRaises(ValueError):
                br.build_release_artifacts(tag, self.output_directory, commit)

    def test_stale_metadata_cannot_package_mutated_source(self):
        br.build_release_artifacts("v1.2.3", self.output_directory, "d" * 40)
        (self.output_directory / "skills/example-skill/SKILL.md").write_text("changed after metadata\n")
        payload, archive = self._tmp / "stale", self._tmp / "stale.tar.gz"
        with self.assertRaisesRegex(ValueError, "checksums differ"):
            br.build_release_payload(self.output_directory, payload, archive)
        self.assertFalse(payload.exists())
        self.assertFalse(archive.exists())


if __name__ == "__main__":
    unittest.main()
