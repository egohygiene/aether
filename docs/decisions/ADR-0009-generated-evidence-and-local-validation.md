---
schema: egohygiene.architecture-decision/v1
id: ADR-0009
title: Clarify tracked generated evidence and repository-local validation
status: proposed
date: "2026-11-13"
decision_scope: repository
visibility: public
owners: [egohygiene/aether]
issue: https://github.com/egohygiene/aether/issues/114
pull_request: null
related: [ADR-0001, ADR-0002, ADR-0006]
supersedes: []
superseded_by: []
affected_repositories: [egohygiene/aether, egohygiene/relay, egohygiene/realm]
affected_contracts: []
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/aether/issues/114
    description: Concrete active-navigation and historical-authority conflicts.
  - type: documentation
    url: https://github.com/egohygiene/aether/blob/2e69182e8bc820add3c19d35470930a917d69dc5/DECISIONS.md
    description: Preserved legacy ADR-0002 and ADR-0006 rules; no new human disposition inferred.
  - type: documentation
    url: https://github.com/egohygiene/aether/blob/2e69182e8bc820add3c19d35470930a917d69dc5/.github/workflows/pr-validation.yml
    description: Existing repository-local validation/build/consumer caller.
  - type: documentation
    url: https://github.com/egohygiene/aether/blob/2e69182e8bc820add3c19d35470930a917d69dc5/.egohygiene/release.json
    description: Existing repository-owned release declaration and manual handoff.
exceptions: []
approval: null
extensions: {}
---

# ADR-0009: Clarify tracked generated evidence and repository-local validation

## Context

Legacy ADR-0006 says generated distributions are release-only and untracked;
merged main `2e69182` instead tracks 365 files under `dist/` and verifies them
with deterministic builders and drift checks. Legacy ADR-0002 and the previous
Copilot instruction ban local CI/release implementation, while the repository
already contains its own validation/release callers and release declaration.
Those are observable conflicts, not proof that the older decisions were
superseded or that a later merge supplied human architecture approval.

Canonical artifact content, governed catalog contracts, generated output and
consumer deployment are already distinct. Reusable execution belongs to Relay,
environment provisioning to Realm, policy/applicability to Hygiene and fleet
convergence to Pace. The proposal must preserve those boundaries.

## Decision

Propose a narrow clarification: retain reproducible generated output in Git as
reviewable evidence when its source and deterministic generator are explicit,
and permit Aether-owned thin validation/release callers over Aether artifacts.
Keep reusable CI execution in Relay and environment provisioning in Realm.
Generated files are never hand-edited and never become canonical artifact
content; tracked output is not proof of stable lifecycle, eligible release,
consumer compatibility or actual publication.

This record remains proposed with null approval. It does not change ADR-0002 or
ADR-0006, add effective supersession links, select a new distribution channel,
or authorize a release. Human review must decide whether to accept this
clarification, require a successor, or restore the older implementation policy.

## Alternatives considered and rejected

These are alternatives evaluated for this new proposal, not reconstructed
historical rationale:

- Remove tracked outputs and all local callers immediately: this would change
  consumer/review inputs and discard useful checked-in evidence before the
  authority conflict is resolved. No such migration is authorized here.
- Treat later merges as implicit supersession: rejected because implementation
  and merge do not establish human disposition.
- Copy Relay/Realm implementations into Aether: rejected because a local caller
  does not justify moving reusable execution or provisioning ownership.

## Consequences and tradeoffs

Tracked generated output increases diff volume and must remain reproducible.
Source-field drift, missing generation and unexpected owned outputs must fail
checks. Draft artifact content can exist in source-derived evidence without
being eligible for a published payload. Preview adapters and real consumer
acceptance remain separate from deterministic unit tests.

Until human disposition, active docs identify both observed source and the
unresolved historical rule. They must not describe this proposal as accepted
policy or use it to waive existing release/publication controls.

## Implementation and evidence links

The evidence above identifies the current repository implementation. The
November 14, 2026 UTC source inventory at that main has 35 specifications,
38 skills, 10 agents, one instruction module,365 tracked generated files and 734
tracked staged files. These counts do not establish artifact maturity.
Existing build/check and consumer gates are implementation evidence only;
issue #38 retains actual release/consumer/provenance/payload acceptance.

## Replacement or exit strategy

If approved, record explicit human disposition and any effective successor
lineage under the selected Hygiene policy before migrating historical authority.
If rejected, propose a separate reviewed migration that inventories affected
consumers, preserves immutable releases and source evidence, and validates a
recoverable alternative. Never delete generated or staged evidence as an
incidental documentation cleanup.

## Follow-up work

- [Issue114](https://github.com/egohygiene/aether/issues/114) owns this factual
  navigation repair and the proposal's review handoff.
- [Issue38](https://github.com/egohygiene/aether/issues/38) owns current release
  workflow, payload, provenance and actual consumer qualification.
- [Issue85](https://github.com/egohygiene/aether/issues/85) owns the broader
  historical ADR evidence/migration work; it is not completed here.
