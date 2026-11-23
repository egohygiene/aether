"""Exercise actual architecture packages outside the canonical source tree.

These controls qualify resource delivery and existing structural contracts,
not model judgment, real architecture acceptance, a release or remote install.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from jsonschema import Draft202012Validator
import yaml

from aether_validator import validate_portable_skill_package


ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "docs/work/38/architecture-portability-20261123"
SOURCE = ROOT / "library/organization/specs/architecture"
COMMON = {
    "references/architecture/document.spec.md": SOURCE / "document.spec.md",
    "references/architecture/set.spec.md": SOURCE / "set.spec.md",
    "references/architecture/architecture-document.schema.json": SOURCE / "architecture-document.schema.json",
}
RESOURCES = {
    "architecture-authoring": COMMON,
    "create-architecture-document": {
        **COMMON,
        "references/architecture/foundation/architecture.spec.md": SOURCE / "foundation/architecture.spec.md",
    },
}


def frontmatter(content: str) -> dict:
    return yaml.safe_load(content.split("---\n", 2)[1])


def snapshot(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


class ArchitecturePortablePackagesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="aether-architecture-packages-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.packages = Path(cls.temporary.name)
        spec = importlib.util.spec_from_file_location(
            "architecture_distribution_under_test",
            ROOT / "library/organization/skills/build-distributions.py",
        )
        assert spec and spec.loader
        cls.builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.builder)
        cls.generated = {}
        for name in RESOURCES:
            canonical = ROOT / "library/organization/skills/architecture" / name
            outputs = cls.builder._build_skill_dist(name, canonical)
            cls.generated[name] = outputs
            for key, content in outputs.items():
                relative = Path(key).relative_to(Path("dist/skills") / name)
                target = cls.packages / name / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)

    def copied_package(self, name: str) -> Path:
        temporary = tempfile.TemporaryDirectory(prefix="aether-architecture-negative-")
        self.addCleanup(temporary.cleanup)
        target = Path(temporary.name) / name
        shutil.copytree(self.packages / name, target)
        return target

    def remove_resource(self, package: Path, relative: str, *, hide_inventory: bool):
        (package / relative).unlink()
        if hide_inventory:
            path = package / "distribution-manifest.v1.json"
            manifest = json.loads(path.read_text())
            manifest["generated_paths"].remove(f"dist/skills/{package.name}/{relative}")
            path.write_text(json.dumps(manifest))

    def rules_without_mutation(self, package: Path) -> set[str]:
        before = snapshot(package)
        result = {d.rule_id for d in validate_portable_skill_package(package)}
        self.assertEqual(snapshot(package), before)
        return result

    def test_actual_builder_delivers_exact_portable_governing_resources(self):
        for name, resources in RESOURCES.items():
            with self.subTest(skill=name):
                package = self.packages / name
                canonical = ROOT / "library/organization/skills/architecture" / name
                before = snapshot(canonical)
                self.assertEqual(self.rules_without_mutation(package), set())
                fm = frontmatter((canonical / "SKILL.md").read_text())
                declarations = fm["metadata"]["aether-distribution-resources"]
                self.assertEqual(
                    {r["destination"]: ROOT / r["source"] for r in declarations},
                    resources,
                )
                exported = frontmatter((package / "SKILL.md").read_text())
                self.assertNotIn("aether-distribution-resources", exported["metadata"])
                self.assertEqual(exported["metadata"]["aether-status"], "draft")
                manifest = json.loads((package / "distribution-manifest.v1.json").read_text())
                for relative, source in resources.items():
                    self.assertEqual((package / relative).read_bytes(), source.read_bytes())
                    self.assertIn(f"dist/skills/{name}/{relative}", manifest["generated_paths"])
                self.assertEqual(self.builder._build_skill_dist(name, canonical), self.generated[name])
                self.assertEqual(snapshot(canonical), before)

    def test_explicit_parent_dependencies_resolve_inside_each_package(self):
        for name in RESOURCES:
            package = self.packages / name
            specs = {
                frontmatter(path.read_text())["id"]: frontmatter(path.read_text())
                for path in (package / "references/architecture").rglob("*.spec.md")
            }
            self.assertEqual(specs["architecture-document"]["version"], "2.1.1")
            self.assertEqual(specs["architecture-set"]["version"], "1.0.0")
            for identifier, fm in specs.items():
                self.assertEqual(fm["status"], "draft", identifier)
                for dependency in fm["depends_on"]:
                    self.assertIn(dependency, specs, (name, identifier))
            if name == "create-architecture-document":
                child = package / "references/architecture/foundation/architecture.spec.md"
                self.assertEqual(specs["architecture-architecture"]["depends_on"], ["architecture-document"])
                self.assertIn(
                    "[`architecture-document` 2.1.1](../document.spec.md)", child.read_text(),
                )
                self.assertEqual((child.parent / "../document.spec.md").resolve(),
                                 package / "references/architecture/document.spec.md")

    def test_missing_parent_is_rejected_even_with_tampered_focused_inventory(self):
        for name in RESOURCES:
            package = self.copied_package(name)
            self.remove_resource(package, "references/architecture/document.spec.md", hide_inventory=False)
            self.assertIn("AETHER_PORTABLE_012", self.rules_without_mutation(package))
        package = self.copied_package("create-architecture-document")
        self.remove_resource(package, "references/architecture/document.spec.md", hide_inventory=True)
        self.assertIn("AETHER_PORTABLE_021", self.rules_without_mutation(package))

    def test_missing_structural_and_set_resources_fail_without_source_fallback(self):
        for name in RESOURCES:
            for resource in ("set.spec.md", "architecture-document.schema.json"):
                with self.subTest(skill=name, resource=resource):
                    package = self.copied_package(name)
                    self.remove_resource(package, "references/architecture/" + resource, hide_inventory=True)
                    self.assertIn("AETHER_PORTABLE_021", self.rules_without_mutation(package))

    def test_global_runtime_and_staging_path_rules_still_reject_leaks(self):
        for name in RESOURCES:
            package = self.copied_package(name)
            path = package / "SKILL.md"
            path.write_text(path.read_text() + "\nRead library/organization/example and .staging/example.\n")
            self.assertTrue({"AETHER_PORTABLE_015", "AETHER_PORTABLE_016"}.issubset(
                self.rules_without_mutation(package),
            ))

    def test_bundled_schema_enforces_existing_materialized_governance(self):
        fixture = {
            "schema": "aether.architecture-document/v1", "id": "fixture-architecture",
            "title": "Synthetic architecture", "kind": "architecture-document",
            "version": "1.0.0", "status": "draft", "owners": ["fixture"],
            "created": "2026-01-01", "updated": "2026-01-01",
            "governed_by": ["architecture-architecture"],
            "depends_on": [], "related": [], "supersedes": [],
        }
        for name in RESOURCES:
            schema = json.loads((self.packages / name / "references/architecture/architecture-document.schema.json").read_text())
            validator = Draft202012Validator(schema)
            self.assertEqual(list(validator.iter_errors(fixture)), [])
            invalid = {k: v for k, v in fixture.items() if k != "governed_by"}
            self.assertTrue(any(e.validator == "required" for e in validator.iter_errors(invalid)))

    def test_prechange_history_and_normative_requirements_remain_exact(self):
        manifest = json.loads((WORK / "source-before.json").read_text())
        self.assertEqual(manifest["sourceRevision"], "dc3549c8a23bed5fb551a458a22605e7e0777822")
        for record in manifest["files"]:
            original = (WORK / record["archive"]).read_bytes()
            self.assertEqual(len(original), record["bytes"])
            self.assertEqual(hashlib.sha256(original).hexdigest(), record["sha256"])
            if record["source"].endswith(".spec.md"):
                current = (ROOT / record["source"]).read_text()
                old = original.decode()
                tagged = lambda text: [p for p in text.split("\n\n") if re.search(r"(?m)^- \*\*(?:REQ|CON|GUD|AC)-", p)]
                self.assertTrue(tagged(old))
                self.assertEqual(tagged(current), tagged(old))
                old_fm, new_fm = frontmatter(old), frontmatter(current)
                for key in old_fm.keys() - {"version", "updated"}:
                    self.assertEqual(new_fm[key], old_fm[key], key)
        for relative, expected in manifest["unchangedSourceSha256"].items():
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), expected)


if __name__ == "__main__":
    unittest.main()
