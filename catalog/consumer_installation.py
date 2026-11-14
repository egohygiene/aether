"""Explicit consumer qualification; deterministic tests do not imply readiness."""

from __future__ import annotations

import argparse
import json
import os
import re
import selectors
import shutil
import signal
import subprocess
import sys
import tempfile
import time
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
LOCAL_REQUIRED = (
    "distribution-build", "clean-local-distribution-install",
    "portable-package-validation", "publish-validation", "removal-cleanup",
)
RELEASE_REQUIRED = (*LOCAL_REQUIRED, "pinned-remote-release-install", "update-behavior")


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
    def __init__(
        self, repo_root: Path, *, report_root: Path | None = None, scope: str = "local",
        remote_repository: str = "egohygiene/aether", remote_tag: str | None = None,
        remote_commit: str | None = None, timeout: int = 120,
    ):
        if scope not in {"local", "release"} or timeout <= 0:
            raise ValueError("A valid qualification scope and positive timeout are required")
        self.repo_root = repo_root
        self.scope = scope
        self.remote_repository = remote_repository
        self.remote_tag = remote_tag
        self.remote_commit = remote_commit
        self.timeout = timeout
        selected_output = report_root or os.environ.get("AETHER_E2E_REPORT_DIR")
        if selected_output:
            self.report_root = Path(selected_output).resolve()
            self.report_root.mkdir(parents=True, exist_ok=False)
        else:
            self.report_root = Path(tempfile.mkdtemp(prefix="aether-consumer-e2e-report-"))
        self.fixture_root = Path(tempfile.mkdtemp(prefix="aether-consumer-e2e-"))
        self.dist_root = self.fixture_root / "dist"
        self.local_consumer = self.fixture_root / "consumer-local"
        self.report_path = self.report_root / "consumer-installation-readiness.v1.json"
        self.bundle_root = self.report_root / "diagnostic-bundle"
        self.replacements = {
            self.repo_root.as_posix(): "<REPO_ROOT>",
            self.fixture_root.as_posix(): "<FIXTURE_ROOT>",
            Path.home().as_posix(): "<HOME>",
        }
        self.scenarios: dict[str, Any] = {}
        self.capabilities: dict[str, Any] = {}

    def cleanup(self) -> None:
        shutil.rmtree(self.fixture_root, ignore_errors=True)

    def sanitize(self, value: str) -> str:
        for source, replacement in self.replacements.items():
            value = value.replace(source, replacement)
        for key in ("GH_TOKEN", "GITHUB_TOKEN"):
            secret = os.environ.get(key)
            if secret:
                value = value.replace(secret, "<REDACTED>")
        # Validator diagnostics may echo an unsafe link outside our fixture.
        # Avoid retaining another user's absolute source path in public receipts.
        value = re.sub(
            r"(?<![\w:/])/(?:home|Users|private|tmp|var/tmp|workspace|workspaces|root|mnt|media|run/user)"
            r"(?:/[^\s\"'<>`),;\]}]+)*", "<PRIVATE_PATH>", value,
        )
        value = re.sub(r"(?<![\w])[A-Za-z]:[\\/][^\s\"'<>`),;\]}]+", "<PRIVATE_PATH>", value)
        return value

    def run_command(self, cwd: Path, *args: str) -> dict[str, Any]:
        result = {"command": self.sanitize(" ".join(args)), "cwd": self.sanitize(cwd.as_posix()),
                  "exit_code": None, "stdout": "", "stderr": "", "status": "blocked"}
        # Qualification targets the POSIX GitHub/cloud workspace. A private
        # process group lets the deadline stop git/gh descendants as well.
        if os.name != "posix":
            result["stderr"] = "Qualification requires POSIX process-group support"
            return result
        process = None
        finished = False
        buffers = {"stdout": bytearray(), "stderr": bytearray()}
        truncated = False
        deadline = time.monotonic() + self.timeout
        try:
            process = subprocess.Popen(list(args), cwd=cwd, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, start_new_session=True)
            with selectors.DefaultSelector() as selector:
                selector.register(process.stdout, selectors.EVENT_READ, "stdout")
                selector.register(process.stderr, selectors.EVENT_READ, "stderr")
                while selector.get_map():
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise subprocess.TimeoutExpired(list(args), self.timeout)
                    for key, _events in selector.select(min(remaining, 0.1)):
                        chunk = os.read(key.fileobj.fileno(), 65536)
                        if not chunk:
                            selector.unregister(key.fileobj)
                            continue
                        target = buffers[key.data]
                        available = max(0, 64000 - len(target))
                        truncated |= len(chunk) > available
                        target.extend(chunk[:available])
                code = process.wait(timeout=max(0.001, deadline - time.monotonic()))
                finished = True
                result.update(exit_code=code, status="pass" if code == 0 else "fail")
        except (OSError, subprocess.TimeoutExpired) as error:
            result["stderr"] = self.sanitize(str(error))[:64000]
        finally:
            if process is not None:
                if not finished:
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                process.stdout.close()
                process.stderr.close()
                process.wait(timeout=1)
        for stream, data in buffers.items():
            output = self.sanitize(data.decode("utf-8", errors="replace"))
            result[stream] = output + ("\n" + result[stream] if result[stream] else "")
        result["output_truncated"] = truncated
        return result

    def _sanitize_report(self, value: Any) -> Any:
        if isinstance(value, str):
            return self.sanitize(value)
        if isinstance(value, dict):
            return {self.sanitize(key): self._sanitize_report(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._sanitize_report(item) for item in value]
        return value

    def _require(self, scenario: dict, *, tools: tuple = (), dependencies: tuple = ()) -> bool:
        missing = [name for name in tools if not self.capabilities.get(name, {}).get("available")]
        unmet = [name for name in dependencies if self.scenarios.get(name, {}).get("status") != "pass"]
        if missing or unmet:
            scenario.update(status="blocked", reason="Unavailable prerequisites",
                            missing_capabilities=missing, unmet_scenarios=unmet)
            return False
        return True

    def _step(self, scenario: dict, cwd: Path, *args: str) -> dict:
        step = self.run_command(cwd, *args)
        scenario["steps"].append(step)
        if step["status"] == "fail" or (step["status"] == "blocked" and scenario["status"] != "fail"):
            scenario["status"] = step["status"]
        return step

    def _probe_capabilities(self) -> None:
        commands = {"git": ("git", "--version")}
        commands.update({f"gh-skill-{name}": ("gh", "skill", name, "--help")
                         for name in ("install", "list", "publish", "update")})
        for name, args in commands.items():
            probe = self.run_command(self.repo_root, *args)
            self.capabilities[name] = {"available": probe["status"] == "pass", "probe": probe}
        valid_remote = bool(
            re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*/[A-Za-z0-9][A-Za-z0-9_.-]*", self.remote_repository)
            and re.fullmatch(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", self.remote_tag or "")
            and re.fullmatch(r"[0-9a-f]{40}", self.remote_commit or "")
        )
        self.capabilities["immutable-remote-selection"] = {
            "available": valid_remote,
            "reason": "Release qualification requires explicit repository, stable tag and full commit",
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
            "tool_versions": {},
            "capabilities": self.capabilities,
            "scenarios": self.scenarios,
        }

        try:
            report["tool_versions"] = self._tool_versions()
            self._probe_capabilities()
            self._build_distribution()
            self._clean_local_distribution_install()
            self._portable_package_validation()
            self._publish_validation()
            self._remote_pinned_install()
            self._update_behavior()
            self._removal_cleanup()
        except Exception as error:
            self.scenarios["harness-error"] = {
                "id": "harness-error", "status": "fail", "reason": self.sanitize(str(error)),
                "steps": [], "checks": [],
            }
        finally:
            def complete(required: tuple) -> bool:
                return bool(required) and all(self.scenarios.get(name, {}).get("status") == "pass"
                                              for name in required) and "harness-error" not in self.scenarios
            report["local_status"] = "ready" if complete(LOCAL_REQUIRED) else "not-ready"
            report["overall_status"] = "ready" if complete(RELEASE_REQUIRED) else "not-ready"
            required = LOCAL_REQUIRED if self.scope == "local" else RELEASE_REQUIRED
            report["qualification"] = {"scope": self.scope, "required_scenarios": list(required),
                                       "complete": complete(required)}
            report = self._sanitize_report(report)
            try:
                self._write_report(report)
                if report["overall_status"] != "ready":
                    self._write_bundle(report)
            finally:
                self.cleanup()
        return report

    def _tool_versions(self) -> dict[str, str]:
        versions = {}
        for name, args in {
            "python": [sys.executable, "--version"],
            "git": ["git", "--version"],
            "gh": ["gh", "--version"],
        }.items():
            result = self.run_command(self.repo_root, *args)
            versions[name] = (result["stdout"] or result["stderr"]).strip()
        return versions

    def _build_distribution(self) -> None:
        scenario = {"id": "distribution-build", "status": "pass", "steps": [], "checks": []}
        self.scenarios[scenario["id"]] = scenario
        self._step(scenario, self.repo_root, sys.executable, "./aether", "distribution", "build",
                   "--output-directory", self.dist_root.as_posix())

    def _clean_local_distribution_install(self) -> None:
        scenario = {
            "id": "clean-local-distribution-install",
            "status": "pass",
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario["id"]] = scenario
        if not self._require(scenario, tools=("git", "gh-skill-install", "gh-skill-list"),
                             dependencies=("distribution-build",)):
            return
        self.local_consumer.mkdir(parents=True, exist_ok=True)
        if self._step(scenario, self.local_consumer, "git", "init", "-q")["status"] != "pass":
            return

        for skill_name, agent, expected_path in PILOT_SKILLS:
            step = self._step(scenario,
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
            if step["status"] == "blocked":
                return
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

        list_step = self._step(scenario,
            self.local_consumer,
            "gh",
            "skill",
            "list",
            "--json",
            "skillName,path,scope,pinned,sourceURL,version",
        )
        if list_step["status"] != "pass":
            return
        installed = json.loads(list_step["stdout"] or "[]")
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
        if not self._require(scenario, dependencies=("clean-local-distribution-install",)):
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
        if not self._require(scenario, tools=("gh-skill-publish",), dependencies=("distribution-build",)):
            return
        step = self._step(scenario,
            self.repo_root,
            "gh",
            "skill",
            "publish",
            self.dist_root.as_posix(),
            "--dry-run",
        )
        if step["status"] == "blocked":
            return
        self.check(
            scenario,
            "publish-dry-run",
            step["exit_code"] == 0,
            "gh skill publish <dist> --dry-run succeeds",
        )

    def _remote_pinned_install(self) -> None:
        repository, tag, commit = self.remote_repository, self.remote_tag, self.remote_commit
        if self.scope != "release":
            self.skipped(
                "pinned-remote-release-install",
                "Remote acceptance is not selected by local qualification",
            )
            return
        scenario = {
            "id": "pinned-remote-release-install",
            "status": "pass",
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario["id"]] = scenario
        if not self._require(scenario, tools=("git", "gh-skill-install", "gh-skill-list", "immutable-remote-selection")):
            return
        for label, pin in [("tag", tag), ("commit", commit)]:
            consumer = self.fixture_root / f"consumer-remote-{label}"
            consumer.mkdir(parents=True, exist_ok=True)
            if self._step(scenario, consumer, "git", "init", "-q")["status"] != "pass":
                return
            step = self._step(scenario,
                consumer,
                "gh",
                "skill",
                "install",
                repository,
                "create-architecture-document",
                "--pin",
                pin,
            )
            if step["status"] == "blocked":
                return
            self.check(
                scenario,
                f"remote-install-{label}",
                step["exit_code"] == 0,
                f"Remote pinned install succeeds by {label}",
            )
            if step["exit_code"] != 0:
                continue
            list_step = self._step(scenario,
                consumer,
                "gh",
                "skill",
                "list",
                "--json",
                "skillName,path,scope,pinned,sourceURL,version",
            )
            if list_step["status"] != "pass":
                return
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
        tag = self.remote_tag
        if self.scope != "release":
            self.skipped(
                "update-behavior",
                "Remote acceptance is not selected by local qualification",
            )
            return
        scenario = {
            "id": "update-behavior",
            "status": "pass",
            "steps": [],
            "checks": [],
        }
        self.scenarios[scenario["id"]] = scenario
        if not self._require(scenario, tools=("git", "gh-skill-install", "gh-skill-update", "immutable-remote-selection")):
            return
        consumer = self.fixture_root / "consumer-update"
        consumer.mkdir(parents=True, exist_ok=True)
        if self._step(scenario, consumer, "git", "init", "-q")["status"] != "pass":
            return
        install_step = self._step(scenario,
            consumer,
            "gh",
            "skill",
            "install",
            self.remote_repository,
            "create-architecture-document",
            "--pin",
            tag,
        )
        if install_step["status"] != "pass":
            return
        skill_path = consumer / ".agents" / "skills" / "create-architecture-document" / "SKILL.md"
        self.check(scenario, "update-installed-path", skill_path.is_file(), "Installed update target exists")
        if scenario["status"] != "pass":
            return
        before = skill_path.read_text(encoding="utf-8")
        skill_path.write_text(before + "\n<!-- local modification -->\n", encoding="utf-8")
        dry_run = self._step(scenario, consumer, "gh", "skill", "update", "--dry-run")
        if dry_run["status"] != "pass":
            return
        apply_run = self._step(scenario, consumer, "gh", "skill", "update", "--all")
        if apply_run["status"] != "pass":
            return
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
        if not self._require(scenario, dependencies=("clean-local-distribution-install",)):
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
        for scenario_id, scenario in report["scenarios"].items():
            (self.bundle_root / f"{scenario_id}.json").write_text(
                json.dumps(scenario, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=("local", "release"), default="local")
    parser.add_argument("--output", type=Path, required=True, help="New report directory; existing paths are refused")
    parser.add_argument("--remote-repository", default="egohygiene/aether")
    parser.add_argument("--remote-tag")
    parser.add_argument("--remote-commit")
    parser.add_argument("--timeout", type=int, default=120, help="Positive per-command deadline in seconds")
    args = parser.parse_args(argv)
    try:
        harness = ConsumerInstallationHarness(
            REPO_ROOT, report_root=args.output, scope=args.scope,
            remote_repository=args.remote_repository, remote_tag=args.remote_tag,
            remote_commit=args.remote_commit, timeout=args.timeout,
        )
        report = harness.run()
    except (OSError, ValueError) as error:
        print(f"Consumer qualification could not start: {error}", file=sys.stderr)
        return 2
    print(json.dumps({"report": str(harness.report_path), "local_status": report["local_status"],
                      "overall_status": report["overall_status"], "qualification": report["qualification"]}))
    return 0 if report["qualification"]["complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
