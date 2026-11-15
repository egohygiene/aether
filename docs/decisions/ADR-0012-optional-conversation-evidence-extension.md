---
schema: egohygiene.architecture-decision/v1
id: ADR-0012
title: Keep optional conversation evidence separate from bounded current continuity
status: proposed
date: "2026-11-15"
decision_scope: repository
visibility: public
owners: [egohygiene/aether]
issue: https://github.com/egohygiene/aether/issues/102
pull_request: null
related: [ADR-0008, ADR-0011]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/aether]
affected_contracts: []
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/aether/issues/102
    description: Optional onboarding, meaningful conversational sequence, correction, concurrency and privacy requirements.
exceptions: []
approval: null
---

# ADR-0012: Keep optional conversation evidence separate from bounded current continuity

## Context

The current checkpoint is intentionally small and replaceable. It cannot retain
meaningful conversational intent and iteration without becoming a transcript or
losing current task clarity. Git/ADRs/work trackers already own implementation,
accepted decisions and mutable provider state; duplicating them creates drift.

## Proposed decision

Offer draft conversation-continuity0.1.0 with an authored onboarding route and
separate `aether.conversation-ledger/v1` output. Reuse the existing continuity
entry point only when a consumer opts in. Preserve fixed root continuity bounds,
current authority and existing bundle ownership. Add no new first-party artifact
kind, required repository file, knowledge database, host hook or rollout engine.

The ledger preserves attributed meaningful iterations and source links. Stable
identities make repeats idempotent; append corrections and deterministic union
preserve history/concurrent contributions. Identity collisions stop reconciliation.
Private inputs never become public merely by relabeling. An authorized privacy
redaction is a separately reviewed exception; the helper cannot rewrite history.

## Alternatives and consequences

Appending chat to CONTINUITY violates bounded current-state semantics; storing
every exchange in ADRs confuses tentative ideas with accepted decisions; requiring
Mindcap/Mindgarden delays minimal handoffs and adds service dependencies. The
small optional contract is useful without those services but still requires
source, privacy and authority review. Schema checks cannot authenticate decisions,
detect all sensitive prose or guarantee automatic recovery.

## Validation, adoption and exit

Synthetic native checks cover saved-file/Git recovery in an isolated process,
attribution, corrections, repeats, concurrent union/collisions, unsafe references,
private admission, lifecycle evidence, version/bounds and stored-content authority.
Golden assertions qualify only declared example structure, not model behavior.
The reference helper is read-only and performs no network or repository writes.

Consumers choose authored paths and a reviewed immutable selection. Existing
Hygiene applicability, Holon42, EgoLint55, Relay60 and Pace26 retain downstream
ownership. Preview upgrade/revert the selected package/instruction without
overwriting authored notes or deleting history. This record remains proposed with
null approval after integration and does not ratify organization adoption.
