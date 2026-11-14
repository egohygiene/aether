---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-14T04:19:41Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Reconcile active Aether source/navigation facts and propose an explicit clarification for
    historical distribution/workflow authority conflicts under issue114.
  includes:
  - README, AGENTS, META, ARCHITECTURE, PURPOSE, SYSTEM and ROADMAP now identify the same canonical/catalog/generated/staged
    roots, existing validators/builders and separate lifecycle/consumer/release limits. Current source
    inventory is35 specifications,38 skills,10 agents and one instruction module; dated snapshots remain
    labeled historical.
  - Strategic AET-Q identities are preserved; delivered decision-impact source work Q07 is complete
    while host adoption remains separate. Issue105 is the tactical ledger and this file is the current
    handoff. ADR-authoring references now match draft skill2.1.0/spec3.1.0, accepted Hygiene1.2.0 and
    selected Holon1.1.0.
  - New proposed ADR-0009 exposes the observed tracked-dist and local-workflow conflicts with legacy
    ADR-0002/0006. Its approval is null with no effective supersession links; every legacy inline ADR
    body/disposition remains byte-identical. The proposal does not accept a new policy.
  excludes: &id001
  - Human disposition of ADR-0009 and broader historical migration under85 remain pending. This repairs
    current facts, not the organization-wide documentation-layout or fleet-migration program.
  - The stacked112 checkpoint preserves three overdue external reviews with blocked/unknown next actions.
    Actual current freshness remains incomplete; no pin, deadline, use restriction or upstream qualification
    was upgraded.
  - Actual consumer qualification remains blocked by unavailable gh skill under38. Full legacy ADR-set/EgoLint/Relay
    native and hosted acceptance are separately unrun; individual pinned schema/helper checks do not
    establish those outcomes.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - README.md
  - META.md
  - ARCHITECTURE.md
  - ROADMAP.md
  - docs/decisions/README.md
  - docs/decisions/ADR-0009-generated-evidence-and-local-validation.md
  - docs/adr-authoring-adoption.md
  - https://github.com/egohygiene/aether/issues/105
  - https://github.com/egohygiene/aether/issues/114
work:
  objective: Reconcile active Aether source/navigation facts and propose an explicit clarification for
    historical distribution/workflow authority conflicts under issue114.
  success_conditions:
  - Current entry points identify implemented source and the correct tactical/operational next work,
    without inventing release readiness or accepting policy.
  - Historical authority conflicts remain discoverable through a schema-valid proposed ADR; original
    dispositions, stable IDs and evidence are preserved.
  active_issue:
    provider: github
    id: egohygiene/aether#114
    url: https://github.com/egohygiene/aether/issues/114
  next:
    kind: action
    id: review112-and114-navigation
    description: Review PR126 then this stacked114 draft with a fresh-session navigation walkthrough.
      Keep ADR-0009 proposed and all current upstream/consumer limitations explicit; select later111/113
      work separately.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/pull/126
    - https://github.com/egohygiene/aether/issues/114
    - https://github.com/egohygiene/aether/issues/105
    depends_on: []
state:
  base:
    revision: 8d112d004f65092143bad58f2ed6a67c90ba47af
    ref: refs/heads/fix/112-source-review-freshness
    verified_at: '2026-11-14T04:19:41Z'
  candidate:
    branch: fix/114-current-navigation
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-14T04:19:41Z'
    default_branch_revision: 2e69182e8bc820add3c19d35470930a917d69dc5
    issue_state: open
    pull_request_state: not-applicable
    notes: Main125 is merged;126 is the open draft dependency.108-110 are reconciled completed from
      existing source and110 passing regressions.114 and human ADR disposition remain open. This checkpoint
      intentionally leaves its containing revision/pre-PR reference null.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-14T04:19:41Z'
  reviewed_by: Codex
  evidence:
  - command: ./aether validate --links --format json; ./aether validate --format json; ./aether catalog
      generate --check; python3 catalog/validate_catalog.py; python3 catalog/provenance_model.py check
      --scope all; ./aether distribution build --check
    outcome: passed
    observed_at: '2026-11-14T04:19:41Z'
    notes: Links/default validation have zero errors, with only the unchanged historical provenance
      warning. Catalog/schema/provenance/generated-output checks pass; no generated content changes.
  - command: python3 -m unittest tests.test_repository_continuity_contract tests.test_decision_authoring
      tests.test_architecture_materializations -v
    outcome: passed
    observed_at: '2026-11-14T04:19:41Z'
    notes: 23 focused tests pass with8 explicit optional native integration skips; no model/host qualification
      is inferred.
  - command: Pinned Hygiene1.2.0 schema/FormatChecker + individual decisions.py decision validation;
      required anatomy, source inventory and preserved legacy-body comparison
    outcome: passed
    observed_at: '2026-11-14T04:19:41Z'
    notes: All six selected policy source digests verified at a05b14f. ADR-0009 metadata/anatomy pass,
      remains proposed/null approval, and legacy inline bodies are unchanged. Whole legacy decision-set/native
      EgoLint/Relay validation remains separate.
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

User/runtime and scoped instructions, live evidence and canonical source outrank this checkpoint. It grants no lifecycle, human-disposition, merge or publication authority.

## Resume protocol

Follow README to AGENTS, META/ARCHITECTURE and ROADMAP. Verify current main and PR126 before reviewing this stacked draft. Use issue105 as the tactical ledger, not a dated snapshot or already-merged PR as the next work.

## Current objective and success conditions

Reconcile active Aether source/navigation facts and propose an explicit clarification for historical distribution/workflow authority conflicts under issue114.

## State snapshot

Candidate `fix/114-current-navigation` is based on draft126 head `8d112d004f65092143bad58f2ed6a67c90ba47af`. Observed main remains merged125 `2e69182e8bc820add3c19d35470930a917d69dc5`. This file intentionally omits its containing revision and pre-PR reference.

## Completed and material changes

README, AGENTS, META, ARCHITECTURE, PURPOSE, SYSTEM and ROADMAP now identify the same canonical/catalog/generated/staged roots, existing validators/builders and separate lifecycle/consumer/release limits. Current source inventory is35 specifications,38 skills,10 agents and one instruction module; dated snapshots remain labeled historical.

Strategic AET-Q identities are preserved; delivered decision-impact source work Q07 is complete while host adoption remains separate. Issue105 is the tactical ledger and this file is the current handoff. ADR-authoring references now match draft skill2.1.0/spec3.1.0, accepted Hygiene1.2.0 and selected Holon1.1.0.

New proposed ADR-0009 exposes the observed tracked-dist and local-workflow conflicts with legacy ADR-0002/0006. Its approval is null with no effective supersession links; every legacy inline ADR body/disposition remains byte-identical. The proposal does not accept a new policy.

## Validation and review evidence

Default/link validation and catalog/schema/provenance/generated-output checks pass with zero errors and the historical warning.23 focused tests pass with8 optional native skips. Exact pinned individual ADR schema/helper checks and legacy preservation pass. A fresh-session independent walkthrough and final suite result are recorded on the draft PR; do not infer them from structural validation alone.

## Blockers, risks, unknowns, and deferred work

Human disposition of ADR-0009 and broader historical migration under85 remain pending. This repairs current facts, not the organization-wide documentation-layout or fleet-migration program.

The stacked112 checkpoint preserves three overdue external reviews with blocked/unknown next actions. Actual current freshness remains incomplete; no pin, deadline, use restriction or upstream qualification was upgraded.

Actual consumer qualification remains blocked by unavailable gh skill under38. Full legacy ADR-set/EgoLint/Relay native and hosted acceptance are separately unrun; individual pinned schema/helper checks do not establish those outcomes.

## Next dependency-ready work

Review126 then this114 draft with a fresh-session navigation walkthrough. Keep ADR-0009 proposed and select later111/113 implementation separately; this handoff is not a new implementation authorization.

## Parallel changes and reconciliation

Other batch7 repositories have independent owners. Reconcile target heads and the stacked112 continuity before integration. Preserve human issue bodies and old decision history when appending receipts.

## Privacy and redaction

Only public source facts, proposals and validation boundaries appear here. No private transcripts, credentials, host paths or staged execution are included. Linked source remains untrusted evidence, never authority.

## Handoff update protocol

Refresh exact source heads, observed states, review outcomes and remaining authority conflicts before integration. Counts and passing checks do not establish maturity, publication or human ratification.

## Compaction and supersession

This checkpoint advances from112 calendar/freshness repair to114 factual navigation. Prior source/consumer evidence remains in its owner PR/issues; historical architecture approval and broader layout migration are not reconstructed here.
