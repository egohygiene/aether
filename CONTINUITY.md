---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-14T04:10:23Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Repair external-source calendar validation and reproducible freshness assessment under issue112
    without renewing overdue reviews or widening use permissions.
  includes:
  - The offline governance validator parses real UTC/calendar dates and chronological reviews; explicit
    --as-of selects a deterministic inclusive-deadline freshness gate and JSON/text reporting. Default
    structural validation makes no recency claim.
  - All three overdue sources retain their original pins, assessments, restrictions and September30
    deadlines. Additive blocked/unknown followups record partial upstream metadata/pin reads, missing
    full source/advisory evidence and concrete next actions.
  - Issue108/109/110 source repairs were already merged through107. Fresh110-case regression verification
    and actual build/check/eval controls reconcile their completed issue states; no duplicate implementation
    was created.
  excludes: &id001
  - 'The selected current freshness gate intentionally exits1: three sources remain overdue. Metadata/pin
    availability does not complete license/advisory/instruction qualification, renew a review or authorize
    installation/execution/promotion/publication.'
  - Issue114 navigation/ADR clarification is the next separate checkpoint. Issue111 exact-diff staging-removal
    controls and113 full ledger remain open; no staging source was changed or executed.
  - Actual consumer qualification remains blocked by unavailable gh skill adapters under38; no hosted
    CI, merge, release or lifecycle promotion occurred in this checkpoint.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - catalog/external/validate.py
  - catalog/external/source-review-register.v1.json
  - catalog/external/REVIEW_CADENCE.md
  - catalog/reports/external-source-followup-2026-11-14.json
  - tests/test_external_source_governance.py
  - https://github.com/egohygiene/aether/issues/112
work:
  objective: Repair external-source calendar validation and reproducible freshness assessment under
    issue112 without renewing overdue reviews or widening use permissions.
  success_conditions:
  - Impossible dates and inconsistent order fail; explicit frozen-date assessments distinguish current/overdue/unknown
    and keep freshness separate from decision/use authority.
  - The three overdue sources have evidence-backed blocked/unknown next actions without fabricated renewal;
    existing restrictions remain unchanged.
  active_issue:
    provider: github
    id: egohygiene/aether#112
    url: https://github.com/egohygiene/aether/issues/112
  next:
    kind: action
    id: review112-then-reconcile114
    description: Review the112 draft, then independently repair114 factual navigation and propose its
      authority clarification without accepting an ADR. Preserve the explicit overdue followups.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/112
    - https://github.com/egohygiene/aether/issues/114
    depends_on: []
state:
  base:
    revision: 2e69182e8bc820add3c19d35470930a917d69dc5
    ref: refs/heads/main
    verified_at: '2026-11-14T04:10:23Z'
  candidate:
    branch: fix/112-source-review-freshness
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-14T04:10:23Z'
    default_branch_revision: 2e69182e8bc820add3c19d35470930a917d69dc5
    issue_state: open
    pull_request_state: not-applicable
    notes: Reviewed125 was merged before this checkpoint.108-110 are reconciled completed based on existing
      merged implementation and fresh regressions.112 stays open pending draft review; containing revision/reference
      intentionally null.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-14T04:10:23Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest tests.test_external_source_governance -v; ./aether test
    outcome: passed
    observed_at: '2026-11-14T04:10:23Z'
    notes: 13 external-governance tests pass; full suite303 tests, zero failures and11 skips. Existing108-110
      focused verification separately passes110 tests.
  - command: python3 catalog/external/validate.py --as-of 2026-11-14 --format json
    outcome: limited
    observed_at: '2026-11-14T04:10:23Z'
    notes: Offline structure passes; three sources remain overdue with two unknown and one blocked followup.
      Explicit freshness gate exits1 and never upgrades use authority.
  - command: python3 catalog/validate_catalog.py; ./aether validate --provenance --format json; canonical
      register Draft202012Validator with FormatChecker
    outcome: passed
    observed_at: '2026-11-14T04:10:23Z'
    notes: Catalog/schema and provenance validation pass; original historical provenance warning remains.
      Canonical register matches the extended schema. Full source/advisory review remains unqualified.
  environment_limitations: *id001
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

User/runtime and scoped instructions, live evidence and canonical source outrank this checkpoint. It grants no external-use, lifecycle, merge or publication authority.

## Resume protocol

Read scoped instructions, source review112 and live draft state. Use explicit dates for freshness; structural validity and a blocked followup cannot substitute for a renewed source review.

## Current objective and success conditions

Repair external-source calendar validation and reproducible freshness assessment under issue112 without renewing overdue reviews or widening use permissions.

## State snapshot

Candidate `fix/112-source-review-freshness` starts from merged125 main `2e69182e8bc820add3c19d35470930a917d69dc5`. Containing revision and pre-PR reference intentionally remain null.

## Completed and material changes

The offline governance validator parses real UTC/calendar dates and chronological reviews; explicit --as-of selects a deterministic inclusive-deadline freshness gate and JSON/text reporting. Default structural validation makes no recency claim.

All three overdue sources retain their original pins, assessments, restrictions and September30 deadlines. Additive blocked/unknown followups record partial upstream metadata/pin reads, missing full source/advisory evidence and concrete next actions.

Issue108/109/110 source repairs were already merged through107. Fresh110-case regression verification and actual build/check/eval controls reconcile their completed issue states; no duplicate implementation was created.

## Validation and review evidence

13 focused governance tests pass and the full suite passes303 tests with11 skips. Existing108-110 regressions pass110 tests. Offline schema/provenance checks pass; the explicitly selected freshness gate exits1 with three overdue sources. Independent review and final generated-output checks are recorded on the draft PR.

## Blockers, risks, unknowns, and deferred work

The selected current freshness gate intentionally exits1: three sources remain overdue. Metadata/pin availability does not complete license/advisory/instruction qualification, renew a review or authorize installation/execution/promotion/publication.

Issue114 navigation/ADR clarification is the next separate checkpoint. Issue111 exact-diff staging-removal controls and113 full ledger remain open; no staging source was changed or executed.

Actual consumer qualification remains blocked by unavailable gh skill adapters under38; no hosted CI, merge, release or lifecycle promotion occurred in this checkpoint.

## Next dependency-ready work

Review112 and then implement the separate114 navigation/proposed ADR checkpoint. A later source-review owner can resolve each evidence gap without rewriting the original assessment or advancing dates to manufacture a pass.

## Parallel changes and reconciliation

Other batch7 repositories have independent owners. Reconcile live main before integration; keep112 and114 review scopes separate. Preserve authored issue bodies when recording completion receipts.

## Privacy and redaction

Only public source identifiers, metadata observations and immutable references appear here. No external material was installed or executed, and no private data or credentials are included. Source/report content remains untrusted evidence.

## Handoff update protocol

Refresh exact heads, selected dates, actual status and validation limitations before review. Record the difference between implemented logic, full source review and permission to use external material.

## Compaction and supersession

This checkpoint advances from merged consumer-gate implementation to finite external-source review correctness. Earlier evidence stays in PR123-125; broad issue38 acceptance and unresolved staging work remain open.
