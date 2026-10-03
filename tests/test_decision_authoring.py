"""Check ADR authoring artifacts against pinned owners, without owning ADR rules."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest.mock import patch

from jsonschema import Draft202012Validator, FormatChecker
import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "library/organization/skills/architecture/create-decisions-document"
SELECTION = json.loads((SKILL / "references/policy-selection.json").read_text())
HYGIENE = os.environ.get("AETHER_ADR_HYGIENE_SOURCE")
RELAY = os.environ.get("AETHER_ADR_RELAY_SOURCE")
RUNTIME = os.environ.get("AETHER_ADR_RUNTIME")
RELAY_PYTHON = os.environ.get("AETHER_ADR_RELAY_PYTHON", sys.executable)


def module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


projections = module("adr_projections", ROOT / "library/organization/projections/build-projections.py")


def rendered_record(identifier="ADR-012") -> str:
    return (SKILL / "templates/ADR.template.md").read_text().replace(
        "ADR-000", identifier
    ).replace("YYYY-MM-DD", "2026-10-03").replace(
        "egohygiene/REPOSITORY", "egohygiene/example"
    ).replace("Replace with a concise proposed choice", "Keep a durable format")


def metadata(text: str) -> dict:
    return yaml.safe_load(text.split("---", 2)[1])


def with_metadata(text: str, value: dict) -> str:
    return "---\n" + yaml.safe_dump(value, sort_keys=False) + "---" + text.split("---", 2)[2]


class DecisionProjectionTests(unittest.TestCase):
    def test_module_rejects_a_stale_authoring_policy(self):
        text = projections.DECISION_IMPACT_PATH.read_text()
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "instruction.md"
            path.write_text(text.replace(SELECTION["policy"]["revision"], "a" * 40))
            with patch.object(projections, "DECISION_IMPACT_PATH", path):
                with self.assertRaisesRegex(ValueError, "policy differs"):
                    projections._load_decision_impact()

    def test_upgrade_repeat_and_removal_preserve_consumer_instructions(self):
        before = "# Local guidance\n\nNever publish without our release approval.\n"
        after = "\n## Local tests\n\nRun our own test command.\n"
        old_block = "<!-- BEGIN AETHER DECISION-IMPACT -->\nOld policy.\n<!-- END AETHER DECISION-IMPACT -->"
        upgraded = projections._apply_decision_impact(before + old_block + after)
        self.assertTrue(upgraded.startswith(before))
        self.assertTrue(upgraded.endswith(after))
        self.assertEqual(projections._apply_decision_impact(upgraded), upgraded)
        removed = projections._remove_managed_module(
            upgraded, start_marker=projections.DECISION_IMPACT_START,
            end_marker=projections.DECISION_IMPACT_END, label="decision-impact",
        )
        self.assertEqual(removed, before + after)
        self.assertIn("Before issue completion or PR handoff", upgraded)
        self.assertIn("Read-only roles remain read-only", upgraded)

    def test_portable_package_preserves_the_selection_and_templates(self):
        portable = ROOT / "dist/skills/create-decisions-document"
        for relative in ["references/policy-selection.json", "templates/ADR.template.md", "templates/policy-reference.template.json"]:
            self.assertEqual((SKILL / relative).read_bytes(), (portable / relative).read_bytes())


@unittest.skipUnless(HYGIENE, "set AETHER_ADR_HYGIENE_SOURCE to the selected owner checkout")
class DecisionOwnerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source = Path(HYGIENE)
        assert subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip() == SELECTION["policy"]["revision"]
        for path, digest in SELECTION["source_digests"].items():
            assert hashlib.sha256((source / path).read_bytes()).hexdigest() == digest, path
        cls.owner = module("selected_hygiene_decisions", source / "tools/decisions.py")
        cls.schemas = source / "schemas"

    def test_proposed_template_matches_owner_metadata_and_sections(self):
        text = rendered_record()
        record = metadata(text)
        schema = json.loads((self.schemas / "architecture-decision.v1.schema.json").read_text())
        Draft202012Validator(schema, format_checker=FormatChecker()).validate(record)
        self.assertEqual(self.owner.validate_decision(record), [])
        self.assertEqual(record["status"], "proposed")
        self.assertIsNone(record["approval"])
        self.assertEqual(re.findall(r"^## (.+)$", text, re.M)[:7], [
            "Context", "Decision", "Alternatives considered and rejected",
            "Consequences and tradeoffs", "Implementation and evidence links",
            "Replacement or exit strategy", "Follow-up work",
        ])

    def test_policy_reference_uses_ratified_source_without_copying_policy(self):
        reference = json.loads((SKILL / "templates/policy-reference.template.json").read_text().replace("egohygiene/REPOSITORY", "egohygiene/example"))
        schema = json.loads((self.schemas / "architecture-decision-policy-reference.v1.schema.json").read_text())
        Draft202012Validator(schema).validate(reference)
        self.assertEqual(self.owner.validate_policy_reference(reference), [])
        self.assertEqual(reference["policy"]["source"]["revision"], SELECTION["policy"]["revision"])

    def test_implementation_reference_cannot_supply_missing_approval(self):
        record = metadata(rendered_record())
        record.update(status="accepted", implementation_status="implemented", pull_request="https://github.com/egohygiene/example/pull/2")
        self.assertTrue(any("APPROVAL" in error for error in self.owner.validate_decision(record)))


@unittest.skipUnless(RELAY and RUNTIME, "set AETHER_ADR_RELAY_SOURCE and AETHER_ADR_RUNTIME for native consumer replay")
class DecisionNativeConsumerTests(unittest.TestCase):
    """Use Relay's public CLI; semantic validation stays in the pinned EgoLint."""

    @classmethod
    def setUpClass(cls):
        cls.relay = Path(RELAY)
        assert subprocess.check_output(["git", "-C", str(cls.relay), "rev-parse", "HEAD"], text=True).strip() == SELECTION["validation"]["relay_revision"]
        cls.profile_bytes = (cls.relay / "catalog/repository-architecture-validation.json").read_bytes()
        cls.profile = json.loads(cls.profile_bytes)
        validator = next(s for s in cls.profile["sources"] if s["repository"] == "egohygiene/egolint")
        assert validator["revision"] == SELECTION["validation"]["egolint_revision"]
        cls.catalog = tomllib.loads((Path(RUNTIME) / "egolint/.config/rules/repository-intelligence.v1.toml").read_text())

    def run_consumer(self, records, *, legacy=False, old_policy=False):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "consumer"
            root.mkdir()
            subprocess.run(["git", "init", "--quiet", "--template=", str(root)], check=True)
            directory = root / "docs/decisions"
            directory.mkdir(parents=True)
            index = "# Architecture decisions\n\n| ID | Title | Status | Date | Record |\n| --- | --- | --- | --- | --- |\n"
            for text in records:
                info = metadata(text)
                name = info["id"] + "-format.md"
                (directory / name).write_text(text)
                index += f"| {info['id']} | {info['title']} | {info['status']} | {info['date']} | [{info['id']}]({name}) |\n"
            (directory / "README.md").write_text(index)
            reference = (SKILL / "templates/policy-reference.template.json").read_text().replace("egohygiene/REPOSITORY", "egohygiene/example")
            if old_policy:
                reference = reference.replace(SELECTION["policy"]["revision"], SELECTION["materialization"]["emitted_policy_revision"])
            (directory / "policy-reference.json").write_text(reference)
            config = 'schema-version = 1\nid = "egolint.repository-intelligence-validation/v1"\nrepository = "egohygiene/example"\n[profile]\nid = "authoring-fixture"\nenforcement = "advisory"\nenabled-rules = ' + json.dumps([rule["id"] for rule in self.catalog["rules"]]) + "\n"
            for pin in self.catalog["upstream-contracts"]:
                config += "\n[[contracts]]\n" + "".join(f"{k} = {json.dumps(v)}\n" for k, v in pin.items())
            config += '\n[adrs]\nstate = "present"\npolicy-reference = "docs/decisions/policy-reference.json"\ndecision-directory = "docs/decisions"\nindex = "docs/decisions/README.md"\n[roadmap]\nstate = "not-applicable"\npath = "ROADMAP.md"\n[commit-history]\nstate = "not-applicable"\nmaximum-commits = 256\n'
            (root / "policy.toml").write_text(config)
            (root / ".gitignore").write_text(".reports/\n")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(["git", "-C", str(root), "-c", "user.name=Synthetic fixture", "-c", "user.email=fixture@example.invalid", "commit", "--quiet", "-m", "test: capture authoring fixture"], check=True)
            revision = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            before = {str(p.relative_to(root)): p.read_bytes() for p in directory.iterdir()}
            request = {
                "schema_version": "relay.repository-architecture-validation-request/v1",
                "profile": {"version": self.profile["version"], "sha256": hashlib.sha256(self.profile_bytes).hexdigest()},
                "repository": {"id": "egohygiene/example", "visibility": "public", "root": ".", "represented_revision": revision},
                "mode": "advisory",
                "adoption": {"repository-contracts": "not-applicable", "architecture-records": "legacy" if legacy else "present", "diagram-sources": "not-applicable"},
                "inputs": {"repository_contracts": [], "repository_intelligence_policy": "policy.toml", "diagram_roots": []},
                "bounds": {"maximum_findings": 256, "maximum_scanned_files": 1000, "maximum_scanned_bytes": 4194304},
                "output": {"format": "json", "path": ".reports/architecture-validation/result.json"},
            }
            path = Path(temp) / "request.json"
            path.write_text(json.dumps(request))
            completed = subprocess.run([RELAY_PYTHON, "-E", "-s", str(self.relay / "scripts/run_repository_architecture_validation.py"), "run", "--repository-root", str(root), "--request", str(path), "--runtime", RUNTIME], capture_output=True, text=True)
            result = json.loads((root / request["output"]["path"]).read_text())
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr + json.dumps(result, indent=2))
            self.assertEqual(before, {str(p.relative_to(root)): p.read_bytes() for p in directory.iterdir()})
            return result

    def test_new_proposal_validates_without_human_acceptance(self):
        result = self.run_consumer([rendered_record()])
        self.assertEqual(result["semantic_status"], "conformant")

    def test_legacy_history_stays_partial(self):
        result = self.run_consumer([rendered_record()], legacy=True)
        self.assertEqual(result["semantic_status"], "legacy")
        self.assertEqual(result["coverage"]["architecture-records"], "partial")

    def test_old_holon_reference_is_not_compatible_with_ratified_validator(self):
        result = self.run_consumer([rendered_record()], old_policy=True)
        self.assertEqual(result["semantic_status"], "nonconformant")
        self.assertIn("EGO-INTEL-CONTRACT-001", [f["id"] for f in result["findings"]])

    def test_proposed_supersession_preserves_human_disposed_predecessor(self):
        old = rendered_record("ADR-004")
        info = metadata(old)
        info.update(status="accepted", approval={"date": "2026-09-01", "by": "Synthetic fixture maintainer", "evidence": "https://github.com/egohygiene/example/issues/4"})
        old = with_metadata(old, info)
        new = rendered_record("ADR-013")
        info = metadata(new)
        info["supersedes"] = ["ADR-004"]
        result = self.run_consumer([old, with_metadata(new, info)])
        self.assertEqual(result["semantic_status"], "conformant")

    def test_implemented_without_approval_fails(self):
        text = rendered_record()
        info = metadata(text)
        info.update(status="accepted", implementation_status="implemented", pull_request="https://github.com/egohygiene/example/pull/2")
        result = self.run_consumer([with_metadata(text, info)])
        self.assertEqual(result["semantic_status"], "nonconformant")
        self.assertIn("EGO-INTEL-ADR-LIFECYCLE-001", [f["id"] for f in result["findings"]])
