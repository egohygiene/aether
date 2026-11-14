---
schema: egohygiene.architecture-decision/v1
id: ADR-0010
title: Bind staging changes to recorded intake and immutable review evidence
status: proposed
date: "2026-11-14"
decision_scope: repository
visibility: public
owners: [egohygiene/aether]
issue: https://github.com/egohygiene/aether/issues/111
pull_request: null
related: [ADR-0005, ADR-0007, ADR-0008, ADR-0009]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/aether]
affected_contracts: []
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/aether/issues/111
    description: Exact intake, supporting-file preimages, human approval and durable disposition controls.
  - type: documentation
    url: https://github.com/egohygiene/aether/blob/23bbfe29fa4b1905fd4c44ec5b41a79cfe683033/DECISIONS.md
    description: Original accepted ADR-0005 conditions and historical hook decisions, preserved without new disposition.
  - type: documentation
    url: https://github.com/egohygiene/aether/blob/23bbfe29fa4b1905fd4c44ec5b41a79cfe683033/catalog/reports/staging-residual-ledger.v1.json
    description: Finite retained-source baseline; inventory is not removal authority.
exceptions: []
approval: null
extensions: {}
---

# ADR-0010: Bind staging changes to recorded intake and immutable review evidence

## Context

Accepted ADR-0005 requires per-file human review or an explicit waiver, a
permitted destination/rejection and an ADR reference on the removal PR. Bucket
names and self-declared JSON approval do not establish those conditions. The
retained ledger accounts for source but intentionally grants no removal rights.

## Decision proposed

Propose exact quarantine intake records and base-admitted per-file review plans.
Actual Git paths, modes, source blobs, reviewed plan commits and retained
destination/rejection bytes must agree. Read a designated account's explicit
digest-bound statement from the actual provider; preserve the distinction
between an authenticated account statement and proof of a person's physical
operation. Agents cannot manufacture a statement claiming a human review.

Run the repository-local, standard-library controller from the immutable base
with only read permissions, before ordinary proposed-source validation. The
first controller admission permits no staging change. Keep historical flat and
hook record adapters separate and preserve their original meanings.

Canonical-source and explicit-rejection evidence have bounded implementations.
External catalog references do not substitute for ADR-0005's planned external
path; external-origin qualification remains unavailable until its own adapter
is reviewed. Unsupported evidence fails closed rather than granting an
exception. No actual removal, approval or source execution occurs here.

## Alternatives considered

- Accept an `approved: true` field or a user name in the proposed head: cannot
  authenticate provider provenance or bind the old source preimage.
- Require immediate adoption of all retained material: confuses inventory with
  rights resolution and makes unrelated work depend on experimental sources.
- Execute the proposed guard with the provider token: lets that same proposed
  source redefine its own admission boundary.
- Move reusable orchestration into Aether: unnecessary; this is its local
  repository wiring and Relay retains shared execution ownership.

## Consequences and limits

Receipt preparation and removal are separate reviewed changes. Changed
preimages, specification bytes, destination bytes or plan payloads need renewed
evidence. New intake remains quarantined. Real approval requires actual
provider access and a designated account statement; synthetic fixtures cannot
provide either. Administrators and workflow edits still require organization
merge governance; this mechanism does not install branch protection.

The proposal implements the existing accepted deletion conditions conservatively
and does not supersede ADR-0005, expand external-source authority or ratify the
separate ADR-0009 local-caller clarification. This record stays proposed with
null approval, independently of implementation and merge evidence.

## Validation and recovery

Synthetic Git/provider controls cover unrecorded nested support, exact positive
intake/removal, renamed/changed source, base-versus-head receipt admission,
forged account/body/conversation, missing ADR references, changed/symlinked
destinations, preserved legacy variants and poisoned proposed controllers.
Hosted controller bootstrap and actual input scheduling are inspected
separately. Rollback restores the prior reviewed controller/policy selection;
it does not remove quarantine source or erase accepted decisions and receipts.
