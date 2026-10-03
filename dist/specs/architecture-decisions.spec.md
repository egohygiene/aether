---
schema: aether.specification/v1
id: architecture-decisions
title: Decisions Architecture Document Specification
kind: specification
version: 3.0.0
status: draft
owners:
  - egohygiene
created: 2026-07-18
updated: 2026-10-03
domain: architecture
tags:
  - architecture
  - governance
  - decisions
  - adr
  - institutional-memory
  - traceability
applies_to:
  - architecture-documents
  - decision-log-documents
depends_on:
  - architecture-document
  - architecture-principles
  - architecture-epistemology
  - architecture-foundations
  - architecture-system
  - architecture-architecture
related:
  - architecture-ai-constitution
  - architecture-methodology
  - architecture-roadmap
  - create-decisions-document
supersedes: []
---

# Decisions Architecture Document Specification

## Introduction

This draft Aether specification defines an authoring workflow for repository-owned
ADRs. It consumes accepted Hygiene policy v1.1.0 at
`c589587395750cd1c79c6fa0bef010189c547249`; it does not redefine policy, schemas or
human authority. The exact selection and approval evidence are in the portable
[authoring package](../../../skills/architecture/create-decisions-document/references/policy-selection.json).

Version 3 changes the earlier accepted-only, inline-log output contract to proposed
record authoring under Hygiene's canonical index and record layout. Existing logs
are migration inputs and remain preserved until an authorized migration. Aether's
specification and skill retain draft lifecycle; independent proposed contracts do
not inherit the ADR policy's acceptance.

## 1. Purpose and Scope

Support historical reconstruction, new proposals, corrections/later outcomes,
references to governing decisions, proposed supersession and justified no-ADR
results. Record consequential choices and evidence needed to understand them.
Brainstorming, meeting archives, issue backlogs, routine edits and automatic
historical rationale generation are outside scope.

## 2. Conceptual Model

A record links context, a proposed or human-disposed choice, rationale,
alternatives, consequences, implementation/verification evidence and lineage.
Disposition, implementation and verification are independent. A merge, release
or passing test cannot supply rationale or human acceptance.

## 3. Decision Significance

Apply the pinned Hygiene policy's significance test before implementation and
again before issue completion/PR handoff. Reuse an existing governing record
when the actual diff implements its design. Routine work needs no duplicate ADR.

## 4. Responsibilities

Aether owns the reusable authoring procedure, templates, evaluations and concise
managed skill-routing guidance. Each repository owns its ADRs, index, evidence
and approved local extensions. `docs/decisions/README.md` is the canonical index;
`DECISIONS.md` is compatibility navigation after reviewed migration.

## 5. Non-Responsibilities

Hygiene owns policy and schemas; EgoLint validation semantics; Holon scaffolding
and generated ownership; Relay execution/collection; Pace fleet adoption;
Observatory normalized projections. This specification does not accept decisions,
implement a validator, publish pages, overwrite consumer instructions or move any
of those responsibilities into Aether.

## 6. Definitions

- **Record:** source-owned ADR with identity, evidence and lifecycle metadata.
- **Disposition:** decision state under the owner contract; non-proposed states
  require human authority. Agents author new records only as proposed.
- **Implementation:** separately evidenced delivery, including unknown migration
  history where permitted by policy.
- **Reconstruction:** a later evidence inventory and draft, not recovered certainty.
- **Correction/outcome:** a dated sourced addition that preserves original meaning.

## 7. Decision Status Model

Consume the policy's `proposed`, `accepted`, `rejected`, `deprecated` and
`superseded` states and separate implementation vocabulary. Do not invent
`historical`, `withdrawn` or `unresolved` decision statuses. Unresolved claims
belong in the migration map or notes. Preserve existing human disposition;
automated authors never assign non-proposed status. Missing approval permits a
proposed draft but blocks promotion.

## 8. Requirements

- **REQ-001:** Inspect scoped instructions, pinned ecosystem context, local policy,
  existing records and relevant organization decisions before writing.
- **REQ-002:** Classify create/update/supersede/reference/ADR not required before
  implementation and repeat against the final diff at handoff.
- **REQ-003:** Use `egohygiene.architecture-decision/v1` and the exact selected policy;
  new records have unused `ADR-NNN` IDs, proposed status and null approval.
- **REQ-004:** Separate rationale, disposition, implementation and verification.
- **REQ-005:** Reconstruct from reachable Git/tags, merged PRs, issues, releases,
  architecture docs and existing records; group by consequential choice.
- **REQ-006:** Preserve contemporaneous reasoning, source links, original IDs,
  files, provenance/blame references and uncertainty.
- **REQ-007:** Distinguish reconstruction date from any proven historical date;
  never backdate a new preference or invent unsupported metadata fields.
- **REQ-008:** Preserve legacy index/body/history through a previewed migration map;
  collisions and uncertain canonical identities require human resolution.
- **REQ-009:** Keep the seven owner-required sections and all required metadata;
  only policy-supported extensions may add metadata.
- **REQ-010:** New superseding proposals preserve the predecessor; effective status
  and reciprocal lineage change only with human disposition under the policy.
- **REQ-011:** Validate with supported pinned owner tools; preserve incomplete,
  unavailable and differing validator results.
- **REQ-012:** PR handoff cites a governing/new/updated ADR, or says `ADR not required`
  with a concise reason; missing acceptance is never hidden by delivery evidence.
- **REQ-013:** Generated guidance preserves consumer prose, role permissions and
  other modules; adding instructions does not establish universal enforcement.

## 9. Constraints

Do not invent rationale, alternatives, dates, approvals or source links. Do not
renumber or delete historical records, overwrite an accepted choice through an
edit, or treat generated views as canonical evidence. Private sources and links
stay within authorized boundaries. Skill instructions never expand tool, merge,
publication or human lifecycle authority.

## 10. Authoring Contract

Inputs: immutable source/evidence inventory, scoped instructions and role,
policy reference, known record IDs/index, governing ADRs, intended change and
available owner-validator versions.

Outputs depend on the operation: a proposed ADR and index entry, a dated
correction/outcome, a proposed replacement, a governing reference, a justified
no-ADR result, or an unresolved migration/evidence report. Include the selected
pins, validation results, source gaps and human-owned next action. A valid draft
need not be accepted to complete authoring.

## 11. Storage and Organization

New records use `docs/decisions/ADR-NNN-short-slug.md`; one canonical index row per
record contains ID, title, status, date and relative link. Keep terminal records.
The local `policy-reference.json` inherits by exact version/full Hygiene commit;
Hygiene itself publishes policy rather than inheriting itself.

Preserve inline logs until reviewed extraction preserves records and inbound
links; then `DECISIONS.md` points to the canonical index without duplicate
rationale. Historical prefixes/widths require the policy's exception process.

## 12. AI Authoring Strategy

Use `create-decisions-document` v2.0.0. Start with evidence and an explicit mode,
preview affected identity/lineage, then author only within the current role's
permissions. Missing skill/validator/history produces explicit unavailable or
evidence-gap results. Static instructions cannot guarantee every agent performs
the checkpoint. Model/host execution evidence remains separate from deterministic
evaluation of checked-in cases and templates.

## 13. Dependency Model

The accepted Hygiene policy is upstream authority. Existing architecture documents
supply local context. Aether's skill/guidance consume the policy, owner validators
check authored records, and downstream systems consume source-owned decisions.
Holon and validator compatibility must be verified before materialization; do not
silently replace generated policy references or promote unrelated proposed pins.

## 14. Validation and Quality Criteria

Validate package metadata/links/evals, canonical/generated parity, managed-block
preservation, template compatibility with pinned owner schemas and native
consumer behavior when available. Validate IDs, indexes, lifecycle and lineage
through owner tools. Report historical versus reconstruction dates, source gaps,
missing authority, incompatible materializers and unavailable host evidence.

## 15. Acceptance Criteria

- [ ] Skill/spec/templates/hooks agree on canonical location and proposed authoring.
- [ ] Exact policy and authority evidence are referenced; draft artifacts stay draft.
- [ ] History, uncertainty, identity and lineage survive reconstruction/migration.
- [ ] Cases cover supported history, missing rationale/authority, proposal,
  supersession, routine implementation, correction and legacy migration.
- [ ] Guidance runs at both checkpoints and preserves consumer instructions.
- [ ] Handoffs cite an ADR or justified no-ADR; adoption/upgrade/rollback are explicit.
- [ ] Repository checks and deterministic evals pass with limitations labeled.

## 16. Examples

- A new persistent format choice produces a proposed ADR without invented approval.
- A merged storage migration can prove implementation while its rationale and
  human disposition remain unknown in a newly reconstructed proposed record.
- A replacement proposal names its predecessor but preserves the accepted record
  while human review is pending.
- A local parser fix implementing the accepted input contract yields a reference
  or `ADR not required`, with no duplicate record.

## 17. Rationale and Context

Using the approved owner contract resolves disagreement between the old
accepted-only skill and the proposed-record hook. Canonical records preserve
why choices were made; generated views and issue execution remain downstream.

## 18. Related Artifacts

- `architecture-document`, `architecture-principles`, `architecture-epistemology`
- `architecture-foundations`, `architecture-system`, `architecture-architecture`
- `architecture-ai-constitution`, `architecture-methodology`, `architecture-roadmap`
- `architecture-authoring`, `create-decisions-document`
