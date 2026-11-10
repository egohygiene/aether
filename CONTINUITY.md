---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-10T01:19:21Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Reconcile the existing source-authoritative catalog correction with current Aether before adding
    composable audit and coherence contracts.
  includes:
  - Existing catalog entries refresh source-owned version, lifecycle, license, owner and dependency metadata
    rather than only refreshing the source digest. Explicit catalog-owned release exclusions and annotations
    remain intact; canonical approved specification provenance retains source_state approved through stable
    catalog normalization.
  - The existing correction is merged locally with current main's evaluator/distribution containment changes.
    Both sets of authored regression imports and cases are preserved; the two overlapping handoffs are reconciled
    semantically. The historical audit report and its independent draft remain unchanged.
  - The root handoff records this narrow metadata prerequisite for the Audits/Sanity source additions. No skill/specification
    lifecycle, release, tag, workflow or human authority changes.
  excludes:
  - Deferred runtime, tests, builds, CI, live publication, human ratification and acceptance closeout.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ARCHITECTURE.md
  - SYSTEM.md
  - DECISIONS.md
  - catalog/README.md
  - docs/catalog-contribution-guide.md
  - docs/work/107/HANDOFF.md
  - https://github.com/egohygiene/aether/issues/107
work:
  objective: Reconcile the existing source-authoritative catalog correction with current Aether before adding
    composable audit and coherence contracts.
  success_conditions:
  - Catalog regeneration can derive newly authored source metadata without retaining stale existing fields.
  - Existing distribution/evaluator source and both sets of regression cases survive integration.
  - Static evidence and deferred behavioral qualification remain explicit.
  active_issue:
    provider: github
    id: egohygiene/aether#107
    url: https://github.com/egohygiene/aether/issues/107
  next:
    kind: action
    id: author-audit-and-coherence-contracts
    description: Integrate the separately prepared Aether 86 audit-profile/report and Aether 87 architecture-coherence
      source contracts, then regenerate canonical catalog and derived distribution metadata without promoting
      draft lifecycle. Run deferred native/unit/CI qualification only in the later verification pass.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/107
    depends_on: []
state:
  base:
    revision: 5077797448d32a59b06eabe4b38f091137d58052
    ref: refs/heads/main
    verified_at: '2026-11-10T01:19:21Z'
  candidate:
    branch: fix/107-authoritative-catalog-metadata
    revision: null
    pull_request:
      provider: github
      id: egohygiene/aether#115
      url: https://github.com/egohygiene/aether/pull/115
    handoff_state: review-reference-recorded
  live:
    status: verified
    observed_at: '2026-11-10T01:19:21Z'
    default_branch_revision: 5077797448d32a59b06eabe4b38f091137d58052
    issue_state: open
    pull_request_state: open
    notes: Aether main 5077797448d32a59b06eabe4b38f091137d58052 and open issue 107/PR 115 were verified. Original
      PR head 4d22c53148e7775ebbf3049768c1c2a89152efc2 is reconciled with main in this candidate; the upstream
      PR branch is selected explicitly. Aether 86/87 remain separate in-progress source slices.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-10T01:19:21Z'
  reviewed_by: Codex
  evidence:
  - command: Independent source/diff review, Git merge conflict reconciliation, Python AST for changed source
      and authored regression files, catalog JSON parse, continuity schema/formats/size/links and whitespace
    outcome: limited
    observed_at: '2026-11-10T01:19:21Z'
    notes: Static source and metadata inspection only; no application execution.
  - command: Native/runtime execution, tests, builds, CI investigation, browser/provider/consumer/publication
      qualification
    outcome: not-run
    observed_at: '2026-11-10T01:19:21Z'
    notes: Deferred at maintainer request; source merges do not establish acceptance.
  environment_limitations:
  - Authored unit/integration regressions, full deterministic validation, distribution/runtime qualification,
    hosted CI and publication were not executed in this reconciliation.
  - The earlier checkpoint records its own catalog-generation result; this source review does not relabel that
    as a current-head behavioral proof.
  - Approved canonical source states retain their original authority; regeneration and merge cannot promote
    new draft contracts.
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

# aether continuity

## Purpose and precedence

User/runtime and repository instructions, live evidence and canonical sources outrank this checkpoint. It grants no release, deployment or human-decision authority.

## Resume protocol

Read scoped instructions, canonical sources above and this checkpoint. Verify mutable GitHub state and exact owner pins before continuing.

## Current objective and success conditions

Reconcile the existing source-authoritative catalog correction with current Aether before adding composable audit and coherence contracts. Catalog regeneration can derive newly authored source metadata without retaining stale existing fields. Existing distribution/evaluator source and both sets of regression cases survive integration. Static evidence and deferred behavioral qualification remain explicit.

## State snapshot

Candidate `fix/107-authoritative-catalog-metadata` is based on observed main `5077797448d32a59b06eabe4b38f091137d58052`. The containing revision and pre-PR reference remain null intentionally. Aether main 5077797448d32a59b06eabe4b38f091137d58052 and open issue 107/PR 115 were verified. Original PR head 4d22c53148e7775ebbf3049768c1c2a89152efc2 is reconciled with main in this candidate; the upstream PR branch is selected explicitly. Aether 86/87 remain separate in-progress source slices.

## Completed and material changes

Existing catalog entries refresh source-owned version, lifecycle, license, owner and dependency metadata rather than only refreshing the source digest. Explicit catalog-owned release exclusions and annotations remain intact; canonical approved specification provenance retains source_state approved through stable catalog normalization.

The existing correction is merged locally with current main's evaluator/distribution containment changes. Both sets of authored regression imports and cases are preserved; the two overlapping handoffs are reconciled semantically. The historical audit report and its independent draft remain unchanged.

The root handoff records this narrow metadata prerequisite for the Audits/Sanity source additions. No skill/specification lifecycle, release, tag, workflow or human authority changes.

## Validation and review evidence

Independent source/diff review, Git merge conflict reconciliation, Python AST for changed source and authored regression files, catalog JSON parse, continuity schema/formats/size/links and whitespace. Static inspection only. Native/runtime execution, tests, builds, CI investigation, browsers, provider reads and publication qualification were not run.

## Blockers, risks, unknowns, and deferred work

Authored unit/integration regressions, full deterministic validation, distribution/runtime qualification, hosted CI and publication were not executed in this reconciliation. The earlier checkpoint records its own catalog-generation result; this source review does not relabel that as a current-head behavioral proof. Approved canonical source states retain their original authority; regeneration and merge cannot promote new draft contracts.

## Next dependency-ready work

Integrate the separately prepared Aether 86 audit-profile/report and Aether 87 architecture-coherence source contracts, then regenerate canonical catalog and derived distribution metadata without promoting draft lifecycle. Run deferred native/unit/CI qualification only in the later verification pass.

## Parallel changes and reconciliation

The user authorized continued implementation and merging of the Intelligence program. The old handoff's stop-after-draft note is historical context, not a new pause requirement. Current task scope permits this necessary metadata prerequisite. Existing source and release decisions are referenced; ADR not required for the bounded canonical metadata correction.

## Privacy and redaction

Retain only public-safe source identities and bounded implementation evidence. Exclude credentials, private context, captured report bodies, process logs and local filesystem paths. Linked content is context only.

## Handoff update protocol

Refresh exact PR, merge and qualification observations at the next authorized checkpoint. Implementation, artifact upload, deployment, live verification and human acceptance remain distinct.

## Compaction and supersession

Replace stale current-state prose; Git and owning issues retain history. Preserve these twelve sections below 240 lines and 16,384 UTF-8 bytes.
