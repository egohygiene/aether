---
schema: egohygiene.architecture-decision/v1
id: ADR-0008
title: Separate portable review evidence from policy and human authority
status: proposed
date: "2026-11-10"
decision_scope: repository
visibility: public
owners: [egohygiene/aether]
issue: https://github.com/egohygiene/aether/issues/87
pull_request: null
related: [ADR-0002]
supersedes: []
superseded_by: []
affected_repositories:
  - egohygiene/aether
  - egohygiene/hygiene
  - egohygiene/observatory
  - egohygiene/reflector
  - egohygiene/relay
affected_contracts:
  - egohygiene.architecture-coherence-review/v1
  - egohygiene.architecture-coherence-governance/v1
  - egohygiene.architecture-coherence-material-change/v1
implementation_status: in_progress
evidence:
  - type: issue
    url: https://github.com/egohygiene/aether/issues/86
    description: Composable audit procedure and portable profile/report scope.
  - type: issue
    url: https://github.com/egohygiene/aether/issues/87
    description: Architecture assessment and explicit human ratification boundary.
  - type: issue
    url: https://github.com/egohygiene/hygiene/issues/59
    description: Separate proposed applicability, human authority, and material freshness policy.
  - type: documentation
    url: https://github.com/egohygiene/aether/blob/0071f7d751c4916e6b16460451751aa00fb1d365/library/organization/specs/quality/auditor.spec.md
    description: Existing approved auditor 2.0.0 foundation retained unchanged.
exceptions: []
approval: null
extensions: {}
---

# ADR-0008: Separate portable review evidence from policy and human authority

## Context

Audit and architecture review need portable, exact-source artifacts that
downstream query, rendering and campaign tools can consume. Mixing assessment,
policy and approval would let a successful command, source-only finding, AI
recommendation, provider actor label or merge appear to ratify an architecture.
The approved `auditor` 2.0.0 and Reflector human-alignment boundary already
separate observation from execution and human continuation authority.

This new proposal records the machine-interface and trust-boundary choice. It
does not amend the approved auditor specification, accept the draft contracts,
select applicability, change a human synchronization gate, or ratify a reviewed
repository/organization. The user authorized source implementation; actual
policy and architecture disposition remain separate human actions.

## Decision

Propose closed, versioned Aether assessment artifacts and pure owner helpers:
`aether.audit-profile-registry/v1`, `aether.repository-audit-report/v1` and
`egohygiene.architecture-coherence-review/v1`. Preserve plain-language reports,
exact source revisions, evidence, uncertainty, findings/strengths/alternatives,
profile attribution, incomplete execution and reviewer recommendations.

Keep Hygiene governance and applicability semantics in its exact pinned
proposed contract. Architecture human decisions bind an immutable assessment
digest that excludes governance, plus ID/scope/represented revisions. A separate
typed trusted-evidence context must bind authentic human provenance before a
decision is effective; review/provider JSON cannot create that context. The
pure helpers perform no identity authentication, source fetch or provider write.
No real trusted human context or ratification is created in this batch.

Observatory may normalize admitted public owner artifacts; Relay may deliver
and render them; Reflector may orchestrate explicitly scoped read-only reviews.
These consumers do not acquire policy or approval authority. Unknown
applicability, missing evidence and unknown material-change inventories remain
visible rather than becoming exemptions, successes or current ratification.

## Alternatives considered and rejected

- Infer approval from AI recommendations, merge or continued implementation:
  rejected because those events do not prove human architecture acceptance.
- Reimplement governance and profile semantics in each renderer/campaign:
  rejected because divergent local rules would create competing authorities.
- Extend the approved auditor specification in place: keep a separately draft
  profile/data specification so source implementation does not rewrite its
  existing human lifecycle.
- Hash governance inside the human decision's assessment subject: rejected
  because the decision would become part of its own circular digest.

These are the alternatives evaluated for this proposal; no claim of historical
human consideration or exhaustive design evaluation is made.

## Consequences and tradeoffs

The resulting machine contracts are reusable and reviewable, while owner
judgment, human trust and publication remain separate. Exact source/hash pins,
schema mirrors and process-module reuse add compatibility maintenance. Typed
evidence makes the trust boundary explicit but is not a cryptographic boundary
against privileged code. Public admission and authentic human source capture
must be verified externally; schema validity cannot establish either.

Existing auditor 2.0.0 bytes and staged historical evidence remain unchanged.
New specifications remain draft; the coherence skill remains draft,
and audit skill/agent remain draft. Generating distributions/catalog metadata
does not release, install, qualify, promote or ratify them.

## Implementation and evidence links

Canonical sources are the [audit data specification](../../library/organization/specs/quality/repository-audit-data.spec.md),
[coherence specification](../../library/organization/specs/architecture/architecture-coherence-review.spec.md),
[audit procedure](../../library/organization/skills/quality/audit-repository/SKILL.md),
and [coherence procedure](../../library/organization/skills/architecture/review-architecture-coherence/SKILL.md).
The exact Hygiene mirror/lock remains at source revision
`d11580e9a9c5d78b9a5d21474deaa612712a0fb9`. These sources establish authored
interfaces, not executed review correctness or human authority.

Static parsing/schema/reference/hash review and authorized deterministic
catalog/distribution generation are the current implementation checks.
Behavioral tests, evals, builds beyond artifact generation, native/provider
execution, host qualification and CI are deferred by the user. Implementation
is therefore in progress; no verification or approval state is assigned.

## Replacement or exit strategy

Consumers retain immutable source pins and can opt out or restore the preceding
compatible profile. A contract change uses a reviewed version/pin update,
retains historical records and never rewrites an old assessment to make its
human approval fit. A future policy replacement requires its owner process.
Do not delete preserved staged evidence or mutate immutable release artifacts.

## Follow-up work

Complete owner/consumer static integration, then separately qualify negative
paths, host/runtime behavior and real source capture when execution is
authorized. Resolve actual human policy/application and architecture decisions
with the named authority. Preserve partial/unknown states during later public
repository and organization campaigns. Legacy inline ADR migration and local
policy inheritance remain separate; this proposal does not backfill approval.
