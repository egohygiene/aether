from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from aether_validator import AetherValidator


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class ValidatorFixture:
    def __init__(self, root: Path):
        self.root = root

    @classmethod
    def create(cls) -> "ValidatorFixture":
        tmp = Path(tempfile.mkdtemp(prefix="aether-validator-test-"))
        fixture = cls(tmp)
        fixture._seed()
        return fixture

    def validator(self) -> AetherValidator:
        return AetherValidator(self.root)

    def _seed(self) -> None:
        write(
            self.root / "library/organization/specs/domain/example.spec.md",
            """---
schema: aether.specification/v1
id: example-spec
title: Example Specification
kind: specification
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-08-01
updated: 2026-08-01
domain: architecture
tags:
  - architecture
depends_on: []
related:
  - example-skill
supersedes: []
---

A deterministic example specification body.
""",
        )

        write(
            self.root / "library/organization/skills/domain/example-skill/SKILL.md",
            """---
name: example-skill
description: Demonstrates a valid skill fixture. Use when validating deterministic Aether rules.
license: MIT
metadata:
  aether-version: \"1.0.0\"
  aether-status: \"draft\"
  aether-spec-id: \"example-spec\"
  aether-scope: \"organization\"
  aether-domain: \"architecture\"
  aether-owners: \"egohygiene\"
  aether-created: \"2026-08-01\"
  aether-updated: \"2026-08-01\"
---

# Example Skill

See [Reference](./references/reference.md).
""",
        )

        write(self.root / "library/organization/skills/domain/example-skill/references/reference.md", "ok\n")
        write(self.root / "library/organization/skills/domain/example-skill/templates/template.md", "template\n")
        write(self.root / "library/organization/skills/domain/example-skill/evals/evals.json", "{}\n")

        write(
            self.root / ".staging/manifests/skills-lock.json",
            json.dumps(
                {
                    "version": 1,
                    "skills": {
                        "example-skill": {
                            "source": "egohygiene/aether",
                            "sourceType": "github",
                            "skillPath": "skills/example-skill/SKILL.md",
                            "computedHash": "a" * 64,
                        }
                    },
                },
                indent=2,
            )
            + "\n",
        )

        write(self.root / "catalog/schemas/aether.artifact-catalog.v1.schema.json", '{"type":"object"}\n')
        write(self.root / "example.json", '{"ok": true}\n')
        write(self.root / "script.sh", "#!/usr/bin/env bash\necho ok\n")

        # Eval v2 schema — required for validate_evals() and run_evals()
        write(
            self.root / "catalog/schemas/aether.skill-evaluations.v2.schema.json",
            json.dumps(
                {
                    "$id": "aether.skill-evaluations/v2",
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                    "required": ["schema", "skill", "version", "cases"],
                    "additionalProperties": False,
                    "properties": {
                        "schema": {"type": "string", "const": "aether.skill-evaluations/v2"},
                        "skill": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
                        "version": {"type": "string", "pattern": "^\\d+\\.\\d+\\.\\d+$"},
                        "cases": {
                            "type": "array",
                            "minItems": 1,
                            "items": {
                                "type": "object",
                                "required": ["id", "description", "category", "trigger", "expected"],
                                "additionalProperties": False,
                                "properties": {
                                    "id": {"type": "string", "pattern": "^[a-z][a-z0-9-]*$"},
                                    "description": {"type": "string", "minLength": 1},
                                    "category": {"type": "string", "enum": ["positive", "negative", "insufficient-evidence", "boundary", "failure"]},
                                    "trigger": {"type": "string", "enum": ["should-trigger", "should-not-trigger", "not-applicable"]},
                                    "tags": {"type": "array", "items": {"type": "string"}},
                                    "expected": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                                    "prohibited": {"type": "array", "items": {"type": "string"}},
                                    "assertions": {
                                        "type": "array",
                                        "items": {
                                            "type": "object",
                                            "required": ["type", "value"],
                                            "additionalProperties": False,
                                            "properties": {
                                                "type": {"type": "string", "enum": ["contains", "not-contains", "matches-pattern", "not-matches-pattern", "file-exists", "file-not-exists"]},
                                                "value": {"type": "string", "minLength": 1},
                                            },
                                        },
                                    },
                                    "fixture": {"type": "string", "minLength": 1},
                                },
                            },
                        },
                    },
                },
                indent=2,
            ) + "\n",
        )

        validator = self.validator()
        validator.write_catalog()


class TestAetherValidatorRegressions(unittest.TestCase):
    def test_missing_skill_name(self):
        fx = ValidatorFixture.create()
        skill = fx.root / "library/organization/skills/domain/example-skill/SKILL.md"
        skill.write_text(skill.read_text().replace("name: example-skill\n", ""), encoding="utf-8")
        diags = fx.validator().validate_skills()
        self.assertTrue(any(d.rule_id == "AETHER_SKILL_001" for d in diags))

    def test_skill_name_directory_mismatch(self):
        fx = ValidatorFixture.create()
        skill = fx.root / "library/organization/skills/domain/example-skill/SKILL.md"
        skill.write_text(skill.read_text().replace("name: example-skill", "name: mismatch"), encoding="utf-8")
        diags = fx.validator().validate_skills()
        self.assertTrue(any(d.rule_id == "AETHER_SKILL_002" for d in diags))

    def test_invalid_description_type(self):
        fx = ValidatorFixture.create()
        skill = fx.root / "library/organization/skills/domain/example-skill/SKILL.md"
        skill.write_text(skill.read_text().replace("description: Demonstrates a valid skill fixture. Use when validating deterministic Aether rules.", "description:\n  - wrong\n"), encoding="utf-8")
        diags = fx.validator().validate_skills()
        self.assertTrue(any(d.rule_id == "AETHER_SKILL_004" for d in diags))

    def test_unsupported_top_level_skill_key(self):
        fx = ValidatorFixture.create()
        skill = fx.root / "library/organization/skills/domain/example-skill/SKILL.md"
        skill.write_text(skill.read_text().replace("license: MIT\n", "license: MIT\nid: forbidden\n"), encoding="utf-8")
        diags = fx.validator().validate_skills()
        self.assertTrue(any(d.rule_id == "AETHER_SKILL_006" for d in diags))

    def test_duplicate_spec_id(self):
        fx = ValidatorFixture.create()
        write(
            fx.root / "library/organization/specs/domain/duplicate.spec.md",
            (fx.root / "library/organization/specs/domain/example.spec.md").read_text(),
        )
        diags, _, _ = fx.validator().validate_specs()
        self.assertTrue(any(d.rule_id == "AETHER_SPEC_006" for d in diags))

    def test_missing_relationship_target(self):
        fx = ValidatorFixture.create()
        spec = fx.root / "library/organization/specs/domain/example.spec.md"
        spec.write_text(spec.read_text().replace("depends_on: []", "depends_on:\n  - missing-spec"), encoding="utf-8")
        _spec_diags, specs, paths = fx.validator().validate_specs()
        diags = fx.validator().validate_graph(specs, paths)
        self.assertTrue(any(d.rule_id == "AETHER_GRAPH_001" for d in diags))

    def test_dependency_cycle(self):
        fx = ValidatorFixture.create()
        write(
            fx.root / "library/organization/specs/domain/second.spec.md",
            """---
schema: aether.specification/v1
id: second-spec
title: Second
kind: specification
version: 1.0.0
status: draft
owners: [egohygiene]
created: 2026-08-01
updated: 2026-08-01
domain: architecture
tags: [architecture]
depends_on:
  - example-spec
related: []
supersedes: []
---

Second.
""",
        )
        first = fx.root / "library/organization/specs/domain/example.spec.md"
        first.write_text(first.read_text().replace("depends_on: []", "depends_on:\n  - second-spec"), encoding="utf-8")
        _spec_diags, specs, paths = fx.validator().validate_specs()
        diags = fx.validator().validate_graph(specs, paths)
        self.assertTrue(any(d.rule_id == "AETHER_GRAPH_003" for d in diags))

    def test_missing_template_or_eval(self):
        fx = ValidatorFixture.create()
        (fx.root / "library/organization/skills/domain/example-skill/evals/evals.json").unlink()
        diags = fx.validator().validate_skills()
        self.assertTrue(any(d.rule_id == "AETHER_SKILL_009" for d in diags))

    def test_broken_local_link_and_path_traversal(self):
        fx = ValidatorFixture.create()
        ref = fx.root / "library/organization/skills/domain/example-skill/references/reference.md"
        ref.write_text("[escape](../../outside.md)\n", encoding="utf-8")
        diags = fx.validator().validate_markdown_links()
        self.assertTrue(any(d.rule_id == "AETHER_LINK_003" for d in diags))

    def test_malformed_json_and_yaml(self):
        fx = ValidatorFixture.create()
        write(fx.root / "bad.json", "{bad json}\n")
        spec = fx.root / "library/organization/specs/domain/example.spec.md"
        spec.write_text(spec.read_text().replace("schema: aether.specification/v1", "schema: ["), encoding="utf-8")
        json_diags = fx.validator().validate_json_files()
        spec_diags, _, _ = fx.validator().validate_specs()
        self.assertTrue(any(d.rule_id == "AETHER_JSON_001" for d in json_diags))
        self.assertTrue(any(d.rule_id == "AETHER_FRONTMATTER_002" for d in spec_diags))

    def test_catalog_drift(self):
        fx = ValidatorFixture.create()
        catalog = fx.root / "catalog/first-party/catalog.v1.json"
        data = json.loads(catalog.read_text())
        data["artifacts"][0]["source_path"] = "library/organization/specs/domain/not-real.spec.md"
        catalog.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        diags = fx.validator().validate_catalog(check_only=True)
        self.assertTrue(any(d.rule_id == "AETHER_CATALOG_002" for d in diags))

    def test_unknown_external_provenance(self):
        fx = ValidatorFixture.create()
        lock = fx.root / ".staging/manifests/skills-lock.json"
        data = json.loads(lock.read_text())
        data["skills"]["example-skill"]["sourceType"] = "gitlab"
        lock.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        diags = fx.validator().validate_provenance()
        self.assertTrue(any(d.rule_id == "AETHER_PROVENANCE_005" for d in diags))

    def test_digest_mismatch(self):
        fx = ValidatorFixture.create()
        catalog = fx.root / "catalog/first-party/catalog.v1.json"
        data = json.loads(catalog.read_text())
        data["artifacts"][0]["source_digest"]["value"] = "0" * 64
        catalog.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
        diags = fx.validator().validate_catalog(check_only=True)
        self.assertTrue(any(d.rule_id == "AETHER_CATALOG_002" for d in diags))

    def test_unclassified_staging_material(self):
        fx = ValidatorFixture.create()
        (fx.root / ".staging" / "unknown").mkdir(parents=True)
        diags = fx.validator().validate_staging(strict=False)
        self.assertTrue(any(d.rule_id == "AETHER_STAGING_001" for d in diags))


_VALID_EVALS_V2 = {
    "schema": "aether.skill-evaluations/v2",
    "skill": "example-skill",
    "version": "1.0.0",
    "cases": [
        {
            "id": "example-positive",
            "description": "Canonical positive use case.",
            "category": "positive",
            "trigger": "should-trigger",
            "expected": ["Produces the correct output"],
        },
        {
            "id": "example-negative",
            "description": "Skill should not trigger for this request.",
            "category": "negative",
            "trigger": "should-not-trigger",
            "expected": ["Declines gracefully"],
        },
        {
            "id": "example-insufficient-evidence",
            "description": "Required evidence is missing.",
            "category": "insufficient-evidence",
            "trigger": "should-trigger",
            "expected": ["Does not fabricate information"],
        },
        {
            "id": "example-boundary",
            "description": "Boundary or pressure test.",
            "category": "boundary",
            "trigger": "should-trigger",
            "expected": ["Handles edge case safely"],
        },
    ],
}


class TestEvalHarness(unittest.TestCase):
    """Tests for the Layer 1 deterministic eval harness."""

    def _fx_with_evals(self, evals_data: dict) -> "ValidatorFixture":
        fx = ValidatorFixture.create()
        path = fx.root / "library/organization/skills/domain/example-skill/evals/evals.json"
        path.write_text(json.dumps(evals_data, indent=2) + "\n", encoding="utf-8")
        return fx

    # ------------------------------------------------------------------
    # validate_evals — structural checks
    # ------------------------------------------------------------------

    def test_valid_v2_evals_produce_no_errors(self):
        fx = self._fx_with_evals(_VALID_EVALS_V2)
        diags = fx.validator().validate_evals()
        errors = [d for d in diags if d.severity == "error"]
        self.assertEqual(errors, [], msg=[d.message for d in errors])

    def test_v1_schema_triggers_deprecation_warning(self):
        fx = self._fx_with_evals({
            "schema": "aether.skill-evaluations/v1",
            "skill": "example-skill",
            "version": "1.0.0",
            "cases": [{"id": "x", "description": "y", "expected": ["z"]}],
        })
        diags = fx.validator().validate_evals()
        self.assertTrue(any(d.rule_id == "AETHER_EVAL_006" for d in diags))
        self.assertFalse(any(d.severity == "error" for d in diags))

    def test_unknown_schema_triggers_error(self):
        fx = self._fx_with_evals({
            "schema": "aether.unknown/v99",
            "skill": "example-skill",
            "version": "1.0.0",
            "cases": [],
        })
        diags = fx.validator().validate_evals()
        self.assertTrue(any(d.rule_id == "AETHER_EVAL_007" for d in diags))

    def test_schema_violation_triggers_eval_001(self):
        bad = dict(_VALID_EVALS_V2)
        # Remove required "category" from first case
        bad["cases"] = [
            {
                "id": "x",
                "description": "y",
                "trigger": "should-trigger",
                "expected": ["z"],
                # category missing intentionally
            }
        ]
        fx = self._fx_with_evals(bad)
        diags = fx.validator().validate_evals()
        self.assertTrue(any(d.rule_id == "AETHER_EVAL_001" for d in diags))

    def test_duplicate_case_id_triggers_eval_002(self):
        bad = dict(_VALID_EVALS_V2)
        dup_case = dict(_VALID_EVALS_V2["cases"][0])
        bad["cases"] = list(_VALID_EVALS_V2["cases"]) + [dup_case]
        fx = self._fx_with_evals(bad)
        diags = fx.validator().validate_evals()
        self.assertTrue(any(d.rule_id == "AETHER_EVAL_002" for d in diags))

    def test_missing_required_categories_triggers_eval_003(self):
        # Only positive case — missing negative, insufficient-evidence, boundary
        bad = {
            "schema": "aether.skill-evaluations/v2",
            "skill": "example-skill",
            "version": "1.0.0",
            "cases": [
                {
                    "id": "example-positive",
                    "description": "Only case",
                    "category": "positive",
                    "trigger": "should-trigger",
                    "expected": ["ok"],
                }
            ],
        }
        fx = self._fx_with_evals(bad)
        diags = fx.validator().validate_evals()
        eval_003 = [d for d in diags if d.rule_id == "AETHER_EVAL_003"]
        self.assertTrue(len(eval_003) > 0)
        missing = eval_003[0].context.get("missing", [])
        self.assertIn("negative", missing)
        self.assertIn("boundary", missing)

    def test_missing_fixture_file_triggers_eval_004(self):
        data = dict(_VALID_EVALS_V2)
        data["cases"] = [
            {
                "id": "example-positive",
                "description": "Positive with fixture.",
                "category": "positive",
                "trigger": "should-trigger",
                "expected": ["ok"],
                "fixture": "fixtures/nonexistent.txt",
            },
            *_VALID_EVALS_V2["cases"][1:],
        ]
        fx = self._fx_with_evals(data)
        diags = fx.validator().validate_evals()
        self.assertTrue(any(d.rule_id == "AETHER_EVAL_004" for d in diags))

    def test_existing_fixture_file_does_not_trigger_eval_004(self):
        fx = ValidatorFixture.create()
        fixture_path = (
            fx.root / "library/organization/skills/domain/example-skill/evals/fixtures/input.txt"
        )
        fixture_path.parent.mkdir(parents=True, exist_ok=True)
        fixture_path.write_text("test input\n", encoding="utf-8")

        data = {
            "schema": "aether.skill-evaluations/v2",
            "skill": "example-skill",
            "version": "1.0.0",
            "cases": [
                {
                    "id": "example-positive",
                    "description": "Positive with existing fixture.",
                    "category": "positive",
                    "trigger": "should-trigger",
                    "expected": ["ok"],
                    "fixture": "fixtures/input.txt",
                },
                *_VALID_EVALS_V2["cases"][1:],
            ],
        }
        (fx.root / "library/organization/skills/domain/example-skill/evals/evals.json").write_text(
            json.dumps(data, indent=2) + "\n", encoding="utf-8"
        )
        diags = fx.validator().validate_evals()
        self.assertFalse(any(d.rule_id == "AETHER_EVAL_004" for d in diags))

    def test_empty_golden_triggers_eval_005_warning(self):
        fx = self._fx_with_evals(_VALID_EVALS_V2)
        golden_dir = fx.root / "library/organization/skills/domain/example-skill/evals/goldens"
        golden_dir.mkdir(parents=True, exist_ok=True)
        (golden_dir / "example-positive.golden.txt").write_text("", encoding="utf-8")
        diags = fx.validator().validate_evals()
        self.assertTrue(any(d.rule_id == "AETHER_EVAL_005" for d in diags))

    # ------------------------------------------------------------------
    # run_evals — result structure
    # ------------------------------------------------------------------

    def test_run_evals_returns_pass_for_valid_evals(self):
        fx = self._fx_with_evals(_VALID_EVALS_V2)
        results = fx.validator().run_evals()
        self.assertEqual(results["status"], "pass")
        self.assertEqual(results["schema"], "aether.eval-run-result/v1")
        self.assertIn("run_id", results)
        self.assertIn("timestamp", results)
        self.assertEqual(results["total_failed"], 0)
        self.assertGreater(results["total_cases"], 0)

    def test_run_evals_skill_filter(self):
        fx = self._fx_with_evals(_VALID_EVALS_V2)
        results = fx.validator().run_evals(skill_filter="example-skill")
        self.assertEqual(results["skills_evaluated"], 1)
        self.assertEqual(results["results"][0]["skill"], "example-skill")

    def test_run_evals_fails_when_fixture_missing(self):
        data = dict(_VALID_EVALS_V2)
        data["cases"] = [
            {
                "id": "example-positive",
                "description": "Positive with missing fixture.",
                "category": "positive",
                "trigger": "should-trigger",
                "expected": ["ok"],
                "fixture": "fixtures/does-not-exist.txt",
            },
            *_VALID_EVALS_V2["cases"][1:],
        ]
        fx = self._fx_with_evals(data)
        results = fx.validator().run_evals(skill_filter="example-skill")
        self.assertEqual(results["status"], "fail")
        self.assertGreater(results["total_failed"], 0)

    def test_run_evals_applies_deterministic_assertion_against_golden(self):
        fx = self._fx_with_evals({
            "schema": "aether.skill-evaluations/v2",
            "skill": "example-skill",
            "version": "1.0.0",
            "cases": [
                {
                    "id": "example-positive",
                    "description": "Positive with assertion.",
                    "category": "positive",
                    "trigger": "should-trigger",
                    "expected": ["ok"],
                    "assertions": [{"type": "contains", "value": "PASS"}],
                },
                *_VALID_EVALS_V2["cases"][1:],
            ],
        })
        # Create golden with the expected content
        golden_dir = (
            fx.root / "library/organization/skills/domain/example-skill/evals/goldens"
        )
        golden_dir.mkdir(parents=True, exist_ok=True)
        (golden_dir / "example-positive.golden.txt").write_text("PASS\n", encoding="utf-8")

        results = fx.validator().run_evals(skill_filter="example-skill")
        case_result = results["results"][0]["cases"][0]
        self.assertEqual(case_result["status"], "pass")

    def test_run_evals_fails_when_assertion_not_met(self):
        fx = self._fx_with_evals({
            "schema": "aether.skill-evaluations/v2",
            "skill": "example-skill",
            "version": "1.0.0",
            "cases": [
                {
                    "id": "example-positive",
                    "description": "Positive with failing assertion.",
                    "category": "positive",
                    "trigger": "should-trigger",
                    "expected": ["ok"],
                    "assertions": [{"type": "contains", "value": "EXPECTED_TEXT"}],
                },
                *_VALID_EVALS_V2["cases"][1:],
            ],
        })
        golden_dir = (
            fx.root / "library/organization/skills/domain/example-skill/evals/goldens"
        )
        golden_dir.mkdir(parents=True, exist_ok=True)
        (golden_dir / "example-positive.golden.txt").write_text("OTHER_TEXT\n", encoding="utf-8")

        results = fx.validator().run_evals(skill_filter="example-skill")
        case_result = results["results"][0]["cases"][0]
        self.assertEqual(case_result["status"], "fail")

    # ------------------------------------------------------------------
    # CLI integration
    # ------------------------------------------------------------------

    def test_validate_evals_scope_integration(self):
        fx = self._fx_with_evals(_VALID_EVALS_V2)
        diags = fx.validator().run_validation(scopes={"evals"})
        errors = [d for d in diags if d.severity == "error"]
        self.assertEqual(errors, [])

    def test_validate_all_scopes_includes_evals(self):
        """run_validation with no explicit scope runs evals too."""
        fx = self._fx_with_evals(_VALID_EVALS_V2)
        # All-scope includes evals; valid evals should not add errors
        all_scopes = {"skills", "specifications", "graph", "catalog", "distribution", "provenance", "staging", "json", "shell", "links", "evals"}
        diags = fx.validator().run_validation(scopes=all_scopes)
        eval_errors = [d for d in diags if d.rule_id.startswith("AETHER_EVAL_") and d.severity == "error"]
        self.assertEqual(eval_errors, [])


class TestAgentValidator(unittest.TestCase):
    """Deterministic tests for library/organization/agents/validate-agents.py."""

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _run_validator(self, agents_dir: Path) -> tuple[int, str]:
        """Execute validate-agents.py against *agents_dir* and return (returncode, output)."""
        import subprocess

        script = (
            Path(__file__).resolve().parents[1]
            / "library"
            / "organization"
            / "agents"
            / "validate-agents.py"
        )
        result = subprocess.run(
            [__import__("sys").executable, str(script)],
            capture_output=True,
            text=True,
            env={**__import__("os").environ, "PYTHONPATH": ""},
        )
        return result.returncode, result.stdout + result.stderr

    # ------------------------------------------------------------------
    # Canonical library smoke test
    # ------------------------------------------------------------------

    def test_canonical_agents_all_valid(self) -> None:
        """All nine canonical agent source files must pass validation."""
        agents_dir = (
            Path(__file__).resolve().parents[1]
            / "library"
            / "organization"
            / "agents"
        )
        rc, output = self._run_validator(agents_dir)
        self.assertEqual(rc, 0, msg=f"validate-agents.py exited non-zero:\n{output}")
        self.assertIn("9 agent(s) validated successfully", output)

    # ------------------------------------------------------------------
    # Unit tests for projection builder
    # ------------------------------------------------------------------

    def test_projection_check_passes_for_current_dist(self) -> None:
        """--check must report no drift for the committed projections."""
        import subprocess

        script = (
            Path(__file__).resolve().parents[1]
            / "library"
            / "organization"
            / "agents"
            / "build-projections.py"
        )
        result = subprocess.run(
            [__import__("sys").executable, str(script), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"build-projections.py --check reported drift:\n{result.stdout}{result.stderr}",
        )

    # ------------------------------------------------------------------
    # Schema unit tests (inline, no subprocess)
    # ------------------------------------------------------------------

    def _write_agent(self, base: Path, agent_id: str, fm_override: dict | None = None, body: str | None = None) -> Path:
        fm = {
            "aether-id": agent_id,
            "name": "Test Agent",
            "description": "A deterministic test agent. Use during validation tests.",
            "tools": ["read", "search"],
            "metadata": {
                "aether-version": "1.0.0",
                "aether-status": "draft",
                "aether-scope": "organization",
                "aether-domain": "quality",
                "aether-owners": "egohygiene",
                "aether-created": "2026-08-08",
                "aether-updated": "2026-08-08",
                "aether-skills": [],
                "aether-specs": [],
            },
        }
        if fm_override:
            fm.update(fm_override)

        if body is None:
            body = (
                "\n## Mission\n\nTest.\n"
                "\n## Operating contract\n\nTest.\n"
                "\n## Workflow\n\n1. Test.\n"
                "\n## Boundaries\n\n- Test.\n"
                "\n## Completion\n\nTest.\n"
            )

        import yaml as _yaml

        agent_dir = base / agent_id
        agent_dir.mkdir(parents=True, exist_ok=True)
        agent_file = agent_dir / "AGENT.md"
        agent_file.write_text(f"---\n{_yaml.dump(fm)}---\n{body}", encoding="utf-8")
        return agent_file

    def _validate_inline(self, agents_dir: Path) -> tuple[int, str]:
        import subprocess
        import sys as _sys

        # Re-run validate-agents.py but override the BASE so it scans our temp dir.
        script = (
            Path(__file__).resolve().parents[1]
            / "library"
            / "organization"
            / "agents"
            / "validate-agents.py"
        )
        # We patch the script by running it via exec with BASE overridden.
        # Simpler: use subprocess with env var — but the script uses __file__.
        # Instead, directly import and call — but it uses module-level globals.
        # Easiest deterministic approach: read, patch BASE, exec in isolated ns.
        source = script.read_text(encoding="utf-8")
        source = source.replace(
            "BASE = Path(__file__).resolve().parent",
            f"BASE = Path({str(agents_dir)!r})",
        )
        # Also patch SKILLS_DIR and SPECS_DIR to avoid false "unknown skill" errors
        repo_root = Path(__file__).resolve().parents[1]
        source = source.replace(
            "SKILLS_DIR = BASE.parent / \"skills\"",
            f"SKILLS_DIR = Path({str(repo_root / 'library' / 'organization' / 'skills')!r})",
        )
        source = source.replace(
            "SPECS_DIR = BASE.parent / \"specs\"",
            f"SPECS_DIR = Path({str(repo_root / 'library' / 'organization' / 'specs')!r})",
        )

        import io
        import contextlib

        captured = io.StringIO()
        ns: dict = {}
        with contextlib.redirect_stdout(captured):
            with contextlib.redirect_stderr(captured):
                try:
                    exec(compile(source, str(script), "exec"), ns)  # noqa: S102
                    rc = ns["main"]()
                except SystemExit as exc:
                    rc = exc.code if isinstance(exc.code, int) else 1

        return rc, captured.getvalue()

    def test_valid_agent_passes(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="aether-agent-test-") as tmp:
            base = Path(tmp)
            self._write_agent(base, "test-agent")
            rc, output = self._validate_inline(base)
        self.assertEqual(rc, 0, msg=output)

    def test_missing_aether_id_fails(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="aether-agent-test-") as tmp:
            base = Path(tmp)
            self._write_agent(base, "test-agent", fm_override={"aether-id": None})
            rc, output = self._validate_inline(base)
        self.assertNotEqual(rc, 0, msg=output)

    def test_aether_id_mismatch_fails(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="aether-agent-test-") as tmp:
            base = Path(tmp)
            self._write_agent(base, "test-agent", fm_override={"aether-id": "wrong-id"})
            rc, output = self._validate_inline(base)
        self.assertNotEqual(rc, 0, msg=output)
        self.assertIn("does not match directory name", output)

    def test_empty_tools_fails(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="aether-agent-test-") as tmp:
            base = Path(tmp)
            self._write_agent(base, "test-agent", fm_override={"tools": []})
            rc, output = self._validate_inline(base)
        self.assertNotEqual(rc, 0, msg=output)
        self.assertIn("tools list must not be empty", output)

    def test_unknown_tool_fails(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="aether-agent-test-") as tmp:
            base = Path(tmp)
            self._write_agent(base, "test-agent", fm_override={"tools": ["read", "admin"]})
            rc, output = self._validate_inline(base)
        self.assertNotEqual(rc, 0, msg=output)
        self.assertIn("unknown tool 'admin'", output)

    def test_missing_body_section_fails(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="aether-agent-test-") as tmp:
            base = Path(tmp)
            self._write_agent(
                base,
                "test-agent",
                body="\n## Mission\n\nTest.\n\n## Workflow\n\n1. Test.\n",
            )
            rc, output = self._validate_inline(base)
        self.assertNotEqual(rc, 0, msg=output)
        self.assertIn("## Operating contract", output)

    def test_invalid_status_fails(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="aether-agent-test-") as tmp:
            base = Path(tmp)
            meta = {
                "aether-version": "1.0.0",
                "aether-status": "published",  # invalid
                "aether-scope": "organization",
                "aether-domain": "quality",
                "aether-owners": "egohygiene",
                "aether-created": "2026-08-08",
                "aether-updated": "2026-08-08",
            }
            self._write_agent(base, "test-agent", fm_override={"metadata": meta})
            rc, output = self._validate_inline(base)
        self.assertNotEqual(rc, 0, msg=output)
        self.assertIn("aether-status", output)


if __name__ == "__main__":
    unittest.main()
