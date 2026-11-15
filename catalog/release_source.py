"""Resolve and recheck an existing release tag; never create or move refs."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


def resolve_release_source(repository: Path, tag: str, default_branch: str,
                           expected_commit: str | None = None) -> dict[str, str]:
    if not re.fullmatch(r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)", tag):
        raise ValueError("release tag must be exact vMAJOR.MINOR.PATCH")
    if expected_commit is not None and not re.fullmatch(r"[0-9a-f]{40}", expected_commit):
        raise ValueError("expected commit must be a full immutable SHA")

    def git(*args: str) -> str:
        result = subprocess.run(["git", "-c", "core.fsmonitor=false", *args], cwd=repository,
                                text=True, capture_output=True, timeout=60, check=False)
        if result.returncode:
            raise ValueError(f"release source verification failed: git {args[0]}")
        return result.stdout.strip()

    git("check-ref-format", "--branch", default_branch)
    ref = f"refs/tags/{tag}"
    lines = git("ls-remote", "--exit-code", "--tags", "origin", ref, ref + "^{}").splitlines()
    remote: dict[str, str] = {}
    for line in lines:
        fields = line.split()
        if (len(fields) != 2 or fields[1] not in {ref, ref + "^{}"}
                or fields[1] in remote or not re.fullmatch(r"[0-9a-f]{40}", fields[0])):
            raise ValueError("remote returned an ambiguous release tag")
        remote[fields[1]] = fields[0]
    if ref not in remote:
        raise ValueError("release tag does not exist at origin")
    commit = remote.get(ref + "^{}", remote[ref])
    if expected_commit is not None and commit != expected_commit:
        raise ValueError("release tag moved after validation")
    if git("rev-parse", "--verify", "HEAD^{commit}") != commit:
        raise ValueError("checked out source differs from the remote release commit")
    if git("rev-parse", "--verify", ref + "^{commit}") != commit:
        raise ValueError("local release tag differs from the remote release commit")
    git("fetch", "--no-tags", "origin",
        f"+refs/heads/{default_branch}:refs/remotes/origin/{default_branch}")
    git("merge-base", "--is-ancestor", commit, f"refs/remotes/origin/{default_branch}")
    return {"release_tag": tag, "release_ref": ref, "commit_sha": commit}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository", type=Path, default=Path("."))
    parser.add_argument("--release-tag", required=True)
    parser.add_argument("--default-branch", required=True)
    parser.add_argument("--expected-commit")
    args = parser.parse_args()
    try:
        print(json.dumps(resolve_release_source(args.repository, args.release_tag,
                                               args.default_branch, args.expected_commit), sort_keys=True))
    except (OSError, ValueError, subprocess.TimeoutExpired) as exc:
        parser.exit(1, f"Release source refused: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
