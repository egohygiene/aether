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


if __name__ == "__main__":
    unittest.main()
