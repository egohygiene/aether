"""Deterministic harness contracts; actual qualification is a separate command."""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

import yaml

from catalog.consumer_installation import (
    ConsumerInstallationHarness, LOCAL_REQUIRED, PILOT_SKILLS, RELEASE_REQUIRED,
    REPORT_SCHEMA, _package_snapshot, _skill_parts, _verify_materialization, main,
)

ROOT = Path(__file__).resolve().parents[1]


def write_export(root: Path, skill: str) -> Path:
    package = root / "skills" / skill
    for folder in ("references", "templates", "evals"):
        (package / folder).mkdir(parents=True, exist_ok=True)
    (package / "SKILL.md").write_text(
        f"---\nname: {skill}\ndescription: Use when testing a synthetic package.\n"
        "metadata:\n  version: '1.0.0'\n---\n\n# Synthetic\n",
        encoding="utf-8",
    )
    (package / "references/guide.md").write_text("# Portable guide\n", encoding="utf-8")
    (package / "templates/sample.md").write_text("# Sample\n", encoding="utf-8")
    (package / "evals/evals.json").write_text(json.dumps({
        "cases": [{"category": "positive"}, {"category": "negative"}],
    }), encoding="utf-8")
    paths = [f"dist/skills/{skill}/{path}" for path in
             ("SKILL.md", "references/guide.md", "templates/sample.md", "evals/evals.json",
              "distribution-manifest.v1.json")]
    (package / "distribution-manifest.v1.json").write_text(json.dumps({
        "schema_version": "aether.distribution-manifest/v1", "generated_paths": paths,
    }), encoding="utf-8")
    return package


def install_export(source: Path, destination: Path) -> None:
    """Model the actually observed gh local header/separator transformation."""
    shutil.copytree(source, destination, dirs_exist_ok=True)
    fm, body = _skill_parts((source / "SKILL.md").read_bytes())
    fm.setdefault("metadata", {})["local-path"] = str(source)
    if body.startswith("\n"):
        body = body[1:]
    (destination / "SKILL.md").write_text(
        "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n" + body, encoding="utf-8",
    )


def multiline_header(skill: str) -> str:
    return ("---\nmetadata:\n  version: '1.0.0'\ndescription: |\n"
            "  Use when documenting a literal ---\n"
            "  inside a multiline description.\n"
            f"name: {skill}\n---\n\n# Synthetic\n")


def historical_truncated_install(source: Path, destination: Path) -> None:
    """Reproduce the reviewed old substring-delimiter error, not valid CLI behavior."""
    shutil.copytree(source, destination, dirs_exist_ok=True)
    _opening, truncated, body = (source / "SKILL.md").read_text().split("---\n", 2)
    fm = yaml.safe_load(truncated)
    fm.setdefault("metadata", {})["local-path"] = str(source)
    (destination / "SKILL.md").write_text(
        "---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n" + body,
        encoding="utf-8",
    )


class SimulatedConsumer(ConsumerInstallationHarness):
    """Model only the external adapter; run real harness/report/check logic."""

    def __init__(self, *args, unavailable=(), failures=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.unavailable = set(unavailable)
        self.failures = set(failures)
        self.commands = []

    def run_command(self, cwd, *args):
        self.commands.append((cwd, args))
        result = {"command": " ".join(args), "cwd": self.sanitize(str(cwd)),
                  "status": "pass", "exit_code": 0, "stdout": "", "stderr": ""}
        if args[-1] == "--help" and args[0:2] == ("gh", "skill"):
            if args[2] in self.unavailable:
                result.update(status="fail", exit_code=1, stderr="unknown command")
        elif "build" in args:
            if "build" in self.failures:
                result.update(status="fail", exit_code=1)
            else:
                self.dist_root.mkdir()
                for name, _agent, _path in PILOT_SKILLS:
                    write_export(self.dist_root, name)
        elif args[0:3] == ("gh", "skill", "install"):
            if "install" in self.failures:
                result.update(status="fail", exit_code=1)
            else:
                skill = args[4]
                path = next(path for name, _, path in PILOT_SKILLS if name == skill)
                package = cwd / path
                install_export(self.dist_root / "skills" / skill, package)
        elif args[0:3] == ("gh", "skill", "list"):
            result["stdout"] = json.dumps([
                {"skillName": name, "path": str(cwd / path), "scope": "project", "pinned": True}
                for name, _, path in PILOT_SKILLS
            ])
            if "malformed-list" in self.failures:
                result["stdout"] = "not JSON"
        elif args[0:3] == ("gh", "skill", "publish") and "publish" in self.failures:
            result.update(status="fail", exit_code=1)
        elif args[0:3] == ("gh", "skill", "update") and "update" in self.failures:
            result.update(status="fail", exit_code=1)
        return result


class TestConsumerInstallationE2E(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)

    def harness(self, **kwargs):
        harness = SimulatedConsumer(ROOT, report_root=self.base / "report", **kwargs)
        self.addCleanup(harness.cleanup)
        return harness

    def run_harness(self, harness, diagnostics=()):
        with patch("catalog.consumer_installation.validate_portable_skill_package", return_value=list(diagnostics)):
            return harness.run()

    def test_generates_machine_readable_readiness_report(self):
        h = self.harness()
        report = self.run_harness(h)
        self.assertEqual(report["schema_version"], REPORT_SCHEMA)
        self.assertEqual(report["local_status"], "ready")
        self.assertEqual(report["overall_status"], "not-ready")
        self.assertTrue(report["qualification"]["complete"])
        self.assertEqual(report["qualification"]["required_scenarios"], list(LOCAL_REQUIRED))
        self.assertEqual(json.loads(h.report_path.read_text()), report)
        self.assertTrue(h.bundle_root.is_dir())
        self.assertFalse(h.fixture_root.exists())

    def test_missing_adapter_blocks_required_scenarios_without_package_defects(self):
        h = self.harness(unavailable={"install", "list", "publish"})
        report = self.run_harness(h)
        self.assertEqual(report["scenarios"]["distribution-build"]["status"], "pass")
        for name in LOCAL_REQUIRED[1:]:
            self.assertEqual(report["scenarios"][name]["status"], "blocked", name)
        self.assertFalse(report["qualification"]["complete"])
        self.assertEqual(report["overall_status"], "not-ready")
        self.assertFalse(any(args[:3] == ("gh", "skill", "install") and "--help" not in args
                             for _, args in h.commands))

    def test_each_real_adapter_or_build_failure_remains_a_failure(self):
        for failure, scenario in (("build", "distribution-build"), ("install", "clean-local-distribution-install"),
                                  ("publish", "publish-validation"), ("malformed-list", "harness-error")):
            with self.subTest(failure=failure):
                h = self.harness(failures={failure})
                report = self.run_harness(h)
                self.assertEqual(report["scenarios"][scenario]["status"], "fail")
                self.assertFalse(report["qualification"]["complete"])
                self.assertTrue(h.report_path.is_file())
                # Each subcase needs a fresh exclusive receipt directory.
                shutil.rmtree(h.report_root)

    def test_package_validation_failure_is_never_ignored(self):
        # Existing validator diagnostics are dataclasses, as consumed by the harness.
        from aether_validator import Diagnostic
        diagnostic = Diagnostic(rule_id="SYNTHETIC", severity="error", message="invalid package",
                                guidance="Repair synthetic package", file="SKILL.md")
        report = self.run_harness(self.harness(), [diagnostic])
        self.assertEqual(report["scenarios"]["portable-package-validation"]["status"], "fail")
        self.assertFalse(report["qualification"]["complete"])

    def test_real_pristine_validator_and_verified_host_tracking_have_separate_scopes(self):
        h = self.harness()
        report = h.run()
        scenario = report["scenarios"]["portable-package-validation"]
        self.assertEqual(scenario["status"], "pass")
        self.assertTrue(report["qualification"]["complete"])
        self.assertEqual(report["overall_status"], "not-ready")
        for skill, _agent, _path in PILOT_SKILLS:
            self.assertEqual(scenario["source_validation_results"][skill], [])
            observation = scenario["installed_observations"][skill]
            self.assertEqual(observation["portable_status"], "fail")
            self.assertEqual({d["rule_id"] for d in observation["diagnostics"]},
                             {"AETHER_PORTABLE_006", "AETHER_PORTABLE_017"})
            self.assertTrue(observation["host_tracking_verified"])

    def test_source_mutation_after_installer_cannot_replace_the_frozen_expected_export(self):
        h = self.harness()
        original_install = h._clean_local_distribution_install

        def mutate_after_install():
            original_install()
            skill = PILOT_SKILLS[0][0]
            (h.dist_root / "skills" / skill / "references/guide.md").write_text("changed\n")

        with patch.object(h, "_clean_local_distribution_install", side_effect=mutate_after_install):
            report = self.run_harness(h)
        self.assertEqual(report["scenarios"]["portable-package-validation"]["status"], "fail")
        self.assertFalse(report["qualification"]["complete"])

    def test_empty_skill_selection_cannot_vacuously_qualify(self):
        with patch("catalog.consumer_installation.PILOT_SKILLS", []):
            report = self.run_harness(self.harness())
        self.assertEqual(report["scenarios"]["distribution-build"]["status"], "fail")
        self.assertFalse(report["qualification"]["complete"])

    def test_empty_duplicate_or_incomplete_manifest_cannot_vacuously_qualify(self):
        for mode in ("empty", "duplicate", "omitted"):
            with self.subTest(mode=mode):
                h = self.harness()
                original = h.run_command

                def corrupt_build(cwd, *args):
                    result = original(cwd, *args)
                    if "build" in args:
                        skill = PILOT_SKILLS[0][0]
                        path = h.dist_root / "skills" / skill / "distribution-manifest.v1.json"
                        manifest = json.loads(path.read_text())
                        paths = manifest["generated_paths"]
                        manifest["generated_paths"] = [] if mode == "empty" else (
                            paths + [paths[0]] if mode == "duplicate" else paths[1:])
                        path.write_text(json.dumps(manifest))
                    return result

                with patch.object(h, "run_command", side_effect=corrupt_build):
                    report = self.run_harness(h)
                scenario = report["scenarios"]["portable-package-validation"]
                self.assertEqual(scenario["status"], "fail")
                self.assertTrue(any(check["id"].startswith("manifest-") and check["status"] == "fail"
                                    for check in scenario["checks"]))
                self.assertFalse(report["qualification"]["complete"])
                shutil.rmtree(h.report_root)

    def test_full_harness_preserves_multiline_description_with_literal_delimiter(self):
        h = self.harness()
        original = h.run_command

        def multiline_build(cwd, *args):
            result = original(cwd, *args)
            if "build" in args:
                skill = PILOT_SKILLS[0][0]
                (h.dist_root / "skills" / skill / "SKILL.md").write_text(multiline_header(skill))
            return result

        with patch.object(h, "run_command", side_effect=multiline_build):
            report = h.run()
        self.assertEqual(report["scenarios"]["portable-package-validation"]["status"], "pass")
        self.assertTrue(report["qualification"]["complete"])

    def test_full_harness_rejects_header_semantic_drift_hidden_by_old_substring_parser(self):
        h = self.harness()
        original = h.run_command

        def broken_adapter(cwd, *args):
            result = original(cwd, *args)
            if "build" in args:
                skill = PILOT_SKILLS[0][0]
                (h.dist_root / "skills" / skill / "SKILL.md").write_text(multiline_header(skill))
            elif args[:3] == ("gh", "skill", "install") and "--help" not in args:
                skill = args[4]
                if skill == PILOT_SKILLS[0][0]:
                    path = next(path for name, _agent, path in PILOT_SKILLS if name == skill)
                    historical_truncated_install(h.dist_root / "skills" / skill, cwd / path)
            return result

        with patch.object(h, "run_command", side_effect=broken_adapter):
            report = h.run()
        scenario = report["scenarios"]["portable-package-validation"]
        self.assertEqual(scenario["source_validation_results"][PILOT_SKILLS[0][0]], [])
        self.assertTrue(any(check["id"] == "materialization-" + PILOT_SKILLS[0][0]
                            and check["status"] == "fail" for check in scenario["checks"]))
        self.assertFalse(report["qualification"]["complete"])

    def test_local_scope_cannot_activate_remote_work_from_ambient_environment(self):
        with patch.dict(os.environ, {"AETHER_E2E_REMOTE_TAG": "v1.0.0", "AETHER_E2E_REMOTE_COMMIT": "a" * 40}):
            h = self.harness()
            report = self.run_harness(h)
        self.assertEqual(report["scenarios"]["pinned-remote-release-install"]["status"], "skip")
        self.assertFalse(any("--pin" in args for _, args in h.commands))

    def test_release_scope_requires_explicit_immutable_selection(self):
        report = self.run_harness(self.harness(scope="release"))
        self.assertEqual(report["scenarios"]["pinned-remote-release-install"]["status"], "blocked")
        self.assertEqual(report["scenarios"]["update-behavior"]["status"], "blocked")
        self.assertFalse(report["qualification"]["complete"])

    def test_simulated_release_scope_requires_all_scenarios_to_pass(self):
        h = self.harness(scope="release", remote_tag="v1.0.0", remote_commit="a" * 40)
        report = self.run_harness(h)
        self.assertEqual(report["qualification"]["required_scenarios"], list(RELEASE_REQUIRED))
        self.assertEqual(report["overall_status"], "ready")
        self.assertTrue(report["qualification"]["complete"])

    def test_real_update_failure_prevents_release_qualification(self):
        h = self.harness(scope="release", remote_tag="v1.0.0", remote_commit="a" * 40,
                         failures={"update"})
        report = self.run_harness(h)
        self.assertEqual(report["local_status"], "ready")
        self.assertEqual(report["scenarios"]["update-behavior"]["status"], "fail")
        self.assertEqual(report["overall_status"], "not-ready")
        self.assertFalse(report["qualification"]["complete"])

    def test_skipped_missing_and_unexpected_scenarios_cannot_vacuously_pass(self):
        h = self.harness()
        methods = ("_build_distribution", "_clean_local_distribution_install", "_portable_package_validation",
                   "_publish_validation", "_remote_pinned_install", "_update_behavior", "_removal_cleanup")
        with contextlib.ExitStack() as stack:
            for name in methods:
                stack.enter_context(patch.object(h, name))
            report = self.run_harness(h)
        self.assertFalse(report["qualification"]["complete"])
        self.assertEqual(report["overall_status"], "not-ready")

    def test_command_unavailability_and_timeout_are_blocked_and_redacted(self):
        h = ConsumerInstallationHarness(ROOT, report_root=self.base / "report")
        self.addCleanup(h.cleanup)
        with patch("catalog.consumer_installation.subprocess.Popen", side_effect=FileNotFoundError("missing adapter")):
            self.assertEqual(h.run_command(ROOT, "gh", "--version")["status"], "blocked")
        with patch.dict(os.environ, {"GH_TOKEN": "synthetic-credential-canary"}):
            self.assertNotIn("synthetic-credential-canary", h.sanitize("synthetic-credential-canary " + str(h.fixture_root)))

    def test_nested_validator_details_are_redacted_in_report_and_bundle(self):
        from aether_validator import Diagnostic
        h = self.harness()
        secret = "synthetic-diagnostic-secret"
        private = str(h.fixture_root / "private-source")
        external_private = "/home/synthetic-other-user/private-document.md"
        diagnostic = Diagnostic(rule_id="SYNTHETIC", severity="error", message=private + secret,
                                guidance="repair " + external_private, file=private,
                                context={"nested": [secret, private, external_private]})
        with patch.dict(os.environ, {"GH_TOKEN": secret}):
            report = self.run_harness(h, [diagnostic])
        for receipt in (h.report_path, *h.bundle_root.glob("*.json")):
            text = receipt.read_text()
            self.assertNotIn(secret, text, receipt.name)
            self.assertNotIn(str(h.fixture_root), text, receipt.name)
            self.assertNotIn(external_private, text, receipt.name)
        self.assertEqual(json.loads(h.report_path.read_text()), report)

    @unittest.skipUnless(os.name == "posix", "Qualification uses POSIX process groups")
    def test_actual_deadline_stops_descendants_and_bounds_output(self):
        h = ConsumerInstallationHarness(ROOT, report_root=self.base / "report", timeout=1)
        self.addCleanup(h.cleanup)
        marker = self.base / "escaped-child"
        child = "import time; from pathlib import Path; time.sleep(1.5); Path(" + repr(str(marker)) + ").touch()"
        parent = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c'," + repr(child) + "]); time.sleep(20)"
        started = time.monotonic()
        result = h.run_command(ROOT, sys.executable, "-c", parent)
        self.assertEqual(result["status"], "blocked")
        self.assertLess(time.monotonic() - started, 3)
        time.sleep(0.7)
        self.assertFalse(marker.exists(), "Descendant must be stopped before it can mutate the fixture")
        output = h.run_command(ROOT, sys.executable, "-c", "import sys;sys.stdout.write('x'*200000);sys.stderr.write('y'*200000)")
        self.assertEqual(output["status"], "pass")
        self.assertTrue(output["output_truncated"])
        self.assertEqual(len(output["stdout"]), 64000)
        self.assertEqual(len(output["stderr"]), 64000)

    def test_existing_receipt_is_never_overwritten(self):
        h = self.harness()
        report = self.run_harness(h)
        before = h.report_path.read_bytes()
        with self.assertRaises(FileExistsError):
            self.harness()
        self.assertEqual(h.report_path.read_bytes(), before)
        self.assertEqual(json.loads(before), report)

    def test_cli_gate_has_meaningful_exit_status(self):
        for unavailable, expected in (((), 0), (("install",), 1)):
            with self.subTest(unavailable=unavailable):
                h = self.harness(unavailable=unavailable)
                with patch("catalog.consumer_installation.ConsumerInstallationHarness", return_value=h), \
                     patch("catalog.consumer_installation.validate_portable_skill_package", return_value=[]), \
                     contextlib.redirect_stdout(io.StringIO()):
                    result = main(["--output", str(h.report_root)])
                self.assertEqual(result, expected)
                shutil.rmtree(h.report_root)


@unittest.skipUnless(os.name == "posix", "Host qualification uses POSIX no-follow reads")
class TestInstalledMaterialization(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.dist = self.base / "dist"
        self.consumer = self.base / "consumer"
        self.consumer.mkdir()
        self.source = write_export(self.dist, "sample-skill")
        self.installed = self.consumer / ".agents/skills/sample-skill"
        self.frozen = _package_snapshot(self.source, self.dist)
        install_export(self.source, self.installed)

    def verify(self):
        return _verify_materialization(
            self.frozen, _package_snapshot(self.installed, self.consumer), self.source,
        )

    def edit_header(self, mutate, body=None):
        path = self.installed / "SKILL.md"
        fm, original_body = _skill_parts(path.read_bytes())
        mutate(fm)
        path.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n" +
                        (original_body if body is None else body), encoding="utf-8")

    def test_exact_tracking_and_observed_separator_pass_without_source_or_instance_writes(self):
        before_source = _package_snapshot(self.source, self.dist)
        before_install = _package_snapshot(self.installed, self.consumer)
        result = self.verify()
        self.assertTrue(result["tracking_matches_selected_source"])
        self.assertEqual(result["body_separator"], "one-blank-lf-omitted")
        self.assertEqual(_package_snapshot(self.source, self.dist), before_source)
        self.assertEqual(_package_snapshot(self.installed, self.consumer), before_install)
        self.assertEqual(_skill_parts((self.installed / "SKILL.md").read_bytes())[0]
                         ["metadata"]["local-path"], str(self.source))

    def test_wrong_missing_relative_or_aliased_tracking_is_rejected(self):
        original = (self.installed / "SKILL.md").read_bytes()
        for value in (str(self.base / "wrong"), "../sample-skill", str(self.source / ".." / self.source.name), None):
            with self.subTest(value=value):
                (self.installed / "SKILL.md").write_bytes(original)
                def change(fm):
                    if value is None:
                        fm["metadata"].pop("local-path")
                    else:
                        fm["metadata"]["local-path"] = value
                self.edit_header(change)
                with self.assertRaises(ValueError):
                    self.verify()

    def test_changed_ordinary_fields_or_extra_metadata_are_rejected(self):
        original = (self.installed / "SKILL.md").read_bytes()
        mutations = [lambda fm: fm.update(description="Changed. Use when testing."),
                     lambda fm: fm.update(unexpected="extra"),
                     lambda fm: fm["metadata"].update(version="2.0.0"),
                     lambda fm: fm["metadata"].update(other_path="/tmp/unexpected")]
        for mutate in mutations:
            (self.installed / "SKILL.md").write_bytes(original)
            self.edit_header(mutate)
            with self.assertRaises(ValueError):
                self.verify()

    def test_boolean_cannot_impersonate_an_ordinary_numeric_metadata_value(self):
        path = self.source / "SKILL.md"
        fm, body = _skill_parts(path.read_bytes())
        fm["metadata"]["counter"] = 1
        path.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n" + body)
        self.frozen = _package_snapshot(self.source, self.dist)
        install_export(self.source, self.installed)
        self.edit_header(lambda fm: fm["metadata"].update(counter=True))
        with self.assertRaises(ValueError):
            self.verify()

    def test_unexpected_body_bytes_indentation_and_blank_lines_are_rejected(self):
        _fm, body = _skill_parts((self.installed / "SKILL.md").read_bytes())
        original = (self.installed / "SKILL.md").read_bytes()
        for changed in ("    " + body, "\n\n" + body, body + "Extra instruction\n", body.rstrip("\n")):
            (self.installed / "SKILL.md").write_bytes(original)
            self.edit_header(lambda _fm: None, body=changed)
            with self.assertRaises(ValueError):
                self.verify()
        # Exact original body is permitted as well as the single observed LF removal.
        (self.installed / "SKILL.md").write_bytes(original)
        self.edit_header(lambda _fm: None, body=_skill_parts(self.frozen["files"]["SKILL.md"])[1])
        self.assertEqual(self.verify()["body_separator"], "unchanged")

    def test_resource_changes_extra_files_missing_files_and_empty_dirs_are_rejected(self):
        target = self.installed / "references/guide.md"
        original = target.read_bytes()
        target.write_bytes(b"changed\n")
        with self.assertRaises(ValueError): self.verify()
        target.write_bytes(original)
        extra = self.installed / "extra.txt"
        extra.write_text("extra\n")
        with self.assertRaises(ValueError): self.verify()
        extra.unlink()
        target.unlink()
        with self.assertRaises(ValueError): self.verify()
        target.write_bytes(original)
        extra_dir = self.installed / "extra-empty"
        extra_dir.mkdir()
        with self.assertRaises(ValueError): self.verify()

    def test_leaf_parent_and_package_links_are_rejected(self):
        target = self.installed / "references/guide.md"
        target.unlink()
        target.symlink_to(self.source / "references/guide.md")
        with self.assertRaises((OSError, ValueError)): self.verify()
        target.unlink()
        target.write_text("# Portable guide\n")
        shutil.rmtree(self.installed / "references")
        (self.installed / "references").symlink_to(self.source / "references", target_is_directory=True)
        with self.assertRaises((OSError, ValueError)): self.verify()
        (self.installed / "references").unlink()
        (self.installed / "references").mkdir()
        (self.installed / "references/guide.md").write_text("# Portable guide\n")
        moved = self.base / "moved"
        self.installed.rename(moved)
        self.installed.symlink_to(moved, target_is_directory=True)
        with self.assertRaises((OSError, ValueError)): self.verify()

    def test_ambiguous_duplicate_alias_and_merge_frontmatter_are_rejected(self):
        samples = ["name: first\nname: second\n", "metadata: &meta {}\nextra: *meta\n",
                   "metadata:\n  <<: {local-path: x}\n", "metadata:\n  local-path: x\n  local-path: y\n"]
        for header in samples:
            with self.subTest(header=header), self.assertRaises(ValueError):
                _skill_parts(("---\n" + header + "---\n# Body\n").encode())

    def test_literal_delimiter_in_multiline_header_cannot_hide_semantic_changes(self):
        path = self.source / "SKILL.md"
        path.write_text(multiline_header("sample-skill"))
        self.frozen = _package_snapshot(self.source, self.dist)
        install_export(self.source, self.installed)
        self.assertTrue(self.verify()["tracking_matches_selected_source"])
        fm, _body = _skill_parts((self.installed / "SKILL.md").read_bytes())
        self.assertEqual(fm["name"], "sample-skill")
        self.assertIn("literal ---\n", fm["description"])
        historical_truncated_install(self.source, self.installed)
        with self.assertRaisesRegex(ValueError, "semantic frontmatter"):
            self.verify()

    def test_reserved_source_tracking_collision_is_not_treated_as_injected_metadata(self):
        path = self.source / "SKILL.md"
        fm, body = _skill_parts(path.read_bytes())
        fm["metadata"]["local-path"] = str(self.source)
        path.write_text("---\n" + yaml.safe_dump(fm, sort_keys=False) + "---\n" + body)
        self.frozen = _package_snapshot(self.source, self.dist)
        with self.assertRaises(ValueError): self.verify()

    def test_file_entry_and_depth_bounds_fail_closed(self):
        for field, value in (("MAX_PACKAGE_FILE_BYTES", 8), ("MAX_PACKAGE_ENTRIES", 2), ("MAX_PACKAGE_BYTES", 8)):
            with patch("catalog.consumer_installation." + field, value), self.assertRaises(ValueError):
                _package_snapshot(self.installed, self.consumer)
        deep = self.installed.joinpath(*(["deep"] * 66))
        deep.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "depth"):
            _package_snapshot(self.installed, self.consumer)

    def test_special_inputs_are_rejected_before_a_potentially_blocking_read(self):
        os.mkfifo(self.installed / "unexpected-pipe")
        with self.assertRaisesRegex(ValueError, "non-regular"):
            _package_snapshot(self.installed, self.consumer)


if __name__ == "__main__":
    unittest.main()
