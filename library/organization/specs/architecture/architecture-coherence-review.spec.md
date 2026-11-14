---
schema: aether.specification/v1
id: architecture-coherence-review
title: Architecture Coherence Review Contract
kind: specification
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-11-10
updated: 2026-11-10
domain: architecture
tags:
  - architecture-coherence
  - human-alignment
  - evidence
applies_to:
  - architecture-reviews
depends_on:
  - specfile
  - reflector
related:
  - auditor
  - review-architecture-coherence
supersedes: []
source_files:
  - architecture-coherence-review.spec.md
---

# Architecture Coherence Review Contract

## Purpose and status

Reconstruct an architecture from actual sources, explain it to its human
alignment authority, and preserve a portable assessment that can be ratified
later. This draft implements the record/procedure requested by
[Aether #87](https://github.com/egohygiene/aether/issues/87). Its existence,
implementation, merge, and execution do not approve an architecture or activate
the proposed Hygiene applicability policy.

Reflector's Human Alignment Anchor and synchronization boundary remain the
governance authority. This contract does not replace ADRs, create a mandatory
development gate, grant implementation authority, or turn CI, audit, lint,
release, or conformance success into architecture approval.

## Requirements

- **FR-001:** A review MUST identify its stable ID, scope, exact represented
  repository revisions, source files and revisions, execution limitations, and
  bounded reviewer/provider metadata. Repository, subsystem, and organization
  scopes are separate subjects; a repository ratification does not ratify an
  organization.
- **FR-002:** The plain-language explanation MUST describe the system, major
  pieces and owners, relationships/flows, boundary rationale, and overall
  assessment. Human understanding is the purpose; schema validity cannot
  establish that an explanation is useful or an architecture is good.
- **FR-003:** Structured assessment MUST preserve strengths, concerns,
  uncertainties, inherited assumptions, questions, confidence and evidence,
  credible alternatives, and an advisory recommended disposition. Wrong,
  risky, unverified, intentional tradeoff, and justified complexity MUST remain
  distinct categories. There is no universal score.
- **FR-004:** A consequential concern MUST reference at least one explicit
  alternative with tradeoffs and why it was not chosen. Material claims MUST
  cite canonical/implementation evidence rather than prior AI prose alone.
  Unverified concerns MAY have no source rather than fabricated evidence.
- **FR-005:** Complete assessment execution MUST account for all seventeen
  dimensions below, including explicit unknown/not-assessed outcomes. Complete
  execution does not mean complete evidence, conformance, human ratification,
  or permission to continue an independently paused Reflector cycle.
- **GOV-001:** Reviewer recommendation and execution MUST remain separate from
  human disposition. AI reviewers MUST emit `governance: null` by default and
  MUST NOT construct trusted human evidence, impersonate an authority, or
  infer consent from silence, continued work, a provider actor label, a merge,
  earlier AI prose, or a JSON `verified` claim.
- **GOV-002:** The optional `governance` subrecord MUST follow the exact pinned
  Hygiene owner contract. Applicability, human exception authority, material
  change, expiry, revision match, and effective state are evaluated there.
  Unknown applicability MUST remain unknown until an owner selects it.
- **GOV-003:** Human decisions MUST bind the exact completed assessment digest,
  ID, scope, and represented revisions. The importer MUST additionally require
  separately trusted human-source evidence. A URL, digest or well-formed human
  claim alone is not evidence of authentic human authorship or authority.
- **GOV-004:** Verified human disposition and present freshness MUST remain
  distinct. Routine source commits MUST NOT automatically invalidate a review.
  Material changes and explicit human invalidations require scoped evidence;
  unavailable/partial inventory cannot establish absence of material changes.
- **PRV-001:** Visibility MUST be explicit. A public assessment MUST NOT contain
  protected source identities or text, private paths, credentials, raw provider
  payloads, or unnecessary personal data. Simple sensitive-text rejection is a
  guard, not a complete secret detector or proof of public membership.
- **PRV-002:** Public consumers MUST independently authenticate the entire
  selected scope and every source repository against an owner-approved public
  admission set before reading identities, text, counts, or hashes. A serialized
  `visibility: public` assertion cannot provide that proof. An organization
  record with a protected scope/source cannot be projected as the same public
  review with the protected part silently removed.
- **VAL-001:** Duplicate JSON members, unknown members, unbounded arrays/text,
  unsupported versions, dangling evidence/alternative/component references,
  mismatched scope/revisions, and ambiguous source paths/URLs MUST be rejected.
  Public diagnostics MUST contain bounded error codes rather than raw payloads.

## Assessment dimensions

The fixed dimension identities are `purpose`, `responsibility-boundaries`,
`source-of-truth`, `dependency-direction`, `cohesion`, `duplicate-ownership`,
`speculative-abstractions`, `missing-ownership`, `coupling`,
`documentation-divergence`, `decision-consistency`, `replaceability`,
`operational-plausibility`, `security-privacy-trust`, `maintainability`,
`justified-complexity`, and `simplest-credible-alternative`.

Each dimension has `coherent`, `concern`, `unknown`, or `not-assessed` status,
an explanation, source IDs, and high/medium/low/unknown confidence. Coherence
alone does not mean the tradeoff is desirable. Prior assumptions, missing
owners, circular dependencies, unjustified abstractions and the simplest
credible alternative deserve explicit challenge. An independent challenger is
optional; its absence is recorded rather than simulated.

## Record and immutable subject

The machine record is `egohygiene.architecture-coherence-review/v1`, contract
version `1.0.0-alpha.1`. Its closed schema is
`catalog/schemas/aether.architecture-coherence-review.v1.schema.json`; the
standalone stdlib helper is distributed with `review-architecture-coherence`.
All schema references are local. Semantic validation adds source/revision,
reference, canonical digest, and governance bindings beyond JSON Schema.

Execution states are complete, partial, blocked and failed. Incomplete reviews
retain limitations, questions and a defer recommendation. They have no
completed-at timestamp and cannot receive a completed-review human decision.
Sources include their repository, full 40-character revision, relative path,
kind, origin, visibility and optional HTTPS URL. GitHub source links bind the
exact repository/blob/revision/path. These references establish what was
declared consumed; the validator does not fetch or independently attest bytes.

`review_subject` returns ID, `assessment_sha256`, scope, represented revisions
and completed-at. The digest is SHA256 over UTF-8 JSON of **all top-level
members except governance**, with sorted object keys, compact comma/colon
separators, `ensure_ascii=False`, `allow_nan=False`, and no trailing newline.
Array order and every assessment byte/value remain significant. This prevents
the circularity of including the ratification record in its own subject.

Human governance is attached in a new artifact/revision; the immutable
assessment subject stays identical and prior captures remain available.
Correcting an assessment produces a new subject and requires a new human
decision. Never rewrite a historical assessment to make old approval fit.

## Human evidence and material staleness

The pinned Hygiene helper validates governance and evaluates its states.
Its `TrustedHumanEvidence` is a separate immutable in-memory context, with an
exact statement digest and private operational capture digest. It has no JSON
decoder. Only a trusted adapter/operator that independently verified the
human source, authority and exact statement may construct it. The owner helper
does not authenticate a GitHub person, retrieve a URL, or establish authority.
The context type makes the trust boundary explicit; access to Python code is
not a cryptographic security boundary.

The human statement binds the full governance claim, review reference, scope
and revisions. `import_human_decision` returns a new record only when this
separate typed evidence matches. A raw provider claim remains unverified even
when its fields resemble a real approval. No trusted evidence is created by
this implementation or by the review skill.

Material-change inputs are supplied separately at evaluation time, with their
scope, review ID, kind, time and evidence. Examples include accepted ADR
topology changes, ownership/dependency/persistence/trust boundaries, runtime
replacement and explicit human invalidation. Ordinary commits retain a
separate revision difference and do not automatically assert materiality.
Unknown change inventory yields unknown freshness; a historical verified
human disposition is still visible without claiming current ratification.

## Operating workflow

1. Select the authorized scope, exact source revisions, human alignment
   authority, output convention, exclusions and review capacity.
2. Read canonical architecture/ADRs/specifications and relevant implementation,
   runtime, dependency and deployment evidence. Inventory missing sources.
3. Reconstruct pieces, responsibilities and flows before evaluating them.
4. Challenge inherited assumptions and consequential choices; explain
   strengths, concerns, credible alternatives and unresolved questions.
5. Record the assessment, limitations and advisory recommendation. Validate
   structure and bindings without executing repository code by default.
6. Present the explanation and subject digest to the actual human authority.
   Ratification is a separate human action. Without it, retain the unreviewed
   or unverified posture and continue only already authorized work.
7. A trusted importer may later attach authentic human governance. Future
   evaluations consume separate material-change inventories and preserve the
   historical decision and assessment.

## Implementation and validation plan

The specification artifact is version 1.0.0 with draft lifecycle; the independent
machine record retains contract version `1.0.0-alpha.1`.

This slice supplies the draft specification, closed schema, portable helper,
review skill and human-readable template. Hygiene owns proposed applicability
and governance policy; Observatory owns normalized query/projection; Relay owns
delivery/rendering; Reflector owns campaign orchestration and human-alignment
continuation. No provider adapter or authentication service is added here.

Static source/schema/syntax review is permitted for the current batch. User
instructions defer behavioral tests, skill evaluations, runtime/source
execution, builds, native acceptance and CI. Catalog/dist regeneration and the
shared continuity/decision reconciliation belong to the integrator. Their
absence is pending qualification, not a pass or acceptance.

## Risks, acceptance and open questions

The contract can enforce bounds and bindings, not architectural judgment,
human understanding, source authenticity or absence of secrets. Callers must
authenticate public admission and trusted human captures outside these pure
helpers. No current repository or organization is ratified by this change.

Source acceptance requires the portable artifact and skill, immutable digest,
explicit unknowns, separate recommendation/human state, and human-only import
boundary. Runtime negative cases, actual human UX, owner policy selection,
provider verification/retention and first real review remain unqualified.
Future organization sanity sweeps should select an explicit public roster and
exact revisions, preserve per-repository and organization authority separately,
and produce review candidates without fabricating ratification.

Related: `reflector`, `auditor`, Hygiene #59, Observatory #21, Relay #76 and
Reflector #258. These references do not close those issues or resolve their
human acceptance requirements.
