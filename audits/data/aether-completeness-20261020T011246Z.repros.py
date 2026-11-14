"""Bounded read-only-source audit repros for Aether dc8a16851f452763ef4f7fbe4bf057d4500b1921.

All test writes use temporary directories; no source, tags, packages or releases
are changed. Uses existing repository test-fixture constructors.
"""
from __future__ import annotations

import contextlib
import argparse
import hashlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--repository-root", type=Path, default=Path.cwd())
sys.dont_write_bytecode = True
ROOT = parser.parse_args().repository_root.resolve()
sys.path.insert(0, str(ROOT))


def load(name: str, relative: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


av = load("audit_aether_validator", "aether_validator.py")
vf = load("audit_validator_fixture", "tests/test_aether_validator.py")
bdt = load("audit_distribution_fixture", "tests/test_build_distributions.py")
brt = load("audit_release_fixture", "tests/test_release_artifacts.py")
sd = load("audit_spec_distribution", "library/organization/specs/build-distributions.py")
results = {}

current_drift = []
for artifact in json.loads((ROOT / "catalog/first-party/catalog.v1.json").read_text())["artifacts"]:
    frontmatter, error = av._parse_frontmatter(ROOT / artifact["source_path"])
    assert error is None
    version = ((frontmatter.get("metadata") or {}).get("aether-version")
               if artifact["kind"] == "skill" else frontmatter.get("version"))
    if str(version) != artifact["artifact_version"]:
        current_drift.append({"id": artifact["id"], "source_version": str(version),
                              "catalog_version": artifact["artifact_version"],
                              "source_path": artifact["source_path"]})
results["current_catalog_version_drift"] = current_drift

# Existing catalog records preserve all old source metadata and refresh only digest.
# Use the actual complete source/catalog corpus, copied into a private temp root.
with tempfile.TemporaryDirectory(prefix="aether-audit-catalog-") as tmp:
    t = Path(tmp)
    shutil.copytree(ROOT / "library", t / "library")
    shutil.copytree(ROOT / "catalog", t / "catalog")
    v = av.AetherValidator(t)
    baseline_diags = v.validate_catalog()
    skill = t / "library/organization/skills/quality/audit-repository/SKILL.md"
    skill.write_text(skill.read_text().replace('aether-version: "1.1.0"', 'aether-version: "9.9.9"')
                     .replace('aether-status: "draft"', 'aether-status: "stable"'))
    v.write_catalog()
    record = next(a for a in v.generate_catalog()["artifacts"] if a["id"] == "skill/audit-repository")
    diags = v.validate_catalog()
    results["catalog_metadata_drift"] = {
        "baseline_catalog_validation_errors": [d.rule_id for d in baseline_diags if d.severity == "error"],
        "source_version": "9.9.9", "catalog_version": record["artifact_version"],
        "source_status": "stable", "catalog_status": record["lifecycle"]["state"],
        "catalog_validation_errors": [d.rule_id for d in diags if d.severity == "error"],
    }

# Build mode returns success even after an artifact generation error.
bd = bdt.bd
with tempfile.TemporaryDirectory(prefix="aether-audit-builder-") as tmp:
    t = Path(tmp)
    original = bd.REPO_ROOT, bd.SKILLS_DIR
    bd.REPO_ROOT, bd.SKILLS_DIR = t, t / "library/organization/skills"
    try:
        skill_dir = bdt._make_skill(t, "broken-skill")
        file = skill_dir / "SKILL.md"
        file.write_text(file.read_text().replace(
            '  aether-version: "1.2.3"',
            '  aether-version: "1.2.3"\n  aether-distribution-resources:\n'
            '    - source: "missing.json"\n      destination: "references/missing.json"',
        ))
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture), contextlib.redirect_stderr(capture):
            build_rc = bd.build(output_directory=t / "dist")
            check_rc = bd.build(check=True, output_directory=t / "dist")
        results["builder_false_success"] = {
            "build_exit_code": build_rc, "check_exit_code": check_rc,
            "generated_files": len(list((t / "dist").rglob("SKILL.md"))),
            "error_logged": "ERROR  broken-skill" in capture.getvalue(),
        }
    finally:
        bd.REPO_ROOT, bd.SKILLS_DIR = original

# Check mode ignores files/packages no longer owned by the generated inventory.
with tempfile.TemporaryDirectory(prefix="aether-audit-extra-dist-") as tmp:
    t = Path(tmp)
    original = bd.REPO_ROOT, bd.SKILLS_DIR
    bd.REPO_ROOT, bd.SKILLS_DIR = t, t / "library/organization/skills"
    try:
        bdt._make_skill(t, "retained-skill")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            bd.build(output_directory=t / "dist")
        stale = t / "dist/skills/removed-skill/SKILL.md"
        stale.parent.mkdir(parents=True)
        stale.write_text("removed source artifact sentinel\n")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = bd.build(check=True, output_directory=t / "dist")
        results["unowned_distribution_inventory"] = {"check_exit_code": rc, "unowned_package_retained": stale.exists()}
    finally:
        bd.REPO_ROOT, bd.SKILLS_DIR = original

# Companion symlinks are dereferenced before portable-package validation can see them.
with tempfile.TemporaryDirectory(prefix="aether-audit-symlink-") as tmp:
    t = Path(tmp)
    repo = t / "repo"
    original = bd.REPO_ROOT, bd.SKILLS_DIR
    bd.REPO_ROOT, bd.SKILLS_DIR = repo, repo / "library/organization/skills"
    try:
        skill_dir = bdt._make_skill(repo, "linked-skill")
        external = t / "outside-sentinel.txt"
        external.write_text("OUTSIDE-REPOSITORY-AUDIT-SENTINEL\n")
        (skill_dir / "references/linked.txt").symlink_to(external)
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = bd.build(output_directory=repo / "dist")
        built = repo / "dist/skills/linked-skill/references/linked.txt"
        results["companion_symlink_read_escape"] = {
            "build_exit_code": rc, "copied_outside_sentinel": built.read_bytes() == external.read_bytes(),
            "generated_output_is_symlink": built.is_symlink(),
        }
    finally:
        bd.REPO_ROOT, bd.SKILLS_DIR = original

# A declared failing assertion is silently omitted when its golden file is absent.
fx = vf.ValidatorFixture.create()
evals = fx.root / "library/organization/skills/domain/example-skill/evals/evals.json"
data = json.loads(json.dumps(vf._VALID_EVALS_V2))
data["cases"][0]["assertions"] = [{"type": "contains", "value": "IMPOSSIBLE-AUDIT-MARKER"}]
evals.write_text(json.dumps(data))
out = fx.validator().run_evals(skill_filter="example-skill")
results["missing_golden_assertion"] = {
    "status": out["status"], "first_case_status": out["results"][0]["cases"][0]["status"],
    "first_case_checks": out["results"][0]["cases"][0]["checks"],
    "validation_errors": [d.rule_id for d in fx.validator().validate_evals() if d.severity == "error"],
}
out = fx.validator().run_evals(skill_filter="nonexistent-audit-skill")
results["unmatched_eval_filter"] = {"status": out["status"], "total_cases": out["total_cases"], "skills": out["skills_evaluated"]}
data["cases"] = []
evals.write_text(json.dumps(data))
out = fx.validator().run_evals(skill_filter="example-skill")
results["schema_invalid_eval_run"] = {
    "status": out["status"], "total_cases": out["total_cases"],
    "validate_errors": [d.rule_id for d in fx.validator().validate_evals() if d.severity == "error"],
}

# Invalid specification identifiers are not rejected before use as output paths.
fx = vf.ValidatorFixture.create()
source = fx.root / "library/organization/specs/domain/example.spec.md"
source.write_text(source.read_text().replace("id: example-spec", "id: ../../escaped"))
spec_diags, _, _ = fx.validator().validate_specs()
original = sd.REPO_ROOT, sd.SPECS_DIR
sd.REPO_ROOT, sd.SPECS_DIR = fx.root, fx.root / "library/organization/specs"
try:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        rc = sd.build(output_directory=fx.root / "dist")
    results["spec_output_escape"] = {
        "spec_validation_errors": [d.rule_id for d in spec_diags if d.severity == "error"],
        "build_exit_code": rc, "wrote_outside_dist": (fx.root / "escaped.spec.md").exists(),
    }
finally:
    sd.REPO_ROOT, sd.SPECS_DIR = original

# Release metadata reruns hash previous generated metadata, including self-reference.
case = brt.TestBuildReleaseArtifacts()
case.setUp()
try:
    br = brt.br
    release = br.build_release_artifacts("v1.2.3", case.output_directory, "a" * 40)
    first = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in release.iterdir() if p.is_file()}
    br.build_release_artifacts("v1.2.3", case.output_directory, "a" * 40)
    second = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in release.iterdir() if p.is_file()}
    provenance = json.loads((release / "release-provenance.v1.json").read_text())
    entries = {x["path"]: x["sha256"] for x in provenance["output_files"]}
    results["release_metadata_rerun"] = {
        "changed_metadata_files": sorted(k for k in first if first[k] != second[k]),
        "provenance_lists_itself": "release/release-provenance.v1.json" in entries,
        "recorded_self_digest_matches_final": entries.get("release/release-provenance.v1.json") == second["release-provenance.v1.json"],
    }
finally:
    case.tearDown()

br = brt.br
results["changelog_header_mismatch"] = {
    "actual_bracketed_header_present": "## [Unreleased]" in (ROOT / "CHANGELOG.md").read_text(),
    "extracted_current_changelog_excerpt": br._extract_unreleased_changelog(ROOT / "CHANGELOG.md"),
}

print(json.dumps(results, indent=2, sort_keys=True))
