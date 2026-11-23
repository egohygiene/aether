"""Exercise the real audit export and its unchanged authority/history boundary."""

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

from aether_validator import FRONTMATTER_RE, validate_portable_skill_package


ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "library/organization/skills/quality/audit-repository"
HISTORY = ROOT / "docs/work/38/audit-portability-20261123"
BASE = "dc3549c8a23bed5fb551a458a22605e7e0777822"
GOVERNING = {
    "specfile": ("2.0.1", "draft", "library/organization/specs/authoring/specfile.spec.md"),
    "auditor": ("2.0.0", "approved", "library/organization/specs/quality/auditor.spec.md"),
    "repository-audit-data": ("1.0.2", "draft", "library/organization/specs/quality/repository-audit-data.spec.md"),
}


def frontmatter(content):
    return yaml.safe_load(FRONTMATTER_RE.match(content.decode()).group(1))


def source_at_baseline(path):
    return subprocess.check_output(["git", "show", BASE + ":" + path], cwd=ROOT)


class AuditPortableGovernanceTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            "audit_portable_builder", ROOT / "library/organization/skills/build-distributions.py",
        )
        self.builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.builder)
        self.temporary = tempfile.TemporaryDirectory(prefix="aether-audit-portable-")
        self.addCleanup(self.temporary.cleanup)
        destination = Path(self.temporary.name)
        self.generated = self.builder._build_skill_dist("audit-repository", PACKAGE)
        for relative, content in self.generated.items():
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        self.package = destination / "dist/skills/audit-repository"

    def test_actual_export_is_strictly_portable_with_complete_governing_closure(self):
        self.assertEqual(validate_portable_skill_package(self.package), [])
        found = {}
        for identifier, (version, status, source) in GOVERNING.items():
            path = self.package / "references/governance" / (identifier + ".spec.md")
            self.assertEqual(path.read_bytes(), (ROOT / source).read_bytes())
            metadata = frontmatter(path.read_bytes())
            self.assertEqual((metadata["id"], str(metadata["version"]), metadata["status"]),
                             (identifier, version, status))
            found[identifier] = metadata
        for identifier, metadata in found.items():
            self.assertLessEqual(set(metadata["depends_on"]), found.keys(), identifier)
        manifest = json.loads((self.package / "distribution-manifest.v1.json").read_text())
        self.assertEqual(manifest["source_digest"], {
            "algorithm": "sha256-utf8-lf",
            "value": hashlib.sha256((PACKAGE / "SKILL.md").read_bytes()).hexdigest(),
        })

    def test_missing_governing_resource_is_not_a_portable_pass(self):
        for identifier in GOVERNING:
            with self.subTest(identifier=identifier):
                path = self.package / "references/governance" / (identifier + ".spec.md")
                original = path.read_bytes()
                path.unlink()
                diagnostics = validate_portable_skill_package(self.package)
                self.assertTrue(any(d.rule_id == "AETHER_PORTABLE_012" and
                                    identifier + ".spec.md" in d.context.get("generated_path", "")
                                    for d in diagnostics))
                path.write_bytes(original)

    def test_real_runtime_canonical_and_staging_paths_still_reject(self):
        path = self.package / "SKILL.md"
        original = path.read_bytes()
        for text, rule in [("library/organization/specs/quality/auditor.spec.md", "AETHER_PORTABLE_015"),
                           (".staging/skills/repository-audit/SKILL.md", "AETHER_PORTABLE_016")]:
            with self.subTest(rule=rule):
                path.write_bytes(original + ("\nLoad " + text + "\n").encode())
                self.assertIn(rule, {d.rule_id for d in validate_portable_skill_package(self.package)})
        path.write_bytes(original)

    def test_exact_historical_bytes_and_restricted_staging_dispositions_remain(self):
        record = json.loads((HISTORY / "source-history.json").read_text())
        self.assertEqual(record["baselineRevision"], BASE)
        self.assertEqual(len(record["archived"]), 8)
        self.assertEqual({item["source_path"] for item in record["archived"]}, {
            "library/organization/skills/quality/audit-repository/SKILL.md",
            "library/organization/skills/quality/audit-repository/references/staged-reconciliation.md",
            "library/organization/skills/quality/audit-repository/references/audit-data-contract.md",
            "library/organization/specs/quality/repository-audit-data.spec.md",
            "library/organization/specs/authoring/specfile.spec.md",
            "library/organization/skills/quality/audit-repository/evals/evals.json",
            "catalog/first-party/staging-dispositions/repository-audit.json",
            "catalog/first-party/staging-dispositions/auditor-agent.json",
        })
        for item in record["archived"]:
            with self.subTest(source=item["source_path"]):
                content = (ROOT / item["archive_path"]).read_bytes()
                self.assertEqual(content, source_at_baseline(item["source_path"]))
                self.assertEqual(len(content), item["bytes"])
                self.assertEqual(hashlib.sha256(content).hexdigest(), item["sha256"])
        self.assertEqual(len(record["unchanged"]), 8)
        self.assertEqual({item["id"] for item in record["unchanged"]}, {
            "staged-repository-audit-skill", "staged-auditor-agent", "auditor", "auditor-agent",
            "audit-contract-helper", "audit-profile-registry", "audit-profile-schema", "audit-report-schema",
        })
        for item in record["unchanged"]:
            with self.subTest(unchanged=item["id"]):
                content = (ROOT / item["source_path"]).read_bytes()
                self.assertEqual(content, source_at_baseline(item["source_path"]))
                self.assertEqual(hashlib.sha256(content).hexdigest(), item["sha256"])
        for name in ["repository-audit", "auditor-agent"]:
            path = "catalog/first-party/staging-dispositions/" + name + ".json"
            before = json.loads(source_at_baseline(path))
            after = json.loads((ROOT / path).read_text())
            for key in ["staging_path", "disposition", "hash_status", "hash_algorithm", "trust_classification"]:
                self.assertEqual(after[key], before[key])
            self.assertEqual(after["lock_reference"], "docs/work/38/audit-portability-20261123/HISTORY.md")
            self.assertTrue((ROOT / after["lock_reference"]).is_file())
        before = (HISTORY / "history/staged-reconciliation-before.md").read_text()
        behavior = before[before.index("| Staged behavior |"):before.index("\nNo staged source is deleted")]
        summary = (self.package / "references/staged-reconciliation.md").read_text()
        self.assertIn(behavior, summary)
        for item in record["unchanged"][:3]:
            self.assertIn(item["sha256"], summary)
        self.assertFalse(any("audit-portability-20261123/history/" in p for p in self.generated))

    def test_specfile_naming_and_canonical_placement_requirements_do_not_change(self):
        relative = "library/organization/specs/authoring/specfile.spec.md"
        before = source_at_baseline(relative).decode()
        after = (ROOT / relative).read_text()
        def section(content, start, end):
            return content.split(start, 1)[1].split(end, 1)[0]
        old_section = section(before, "## 4. Naming and Placement", "## 5. Metadata Contract")
        new_section = section(after, "## 4. Naming and Placement", "## 5. Metadata Contract")
        self.assertEqual([line for line in old_section.splitlines() if line.startswith("- ")],
                         [line for line in new_section.splitlines() if line.startswith("- ")])
        self.assertIn("    .github/specs/", new_section)
        self.assertIn("neither moves those sources nor", new_section)
        self.assertEqual(after.split("## 5. Metadata Contract", 1)[1], before.split("## 5. Metadata Contract", 1)[1])
        old_meta = frontmatter(before.encode())
        new_meta = frontmatter(after.encode())
        for key in old_meta.keys() - {"version", "updated"}:
            self.assertEqual(old_meta[key], new_meta[key])
        self.assertEqual((ROOT / "ARCHITECTURE.md").read_bytes(), source_at_baseline("ARCHITECTURE.md"))
        self.assertTrue((ROOT / relative).is_file())


if __name__ == "__main__":
    unittest.main()
