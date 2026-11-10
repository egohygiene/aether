---
name: review-architecture-coherence
description: Reconstructs a repository, subsystem, or organization architecture from exact source revisions and prepares a portable evidence-based explanation and coherence assessment for its human alignment authority. Use for architecture drift, ownership or dependency concerns, consequential design review, or an explicit sanity review; never use it to imply AI ratification or authorize implementation.
license: MIT
metadata:
  aether-version: "1.0.0-alpha.1"
  aether-status: "experimental"
  aether-spec-id: "architecture-coherence-review"
  aether-scope: "organization"
  aether-domain: "architecture"
  aether-owners: "egohygiene"
  aether-created: "2026-11-10"
  aether-updated: "2026-11-10"
  aether-distribution-resources:
    - source: "catalog/schemas/aether.architecture-coherence-review.v1.schema.json"
      destination: "references/aether.architecture-coherence-review.v1.schema.json"
---

# Review Architecture Coherence

<!-- aether-continuity-disposition: reader -->

Read local instructions and existing continuity in Resume mode. This procedure
is read-only by default: inspect existing sources and return a review candidate.
Write an artifact only to an authorized output path. Review permission does not
authorize implementation, source execution, provider writes, issue creation,
publication, or changing governance. A separately authorized writer can refresh
continuity; do not manufacture a checkpoint edit during a read-only review.

## Inputs

- repository/subsystem/organization scope and exclusions;
- exact represented repository revisions and public admission, if publishing;
- canonical architecture, purpose, owner boundaries, ADRs and specifications;
- relevant implementation, dependency, runtime/dataflow and deployment evidence;
- human alignment authority and the actual review request, if known;
- output location/convention, visibility, time/review capacity and known gaps.

Missing authority, applicability, evidence or revision stays unknown. An absent
policy selection does not become a requirement or exemption. Private material
does not become public because a review calls it public.

## Procedure

1. Read `architecture-coherence-review` and Reflector's human alignment and
   synchronization rules. Resolve the exact requested scope before examining
   sources. A repository review does not ratify an organization architecture.
2. Read canonical sources and selected implementation at the represented
   revisions. Inventory what was actually inspected. Prior AI explanations are
   context; they are not sufficient evidence for an architectural conclusion.
3. Reconstruct the architecture in plain language: what the system does, its
   major pieces and owners, how control/data/trust/deployment flows, and why its
   boundaries exist. Record components and relationships with source IDs.
4. Assess all seventeen owner dimensions. Preserve unknown/not-assessed and
   confidence; do not infer goodness from coherence, CI, lint, conformance,
   audit results or release success.
5. Explain strengths and concerns. Distinguish wrong, risky, unverified,
   intentional tradeoff and justified complexity. Expose inherited assumptions.
   For each consequential concern, describe a credible alternative, its
   tradeoffs, and why the current choice may still be justified. Ask whether a
   simpler solution suffices. An optional independent challenge may help;
   record when none occurred and never simulate a second reviewer.
6. Prepare the human explanation using
   [REVIEW.template.md](templates/REVIEW.template.md) and the closed machine
   record. Recommend ratify, ratify-with-notes, revise, reject or defer as an
   **advisory reviewer recommendation**. Use partial/blocked/failed with visible
   limitations when incomplete; do not fill gaps with invented sources.
7. Emit `governance: null`. Validate the record with the portable helper and
   report what actually ran. The helper never fetches sources or runs reviewed
   code. Read [the contract/API guide](references/contract-and-human-boundary.md)
   for exact digest and separately trusted human evidence semantics.
8. Present the explanation, exact scope/revisions, assessment digest,
   uncertainties and questions to the real human alignment authority. Stop at
   any independently applicable Reflector synchronization boundary. If no
   ratification is supplied, report an unreviewed assessment and a safe handoff;
   do not interpret silence or continued implementation as acceptance.

## Human boundary

The human may ratify, ratify with notes, require revision, reject or defer the
reviewed architecture at its exact subject. That is an intentional basis for
further work, not proof of optimality, security, conformance, correctness or
permanent validity. Applicability exceptions belong to the Hygiene policy.

Never populate a human decision, construct `TrustedHumanEvidence`, impersonate
the human, or mark a provider claim verified. A later privileged adapter must
independently verify authentic human provenance/authority and import the exact
bound statement. A URL or a JSON actor field cannot supply that authority.

## Completion and follow-up

Return the explanation and machine artifact/candidate, subject digest, exact
sources and visibility, execution status, missing evidence, reviewer
recommendation, open human questions, checks actually run and remaining work.
Preserve earlier artifacts when correcting an assessment. Future material
changes are separate observations, not edits that rewrite an old approval.
Do not change architecture, canonical policy or enforcement as part of review.

This is first-party Aether source authored for #87, licensed MIT. Its status is
experimental; artifact implementation is not owner policy selection, skill
adoption or real human ratification. Behavioral evaluations remain separate
qualification work when execution is authorized.
