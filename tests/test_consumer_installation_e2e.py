from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from aether_validator import validate_portable_skill_package

REPO_ROOT = Path(__file__).resolve().parents[1]
REPORT_SCHEMA = "aether.consumer-installation-readiness/v1"
PILOT_SKILLS = [
    ("architecture-authoring", "github-copilot", ".agents/skills/architecture-authoring"),
    ("create-architecture-document", "cursor", ".agents/skills/create-architecture-document"),
    ("audit-repository", "claude-code", ".claude/skills/audit-repository"),
]


def _frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    _, fm, _rest = text.split("---\n", 2)
    data = yaml.safe_load(fm) or {}
    return data if isinstance(data, dict) else {}


def _tree_lines(root: Path) -> list[str]:
    if not root.exists():
        return []
    lines = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root).as_posix()
        lines.append(f"{rel}/" if path.is_dir() else rel)
    return lines


class ConsumerInstallationHarness:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.fixture_root = Path(tempfile.mkdtemp(prefix="aether-consumer-e2e-"))
        self.dist_root = self.fixture_root / "dist"
        self.local_consumer = self.fixture_root / "consumer-local"
        self.report_root = (
            Path(os.environ["AETHER_E2E_REPORT_DIR"]).resolve()
            if os.environ.get("AETHER_E2E_REPORT_DIR")
            else Path(tempfile.mkdtemp(prefix="aether-consumer-e2e-report-"))
        )
        self.report_root.mkdir(parents=True, exist_ok=True)
        self.report_path = self.report_root / "consumer-installation-readiness.v1.json"
        self.bundle_root = self.report_root / "diagnostic-bundle"
        self.replacements = {
            self.repo_root.as_posix(): "<REPO_ROOT>",
            self.fixture_root.as_posix(): "<FIXTURE_ROOT>",
            Path.home().as_posix(): "<HOME>",
        }
        self.scenarios: dict[str, Any] = {}

    def cleanup(self) -> None:
        shutil.rmtree(self.fixture_root, ignore_errors=True)

    def sanitize(self, value: str) -> str:
        for source, replacement in self.replacements.items():
            value = value.replace(source, replacement)
        return value

    def run_command(self, cwd: Path, *args: str) -> dict[str, Any]:
        result = subprocess.run(
            list(args),
            cwd=cwd,
            capture_output=True,
            text=True,
        )
        return {
            "command": self.sanitize(" ".join(args)),
            "cwd": self.sanitize(cwd.as_posix()),
            "exit_code": result.returncode,
            "stdout": self.sanitize(result.stdout),
            "stderr": self.sanitize(result.stderr),
            "status": "pass" if result.returncode == 0 else "fail",
        }

    def check(self, scenario: dict[str, Any], check_id: str, ok: bool, message: str, **details: Any) -> None:
        scenario["checks"].append(
            {
                "id": check_id,
                "status": "pass" if ok else "fail",
                "message": message,
                "details": details,
            }
        )
        if not ok:
            scenario["status"] = "fail"

    def skipped(self, scenario_id: str, reason: str) -> dict[str, Any]:
        scenario = {
            "id": scenario_id,
            "status": "skip",
            "reason": reason,
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario_id] = scenario
        return scenario

    def run(self) -> dict[str, Any]:
        report = {
            "schema_version": REPORT_SCHEMA,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "repository": "egohygiene/aether",
            "pilot_skills": [skill for skill, _agent, _path in PILOT_SKILLS],
            "tool_versions": self._tool_versions(),
            "scenarios": self.scenarios,
        }

        try:
            self._clean_local_distribution_install()
            self._portable_package_validation()
            self._publish_validation()
            self._remote_pinned_install()
            self._update_behavior()
            self._removal_cleanup()
        finally:
            report["overall_status"] = (
                "ready"
                if all(s["status"] == "pass" for s in self.scenarios.values() if s["status"] != "skip")
                else "not-ready"
            )
            self._write_report(report)
            if report["overall_status"] != "ready":
                self._write_bundle(report)
            self.cleanup()
        return report

    def _tool_versions(self) -> dict[str, str]:
        versions = {}
        for name, args in {
            "python": [sys.executable, "--version"],
            "git": ["git", "--version"],
            "gh": ["gh", "--version"],
        }.items():
            result = subprocess.run(args, cwd=self.repo_root, capture_output=True, text=True)
            versions[name] = self.sanitize((result.stdout or result.stderr).strip())
        return versions

    def _clean_local_distribution_install(self) -> None:
        scenario = {
            "id": "clean-local-distribution-install",
            "status": "pass",
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario["id"]] = scenario

        self.local_consumer.mkdir(parents=True, exist_ok=True)
        scenario["steps"].append(self.run_command(self.local_consumer, "git", "init", "-q"))
        build_step = self.run_command(
            self.repo_root,
            sys.executable,
            "./aether",
            "distribution",
            "build",
            "--output-directory",
            self.dist_root.as_posix(),
        )
        scenario["steps"].append(build_step)
        if build_step["exit_code"] != 0:
            scenario["status"] = "fail"
            return

        for skill_name, agent, expected_path in PILOT_SKILLS:
            step = self.run_command(
                self.local_consumer,
                "gh",
                "skill",
                "install",
                self.dist_root.as_posix(),
                skill_name,
                "--from-local",
                "--agent",
                agent,
            )
            scenario["steps"].append(step)
            self.check(
                scenario,
                f"install-{skill_name}",
                step["exit_code"] == 0,
                f"Install {skill_name} for {agent}",
            )
            installed_dir = self.local_consumer / expected_path
            self.check(
                scenario,
                f"path-{skill_name}",
                installed_dir.exists(),
                f"Installed path exists for {skill_name}",
                expected_path=expected_path,
            )

        list_step = self.run_command(
            self.local_consumer,
            "gh",
            "skill",
            "list",
            "--json",
            "skillName,path,scope,pinned,sourceURL,version",
        )
        scenario["steps"].append(list_step)
        installed = json.loads(list_step["stdout"] or "[]") if list_step["exit_code"] == 0 else []
        by_name = {entry["skillName"]: entry for entry in installed}
        for skill_name, _agent, expected_path in PILOT_SKILLS:
            entry = by_name.get(skill_name)
            self.check(
                scenario,
                f"list-{skill_name}",
                entry is not None,
                f"gh skill list returns {skill_name}",
            )
            if entry:
                self.check(
                    scenario,
                    f"scope-{skill_name}",
                    entry.get("scope") == "project",
                    f"{skill_name} installs at project scope",
                )
                self.check(
                    scenario,
                    f"placement-{skill_name}",
                    entry.get("path", "").endswith(expected_path),
                    f"{skill_name} is placed in the expected host directory",
                    path=entry.get("path"),
                )
        scenario["fixture_tree"] = _tree_lines(self.local_consumer)

    def _portable_package_validation(self) -> None:
        scenario = {
            "id": "portable-package-validation",
            "status": "pass",
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario["id"]] = scenario
        if not self.local_consumer.exists():
            scenario["status"] = "skip"
            scenario["reason"] = "local consumer fixture was not created"
            return

        package_results = {}
        for skill_name, _agent, expected_path in PILOT_SKILLS:
            package_dir = self.local_consumer / expected_path
            if not package_dir.exists():
                self.check(
                    scenario,
                    f"package-{skill_name}",
                    False,
                    f"Portable package directory missing for {skill_name}",
                )
                continue
            diagnostics = [asdict(diag) for diag in validate_portable_skill_package(package_dir)]
            package_results[skill_name] = diagnostics
            self.check(
                scenario,
                f"portable-{skill_name}",
                not any(diag["severity"] == "error" for diag in diagnostics),
                f"Portable validator passes for {skill_name}",
                diagnostics=diagnostics,
            )
            manifest_path = package_dir / "distribution-manifest.v1.json"
            if manifest_path.exists():
                manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
                self.check(
                    scenario,
                    f"manifest-{skill_name}",
                    all((package_dir / Path(path).relative_to(f"dist/skills/{skill_name}")).exists() for path in manifest["generated_paths"]),
                    f"Manifest resources resolve for {skill_name}",
                )
            else:
                self.check(
                    scenario,
                    f"manifest-{skill_name}",
                    False,
                    f"Manifest exists for {skill_name}",
                )
            evals_path = package_dir / "evals" / "evals.json"
            if evals_path.exists():
                evals = json.loads(evals_path.read_text(encoding="utf-8"))
                categories = {case["category"] for case in evals.get("cases", []) if "category" in case}
            else:
                categories = set()
            self.check(
                scenario,
                f"routing-{skill_name}",
                {"positive", "negative"}.issubset(categories),
                f"{skill_name} evals cover positive and negative routing cases",
                categories=sorted(categories),
            )
            fm = _frontmatter(package_dir / "SKILL.md")
            self.check(
                scenario,
                f"frontmatter-{skill_name}",
                isinstance(fm.get("description"), str) and "use when" in fm["description"].lower(),
                f"{skill_name} frontmatter is discoverable and routing-oriented",
            )
            self.check(
                scenario,
                f"templates-{skill_name}",
                self._render_templates(package_dir),
                f"{skill_name} templates render into structurally valid sample artifacts",
            )
        scenario["validation_results"] = package_results

    def _render_templates(self, package_dir: Path) -> bool:
        replacements = {
            "replace-with-stable-document-id": "sample-document",
            "replace-with-architecture-document-id": "sample-architecture",
            "Replace With Document Title": "Sample Document",
            "replace-with-owner": "egohygiene",
            "YYYY-MM-DDTHH:MM:SSZ": "2026-08-09T00:00:00Z",
            "YYYY-MM-DD": "2026-08-09",
            "replace-with-id": "sample-audit",
            "replace-with-name": "Sample Audit",
            "Replace With Audit Title": "Sample Audit",
            "replace-with-system-document-id": "sample-system",
        }
        for template_path in sorted((package_dir / "templates").rglob("*.md")):
            rendered = template_path.read_text(encoding="utf-8")
            for needle, replacement in replacements.items():
                rendered = rendered.replace(needle, replacement)
            if rendered.startswith("---\n"):
                try:
                    _, fm, body = rendered.split("---\n", 2)
                    if not isinstance(yaml.safe_load(fm), dict):
                        return False
                    if "#" not in body:
                        return False
                except Exception:  # noqa: BLE001
                    return False
        return True

    def _publish_validation(self) -> None:
        scenario = {
            "id": "publish-validation",
            "status": "pass",
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario["id"]] = scenario
        if not self.dist_root.exists():
            scenario["status"] = "skip"
            scenario["reason"] = "distribution fixture was not built"
            return
        step = self.run_command(
            self.repo_root,
            "gh",
            "skill",
            "publish",
            self.dist_root.as_posix(),
            "--dry-run",
        )
        scenario["steps"].append(step)
        self.check(
            scenario,
            "publish-dry-run",
            step["exit_code"] == 0,
            "gh skill publish <dist> --dry-run succeeds",
        )

    def _remote_pinned_install(self) -> None:
        repository = os.environ.get("AETHER_E2E_REMOTE_REPOSITORY", "egohygiene/aether")
        tag = os.environ.get("AETHER_E2E_REMOTE_TAG")
        commit = os.environ.get("AETHER_E2E_REMOTE_COMMIT")
        if not tag or not commit:
            self.skipped(
                "pinned-remote-release-install",
                "set AETHER_E2E_REMOTE_TAG and AETHER_E2E_REMOTE_COMMIT after an approved release exists",
            )
            return
        scenario = {
            "id": "pinned-remote-release-install",
            "status": "pass",
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario["id"]] = scenario
        for label, pin in [("tag", tag), ("commit", commit)]:
            consumer = self.fixture_root / f"consumer-remote-{label}"
            consumer.mkdir(parents=True, exist_ok=True)
            scenario["steps"].append(self.run_command(consumer, "git", "init", "-q"))
            step = self.run_command(
                consumer,
                "gh",
                "skill",
                "install",
                repository,
                "create-architecture-document",
                "--pin",
                pin,
            )
            scenario["steps"].append(step)
            self.check(
                scenario,
                f"remote-install-{label}",
                step["exit_code"] == 0,
                f"Remote pinned install succeeds by {label}",
            )
            if step["exit_code"] != 0:
                continue
            list_step = self.run_command(
                consumer,
                "gh",
                "skill",
                "list",
                "--json",
                "skillName,path,scope,pinned,sourceURL,version",
            )
            scenario["steps"].append(list_step)
            installed = json.loads(list_step["stdout"] or "[]") if list_step["exit_code"] == 0 else []
            entry = next((item for item in installed if item["skillName"] == "create-architecture-document"), None)
            self.check(
                scenario,
                f"remote-list-{label}",
                entry is not None and entry.get("pinned") is True,
                f"Remote pinned install is tracked as pinned by {label}",
                entry=entry,
            )

    def _update_behavior(self) -> None:
        tag = os.environ.get("AETHER_E2E_REMOTE_TAG")
        if not tag:
            self.skipped(
                "update-behavior",
                "set AETHER_E2E_REMOTE_TAG after an approved release exists",
            )
            return
        scenario = {
            "id": "update-behavior",
            "status": "pass",
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario["id"]] = scenario
        consumer = self.fixture_root / "consumer-update"
        consumer.mkdir(parents=True, exist_ok=True)
        scenario["steps"].append(self.run_command(consumer, "git", "init", "-q"))
        install_step = self.run_command(
            consumer,
            "gh",
            "skill",
            "install",
            os.environ.get("AETHER_E2E_REMOTE_REPOSITORY", "egohygiene/aether"),
            "create-architecture-document",
            "--pin",
            tag,
        )
        scenario["steps"].append(install_step)
        if install_step["exit_code"] != 0:
            scenario["status"] = "fail"
            return
        skill_path = consumer / ".agents" / "skills" / "create-architecture-document" / "SKILL.md"
        before = skill_path.read_text(encoding="utf-8")
        skill_path.write_text(before + "\n<!-- local modification -->\n", encoding="utf-8")
        dry_run = self.run_command(consumer, "gh", "skill", "update", "--dry-run")
        apply_run = self.run_command(consumer, "gh", "skill", "update", "--all")
        scenario["steps"].extend([dry_run, apply_run])
        after = skill_path.read_text(encoding="utf-8")
        self.check(
            scenario,
            "pinned-does-not-float",
            dry_run["exit_code"] == 0 and apply_run["exit_code"] == 0,
            "Pinned update commands complete without forcing an overwrite",
        )
        self.check(
            scenario,
            "local-modifications-preserved",
            after.endswith("<!-- local modification -->\n"),
            "Local modifications are not silently destroyed",
        )

    def _removal_cleanup(self) -> None:
        scenario = {
            "id": "removal-cleanup",
            "status": "pass",
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario["id"]] = scenario
        if not self.local_consumer.exists():
            scenario["status"] = "skip"
            scenario["reason"] = "local consumer fixture was not created"
            return
        unrelated = self.local_consumer / ".agents" / "skills" / "unrelated-local" / "SKILL.md"
        unrelated.parent.mkdir(parents=True, exist_ok=True)
        unrelated.write_text(
            "---\nname: unrelated-local\ndescription: Local-only skill. Use when preserving unrelated files.\n---\n",
            encoding="utf-8",
        )
        for _skill_name, _agent, expected_path in PILOT_SKILLS:
            shutil.rmtree(self.local_consumer / expected_path, ignore_errors=True)
        self.check(
            scenario,
            "unrelated-skill-preserved",
            unrelated.exists(),
            "Manual cleanup preserves unrelated local skills",
        )
        self.check(
            scenario,
            "installed-skills-removed",
            all(not (self.local_consumer / expected_path).exists() for _skill, _agent, expected_path in PILOT_SKILLS),
            "Manual cleanup removes the installed pilot skills",
        )
        scenario["fixture_tree"] = _tree_lines(self.local_consumer)

    def _write_report(self, report: dict[str, Any]) -> None:
        self.report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    def _write_bundle(self, report: dict[str, Any]) -> None:
        self.bundle_root.mkdir(parents=True, exist_ok=True)
        (self.bundle_root / "readiness-report.v1.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        (self.bundle_root / "tool-versions.json").write_text(
            json.dumps(report["tool_versions"], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        for scenario_id, scenario in self.scenarios.items():
            (self.bundle_root / f"{scenario_id}.json").write_text(
                json.dumps(scenario, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )


class TestConsumerInstallationE2E(unittest.TestCase):
    def test_generates_machine_readable_readiness_report(self):
        harness = ConsumerInstallationHarness(REPO_ROOT)
        report = harness.run()

        self.assertTrue(harness.report_path.exists())
        self.assertEqual(report["schema_version"], REPORT_SCHEMA)
        self.assertEqual(report["scenarios"]["clean-local-distribution-install"]["status"], "pass")
        self.assertEqual(report["scenarios"]["publish-validation"]["status"], "pass")
        self.assertIn(report["overall_status"], {"ready", "not-ready"})
        if report["overall_status"] == "not-ready":
            self.assertTrue(harness.bundle_root.exists())


if __name__ == "__main__":
    unittest.main()
