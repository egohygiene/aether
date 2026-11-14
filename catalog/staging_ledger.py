#!/usr/bin/env python3
"""Inventory retained Git blobs without executing, adopting or removing them."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEDGER = Path("catalog/reports/staging-residual-ledger.v1.json")
SCHEMA = Path("catalog/schemas/aether.staging-residual-ledger.v1.schema.json")
SKILL_INVENTORY = "catalog/reports/staged-skills-inventory.v1.json"
AGENT_LEDGER = ".staging/manifests/agents-ledger.json"
DISPOSITIONS = "catalog/first-party/staging-dispositions"
BUCKETS = {"agents", "hooks", "instructions", "integrations", "manifests", "scripts", "skills", "specs"}


class GitSource:
    """Read an immutable Git tree; never follow a staged filesystem alias."""

    def __init__(self, root: Path, revision: str):
        self.root = root
        if revision.startswith("-"):
            raise ValueError("revision cannot be a Git option")
        self.revision = self.git("rev-parse", "--verify", "--end-of-options", revision + "^{commit}").decode().strip()
        if not re.fullmatch(r"[0-9a-f]{40}", self.revision):
            raise ValueError("an immutable SHA-1 Git commit is required")
        self.inputs: dict[str, str] = {}

    def git(self, *args: str) -> bytes:
        return subprocess.check_output(["git", "-C", str(self.root), *args], stderr=subprocess.PIPE)

    def paths(self, prefix: str) -> list[dict[str, str]]:
        rows = []
        for raw in self.git("ls-tree", "-r", "-z", self.revision, "--", prefix).split(b"\0"):
            if not raw:
                continue
            metadata, name = raw.split(b"\t", 1)
            mode, kind, blob = metadata.decode().split()
            if kind != "blob":
                raise ValueError("staging submodules require a separate explicit inventory adapter")
            rows.append({"path": name.decode("utf-8"), "mode": mode, "blob": blob})
        return rows

    def read(self, path: str) -> bytes:
        if PurePosixPath(path).is_absolute() or ".." in PurePosixPath(path).parts:
            raise ValueError("source paths must be repository-relative")
        data = self.git("cat-file", "blob", self.revision + ":" + path)
        self.inputs[path] = hashlib.sha256(data).hexdigest()
        return data

    def optional_json(self, path: str, default: Any) -> Any:
        try:
            return json.loads(self.read(path))
        except subprocess.CalledProcessError:
            return default

    def blobs(self, ids: list[str]) -> dict[str, bytes]:
        unique = sorted(set(ids))
        if not unique:
            return {}
        output = subprocess.run(["git", "-C", str(self.root), "cat-file", "--batch"],
                                input=("\n".join(unique) + "\n").encode(),
                                check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
        stream = io.BytesIO(output)
        result = {}
        for expected in unique:
            sha, kind, size = stream.readline().decode().split()
            if sha != expected or kind != "blob":
                raise ValueError("unexpected Git object in staging inventory")
            data = stream.read(int(size))
            if len(data) != int(size) or stream.read(1) != b"\n":
                raise ValueError("incomplete Git blob")
            result[sha] = data
        return result


def frontmatter(data: bytes) -> dict[str, Any]:
    text = data.decode("utf-8")
    if not text.startswith("---\n"):
        return {}
    value = yaml.safe_load(text.split("---", 2)[1])
    return value if isinstance(value, dict) else {}


def unit_id(path: str) -> str:
    parts = PurePosixPath(path).parts
    if len(parts) < 3 or parts[0] != ".staging" or parts[1] not in BUCKETS:
        raise ValueError("unclassified staging path: " + path)
    return parts[1] + "/" + parts[2]


def issue(number: int) -> str:
    return "https://github.com/egohygiene/aether/issues/" + str(number)


def build(root: Path, revision: str) -> dict[str, Any]:
    source = GitSource(root, revision)
    files = source.paths(".staging")
    blobs = source.blobs([row["blob"] for row in files])
    groups: dict[str, list[str]] = defaultdict(list)
    for row in files:
        row["unit"] = unit_id(row["path"])
        row["sha256"] = hashlib.sha256(blobs[row["blob"]]).hexdigest()
        row["bytes"] = len(blobs[row["blob"]])
        groups[row["unit"]].append(row["path"])

    old_inventory = source.optional_json(SKILL_INVENTORY, {"entries": []})
    skill_rows = {entry["staging_path"]: entry for entry in old_inventory["entries"]}
    agents = source.optional_json(AGENT_LEDGER, {"covered": {}, "move-out": {}})
    covered = {entry["staged-path"]: entry for entry in agents.get("covered", {}).values()}
    moving = {entry["staged-path"]: entry for entry in agents.get("move-out", {}).values()}
    dispositions = []
    for row in source.paths(DISPOSITIONS):
        if row["path"].endswith(".json"):
            record = json.loads(source.read(row["path"]))
            paths = record.get("staging_paths", [record.get("staging_path", "")])
            dispositions.append((row["path"], paths, record))

    units = []
    for identity, members in sorted(groups.items()):
        bucket, name = identity.split("/", 1)
        unit: dict[str, Any] = {
            "id": identity, "bucket": bucket, "members": members,
            "state": "retained", "disposition": "deferred-retention",
            "owner": "Aether staging curator; ownership review required",
            "owner_state": "needs-review", "source_records": [],
            "references": [issue(113)], "receipt_state": "unknown",
            "next_checkpoint": "STG-OWNER-REVIEW-" + bucket.upper(),
            "removal_authority": False,
        }
        matching = [(path, record) for path, paths, record in dispositions
                    if any(member == prefix or (prefix.endswith("/") and member.startswith(prefix))
                           for prefix in paths for member in members)]
        unit["source_records"] = [path for path, _ in matching]
        if matching:
            unit["declared_dispositions"] = sorted({record["disposition"] for _, record in matching})
            owners = sorted({record["owner"] for _, record in matching if record.get("owner")})
            if owners:
                unit["owner"] = "; ".join(owners)
                unit["owner_state"] = "recorded-routing; receipt-unverified"
            unit["disposition"] = "retained-recorded-disposition"
        if bucket == "skills":
            path = ".staging/skills/" + name + "/SKILL.md"
            prior = skill_rows.get(path)
            if prior:
                unit["source_records"].append(SKILL_INVENTORY + "#" + path)
                unit["classification"] = prior["classification"]
                if prior.get("external_catalog_id"):
                    unit["external_catalog_id"] = prior["external_catalog_id"]
                    unit["owner"] = "Aether external-source curator"
                    unit["owner_state"] = "curation-only; upstream-rights-not-renewed"
                    unit["references"].append(issue(112))
            unit["next_checkpoint"] = "STG-SKILL-RIGHTS-AND-DISPOSITION"
            if name == "repository-audit":
                unit["references"] += [issue(68), issue(86)]
        elif bucket == "agents":
            path = members[0]
            unit["source_records"].append(AGENT_LEDGER)
            unit["references"] += [issue(41), issue(64)]
            if path in covered:
                canonical = covered[path]["canonical-path"]
                current = source.read(canonical)
                staged = blobs[next(row["blob"] for row in files if row["path"] == path)]
                first, second = frontmatter(staged), frontmatter(current)
                metadata = second.get("metadata", {})
                unit["canonical_comparison"] = {
                    "path": canonical, "sha256": hashlib.sha256(current).hexdigest(),
                    "staged_tools": first.get("tools", []), "canonical_tools": second.get("tools", []),
                    "shared_skills": metadata.get("aether-skills", []),
                    "shared_specs": metadata.get("aether-specs", []),
                    "byte_identical": staged == current,
                    "scope": "Local Git source and explicit tool/composition delta; semantic completeness and human removal approval are not asserted.",
                }
                unit["owner"] = "Aether canonical agent maintainer"
                unit["owner_state"] = "recorded-canonical-source"
                unit["receipt_state"] = "local-source-only"
                unit["next_checkpoint"] = "STG-CANONICAL-AGENT-COMPLETENESS-REVIEW"
            elif path in moving:
                unit["disposition"] = "retained-transfer-pending"
                unit["next_checkpoint"] = "STG-DOMAIN-AGENT-OWNER-AND-RECEIPT"
                unit["references"] += [issue(51), issue(69)]
        elif bucket == "instructions":
            unit["references"].append(issue(40))
        elif bucket in {"scripts", "integrations"}:
            unit["references"] += [issue(67), issue(77)]
        elif bucket == "specs":
            unit["next_checkpoint"] = "STG-SPEC-DOMAIN-AND-PROVENANCE-REVIEW"
        unit["source_records"] = sorted(set(unit["source_records"]))
        unit["references"] = sorted(set(unit["references"]))
        units.append(unit)

    current = {row["path"] for row in files}
    historical = []
    for path, row in sorted(skill_rows.items()):
        if row.get("current_staging_state") == "removed":
            if path in current:
                raise ValueError("historical removal is currently retained: " + path)
            historical.append({"path": path, "state": "historical-absent", "classification": row["classification"],
                               "source_record": SKILL_INVENTORY + "#" + path, "removal_authority": False})
    staging_tree = source.git("rev-parse", source.revision + ":.staging").decode().strip()
    return {
        "schema_version": "aether.staging-residual-ledger/v1",
        "source": {"revision": source.revision, "staging_tree": staging_tree,
                   "hash_algorithm": "sha256-raw-git-blob", "generator": "catalog.staging_ledger/v1"},
        "source_inputs": [{"path": path, "sha256": digest} for path, digest in sorted(source.inputs.items())],
        "totals": {"files": len(files), "bytes": sum(row["bytes"] for row in files), "units": len(units),
                   "current_skill_roots": sum(row["path"].endswith("/SKILL.md") and len(PurePosixPath(row["path"]).parts) == 4
                                              and row["path"].startswith(".staging/skills/") for row in files),
                   "historical_removed_skill_roots": len(historical),
                   "by_bucket": dict(sorted(Counter(row["path"].split("/")[1] for row in files).items()))},
        "files": files, "units": units, "historical_removed_skills": historical,
        "authority": "Inventory and deferred jobs only; no execution, adoption, transfer, rights clearance, lifecycle promotion or removal approval.",
    }


def validate(data: dict[str, Any], root: Path, current_revision: str = "HEAD") -> list[str]:
    """Verify exact immutable reconstruction and reject current-source drift."""
    from jsonschema import Draft202012Validator
    schema = json.loads((ROOT / SCHEMA).read_text(encoding="utf-8"))
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(data)]
    if errors:
        return errors
    try:
        expected = build(root, data["source"]["revision"])
        if data != expected:
            errors.append("ledger differs from its immutable source, memberships, dispositions or evidence")
        current = GitSource(root, current_revision)
        tree = current.git("rev-parse", current.revision + ":.staging").decode().strip()
        if tree != data["source"]["staging_tree"]:
            errors.append("current tracked staging tree differs; reconcile ledger before intake/removal")
        for entry in data["source_inputs"]:
            if hashlib.sha256(current.read(entry["path"])).hexdigest() != entry["sha256"]:
                errors.append("current owner/disposition source differs: " + entry["path"])
    except (KeyError, ValueError, subprocess.CalledProcessError) as error:
        errors.append("immutable/current source unavailable or incompatible: " + type(error).__name__)
    return errors


def summary(data: dict[str, Any]) -> str:
    """Render the same frozen inventory without retiming or adding approval."""
    totals = data["totals"]
    lines = ["# Current retained-staging ledger", "",
             "Generated by `python -m catalog.staging_ledger report` from the "
             "[machine ledger](../catalog/reports/staging-residual-ledger.v1.json). "
             "Tracking: [#113](https://github.com/egohygiene/aether/issues/113).", "",
             "Represented source: `" + data["source"]["revision"] + "`; staging tree: `" + data["source"]["staging_tree"] + "`.", "",
             f"{totals['files']} tracked files ({totals['bytes']:,} raw Git-blob bytes) belong to "
             f"{totals['units']} finite semantic units. Every file has exactly one unit, mode, Git blob and SHA-256. "
             f"{totals['current_skill_roots']} current skill roots and {totals['historical_removed_skill_roots']} historical absent roots remain distinct.", "",
             "| Class | Tracked files | Retained units |", "| --- | ---: | ---: |"]
    counts = Counter(unit["bucket"] for unit in data["units"])
    lines += [f"| {bucket} | {count} | {counts[bucket]} |" for bucket, count in totals["by_bucket"].items()]
    lines += ["", "## Nine canonical-agent comparisons", "",
              "Canonical paths and raw hashes are verified against the represented Git source. "
              "The ledger records actual tool lists plus shared skill/spec references. Canonical front matter, "
              "repository-relative links and continuity composition differ from the staged provider files. "
              "These comparisons do not assert semantic completeness, a current host test or human removal approval.", "",
              "| Agent | Staged tools | Canonical tools | Receipt |", "| --- | --- | --- | --- |"]
    for unit in data["units"]:
        if "canonical_comparison" in unit:
            comparison = unit["canonical_comparison"]
            lines.append("| " + unit["id"].split("/", 1)[1] + " | " + ", ".join(comparison["staged_tools"]) +
                         " | " + ", ".join(comparison["canonical_tools"]) + " | local source only; completeness review deferred |")
    lines += ["", "## Recorded dispositions and bounded next jobs", "",
              "- Four domain agents retain their recorded move-out intent; destination owner confirmation and durable transfer receipts remain unknown. Review the owner/receipt checkpoint, composing existing #51/#69 rather than duplicating those capabilities.",
              "- Each hook/integration unit links existing typed disposition records and their original reasons. A record scoped to subpaths does not silently extend that decision to every member of a grouped integration. Rejected prototypes remain retained evidence; move-out routing is not a transfer receipt.",
              "- All current skill units link the prior inventory: 56 external catalog records retain restrictions and overdue-review follow-ups, while 130 unknown-provenance roots remain explicitly retained for rights/owner review. The retained repository-audit copy points to #68/#86; it is not a seventh historical removal.",
              "- Instructions route to existing #40; generic agents to #41/#64; host scripts/integrations to #67/#77. Specs, manifests and unresolved supporting material name a bounded ownership/provenance checkpoint in each unit. Deferred retention is valid and does not create one issue per file.",
              "- Every unit has an owner or explicit ownership-review role, a finite next-checkpoint identifier, source/reference links, receipt state and `removal_authority: false`.", "",
              "## Reproduce and reconcile", "", "```bash",
              "python -m catalog.staging_ledger check",
              "python -m catalog.staging_ledger generate --revision " + data["source"]["revision"] + " --ledger <new-path>",
              "python -m catalog.staging_ledger report", "```", "",
              "Generation reads Git objects only, including symlink blobs without following their targets. "
              "The same immutable revision yields identical identities and output. Check validates the closed schema, "
              "exact reconstruction, every file/unit/digest and current staging/owner-input drift. "
              "It creates no issues and executes no staged file.", "",
              "## Authority and historical evidence", "",
              "This ledger supplies inventory and deferred jobs. It cannot authorize execution, copying/adoption, "
              "rights clearance, lifecycle promotion, transfer or deletion. ADR-0005 and existing hook decisions "
              "retain their original dispositions. The [August status](staging-evacuation-status.md) and "
              "[October audit](../audits/aether-completeness-20261020T011246Z.md) remain dated evidence. "
              "#111 owns actual intake and base/head removal controls; a passing inventory check is not that gate."]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("generate", "check", "report"))
    parser.add_argument("--repository-root", type=Path, default=ROOT)
    parser.add_argument("--revision", default="HEAD")
    parser.add_argument("--ledger", type=Path, default=LEDGER)
    args = parser.parse_args()
    path = args.ledger if args.ledger.is_absolute() else args.repository_root / args.ledger
    try:
        if args.command == "generate":
            data = build(args.repository_root, args.revision)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print(json.dumps(data["totals"], sort_keys=True))
            return 0
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = validate(data, args.repository_root, args.revision)
        if args.command == "report" and not errors:
            print(summary(data), end="")
            return 0
        print(json.dumps({"status": "fail" if errors else "pass", "errors": errors}, sort_keys=True))
        return int(bool(errors))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print("Staging ledger input unavailable: " + type(error).__name__, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
