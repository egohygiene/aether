---
name: create-purpose-document
description: Creates or updates PURPOSE.md from repository evidence. Use when a project needs to define, repair, or review why it exists and whom it serves.
license: MIT
metadata:
  aether-version: "1.1.0"
  aether-status: "draft"
  aether-spec-id: "architecture-purpose"
  aether-scope: "organization"
  aether-domain: "architecture"
  aether-owners: "egohygiene"
  aether-created: "2026-08-01"
  aether-updated: "2026-09-08"
---

# Create Purpose Document

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

For repository-scoped work, compose `maintain-repository-continuity` in
**Resume** mode before selecting work. After an authorized repository change
passes domain validation, compose **Refresh** and **Verify** immediately before
presenting the pull request, and include the reconciled root `CONTINUITY.md` in
the same change. A policy-permitted no-change or exemption result must be
documented instead of fabricating an edit.

- **Contribute:** Purpose, audience, outcomes, non-goals, validation, and unresolved stakeholder input
- **Never claim:** That a drafted purpose has stakeholder acceptance without evidence

## Purpose

Create or update `PURPOSE.md` in conformance with `architecture-purpose`.

Primary question:

> Why does this exist, for whom, and what enduring value should it create?

## Use This Skill When

- the canonical document does not exist
- an existing document is incomplete or inconsistent
- upstream identity has changed
- repository architecture is being established or repaired

## Required Inputs

- founding intent
- organizational mission
- stakeholder and beneficiary evidence
- domain research
- existing identity material
- historical project goals

Missing evidence must be recorded rather than invented.

## Workflow

1. Gather evidence about founding intent and beneficiary needs.
2. Separate enduring intent from implementation and current features.
3. Identify the core need.
4. Identify beneficiaries without overgeneralizing.
5. Describe enduring value in outcome-oriented language.
6. Define what falls outside the purpose.
7. Test durability across technology and delivery changes.
8. Review downstream implications.

## Output Contract

Produce:

- `PURPOSE.md`
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
`architecture-purpose`.

## Completion Criteria

- [ ] The governing specification is identified.
- [ ] Required upstream evidence has been read.
- [ ] The document answers its primary identity question.
- [ ] Non-responsibilities are respected.
- [ ] Assumptions and open questions are visible.
- [ ] Structural, semantic, relationship, and evidence checks pass.
- [ ] Downstream review needs are reported.
