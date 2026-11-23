---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-23T06:07:56.997250+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Make the two architecture pilots portable with exact complete governing resources while preserving
    original requirements, source history and draft lifecycle.
  includes:
  - Authored draft parent/child locator clarification, exact package-local parent/set/schema closure and
    stable governing metadata.
  - Exact repository-only pre-change source and unresolved comparison mapping; no generated content rewriting.
  - Actual selected two-pilot local install/materialization/dry-run/cleanup and preserved remote/combined/release
    limits.
  excludes:
  - No portable-validator, builder, installed-host adapter or stable/ADR lifecycle rule changes.
  - No staged modification/deletion/promotion, global/user installation, remote qualification, tags/releases,
    hosted dispatch or publication.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - DECISIONS.md
  - library/organization/skills/architecture/architecture-authoring/SKILL.md
  - library/organization/skills/architecture/create-architecture-document/SKILL.md
  - library/organization/specs/architecture/document.spec.md
  - library/organization/specs/architecture/foundation/architecture.spec.md
  - library/organization/specs/architecture/set.spec.md
  - library/organization/specs/architecture/architecture-document.schema.json
  - docs/work/38/architecture-portability-20261123/HISTORY.md
  - docs/work/38/architecture-portability-20261123/VALIDATION.md
  - docs/work/38/architecture-portability-20261123/qualification.json
  - docs/work/38/architecture-portability-20261123/consumer-local.json
  - docs/work/38/architecture-portability-20261123/roadmap-impact.json
work:
  objective: Make the two architecture pilots portable with exact complete governing resources while preserving
    original requirements, source history and draft lifecycle.
  success_conditions:
  - Both real exported architecture packages pass strict pristine validation and retain byte-identical
    governing resources.
  - Missing parent/schema/set fails without canonical fallback; all tagged normative paragraphs and original
    graph/lifecycle metadata remain preserved.
  - Actual scoped local CLI stages pass, with full tests and exact source-bound observations; no remote/combined/release
    inference.
  active_issue:
    provider: github
    id: egohygiene/aether#38
    url: https://github.com/egohygiene/aether/issues/38
  next:
    kind: action
    id: integrate-original-three-pilot-local-gate
    description: Review and integrate this architecture checkpoint with the separately owned audit checkpoint,
      regenerate combined outputs and rerun the unchanged original three-pilot local gate; preserve remote/stable-release
      acceptance.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/38
    depends_on: []
state:
  base:
    revision: dc3549c8a23bed5fb551a458a22605e7e0777822
    ref: refs/heads/main
    verified_at: '2026-11-23T06:07:56.997250+00:00'
  candidate:
    branch: codex/38-portable-architecture-20261123
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-23T06:07:56.997250+00:00'
    default_branch_revision: dc3549c8a23bed5fb551a458a22605e7e0777822
    issue_state: open
    pull_request_state: not-applicable
    notes: Fresh provider reads verify merged141/142 main dc3549 and open38; no open Aether PR exists
      at observation. This architecture candidate has no PR yet; parent owns integration/publication.
      No release or lifecycle promotion.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-23T06:07:56.997250+00:00'
  reviewed_by: Codex
  evidence:
  - command: Seven real architecture package controls and eight continuity integration controls
    outcome: passed
    observed_at: '2026-11-23T06:07:56.997250+00:00'
    notes: Actual builder/strict validator, exact resources, missing-parent/schema/set even after inventory
      tampering, unchanged015/016 rejection, schema governance and six archived originals. Eval revisions
      aligned without changing cases.
  - command: ./aether test at8848f2f19904f5cc432d6438e8f6dedbcc17bbe8
    outcome: passed
    observed_at: '2026-11-23T06:07:56.997250+00:00'
    notes: 435discovered:424passed/11existing optional-native skips in20.224s. Earlier old-eval revision
      failure retained and resolved; no new remote/native OS claim.
  - command: Actual gh2.96 ConsumerInstallationHarness local scope with process-local first two architecture
      entries
    outcome: passed
    observed_at: '2026-11-23T06:07:56.997250+00:00'
    notes: All5required local scenarios pass; localready/complete, overallnot-ready as remote skipped.
      Raw006/017 tracking observations retained; exact installed semantic/resource inventories pass. Production
      three-pilot list remains unchanged.
  - command: Canonical source/link/JSON, catalog/distribution drift, protected inputs and whitespace
    outcome: passed
    observed_at: '2026-11-23T06:07:56.997250+00:00'
    notes: Only historical AETHER_PROVENANCE_009 warning; link/JSON0diagnostics. Staging/decisions/set/schema/global
      validator/builder/host adapter unchanged. All20package hashes and independent source review match.
  - command: Roadmap-impact reconciliation against actual diff and existing AET-Q01/AET-Q05
    outcome: passed
    observed_at: '2026-11-23T06:07:56.997250+00:00'
    notes: Single not-affected receipt; no roadmap mutation, strategic completion, maturity or human disposition
      inferred.
  environment_limitations:
  - The source-bound actual consumer/test selection is8848f2f; this later handoff does not relabel it
    as a new run.
  - The audit sibling/combined three-pilot check, remote install/update/rollback and stable-release acceptance
    remain separate.
  - CLI filesystem installation is not model authoring, automatic host discovery, native OS matrix or
    signer authentication.
  - Historical Issue016 provider mapping is unverified; original staged comparison and ADR0005 human deletion
    gate remain intact.
  - Pinned continuity structure is narrower than official released EgoLint conformance.
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

User/runtime and scoped instructions, live work state and canonical source outrank this operational snapshot. This is a draft architecture package checkpoint, not stable policy or release acceptance.

## Resume protocol

Read AGENTS, the four authored canonical sources, their history/validation packet and live issue/PR state. Earlier141→142 are merged atdc3549. Preserve unrelated dirty checkouts and immutable prior observations.

## Current objective and success conditions

Make the two architecture pilots portable with exact complete governing resources while preserving original requirements, source history and draft lifecycle.

## State snapshot

Base/main isdc3549c8a23bed5fb551a458a22605e7e0777822. Candidate codex/38-portable-architecture-20261123 has null containing revision/pre-PR reference. Actual clean tested source is8848f2f19904f5cc432d6438e8f6dedbcc17bbe8; later evidence is not relabeled execution.

## Completed and material changes

Draft parent2.1.1 and child1.1.1 clarify existing stable identity/source-versus-installed locators. Draft skills1.2.0 package three/four governing resources, including unchanged set1.0.0/schema. Relative parent/schema/set links resolve in canonical and installed hierarchies. Six original Git blobs and former paths remain repository-only. Tagged normative paragraphs, original graph/owner/status/creation metadata and staged bytes remain unchanged. The old comparison ordinal has no invented provider mapping or retirement authority.

## Validation and review evidence

Seven package/eight continuity controls pass. Full435suite:424pass/11existing skips. Actual compatible CLI local5/5pass with exact installed materialization; overallnot-ready preserves remote skips/raw006/017. Source validation retains only old009warning; links/JSON, catalog/dist drift, protected inputs and whitespace pass. Independent source review reproduced/closed the wrong provider inference and confirms exact history/requirements/negative controls. Read the source-bound packet for all20file hashes and scoped results.

## Blockers, risks, unknowns, and deferred work

This architecture-only cohort does not qualify the third audit pilot, whole original cohort, remote/update/rollback, stable payload or actual model use. Native host matrix/discovery and independent CLI authenticity remain unobserved. Historical comparison mapping is unknown, never completed by this portability change. Existing ADR0002/0006 conflict and proposed0009 remain untouched.

## Next dependency-ready work

Review this draft, integrate the separately reviewed audit checkpoint, regenerate combined catalog/distributions and execute the original unchanged three-pilot local gate. Then retain existing remote/stable/consumer release acceptance under38; do not infer authority or completion from local readiness.

## Parallel changes and reconciliation

The audit worker owns audit-repository, draft specfile/audit-data, approved-byte-preserving closure and its own history. Both branches regenerate their own evidence; parent must reconcile shared catalog/dist and root continuity semantically. No open peer PR was observed; known in-progress branches are not called merged.

## Privacy and redaction

Public artifact facts, synthetic controls and sanitized local reports only. No private transcript, credentials, environment values, HOME repurposing or personal paths are stored. Actual cleanup preserves unrelated fixture content and user/global state.

## Handoff update protocol

Reverify live state after domain checks and before parent PR handoff. Reference ADR0001/0002/0004/0005 and existing source/host contracts. Single roadmap disposition is not-affected, AET-Q01/AET-Q05. Validate pinned schema,12headings and16384-byte/240-line budgets. No ADR lifecycle promotion or duplicate issue.

## Compaction and supersession

Git, archived originals and the existing issue retain history. Replace current operational prose on integration; preserve exact source/results and unresolved human/release boundaries.
