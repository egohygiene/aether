---
name: create-manifesto-document
description: Creates or updates MANIFESTO.md from repository evidence and values. Use when a project needs to define, repair, or review its public statement of values, commitments, and beliefs.
license: MIT
metadata:
  aether-version: "1.1.0"
  aether-status: "draft"
  aether-spec-id: "architecture-manifesto"
  aether-scope: "organization"
  aether-domain: "architecture"
  aether-owners: "egohygiene"
  aether-created: "2026-08-01"
  aether-updated: "2026-09-08"
---

# Create Manifesto Document

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

For repository-scoped work, compose `maintain-repository-continuity` in
**Resume** mode before selecting work. After an authorized repository change
passes domain validation, compose **Refresh** and **Verify** immediately before
presenting the pull request, and include the reconciled root `CONTINUITY.md` in
the same change. A policy-permitted no-change or exemption result must be
documented instead of fabricating an edit.

- **Contribute:** Cited values, commitments, tensions, validation, and unresolved stakeholder review
- **Never claim:** That drafted values or commitments have organization approval without evidence

## Purpose

Create or update `MANIFESTO.md` in conformance with `architecture-manifesto`.

Primary question:

> What do we believe strongly enough to state publicly and stand behind?

## Use This Skill When

- the canonical document does not exist
- an existing document is incomplete or inconsistent
- upstream identity has changed
- repository architecture is being established or repaired

## Required Inputs

- PURPOSE.md
- VISION.md
- PRINCIPLES.md
- PILLARS.md
- organizational values
- historical language and culture
- community context
- existing public commitments

Missing evidence must be recorded rather than invented.

## Workflow

1. Read every upstream identity document.
2. Identify convictions repeated across them.
3. Distinguish beliefs from features and policies.
4. Express beliefs in human language.
5. Test commitments for credibility.
6. Remove generic or inflated marketing language.
7. Validate internal consistency.
8. Review tone, accessibility, and longevity.

## Output Contract

Produce:

- `MANIFESTO.md`
- governing specification identifier and version
- assumptions and unresolved questions
- validation results
- downstream review recommendations

## Constraints

- Preserve canonical terminology.
- Separate evidence from inference.
- Do not fabricate intent.
- Do not introduce implementation details outside the specification.
- Do not silently resolve contradictions.
- Do not claim completion when upstream artifacts are missing.

## Validation

Use `references/validation-checklist.md` and the acceptance criteria in
`architecture-manifesto`.

## Completion Criteria

- [ ] The governing specification is identified.
- [ ] Required upstream evidence has been read.
- [ ] The document answers its primary identity question.
- [ ] Non-responsibilities are respected.
- [ ] Assumptions and open questions are visible.
- [ ] Structural, semantic, relationship, and evidence checks pass.
- [ ] Downstream review needs are reported.
