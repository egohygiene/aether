---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-03T04:38:01Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Make skill/spec distribution generation fail honestly and compare the complete owned output
    inventory without deleting unknown files.
  includes: &id001
  - Generation/discovery/output-I/O errors return nonzero in build and check modes; partial generation/write
    counts remain explicit.
  - Detect obsolete packages, extra companion files and empty directories under each owned skills/specs
    subtree, including when no artifacts remain.
  - Preserve custom-output behavior, deterministic valid output bytes, unknown files and top-level failure
    propagation.
  excludes:
  - Tests/hosted CI, publishing/tagging, issue closure, release-engine redesign and automatic cleanup.
  - 'Symlink/path confinement under #110 and catalog metadata work in draft115.'
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - library/organization/skills/build-distributions.py
  - library/organization/specs/build-distributions.py
  - tests/test_build_distributions.py
  - tests/test_build_spec_distributions.py
  - tests/test_release_artifacts.py
  - README.md
  - DECISIONS.md
  - https://github.com/egohygiene/aether/issues/108
work:
  objective: Make skill/spec distribution generation fail honestly and compare the complete owned output
    inventory without deleting unknown files.
  success_conditions: *id001
  active_issue:
    provider: github
    id: egohygiene/aether#108
    url: https://github.com/egohygiene/aether/issues/108
  next:
    kind: action
    id: review-draft-and-qualify
    description: Review the builder inventory/failure draft and run issue108 negative/partial/CLI regressions
      during qualification; reconcile CONTINUITY with parallel catalog draft115 before a later merge.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/108
    depends_on: []
state:
  base:
    revision: dc8a16851f452763ef4f7fbe4bf057d4500b1921
    ref: refs/heads/main
    verified_at: '2026-11-03T04:38:01Z'
  candidate:
    branch: codex/108-honest-distribution-builds
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-03T04:38:01Z'
    default_branch_revision: dc8a16851f452763ef4f7fbe4bf057d4500b1921
    issue_state: open
    pull_request_state: not-applicable
    notes: Main dc8a168 and open issue108 were freshly verified. Four-digit source work already merged
      in PR104; old handoff next-step prose is superseded. Draft115 (catalog metadata) and audit106 remain
      open/untouched. This candidate is independent of the dirty catalog worktree and performs no merge
      or release.
  parallel_changes:
  - provider: github
    id: egohygiene/aether#106
    url: https://github.com/egohygiene/aether/pull/106
  - provider: github
    id: egohygiene/aether#115
    url: https://github.com/egohygiene/aether/pull/115
review:
  status: partial
  reviewed_at: '2026-11-03T04:38:01Z'
  reviewed_by: Codex
  evidence:
  - command: ./aether distribution build --output-directory dist
    outcome: passed
    observed_at: '2026-11-03T04:38:01Z'
    notes: Current canonical valid inputs generated successfully through all four existing top-level generators.
      Final edited builders returned0. No suite ran.
  - command: ./aether distribution build --output-directory dist --check
    outcome: passed
    observed_at: '2026-11-03T04:38:01Z'
    notes: Complete current skill/spec owned inventory and existing other-generator checks pass; output/catalog
      regeneration leaves tracked derived bytes unchanged.
  - command: ./aether catalog generate
    outcome: passed
    observed_at: '2026-11-03T04:38:01Z'
    notes: Required canonical-source regeneration succeeds; first-party catalog bytes are unchanged. No
      dirty draft115 source was used.
  - command: AST parsing of both builders and three regression sources; git diff --check
    outcome: passed
    observed_at: '2026-11-03T04:38:01Z'
    notes: Five Python sources parse and whitespace is clean. Eleven new regression methods plus a stronger
      full-inventory rebuild assertion are authored but unexecuted.
  - command: Pinned Aether continuity metadata/schema, twelve-section/budget/privacy inspection
    outcome: passed
    observed_at: '2026-11-03T04:38:01Z'
    notes: Checkpoint meets structural schema and size limits; official released EgoLint conformance is
      not executed.
  - command: Builder negative/partial/custom-output fixtures, command propagation regression suites and
      hosted CI
    outcome: not-run
    observed_at: '2026-11-03T04:38:01Z'
    notes: Normal valid-source generation/check is bounded product evidence; newly authored failure-case
      regressions remain unexecuted.
  environment_limitations:
  - Negative, partial-failure, collision and custom-output regressions are authored but have not run;
    issue108 stays open.
  - Existing top-level propagation already preserves generator errors; only regression coverage was added
    there, avoiding catalog draft115 source overlap.
  - 'Inventory checks do not establish symlink/path confinement; #110 remains separate.'
  - Official released EgoLint continuity conformance and broader suites are unexecuted.
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

Record the bounded issue108 draft only. User/runtime and scoped instructions, live evidence and canonical sources outrank this operational checkpoint.

## Resume protocol

Read AGENTS, the builders, README distribution behavior and issue108. Verify main/PR state and preserve parallel catalog draft115; PR104 has already merged.

## Current objective and success conditions

Return nonzero for required generation/I/O failures in both modes and reject unexpected owned inventory while retaining unknown bytes for review. Keep deterministic outputs and custom roots compatible.

## State snapshot

Base main is dc8a16851f452763ef4f7fbe4bf057d4500b1921. Issue108 is open; candidate branch codex/108-honest-distribution-builds has null self-revision/PR before creation. Existing drafts106/115 remain open.

## Completed and material changes

Both canonical builders separate missing/stale drift from generation/I/O failures, report partial counts and compare all owned files/directories, even after the last source artifact is removed. Output collisions fail. Unknown entries are diagnosed and retained. Top-level propagation code is unchanged; its regression is added.

## Validation and review evidence

Valid-source top-level distribution build and --check both returned0 after the final source edit. Catalog regeneration returned0; no tracked dist/catalog bytes changed. Five Python sources parse; git diff --check and continuity schema/structure/budget checks pass.

## Blockers, risks, unknowns, and deferred work

Eleven new regression methods and the improved rebuild comparison are unexecuted, as are hosted CI and broader suites. #110 retains confinement; #38/#94/#95 retain separate release/publication work. No contract/ADR lifecycle is promoted.

## Next dependency-ready work

Review and execute issue108 acceptance regressions in the qualification phase. Keep the issue open until failure/custom-output/CLI paths have actual proof, and reconcile the operational handoff with catalog draft115 before merging.

## Parallel changes and reconciliation

Draft106 is audit work; draft115 changes catalog metadata independently. Their source changes are preserved. Root CONTINUITY will need semantic reconciliation at merge rather than concatenating working snapshots.

## Privacy and redaction

Only public scoped project facts and source paths are retained. No private context, credentials, local workspace paths or unrelated source are included.

## Handoff update protocol

Refresh after review and actual negative-case checks. ADR not required: routine implementation repair of the existing canonical-to-derived contract, without new publication authority or format. Pinned Aether continuity guidance is applied; no merge, issue closure, tag or publication occurs.

## Compaction and supersession

Keep twelve required sections and existing byte/line budgets. Canonical builders, Git and issue108 retain detailed implementation/history; this file records only the current handoff.
