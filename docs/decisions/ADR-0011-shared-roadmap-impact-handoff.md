---
schema: egohygiene.architecture-decision/v1
id: ADR-0011
title: Compose roadmap-impact reconciliation as one shared agent handoff module
status: proposed
date: "2026-11-14"
decision_scope: repository
visibility: public
owners: [egohygiene/aether]
issue: https://github.com/egohygiene/aether/issues/88
pull_request: null
related: [ADR-0007, ADR-0008, ADR-0009]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/aether]
affected_contracts: []
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/aether/issues/88
    description: Shared completion invariant, four dispositions, least-authority and organization signal requirements.
  - type: documentation
    url: https://github.com/egohygiene/hygiene/blob/d51043f1e4d2ddc22ef4534bd0d65c0053afcbda/docs/ecosystem/ORGANIZATION_ROADMAP.md
    description: Proposed canonical organization-roadmap ownership, stable initiative references and independent human intent.
exceptions: []
approval: null
---

# ADR-0011: Compose roadmap-impact reconciliation as one shared agent handoff module

## Context

Existing roadmap authoring, continuity and decision-impact guidance can preserve
strategy, but task completion does not consistently report whether roadmap truth
changed. Copying a new procedure into every role would make provider projections
drift. Updating every roadmap on every PR would produce noise and false intent.

## Proposed decision

Compose one draft `roadmap-impact` module and `reconcile-roadmap-impact` skill
through the canonical agent/projection system. Reuse `architecture-roadmap` and
`create-roadmap-document`, and emit a bounded `aether.roadmap-impact/v1` receipt:
updated, proposed, not-affected or blocked, with reason and evidence.

Keep receipt validation distinct from factual verification and authorization.
Read-only roles may propose implications but gain no tools. Any intent delta
needs independently verified human review. Organization impact is an inferred
typed signal to Hygiene's owner source, not a local strategy write. Public
signals cannot be exported from a private receipt.

## Alternatives and consequences

Per-role copied prose duplicates a shared concern; a mandatory roadmap edit
confuses maintenance with strategy; an automatic strategy engine cannot infer
human intent from activity. Shared static composition keeps semantics in one
place but cannot guarantee host discovery or enforcement.

The receipt is an Aether-owned output contract, not a new roadmap format or
first-party artifact kind. Its canonical catalog schema has a byte-identical
portable skill projection. Required script/runtime and unsupported host loading
remain explicit; default-bundle/release/install acceptance is independent.

## Validation and rollout

Synthetic receipts and adversarial role/source/intent/privacy controls exercise
all four branches. Provider tests build actual outputs, verify singular
idempotent managed blocks and unchanged tool ceilings, and retain consumer
prose. Deterministic golden assertions prove only their declared structure,
not agent judgment, authentic review or actual host installation.

Select reviewed immutable source/module versions, preview upgrades and preserve
authored instructions. Roll back the selected managed block/package without
erasing roadmap history or receipts. This proposal stays proposed/null approval
regardless of source integration and does not supersede prior decisions.
