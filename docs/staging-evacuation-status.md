# Staging Evacuation Status

**Scope:** `.staging/` disposition audit for issue #18  
**Date:** 2026-08-09  
**Status:** Partially complete — preconditions not yet fully satisfied

---

## Current Inventory

| Metric | Count |
|---|---|
| Total files in `.staging/` | 734 |
| Top-level classification buckets | 8 |
| Skill directories | 186 |
| Skills with `SKILL.md` | 186 |
| External catalog entries (approved) | 56 |
| First-party disposition records | 14 |
| Historical removed skill copies | 6 |

### Classification buckets

All top-level `.staging/` directories are classified under known buckets:
`agents`, `hooks`, `instructions`, `integrations`, `manifests`, `scripts`,
`skills`, `specs`.

Strict CI validation (`./aether validate --staging --strict-staging`) confirms
no unclassified top-level unit exists.

---

## Skills Disposition Summary

The staged skills inventory (`catalog/reports/staged-skills-inventory.v1.json`)
covers 192 entries (186 current + 6 historically removed).

| Classification | Count |
|---|---|
| Approved external catalog entry | 56 |
| First-party candidate (handled by named issue) | 6 |
| Unknown provenance — requires human review | 130 |

### Approved external skills (56)

All 56 entries are cataloged in `catalog/external/approved-skills.v1.json` with
upstream repository, skill path, pin example, and provenance evidence.  Their
`.staging/skills/` copies are preserved until Alan acknowledges removal is safe
(ADR-005 deletion gate, condition 2: external catalog entry exists).

### First-party candidates (6)

Six skills have disposition records in `catalog/first-party/staging-dispositions/`
under named issues.  They remain in staging until the adopting issues are merged.

### Unknown provenance — 130 skills

130 skills have no upstream source in the lock file and no individual disposition
record.  **ADR-005 deletion gate is not satisfied** for these files.
Human review is required before any removal.

---

## Agents Disposition

Covered in `/.staging/manifests/agents-ledger.json`:

| Agent | Status |
|---|---|
| architect | Adopted → `library/organization/agents/architect/` |
| arxiv-publisher | Adopted → `library/organization/agents/arxiv-publisher/` |
| auditor | Adopted → `library/organization/agents/auditor/` |
| bug-fix-teammate | Adopted → `library/organization/agents/bug-fix-teammate/` |
| cleanup-specialist | Adopted → `library/organization/agents/cleanup-specialist/` |
| github-issue-creator | Adopted → `library/organization/agents/github-issue-creator/` |
| implementation-planner | Adopted → `library/organization/agents/implementation-planner/` |
| specfile-creator | Adopted → `library/organization/agents/specfile-creator/` |
| test-specialist | Adopted → `library/organization/agents/test-specialist/` |
| flutter-architect | Move-out (Flutter) — awaiting Alan's acknowledgment |
| flutter-engineer | Move-out (Flutter) — awaiting Alan's acknowledgment |
| knowledge-extractor | Move-out (Mindgarden) — awaiting Alan's acknowledgment |
| synapse-creator | Move-out (Mindgarden) — awaiting Alan's acknowledgment |

The staged copies of all 13 agents **remain in `.staging/agents/`** per ADR-005
until:
- 9 adopted agents: canonical content confirmed complete
- 4 move-out agents: Alan acknowledges receipt in the destination repository

---

## Hooks Disposition

Eight hook prototypes are in `.staging/hooks/`:
`dependency-license-checker`, `fix-broken-links`, `governance-audit`,
`secrets-scanner`, `session-auto-commit`, `session-logger`, `tool-guardian`,
plus corresponding `integrations/github-copilot/` material.

Per **ADR-007** (Staged hook prototype disposition for first release), hooks
are **not removed** from `.staging/` at this milestone.  All are pending:

1. Ownership classification (Aether provider adapter vs. Egolint/Relay)
2. Threat-model review per the eight-point checklist in `DECISIONS.md`
3. Human approval before adoption

---

## Integrations Disposition

`.staging/integrations/` contains:

| Integration | Notes |
|---|---|
| `claude/` | Cross-repo (Claude); move-out pending Alan |
| `continue/` | Cross-repo (Continue); move-out pending Alan |
| `github-copilot/` | Copilot hook scripts; under ADR-007 review |
| `opencode/` | Cross-repo (OpenCode); move-out pending Alan |
| `specify/` | Cross-repo (Specify); move-out pending Alan |

None may be removed without Alan's acknowledgment or an individual rejection
record.

---

## Instructions / Scripts / Specs Disposition

| Bucket | Files | Status |
|---|---|---|
| `.staging/instructions/` | 2 | Require individual human review |
| `.staging/scripts/` | 2 | Require individual human review |
| `.staging/specs/` | 6 | Require individual human review |

---

## Tasks.txt Note

No `tasks.txt` file is present in the current `.staging/manifests/` directory.
The ideas originally captured in `.staging/tasks.txt` (as described in the
issue) appear to have been resolved in prior issues or are tracked in the
existing issue backlog.  If a `tasks.txt` was present in an earlier branch
state, its durable decisions should be confirmed as captured in
`DECISIONS.md`, `ROADMAP.md`, or the GitHub issue backlog before this
document is finalized.

---

## Precondition Status (per Issue #18)

| Precondition | Status |
|---|---|
| Issues 001–016 merged or superseded | Verify against GitHub milestone |
| Alan acknowledged move-out paths | **Blocking** — 4 agents + integrations not confirmed |
| First-party candidates adopted/reconciled/rejected | Partial — 6 recorded; 130 unknown |
| External snapshots governed by catalog | Done — 56 in `approved-skills.v1.json` |
| Legacy bundles have authoritative replacements | Not fully assessed |
| Branch clean and CI passes | CI passes (strict staging: 0 diagnostics) |

---

## Strict CI Validation — Item 10

`./aether validate --staging --strict-staging` is now included in the PR
validation workflow (`.github/workflows/pr-validation.yml`).  Any pull request
that introduces an unclassified top-level `.staging/` directory will fail CI.

This enforces the intake requirement: future staging content must be classified
under a known bucket and accompanied by a machine-readable intake record.

---

## Residual Backlog (bounded)

The following items are deferred to a subsequent milestone, not automatically
reopened:

1. **130 unknown-provenance skills**: Require human review for each; batch or
   individual disposition records needed.
2. **4 move-out agents**: Remove after Alan confirms receipt.
3. **Hooks**: Remove after ADR-007 threat-model review and ownership decision.
4. **Cross-repo integrations**: Remove after Alan confirms receipt.
5. **Instructions / Scripts / Specs**: Individual human review required.
6. **tasks.txt ideas**: Confirm all durable decisions are in DECISIONS.md or backlog.
7. **Final `.staging/` removal**: Only after all six items above are resolved.
