#!/usr/bin/env python3
"""Check quarantine intake and immutable removal evidence; never remove files."""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
from typing import Any, Callable
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
LEDGER = "catalog/reports/staging-residual-ledger.v1.json"
INTAKES = "catalog/staging/intakes.v1.json"
APPROVALS = "catalog/staging/removal-approvals.v1.json"
POLICY = "catalog/staging/guard-policy.v1.json"
DISPOSITIONS = "catalog/first-party/staging-dispositions/"
REPOSITORY = "egohygiene/aether"
LIMIT = 8 * 1024 * 1024
SHA = re.compile(r"[0-9a-f]{40}\Z")
DIGEST = re.compile(r"[0-9a-f]{64}\Z")
MISSING = object()


def require(condition: Any, message: str) -> None:
    if not condition:
        raise ValueError(message)


def document(raw: bytes) -> dict[str, Any]:
    require(len(raw) <= LIMIT, "input exceeds bound")
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    def invalid(_):
        raise ValueError("non-finite JSON number")
    data = json.loads(raw, object_pairs_hook=pairs, parse_constant=invalid)
    require(isinstance(data, dict), "JSON object required")
    return data


def text(value: Any) -> str:
    require(isinstance(value, str) and 0 < len(value) <= 2048 and
            not any(ord(c) < 32 or ord(c) == 127 for c in value), "invalid bounded text")
    return value


def path(value: Any, *, staged=False) -> str:
    value = text(value)
    require(not value.startswith("/") and "\\" not in value and
            PurePosixPath(value).as_posix() == value and
            not set(value.split("/")) & {"", ".", "..", ".git"} and
            (not staged or value.startswith(".staging/")), "invalid repository path")
    return value


def revision(value: Any) -> str:
    require(isinstance(value, str) and SHA.fullmatch(value), "full immutable commit/blob required")
    return value


def digest(value: Any) -> str:
    require(isinstance(value, str) and DIGEST.fullmatch(value), "SHA-256 required")
    return value


def closed(value: Any, fields: set[str]) -> dict[str, Any]:
    require(isinstance(value, dict) and set(value) == fields, "unsupported control record shape")
    return value


def git(root: Path, *args: str) -> bytes:
    environment = {"PATH": os.defpath, "LC_ALL": "C.UTF-8", "GIT_CONFIG_NOSYSTEM": "1",
                   "GIT_CONFIG_GLOBAL": os.devnull, "GIT_NO_REPLACE_OBJECTS": "1",
                   "GIT_NO_LAZY_FETCH": "1", "GIT_TERMINAL_PROMPT": "0", "GIT_OPTIONAL_LOCKS": "0"}
    result = subprocess.run(["git", "--no-optional-locks", "--literal-pathspecs", "-c", "core.hooksPath=/dev/null",
                             "-c", "core.fsmonitor=false", "-c", "protocol.allow=never", "-C", str(root), *args],
                            env=environment, check=True, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30)
    require(len(result.stdout) <= LIMIT, "Git output exceeds bound")
    return result.stdout


def tree(root: Path, ref: str, prefix="") -> dict[str, tuple[str, str]]:
    result = {}
    arguments = ["ls-tree", "-r", "-z", revision(ref)] + (["--", prefix] if prefix else [])
    for row in git(root, *arguments).split(b"\0"):
        if row:
            header, name = row.split(b"\t", 1)
            mode, kind, identity = header.decode().split()
            require(kind == "blob", "submodule requires a separately reviewed adapter")
            result[path(name.decode())] = mode, revision(identity)
    return result


def blob(root: Path, ref: str, name: str) -> bytes:
    return git(root, "cat-file", "blob", revision(ref) + ":" + path(name))


def git_json(root: Path, ref: str, name: str, default=None):
    try:
        return document(blob(root, ref, name))
    except subprocess.CalledProcessError:
        if default is not None:
            return default
        raise


def local_json(root: Path, name: str, default=MISSING):
    try:
        return document(local_bytes(root, name))
    except FileNotFoundError:
        if default is not MISSING:
            return default
        raise


def local_bytes(root: Path, name: str, *, literal_symlink=False) -> bytes:
    """Admit bounded regular bytes through no-follow directory descriptors."""
    components = path(name).split("/")
    require(hasattr(os, "O_NOFOLLOW") and hasattr(os, "O_DIRECTORY"), "safe local input admission unavailable")
    descriptors = []
    try:
        current = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        descriptors.append(current)
        for component in components[:-1]:
            current = os.open(component, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=current)
            descriptors.append(current)
        mode = os.stat(components[-1], dir_fd=current, follow_symlinks=False).st_mode
        if stat.S_ISLNK(mode):
            require(literal_symlink, "control source must not be an alias")
            return os.readlink(components[-1], dir_fd=current).encode("utf-8")
        require(stat.S_ISREG(mode), "special staging input is unsupported")
        descriptor = os.open(components[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=current)
        with os.fdopen(descriptor, "rb") as stream:
            observed = os.fstat(stream.fileno())
            require(stat.S_ISREG(observed.st_mode) and observed.st_size <= LIMIT, "regular bounded input required")
            payload = stream.read(LIMIT + 1)
            require(len(payload) <= LIMIT, "input exceeds bound")
            return payload
    finally:
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def intake_records(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    closed(data, {"schema_version", "records"})
    require(data["schema_version"] == "aether.staging-intakes/v1" and isinstance(data["records"], list), "intake contract mismatch")
    result, ids = {}, set()
    for row in data["records"]:
        closed(row, {"id", "path", "sha256", "owner", "classification", "reason", "authority"})
        identity = text(row["id"])
        name = path(row["path"], staged=True)
        digest(row["sha256"])
        text(row["owner"]); text(row["reason"])
        require(row["classification"] in {"first-party-candidate", "external-snapshot", "unknown-provenance", "consumer-prototype"}, "unsupported intake classification")
        require(row["authority"] == "quarantine-only", "intake cannot grant adoption or removal")
        require(identity not in ids and name not in result, "duplicate intake identity/path")
        ids.add(identity); result[name] = row
    return result


def disposition_record(data: dict[str, Any]) -> None:
    """Keep flat first-party and singular/plural historical hook adapters distinct."""
    require(("staging_path" in data) != ("staging_paths" in data), "disposition needs exactly one path adapter")
    paths = data.get("staging_paths", [data.get("staging_path")])
    require(isinstance(paths, list) and paths, "disposition paths required")
    for value in paths:
        path(value.rstrip("/") if isinstance(value, str) else value, staged=True)
    text(data.get("reason"))
    if "lock_reference" in data:
        require(data.get("disposition") in {"preserve-migration-evidence", "ingest-planned", "external-reference", "not-adopted"}, "unsupported first-party disposition")
        require(data.get("hash_status") in {"reconstructed", "unverified", "unknown"}, "unsupported historical hash state")
        require(data.get("hash_algorithm") in {"sha256-utf8-lf", "sha256-tree", "unknown"}, "unsupported historical hash algorithm")
        text(data["lock_reference"]); text(data.get("trust_classification"))
    else:
        require(data.get("disposition") in {"move-out", "reject", "needs-human-review"}, "unsupported hook disposition")
        require(data.get("owner") is None or isinstance(data.get("owner"), str), "hook owner must remain explicit")
        text(data.get("adr_reference")); text(data.get("trust_classification"))
        reviewed_date = text(data.get("reviewed_date"))
        require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", reviewed_date), "calendar review date required")
        date.fromisoformat(reviewed_date)
        for field in ("safety_concerns", "adoption_blocked_by", "adoption_conditions"):
            if field in data:
                require(isinstance(data[field], list), "hook reasons must be arrays")
                for value in data[field]: text(value)
    # These legacy records preserve decisions; neither adapter authenticates approval.


def check_worktree(root: Path) -> list[str]:
    errors = []
    try:
        ledger = local_json(root, LEDGER, {"files": []})
        baseline = {row["path"]: row["sha256"] for row in ledger["files"]}
        intakes = intake_records(local_json(root, INTAKES, {"schema_version": "aether.staging-intakes/v1", "records": []}))
        approvals(local_json(root, APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": []}))
        configured_policy = local_json(root, POLICY, None)
        if configured_policy is not None:
            policy_record(configured_policy)
        staging = root / ".staging"
        require(not staging.is_symlink(), "staging root must not be an alias")
        if staging.exists():
            for directory, directories, files in os.walk(staging, followlinks=False):
                aliases = [name for name in directories if (Path(directory) / name).is_symlink()]
                directories[:] = [name for name in directories if name not in aliases]
                for name in files + aliases:
                    selected = Path(directory) / name
                    relative = selected.relative_to(root).as_posix()
                    payload = local_bytes(root, relative, literal_symlink=True)
                    observed = hashlib.sha256(payload).hexdigest()
                    if baseline.get(relative) != observed and intakes.get(relative, {}).get("sha256") != observed:
                        errors.append("unrecorded or changed quarantine intake: " + relative)
        for selected in sorted((root / DISPOSITIONS).glob("*.json")):
            disposition_record(local_json(root, selected.relative_to(root).as_posix()))
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors.append("staging control unavailable or invalid: " + type(error).__name__)
    return errors


def approvals(data: dict[str, Any]) -> dict[str, dict[str, Any]]:
    closed(data, {"schema_version", "records"})
    require(data["schema_version"] == "aether.staging-removal-approvals/v1" and isinstance(data["records"], list), "approval contract mismatch")
    result = {}
    for row in data["records"]:
        closed(row, {"id", "source", "specification", "disposition", "attestation"})
        identity = text(row["id"])
        require(identity not in result, "duplicate removal record")
        closed(row["source"], {"revision", "path", "mode", "blob"})
        revision(row["source"]["revision"]); path(row["source"]["path"], staged=True); revision(row["source"]["blob"])
        require(row["source"]["mode"] in {"100644", "100755", "120000"}, "unsupported preimage mode")
        text(row["specification"])
        require(isinstance(row["disposition"], dict) and row["disposition"].get("kind") in {"canonical", "external-planned", "rejected"}, "unsupported removal disposition")
        closed(row["disposition"], {"kind", "revision", "path", "sha256"})
        revision(row["disposition"]["revision"])
        path(row["disposition"]["path"])
        digest(row["disposition"]["sha256"])
        if row["attestation"] is not None:
            closed(row["attestation"], {"pull_request", "comment_id", "review_commit"})
            for field in ("pull_request", "comment_id"):
                require(type(row["attestation"][field]) is int and row["attestation"][field] > 0, "provider record identity required")
            revision(row["attestation"]["review_commit"])
        result[identity] = row
    return result


def payload_digest(row: dict[str, Any]) -> str:
    payload = {key: value for key, value in row.items() if key != "attestation"}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()


def policy_record(policy: dict[str, Any]) -> None:
    closed(policy, {"schema_version", "repository", "approvers", "adr"})
    require(policy["schema_version"] == "aether.staging-guard-policy/v1" and policy["adr"] == "ADR-0005"
            and policy["repository"] == REPOSITORY, "base policy incompatible")
    require(isinstance(policy["approvers"], list) and policy["approvers"], "designated approval accounts unavailable")
    identities = set()
    for account in policy["approvers"]:
        closed(account, {"id", "login"})
        require(type(account["id"]) is int and account["id"] > 0 and account["id"] not in identities,
                "unique stable provider account identity required")
        text(account["login"])
        identities.add(account["id"])


class GitHubEvidence:
    """Read provider records over authenticated HTTPS; accept no fixture-file CLI."""
    def __init__(self, repository: str):
        require(re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository), "repository identity required")
        self.repository = repository

    def __call__(self, suffix: str) -> dict[str, Any]:
        token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        require(bool(token), "provider approval evidence unavailable")
        request = urllib.request.Request("https://api.github.com/repos/" + self.repository + "/" + suffix,
            headers={"Accept": "application/vnd.github+json", "Authorization": "Bearer " + str(token), "X-GitHub-Api-Version": "2022-11-28"})
        with urllib.request.urlopen(request, timeout=20) as response:
            return document(response.read(LIMIT + 1))


def check_diff(root: Path, base: str, head: str, pull_request: int = 0,
               provider: Callable[[str], dict[str, Any]] | None = None) -> dict[str, Any]:
    revision(base); revision(head)
    git(root, "merge-base", "--is-ancestor", base, head)
    before, after = tree(root, base, ".staging"), tree(root, head, ".staging")
    changes = [name for name in sorted(set(before) | set(after)) if before.get(name) != after.get(name)]
    incoming = intake_records(git_json(root, head, INTAKES, {"schema_version": "aether.staging-intakes/v1", "records": []}))
    old = approvals(git_json(root, base, APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": []}))
    current = approvals(git_json(root, head, APPROVALS, {"schema_version": "aether.staging-removal-approvals/v1", "records": []}))
    require(all(current.get(key) == value or (
                    value["attestation"] is None and current.get(key) is not None and
                    current[key]["attestation"] is not None and
                    payload_digest(current[key]) == payload_digest(value))
                for key, value in old.items()),
            "base-admitted approval payloads and completed attestations are immutable")
    changed_old = [name for name in changes if name in before]
    for name in changed_old:
        matching = [row for row in old.values() if row["source"]["path"] == name and
                    (row["source"]["mode"], row["source"]["blob"]) == before[name]]
        require(len(matching) == 1 and matching[0]["attestation"] is not None,
                "missing base-admitted exact preimage approval: " + name)
    policy = git_json(root, base, POLICY) if changed_old else None
    if policy:
        policy_record(policy)
        provider = provider or GitHubEvidence(policy["repository"])
        pr = provider("pulls/" + str(pull_request))
        require(pull_request > 0 and pr.get("head", {}).get("sha") == head and pr.get("base", {}).get("sha") == base, "actual PR base/head do not match")
        require(pr.get("base", {}).get("repo", {}).get("full_name") == REPOSITORY, "actual PR repository does not match")
        require(re.search(r"\bADR-0005\b", pr.get("body") or ""), "removal PR must reference ADR-0005")
    verified = []
    for name in changes:
        if name in after:
            observed = hashlib.sha256(blob(root, head, name)).hexdigest()
            require(incoming.get(name, {}).get("sha256") == observed, "new or changed source needs exact intake: " + name)
        if name not in before:
            continue
        matching = [row for row in old.values() if row["source"]["path"] == name and
                    (row["source"]["mode"], row["source"]["blob"]) == before[name]]
        require(len(matching) == 1, "missing base-admitted exact preimage approval: " + name)
        row = matching[0]
        require(row["attestation"] is not None, "human account attestation unavailable")
        git(root, "merge-base", "--is-ancestor", row["source"]["revision"], base)
        require(tree(root, row["source"]["revision"], name).get(name) == before[name], "recorded source preimage changed")
        disposition = row["disposition"]
        closed(disposition, {"kind", "revision", "path", "sha256"})
        destination = path(disposition["path"])
        revision(disposition["revision"]); digest(disposition["sha256"])
        git(root, "merge-base", "--is-ancestor", disposition["revision"], base)
        retained = blob(root, disposition["revision"], destination)
        require(tree(root, disposition["revision"], destination).get(destination, (None,))[0] in {"100644", "100755"}
                and tree(root, head, destination).get(destination, (None,))[0] in {"100644", "100755"},
                "durable destination must be regular Git source")
        require(hashlib.sha256(retained).hexdigest() == disposition["sha256"] and
                blob(root, head, destination) == retained, "durable destination/rejection receipt changed")
        if disposition["kind"] == "canonical":
            require(destination.startswith("library/organization/"), "canonical disposition requires canonical source")
        elif disposition["kind"] == "external-planned":
            raise ValueError("external planned-source removal needs a separately qualified origin adapter; external catalog alone does not satisfy ADR-0005")
        else:
            recorded = document(retained)
            disposition_record(recorded)
            require(recorded.get("disposition") in {"reject", "not-adopted"}, "rejection must be explicit")
            targets = recorded.get("staging_paths", [recorded.get("staging_path", "")])
            require(any(name == value or (value.endswith("/") and name.startswith(value)) for value in targets), "rejection receipt is for different source")
        if not row["specification"].startswith("out-of-scope: "):
            specification = path(row["specification"])
            require(specification.startswith("library/organization/specs/") and specification.endswith(".spec.md"), "review specification or explicit waiver required")
            require(blob(root, base, specification) == blob(root, row["attestation"]["review_commit"], specification),
                    "review specification changed after attestation")
        else:
            text(row["specification"][len("out-of-scope: "):])
        attestation = row["attestation"]
        git(root, "merge-base", "--is-ancestor", attestation["review_commit"], base)
        reviewed = approvals(git_json(root, attestation["review_commit"], APPROVALS)).get(row["id"])
        require(reviewed is not None and payload_digest(reviewed) == payload_digest(row), "approval scope changed after reviewed commit")
        comment = provider("issues/comments/" + str(attestation["comment_id"]))
        require(comment.get("user", {}).get("type") == "User" and
                comment.get("user", {}).get("id") in {account["id"] for account in policy["approvers"]},
                "provider account is not designated human attester")
        require(comment.get("issue_url") == "https://api.github.com/repos/" + policy["repository"] + "/issues/" + str(attestation["pull_request"]), "attestation belongs to another conversation")
        marker = "AETHER-STAGING-APPROVE " + row["id"] + " sha256:" + payload_digest(row) + " source:" + attestation["review_commit"]
        body = comment.get("body")
        require(isinstance(body, str) and body.strip() == marker, "provider attestation must be the sole explicit exact-plan statement")
        verified.append(row["id"])
    return {"schema_version": "aether.staging-diff-evidence/v1", "base": base, "head": head,
            "changed_paths": changes, "verified_attestations": verified,
            "scope": "Provider account statements bound to immutable plans; no proof of a human's physical presence, lifecycle promotion or permission to execute staged code."}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("intake", "diff"))
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--pull-request", type=int, default=0)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--controller-revision", help="CI requires this script to match the immutable base controller")
    args = parser.parse_args()
    try:
        if args.command == "intake":
            errors = check_worktree(args.repository_root)
            report = {"status": "fail" if errors else "pass", "errors": errors, "scope": "quarantine-intake-only"}
        else:
            if args.controller_revision:
                require(revision(args.controller_revision) == args.base and
                        Path(__file__).read_bytes() == blob(args.repository_root, args.base, "catalog/staging_guard.py"),
                        "controller does not match the immutable base")
            report = check_diff(args.repository_root, args.base, args.head, args.pull_request)
            report["controller_revision"] = args.controller_revision
            errors = []
            report["status"] = "pass"
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError, urllib.error.URLError) as error:
        errors = [str(error) if isinstance(error, ValueError) else "staging evidence unavailable: " + type(error).__name__]
        report = {"status": "fail", "errors": errors}
    encoded = json.dumps(report, sort_keys=True) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(encoded)
    print(encoded, end="")
    return int(bool(errors))


if __name__ == "__main__":
    raise SystemExit(main())
