"""Tests for the repository release contract and Aether's own declaration."""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:  # The portable validator intentionally supports stdlib-only use.
    Draft202012Validator = None


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "catalog" / "schemas" / "aether.repository-release.v1.schema.json"
DECLARATION_PATH = ROOT / ".egohygiene" / "release.json"
VALIDATOR_PATH = ROOT / "library" / "organization" / "specs" / "release" / "validate.py"

SPEC = importlib.util.spec_from_file_location("repository_release_validator", VALIDATOR_PATH)
assert SPEC is not None
assert SPEC.loader is not None
release_validator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release_validator)


class RepositoryReleaseContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.declaration = json.loads(DECLARATION_PATH.read_text(encoding="utf-8"))

    def schema_errors(self, data: dict) -> list:
        if Draft202012Validator is not None:
            return list(Draft202012Validator(self.schema).iter_errors(data))
        return release_validator._basic_schema_errors(data)

    def test_aether_declaration_is_schema_valid_and_locally_complete(self) -> None:
        self.assertEqual(self.schema_errors(self.declaration), [])
        result = release_validator.validate_release_declaration(ROOT, release_version="v1.2.3")
        self.assertEqual(result["repository"]["id"], "egohygiene/aether")
        self.assertEqual(result["repository"]["release_profile"], "contract")

    def test_invalid_fixture_fails_schema_validation(self) -> None:
        fixture = json.loads(
            (
                ROOT
                / "catalog"
                / "fixtures"
                / "aether.repository-release.v1.schema"
                / "invalid.json"
            ).read_text(encoding="utf-8")
        )
        self.assertTrue(self.schema_errors(fixture))

    def test_profile_examples_are_schema_valid(self) -> None:
        examples = sorted(
            (
                ROOT
                / "catalog"
                / "fixtures"
                / "aether.repository-release.v1.schema"
                / "examples"
            ).glob("*.json")
        )
        self.assertEqual(
            {path.stem for path in examples},
            {
                "archived",
                "container-image",
                "contract-only",
                "npm-react",
                "publication",
                "rust-cli",
                "static-site",
                "workspace",
            },
        )
        for path in examples:
            with self.subTest(example=path.stem):
                self.assertEqual(self.schema_errors(json.loads(path.read_text(encoding="utf-8"))), [])

    def test_reference_validator_requires_an_unreleased_changelog_heading(self) -> None:
        temporary = Path(tempfile.mkdtemp(prefix="aether-release-contract-"))
        (temporary / ".egohygiene").mkdir()
        (temporary / ".github" / "workflows").mkdir(parents=True)
        (temporary / "Taskfile.yml").write_text("version: \"3\"\n", encoding="utf-8")
        (temporary / ".github" / "workflows" / "release.yml").write_text("name: Release\n", encoding="utf-8")
        (temporary / "Cargo.toml").write_text("[package]\n", encoding="utf-8")
        (temporary / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
        declaration = json.loads(
            (
                ROOT
                / "catalog"
                / "fixtures"
                / "aether.repository-release.v1.schema"
                / "valid.json"
            ).read_text(encoding="utf-8")
        )
        (temporary / ".egohygiene" / "release.json").write_text(
            json.dumps(declaration, indent=2) + "\n", encoding="utf-8"
        )

        with self.assertRaisesRegex(release_validator.ReleaseContractError, "Unreleased heading"):
            release_validator.validate_release_declaration(temporary)

    def test_plan_output_is_deterministic_and_non_publishing(self) -> None:
        data = release_validator.validate_release_declaration(ROOT, release_version="v1.2.3")
        first = release_validator.render_plan(data, "v1.2.3")
        second = release_validator.render_plan(data, "v1.2.3")
        self.assertEqual(first, second)
        self.assertIn("Create or review a release PR", first)
        self.assertNotIn("publish a package", first.lower())

    def test_aether_workflow_is_manual_and_refuses_overwrites(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release-first-party-skills.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_dispatch:", workflow)
        self.assertNotIn("\n  push:", workflow)
        self.assertIn("Require tag on default-branch history", workflow)
        self.assertNotIn("--clobber", workflow)

    def test_distributed_validator_works_without_aether_checkout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="aether-release-skill-") as temporary_directory:
            temporary = Path(temporary_directory)
            package = temporary / "prepare-repository-release"
            shutil.copytree(ROOT / "dist" / "skills" / "prepare-repository-release", package)
            repository = temporary / "consumer"
            (repository / ".egohygiene").mkdir(parents=True)
            (repository / ".github" / "workflows").mkdir(parents=True)
            (repository / "CHANGELOG.md").write_text(
                "# Changelog\n\n## [Unreleased]\n", encoding="utf-8"
            )
            (repository / "pyproject.toml").write_text(
                "[project]\nname = \"example\"\nversion = \"0.1.0\"\n", encoding="utf-8"
            )
            (repository / "Taskfile.yml").write_text(
                "\n".join(
                    [
                        'version: "3"',
                        "tasks:",
                        "  release:plan: {}",
                        "  release:prepare: {}",
                        "  release:verify: {}",
                        "  release:publish: {}",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
            (repository / ".github" / "workflows" / "release.yml").write_text(
                "name: Release\non:\n  workflow_dispatch:\n", encoding="utf-8"
            )
            fixture = json.loads(
                (
                    ROOT
                    / "catalog"
                    / "fixtures"
                    / "aether.repository-release.v1.schema"
                    / "valid.json"
                ).read_text(encoding="utf-8")
            )
            (repository / ".egohygiene" / "release.json").write_text(
                json.dumps(fixture, indent=2) + "\n", encoding="utf-8"
            )

            result = subprocess.run(
                [
                    "python3",
                    str(package / "scripts" / "validate-release-declaration.py"),
                    "--repository",
                    str(repository),
                    "--release-version",
                    "v0.1.0",
                    "--format",
                    "json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(json.loads(result.stdout)["repository"], "egohygiene/example")
