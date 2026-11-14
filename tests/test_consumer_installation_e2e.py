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

from catalog.consumer_installation import (
    ConsumerInstallationHarness, LOCAL_REQUIRED, PILOT_SKILLS, RELEASE_REQUIRED,
    REPORT_SCHEMA, main,
)

ROOT = Path(__file__).resolve().parents[1]


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
        elif args[0:3] == ("gh", "skill", "install"):
            if "install" in self.failures:
                result.update(status="fail", exit_code=1)
            else:
                skill = args[4]
                path = next(path for name, _, path in PILOT_SKILLS if name == skill)
                package = cwd / path
                (package / "evals").mkdir(parents=True)
                (package / "SKILL.md").write_text("---\nname: synthetic\ndescription: Use when testing a synthetic package.\n---\n# Synthetic\n")
                (package / "distribution-manifest.v1.json").write_text(json.dumps({
                    "generated_paths": [f"dist/skills/{skill}/SKILL.md"],
                }))
                (package / "evals/evals.json").write_text(json.dumps({
                    "cases": [{"category": "positive"}, {"category": "negative"}],
                }))
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


if __name__ == "__main__":
    unittest.main()
