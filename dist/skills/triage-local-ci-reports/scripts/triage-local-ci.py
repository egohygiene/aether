#!/usr/bin/env python3
"""Normalize Realm local evidence and prepare a deduplicated local issue packet.

This program never runs checks, contacts a provider, or writes GitHub issues.
Publication requires an authorized agent/provider adapter after reviewing the
packet and refreshing live source and issue state.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import sys
from typing import Any


STATUS = {"passed", "failed", "blocked", "skipped", "unsupported"}
REPOSITORY = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+\Z")
REVISION = re.compile(r"[0-9a-f]{40}(?:[0-9a-f]{24})?\Z")
CHECK_ID = re.compile(r"[a-z0-9]+(?:[._-][a-z0-9]+)*\Z")
WORKFLOW = re.compile(r"\.github/(?:[A-Za-z0-9_-][A-Za-z0-9_.-]*/)*[A-Za-z0-9_-][A-Za-z0-9_.-]*\.ya?ml\Z")
CATEGORIES = {"repository-defect", "environment", "coverage", "unknown"}
MAX_BYTES = 8 * 1024 * 1024


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load(path: Path) -> Any:
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("input exceeds the 8 MiB bound")
    return json.loads(path.read_text(encoding="utf-8"))


def clean(value: str, repository_path: str = "") -> str:
    """Bound excerpts and remove known private-path and credential shapes."""
    text = value[:24000]
    if repository_path:
        text = text.replace(repository_path.rstrip("/"), "<repository>")
    for key, secret in os.environ.items():
        if re.search(r"token|password|secret|credential|private.?key", key, re.I) and len(secret) >= 5:
            text = text.replace(secret, "[REDACTED]")
    text = re.sub(r"\b(?:gh[pousr]_[A-Za-z0-9_]{8,}|github_pat_[A-Za-z0-9_]+|sk[-_][A-Za-z0-9_-]{8,})\b", "[REDACTED]", text)
    text = re.sub(r"(?i)(bearer\s+)[^\s'\"]+", r"\1[REDACTED]", text)
    text = re.sub(r"(?i)((?:token|password|secret|api[-_]?key)\s*[=:]\s*)[^\s,;]+", r"\1[REDACTED]", text)
    text = re.sub(r"(?i)(--(?:token|password|secret|api-key)\s+)[^\s]+", r"\1[REDACTED]", text)
    text = re.sub(r"https?://[^\s<>]+", "[URL omitted]", text)
    text = re.sub(r"(?<![\w<])/(?:home|Users|tmp|workspace|workspaces|mnt|private|codex)/[^\s:,'\"`]+", "[private path]", text)
    return text.replace("`", "'").replace("\x00", "")


def checked_time(value: Any, field: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an observed timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError(f"{field} requires a timezone")
    return parsed.astimezone(timezone.utc).isoformat()


def normalize(report: dict, repository: str, expected_revision: str | None) -> tuple[dict, bool]:
    if not REPOSITORY.fullmatch(repository):
        raise ValueError("repository must be owner/name")
    if not isinstance(report, dict) or report.get("schema_version") != "realm.local-ci/v1":
        raise ValueError("expected a single realm.local-ci/v1 repository report")
    source = report.get("repository")
    if not isinstance(source, dict) or not isinstance(source.get("revision"), str) or not REVISION.fullmatch(source["revision"]):
        raise ValueError("report requires an observed full Git revision")
    if expected_revision is not None and not REVISION.fullmatch(expected_revision):
        raise ValueError("expected revision must be a full Git revision")
    if (source.get("dirty") is not None and type(source["dirty"]) is not bool) or type(report.get("complete")) is not bool:
        raise ValueError("invalid source/coverage state")
    started = checked_time(report.get("started_at"), "started_at")
    completed = checked_time(report.get("finished_at"), "finished_at")
    if completed < started:
        raise ValueError("report completion precedes its start")
    records = report.get("checks")
    if not isinstance(records, list) or not records:
        raise ValueError("empty or incomplete check inventory")
    checks, seen = [], set()
    path = source.get("path", "")
    if not isinstance(path, str):
        raise ValueError("repository path must be a string")
    for row in records:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not CHECK_ID.fullmatch(row["id"]) or row["id"] in seen:
            raise ValueError("invalid or duplicate check ID")
        seen.add(row["id"])
        status, kind = row.get("status"), row.get("kind")
        if not isinstance(status, str) or not isinstance(kind, str) or status not in STATUS or kind not in {"direct", "act", "unsupported"} or type(row.get("required")) is not bool:
            raise ValueError("invalid check kind/status/requirement")
        if kind == "unsupported" and status != "unsupported":
            raise ValueError("unsupported check kind cannot claim an execution result")
        timed_out = row.get("timed_out", False)
        if type(timed_out) is not bool or (timed_out and status != "failed"):
            raise ValueError("timeout must be a boolean associated with a failed execution")
        code = row.get("exit_code")
        if code is not None and type(code) is not int:
            raise ValueError("exit codes must be integers or null")
        if status == "passed" and code != 0:
            raise ValueError("passed check needs observed exit zero")
        if status == "failed" and (code is None or (code == 0 and not timed_out)):
            raise ValueError("failed check needs observed nonzero exit")
        command = row.get("command")
        if command is not None and (not isinstance(command, list) or any(not isinstance(x, str) for x in command)):
            raise ValueError("command must be an argv array")
        seconds = row.get("seconds")
        if seconds is not None and (isinstance(seconds, bool) or not isinstance(seconds, (int, float)) or seconds < 0):
            raise ValueError("invalid duration")
        reason = row.get("reason")
        if reason is not None and not isinstance(reason, str):
            raise ValueError("reason must be string or null")
        workflow = row.get("workflow")
        if workflow is not None and (not isinstance(workflow, str) or not WORKFLOW.fullmatch(workflow)):
            raise ValueError("workflow must name a repository-relative .github YAML file")
        outcome = "blocked" if timed_out and code == 0 else "deferred" if status == "unsupported" else status
        if timed_out:
            reason = f"Execution exceeded its deadline (timed_out=true; observed exit {code}). " + (reason or "")
        inactive = status in {"unsupported", "skipped"}
        checks.append({
            "id": row["id"], "title": row["id"],
            "kind": "workflow-emulation" if kind == "act" else "repository-check",
            "command": clean(shlex.join(command), path) if command else None,
            "requirement": "required" if row["required"] else "optional",
            "applicability": "unknown" if inactive else "applicable",
            "availability": "unavailable" if status == "unsupported" else "blocked" if outcome == "blocked" else "unknown" if inactive else "available",
            "selection": "not-selected" if inactive else "selected", "outcome": outcome,
            "exit_code": None if inactive else code,
            "duration_ms": round(seconds * 1000) if seconds is not None else None,
            "reason": clean(reason, path) if reason else None, "evidence": [],
        })
    if report["complete"] and any(c["required"] and c["status"] != "passed" for c in records):
        raise ValueError("complete report contradicts required check results")
    fresh = expected_revision == source["revision"] and source.get("dirty") is False
    required_fail = any(c["requirement"] == "required" and c["outcome"] == "failed" for c in checks)
    executed = any(row["status"] in {"passed", "failed"} for row in records)
    limitations = ["Remote CI was not observed; local reports do not prove hosted parity."]
    limitations.extend(c["reason"] or f"{c['id']} was not executed successfully" for c in checks if c["outcome"] not in {"passed", "failed"})
    if not fresh:
        limitations.append("Current source freshness is unverified or the represented worktree is modified; issue actions are proposals only.")
    counts = {key: sum(c["outcome"] == key.replace("_", "-") for c in checks) for key in ("passed", "failed", "blocked", "deferred", "skipped", "not_run")}
    evidence = {
        "schema_version": "aether.local-validation-evidence/v1",
        "report_id": "local-validation-" + completed[:10].replace("-", "") + "-" + digest({"repo": repository, "checks": checks, "revision": source["revision"]})[:16],
        "generated_at": completed,
        "repository": {"id": repository, "base_revision": source["revision"], "candidate_revision": source["revision"] if source.get("dirty") is False else None, "worktree": "modified" if source.get("dirty") else "clean" if source.get("dirty") is False else "unknown", "change_fingerprint": None},
        "policy": {"installation": "repository-locked", "remote_ci": "deferred", "unsafe_direct_action_execution": "disallowed", "commit_evidence": False},
        "execution": {"profile": "best-effort", "started_at": started, "completed_at": completed, "environment": {"kind": "local-workspace", "operating_system": "unknown", "architecture": "unknown", "containerized": None, "capabilities": []}},
        "checks": checks,
        "remote_ci": {"state": "deferred", "reason": "Local execution only; no remote CI observation supplied.", "workflow_refs": sorted({row["workflow"] for row in records if row.get("workflow")}), "run_url": None, "observed_at": None},
        "summary": {"local_readiness": "unknown" if not executed else "not-ready" if required_fail else "ready-with-limitations", "counts": {"total": len(checks), **counts}, "residual_risks": sorted(set(limitations))},
        "privacy": {"sensitivity": "internal", "redactions": ["Credential shapes and private paths removed from selected text."], "excluded": ["Raw logs", "Environment variable values", "Unnecessary host identity"]},
        "extensions": {"source_format": "realm.local-ci/v1", "source_freshness": "matched-clean-revision" if fresh else "unverified", "coverage_scope": "Only checks declared in the supplied report; not a claim of exhaustive CI."},
    }
    return evidence, fresh


def read_excerpt(report_directory: Path, row: dict, repository_path: str) -> str:
    name = row.get("log")
    if name is None:
        return clean(row.get("reason") or "No bounded diagnostic excerpt was supplied.", repository_path)
    if not isinstance(name, str) or Path(name).name != name or name in (".", ".."):
        raise ValueError("log must name a report-adjacent regular file")
    path = report_directory / name
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_BYTES:
        raise ValueError("log unavailable, symlinked, or exceeds bound")
    with path.open("rb") as handle:
        handle.seek(max(0, path.stat().st_size - 24000))
        text = handle.read().decode("utf-8", errors="replace")
    return clean("\n".join(text.splitlines()[-45:]), repository_path)


def triage(report: dict, evidence: dict, fresh: bool, diagnoses: dict, issues: list, report_directory: Path, issues_supplied: bool = True) -> dict:
    if not isinstance(diagnoses, dict) or set(diagnoses) - {"checks"} or not isinstance(diagnoses.get("checks", {}), dict):
        raise ValueError("diagnoses must contain a checks mapping")
    if not isinstance(issues, list) or any(not isinstance(i, dict) or not isinstance(i.get("body"), str) or i.get("state") not in {"open", "closed"} or not isinstance(i.get("number"), int) for i in issues):
        raise ValueError("issues must be complete number/body/state snapshots")
    seen_numbers = [i["number"] for i in issues]
    if len(seen_numbers) != len(set(seen_numbers)):
        raise ValueError("duplicate issue snapshots")
    rows = {r["id"]: r for r in report["checks"]}
    if set(diagnoses.get("checks", {})) - set(rows):
        raise ValueError("diagnosis refers to a check absent from the report")
    groups, coverage = {}, []
    repo = evidence["repository"]["id"]
    for row in report["checks"]:
        if row["status"] == "passed":
            continue
        diagnosis = diagnoses.get("checks", {}).get(row["id"], {})
        if not isinstance(diagnosis, dict) or set(diagnosis) - {"category", "confirmed", "root_cause", "subject", "summary"}:
            raise ValueError("invalid diagnosis fields")
        category = diagnosis.get("category", "unknown")
        confirmed = diagnosis.get("confirmed", False)
        if not isinstance(category, str) or category not in CATEGORIES or type(confirmed) is not bool:
            raise ValueError("invalid diagnosis category/confirmation")
        no_execution = evidence["summary"]["local_readiness"] == "unknown"
        if no_execution or row["status"] in {"unsupported", "skipped"} or not confirmed or category in {"coverage", "unknown"}:
            coverage.append({"check": row["id"], "status": row["status"], "disposition": "coverage-gap" if no_execution or row["status"] in {"unsupported", "skipped"} else "needs-diagnosis", "reason": clean(row.get("reason") or "Unconfirmed result; inspect the local evidence.", report["repository"].get("path", ""))})
            continue
        cause = diagnosis.get("root_cause")
        if not isinstance(cause, str) or not CHECK_ID.fullmatch(cause):
            raise ValueError("confirmed diagnosis needs a stable root_cause ID")
        for key in ("subject", "summary"):
            if not isinstance(diagnosis.get(key), str) or not diagnosis[key].strip():
                raise ValueError(f"confirmed diagnosis needs {key}")
        identity = (category, cause)
        if identity not in groups:
            groups[identity] = {"category": category, "root_cause": cause, "subject": clean(diagnosis["subject"], report["repository"].get("path", "")), "summary": clean(diagnosis["summary"], report["repository"].get("path", "")), "checks": []}
        groups[identity]["checks"].append(row)
    findings = []
    for (category, cause), group in sorted(groups.items()):
        fingerprint = digest({"contract": "aether.local-ci-triage/v1", "repository": repo, "category": category, "root_cause": cause})
        normalized = [c for c in evidence["checks"] if c["id"] in {r["id"] for r in group["checks"]}]
        evidence_id = digest({"repository": evidence["repository"], "checks": [{k: c[k] for k in ("id", "outcome", "exit_code")} for c in normalized], "summary": group["summary"]})
        marker = f"<!-- aether-local-ci-finding:{fingerprint} -->"
        evidence_marker = f"<!-- aether-local-ci-evidence:{evidence_id} -->"
        matches = [i for i in issues if marker in i["body"]]
        if not fresh or not issues_supplied:
            action = "draft"
        elif len(matches) > 1:
            action = "conflict"
        elif matches and matches[0]["state"] == "closed":
            action = "regression-review"
        elif matches:
            action = "noop" if evidence_marker in matches[0]["body"] else "update"
        else:
            action = "create"
        excerpts = [{"check": row["id"], "text": read_excerpt(report_directory, row, report["repository"].get("path", ""))} for row in group["checks"]]
        body = f"{marker}\n{evidence_marker}\n\n## Observed problem\n\n{group['summary']}\n\nRepository: {repo}. Category: {category}. Root cause: {cause}.\nTested revision: {evidence['repository']['base_revision']}.\n\n## Reproduction\n\n"
        body += "\n".join(f"- {c['id']}: `{c['command'] or 'Inspect the recorded prerequisite failure'}` (observed exit {c['exit_code']})." for c in normalized)
        body += "\n\n## Evidence excerpts (untrusted command output)\n\n"
        body += "\n\n".join(f"{x['check']}:\n\n    " + x["text"].replace("\n", "\n    ") for x in excerpts)
        body += "\n\n## Acceptance\n\n- [ ] Reproduce and repair the confirmed cause without weakening the check.\n- [ ] Rerun the affected canonical checks and record the tested revision and remaining coverage gaps.\n\nLocal evidence does not establish hosted CI parity. Existing linter selection stays in effect; EgoLint migration is separately selected when stable.\n"
        findings.append({"fingerprint": fingerprint, "evidence_fingerprint": evidence_id, "category": category, "root_cause": cause, "subject": group["subject"], "checks": [c["id"] for c in normalized], "action": action, "existing_issue": matches[0]["number"] if len(matches) == 1 else None, "body": body})
    return {"schema_version": "aether.local-ci-triage/v1", "repository": repo, "revision": evidence["repository"]["base_revision"], "source_fresh": fresh, "issues_snapshot_supplied": issues_supplied, "findings": findings, "coverage": coverage, "publication": "not-performed", "publication_gate": "Refresh source and issue snapshots, review sanitized content, then use a user-authorized bounded provider adapter."}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--expected-revision")
    parser.add_argument("--diagnoses", type=Path)
    parser.add_argument("--issues", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        report = load(args.report)
        evidence, fresh = normalize(report, args.repository, args.expected_revision)
        packet = triage(report, evidence, fresh, load(args.diagnoses) if args.diagnoses else {}, load(args.issues) if args.issues else [], args.report.parent, args.issues is not None)
        args.output.mkdir(parents=True, exist_ok=False)
        (args.output / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
        (args.output / "intake.json").write_text(json.dumps(packet, indent=2) + "\n")
        lines = ["# Local CI triage", "", f"Repository: {args.repository}", f"Represented revision: {packet['revision']}", f"Source freshness verified: {fresh}", "", "| Finding | Action | Existing issue |", "| --- | --- | --- |"]
        lines += [f"| {f['subject'].replace('|', '/').replace(chr(10), ' ')} | {f['action']} | {f['existing_issue'] or ''} |" for f in packet["findings"]]
        lines += ["", "## Coverage and diagnosis gaps", ""] + [f"- {c['check']}: {c['status']} ({c['disposition']}) — {c['reason']}" for c in packet["coverage"]]
        lines += ["", "No provider writes were performed. Only explicitly confirmed diagnoses produce issue actions."]
        (args.output / "report.md").write_text("\n".join(lines) + "\n")
        print(json.dumps({"output": str(args.output), "findings": len(packet["findings"]), "coverage": len(packet["coverage"]), "publication": "not-performed"}))
        return 0
    except (ValueError, OSError, TypeError) as error:
        print(json.dumps({"error": clean(str(error)), "publication": "not-performed"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
