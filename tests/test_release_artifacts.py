"""Tests for release metadata and distribution CLI helpers."""

from __future__ import annotations

import importlib.util
import json
import sys
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
        self.assertEqual(run_script.call_count, 3)
        calls = run_script.call_args_list
        self.assertTrue(str(calls[0].args[0]).endswith("specs/build-distributions.py"))
        self.assertTrue(str(calls[1].args[0]).endswith("skills/build-distributions.py"))
        self.assertTrue(str(calls[2].args[0]).endswith("build-projections.py"))
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
            "# Changelog\n\n## Unreleased\n\n- Example release notes.\n\n## Older\n\n- Done.\n",
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
        br.CATALOG_PATH = self.catalog_path
        br.LICENSE_PATH = self.license_path
        br.CHANGELOG_PATH = self.changelog_path
        br.RELEASE_SCHEMA_PATH = self.schema_path

    def tearDown(self):
        br.CATALOG_PATH = self._orig_catalog_path
        br.LICENSE_PATH = self._orig_license_path
        br.CHANGELOG_PATH = self._orig_changelog_path
        br.RELEASE_SCHEMA_PATH = self._orig_schema_path

    def test_build_release_artifacts_writes_expected_files(self):
        release_dir = br.build_release_artifacts("v1.2.3", self.output_directory, "deadbeef")

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
            br.build_release_artifacts("v1.2.3", self.output_directory, "deadbeef")


if __name__ == "__main__":
    unittest.main()
