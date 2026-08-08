# Core engineering skill curation ledger

This ledger records the canonical promotion decisions for the six first-party
engineering skills curated from staging in issue 010.

| Skill | Canonical path | Provenance | Legacy variants reviewed | Resources added | Eval coverage | Staging disposition |
|---|---|---|---|---|---|---|
| `skill-authoring` | `library/organization/skills/authoring/skill-authoring/` | First-party Ego Hygiene content curated from `.staging/skills/skill-authoring/SKILL.md` | `create-skill` reviewed as older overlap; no external text adopted | `references/validation-checklist.md`, `templates/SKILL.template.md` | positive, negative, insufficient-evidence, boundary, update-tagged revision case | canonicalized; staged copy removed; record in `staging-dispositions/skill-authoring.json` |
| `github-issue-authoring` | `library/organization/skills/authoring/github-issue-authoring/` | First-party Ego Hygiene content curated from `.staging/skills/github-issue-authoring/SKILL.md` | `github-issue`, `github-issues`, `create-github-issue-feature-from-specification`, and `create-github-issues-feature-from-implementation-plan` reviewed as synonym or specialized overlap | `references/copy-ready-checklist.md`, `templates/GITHUB_ISSUE.template.md` | positive, negative, insufficient-evidence, boundary, update-tagged revision case | canonicalized; staged copy removed; record in `staging-dispositions/github-issue-authoring.json` |
| `implementation-planning` | `library/organization/skills/authoring/implementation-planning/` | First-party Ego Hygiene content curated from `.staging/skills/implementation-planning/SKILL.md` | `create-implementation-plan` reviewed as overlapping synonym | `references/phase-design-checklist.md`, `templates/IMPLEMENTATION_PLAN.template.md` | positive, negative, insufficient-evidence, boundary, update-tagged revision case | canonicalized; staged copy removed; record in `staging-dispositions/implementation-planning.json` |
| `bug-fixing` | `library/organization/skills/quality/bug-fixing/` | First-party Ego Hygiene content curated from `.staging/skills/bug-fixing/SKILL.md` | `diagnose` reviewed as narrower overlap | `references/regression-checklist.md`, `templates/BUG_FIX_REPORT.template.md` | positive, negative, insufficient-evidence, boundary, update-tagged revision case | canonicalized; staged copy removed; record in `staging-dispositions/bug-fixing.json` |
| `repository-cleanup` | `library/organization/skills/quality/repository-cleanup/` | First-party Ego Hygiene content curated from `.staging/skills/repository-cleanup/SKILL.md` | `repository-audit` reviewed as adjacent but intentionally distinct workflow | `references/classification-checklist.md`, `templates/CLEANUP_PLAN.template.md` | positive, negative, insufficient-evidence, boundary, update-tagged revision case | canonicalized; staged copy removed; record in `staging-dispositions/repository-cleanup.json` |
| `test-engineering` | `library/organization/skills/quality/test-engineering/` | First-party Ego Hygiene content curated from `.staging/skills/test-engineering/SKILL.md` | `breakdown-test` and `pytest-coverage` reviewed as narrower overlaps | `references/determinism-checklist.md`, `templates/TEST_PLAN.template.md` | positive, negative, insufficient-evidence, boundary, update-tagged revision case | canonicalized; staged copy removed; record in `staging-dispositions/test-engineering.json` |

## Notes

- No new governing specification was added for these six skills. The workflows
  were normalized as reusable procedures without introducing new normative
  contracts solely for symmetry.
- The canonical text remains provider-neutral. GitHub-specific behavior is
  limited to the issue artifact itself, not to host-specific tool instructions.
- Reviewed overlap that was not adopted remains in staging for independent
  follow-up and provenance preservation.
