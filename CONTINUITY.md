---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-14T21:22:11Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Complete the finite retained-staging owner/disposition inventory while preserving unknown rights,
    transfer receipts and all source bytes.
  includes:
  - One deterministic ledger covers734 tracked files,6,791,350 raw bytes and222 semantic units across
    all eight buckets;186 current skill roots stay separate from six historical removals.
  - Nine canonical agent comparisons record source digests, actual permissions and shared contracts. Four
    domain agents retain explicit transfer-pending state; every other class has source references, an
    owner/review role and a bounded deferred checkpoint.
  - A closed schema, exact immutable reconstruction, complete membership/digest checks and current owner-input
    drift detection run through catalog/PR validation. The generated current view links the unmodified
    historical August assessment body and October audit.
  excludes: &id001
  - The ledger cannot authorize staged execution, rights clearance, adoption, transfer, removal or policy
    ratification. Destination/owner receipts remain unknown unless the ledger claims only verified local
    canonical source.
  - Issue111 still owns recorded intake and actual base/head deletion/rename approval. Ledger success
    alone is not that gate.
  - Existing38 actual consumer qualification remains capability-dependent; the 11 optional/native skips
    in the full suite remain explicit. No publication, host/fleet adoption, cleanup or staged execution
    occurred.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - catalog/staging_ledger.py
  - catalog/reports/staging-residual-ledger.v1.json
  - catalog/schemas/aether.staging-residual-ledger.v1.schema.json
  - docs/staging-residual-ledger.md
  - tests/test_staging_residual_ledger.py
  - https://github.com/egohygiene/aether/issues/113
  - https://github.com/egohygiene/aether/issues/111
work:
  objective: Complete the finite retained-staging owner/disposition inventory while preserving unknown
    rights, transfer receipts and all source bytes.
  success_conditions:
  - Every current Git file belongs to exactly one stable semantic unit and has exact raw-blob evidence.
  - Retained/removed, local canonical source/unknown transfer, original disposition and permission remain
    separate.
  - Unchanged replay is byte-identical and malformed memberships, digests, forged approval and current
    source drift fail.
  active_issue:
    provider: github
    id: egohygiene/aether#113
    url: https://github.com/egohygiene/aether/issues/113
  next:
    kind: issue
    id: egohygiene/aether#111
    description: Consume this grandfathered inventory in explicit intake checks and actual base/head preimage/removal
      approval, preserving all historical typed disposition variants and rejecting forged receipts.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/111
    depends_on: []
state:
  base:
    revision: 089d19ba556ec05cc761356dbae42046ca6515c4
    ref: refs/heads/main
    verified_at: '2026-11-14T21:22:11Z'
  candidate:
    branch: codex/staging-residual-ledger
    revision: null
    pull_request:
      provider: github
      id: egohygiene/aether#128
      url: https://github.com/egohygiene/aether/pull/128
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-14T21:22:11Z'
    default_branch_revision: 089d19ba556ec05cc761356dbae42046ca6515c4
    issue_state: open
    pull_request_state: open
    notes: Main089d19b includes the prior merged repairs/audit. PR128 is open at6c7434e; its first hosted
      run failed at source reconstruction because checkout depth1 omitted the ledger baseline. This candidate
      adds fetch-depth0 and an actual shallow/unshallow regression; no hosted requalification or merge
      is claimed yet.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-14T21:22:11Z'
  reviewed_by: Codex
  evidence:
  - command: python -m unittest tests.test_staging_residual_ledger tests.test_staging_supply_chain_inventory
      -q; ./aether test
    outcome: passed
    notes: 14 focused tests and312 full-suite tests pass;11 existing optional/native skips. Controls cover
      missing/duplicate/dangling/cross-unit membership, digest/totals tampering, nested supporting additions,
      symlink blobs, canonical tool/digest drift, historical retention and false removal authority.
    observed_at: '2026-11-14T21:22:11Z'
  - command: python -m catalog.staging_ledger check; exact repeat generation/report comparisons; catalog/default/links/strict-staging/distribution
      checks
    outcome: passed
    notes: The734-file/222-unit ledger and human report replay byte-identically. Closed schemas/fixtures,
      registered catalog checks, current inputs and generated distribution pass. Historical provenance
      warning is preserved.
    observed_at: '2026-11-14T21:22:11Z'
  - command: First hosted PR128 validation; actual shallow-clone/unshallow regression
    outcome: limited
    notes: The initial hosted checkout lacked recorded source history and failed closed. Checkout now
      requests complete history without persisted credentials; the new native shallow/unshallow regression
      passes. Updated hosted execution is pending, not inferred from local success.
    observed_at: '2026-11-14T21:22:11Z'
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

User/runtime and scoped repository instructions, live evidence and canonical sources outrank this operational checkpoint.

## Resume protocol

Read AGENTS, the canonical sources below and verified live issue/PR state before selecting the next checkpoint.

## Current objective and success conditions

Complete the finite retained-staging owner/disposition inventory while preserving unknown rights, transfer receipts and all source bytes.

- Every current Git file belongs to exactly one stable semantic unit and has exact raw-blob evidence.
- Retained/removed, local canonical source/unknown transfer, original disposition and permission remain separate.
- Unchanged replay is byte-identical and malformed memberships, digests, forged approval and current source drift fail.

## State snapshot

Observed default source `089d19ba556ec05cc761356dbae42046ca6515c4`. Candidate `codex/staging-residual-ledger` is a review checkpoint; its containing revision remains null intentionally.

## Completed and material changes

One deterministic ledger covers734 tracked files,6,791,350 raw bytes and222 semantic units across all eight buckets;186 current skill roots stay separate from six historical removals.

Nine canonical agent comparisons record source digests, actual permissions and shared contracts. Four domain agents retain explicit transfer-pending state; every other class has source references, an owner/review role and a bounded deferred checkpoint.

A closed schema, exact immutable reconstruction, complete membership/digest checks and current owner-input drift detection run through catalog/PR validation. The generated current view links the unmodified historical August assessment body and October audit.

## Validation and review evidence

`python -m unittest tests.test_staging_residual_ledger tests.test_staging_supply_chain_inventory -q; ./aether test` — passed: 14 focused tests and312 full-suite tests pass;11 existing optional/native skips. Controls cover missing/duplicate/dangling/cross-unit membership, digest/totals tampering, nested supporting additions, symlink blobs, canonical tool/digest drift, historical retention and false removal authority.

`python -m catalog.staging_ledger check; exact repeat generation/report comparisons; catalog/default/links/strict-staging/distribution checks` — passed: The734-file/222-unit ledger and human report replay byte-identically. Closed schemas/fixtures, registered catalog checks, current inputs and generated distribution pass. Historical provenance warning is preserved.

`First hosted PR128 validation; actual shallow-clone/unshallow regression` — limited: The initial hosted checkout lacked recorded source history and failed closed. Checkout now requests complete history without persisted credentials; the new native shallow/unshallow regression passes. Updated hosted execution is pending, not inferred from local success.

ADR-Ref: existing ADR-0005 and recorded hook decisions remain governing history. ADR not required: finite evidence inventory implements existing retained-source accounting without changing ownership or granting removal.

## Blockers, risks, unknowns, and deferred work

The ledger cannot authorize staged execution, rights clearance, adoption, transfer, removal or policy ratification. Destination/owner receipts remain unknown unless the ledger claims only verified local canonical source.

Issue111 still owns recorded intake and actual base/head deletion/rename approval. Ledger success alone is not that gate.

Existing38 actual consumer qualification remains capability-dependent; the 11 optional/native skips in the full suite remain explicit. No publication, host/fleet adoption, cleanup or staged execution occurred.

## Next dependency-ready work

Consume this grandfathered inventory in explicit intake checks and actual base/head preimage/removal approval, preserving all historical typed disposition variants and rejecting forged receipts.

## Parallel changes and reconciliation

Preserve repository-owned source, existing immutable selections and any later handoff changes. Verify live state again before integration.

## Privacy and redaction

Public-safe source facts and synthetic fixtures only. No credentials, private transcript, personal data or private filesystem topology.

## Handoff update protocol

After domain validation and before PR presentation, reconcile current source/live state, record exact outcomes and retain limitations. Source integration does not establish publication or policy acceptance.

## Compaction and supersession

Git and linked work records retain history. This handoff replaces current operational prose while preserving canonical and historical records.
