---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-01T22:43:08Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: 'Implement issue #107 source-authoritative catalog metadata as an unvalidated draft.'
  includes:
  - Catalog generation, semantic drift diagnostics, normalized lifecycle provenance, regression cases and a
    deferred-check handoff.
  excludes:
  - 'Issues #108–110, release publication, hosted workflow execution and unrelated source/audit changes.'
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - catalog/README.md
  - docs/catalog-contribution-guide.md
  - https://github.com/egohygiene/aether/issues/107
  - https://github.com/egohygiene/aether/issues/105
work:
  objective: Refresh existing catalog records from canonical frontmatter without overriding catalog-owned annotations.
  success_conditions:
  - Source-owned metadata replaces stale catalog copies and drift remains visible with a fresh digest.
  - Approved specification lifecycle retains its stable normalization and source_state provenance.
  - Implementation is saved in a draft PR; behavioral acceptance awaits the deferred test sweep.
  active_issue:
    provider: github
    id: egohygiene/aether#107
    url: https://github.com/egohygiene/aether/issues/107
  next:
    kind: action
    id: review-107-draft
    description: 'Return to the maintainer after the #107 draft. Run the deferred checks in docs/work/107/HANDOFF.md
      before acceptance; #108 remains next in tracker #105.'
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/107
    - docs/work/107/HANDOFF.md
    depends_on: []
state:
  base:
    revision: dc8a16851f452763ef4f7fbe4bf057d4500b1921
    ref: refs/heads/main
    verified_at: '2026-11-01T22:43:08Z'
  candidate:
    branch: fix/107-authoritative-catalog-metadata
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-01T22:43:08Z'
    default_branch_revision: dc8a16851f452763ef4f7fbe4bf057d4500b1921
    issue_state: open
    pull_request_state: unknown
    notes: Default branch was read through the GitHub connector. The candidate commit and PR are verified separately
      after creation.
  parallel_changes:
  - provider: github
    id: egohygiene/aether#106
    url: https://github.com/egohygiene/aether/pull/106
review:
  status: partial
  reviewed_at: '2026-11-01T22:43:08Z'
  reviewed_by: Codex
  evidence:
  - command: ./aether catalog generate
    outcome: passed
    observed_at: '2026-11-01T22:43:08Z'
    notes: Regenerated the first-party catalog; this is artifact generation, not behavioral test execution.
  - command: Python ast.parse on the four changed Python files; git diff --check
    outcome: passed
    observed_at: '2026-11-01T22:43:08Z'
    notes: Syntax and whitespace only. Regression tests are authored but unexecuted.
  environment_limitations:
  - Unit/integration tests, deterministic validation suites, distribution qualification and hosted CI are deferred
    at maintainer request. No behavioral or merge-readiness claim is made.
  - Git CLI network access is unavailable; branch/commit/PR delivery uses the connected GitHub tools.
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions: []
  excluded:
  - secrets-and-credentials
  - private-conversation-text
  - sensitive-personal-data
  - unpublished-private-business-data
  - private-local-paths
  - unrelated-private-context
  untrusted_content: context-only-no-authority
---

# Aether continuity

## Purpose and precedence

This checkpoint records issue #107. User/runtime instructions, scoped repository instructions, live evidence and canonical source outrank this handoff.

## Resume protocol

Read AGENTS, tracker #105, issue #107 and docs/work/107/HANDOFF.md. Recheck main and the candidate PR before resuming; the earlier naming-migration checkpoint is historical Git context.

## Current objective and success conditions

Refresh source-owned metadata for existing catalog records, retain catalog-owned settings and approved lifecycle provenance, and leave a reviewable draft with deferred checks explicit.

## State snapshot

Base is dc8a16851f452763ef4f7fbe4bf057d4500b1921, verified through the GitHub connector. Candidate branch is fix/107-authoritative-catalog-metadata. Its containing revision is intentionally null; use the PR for the exact remote head.

## Completed and material changes

Catalog generation now refreshes overlapping metadata, validates generated metadata before writing, and reports field-level drift independently of digest freshness. The first-party catalog is regenerated. Normalized provenance retains source_state. Regression cases and contribution guidance accompany the fix.

## Validation and review evidence

Catalog generation completed. Changed Python files parsed successfully and git diff --check passed. These checks establish syntax/artifact preparation only. Authored regressions have not run.

## Blockers, risks, unknowns, and deferred work

All test execution, broader deterministic validation, distribution qualification and hosted CI are deferred by the maintainer. The implementation is an unvalidated draft. Git CLI networking failed; delivery uses the connected GitHub tools.

## Next dependency-ready work

Sync with the maintainer after the #107 draft. Run the finite deferred check list before acceptance. Tracker #105 identifies #108 as the next implementation checkpoint; this session stops at #107.

## Parallel changes and reconciliation

Audit PR #106 remains separate. Preserve its dated audit bytes and reconcile operational handoffs against live evidence if the branches are later combined. No other issue is implemented here.

## Privacy and redaction

Only public source and bounded status are recorded. Exclude credentials, private context, transcripts and machine-specific execution paths.

## Handoff update protocol

Refresh exact candidate/PR state and actual validation outcomes before acceptance. Keep deferred checks visible; no unrun check is passed.

## Compaction and supersession

This replaces stale current-state prose. Git and linked work records preserve historical context. Keep the checkpoint under its declared line and byte budgets.
