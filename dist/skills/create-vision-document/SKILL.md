---
name: create-vision-document
description: Creates or updates VISION.md from repository evidence and identity context. Use when a project needs to define, repair, or review the aspirational future state it is working toward.
license: MIT
metadata:
  aether-version: "1.1.0"
  aether-status: "draft"
  aether-spec-id: "architecture-vision"
  aether-scope: "organization"
  aether-domain: "architecture"
  aether-owners: "egohygiene"
  aether-created: "2026-08-01"
  aether-updated: "2026-09-08"
---

# Create Vision Document

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

For repository-scoped work, compose `maintain-repository-continuity` in
**Resume** mode before selecting work. After an authorized repository change
passes domain validation, compose **Refresh** and **Verify** immediately before
presenting the pull request, and include the reconciled root `CONTINUITY.md` in
the same change. A policy-permitted no-change or exemption result must be
documented instead of fabricating an edit.

- **Contribute:** Target state, horizons, supporting evidence, validation, and unresolved stakeholder review
- **Never claim:** That an aspirational target is current state or approved commitment without evidence

## Purpose

Create or update `VISION.md` in conformance with `architecture-vision`.

Primary question:

> What future should become more possible when the purpose is fulfilled?

## Use This Skill When

- the canonical document does not exist
- an existing document is incomplete or inconsistent
- upstream identity has changed
- repository architecture is being established or repaired

## Required Inputs

- PURPOSE.md
- stakeholder aspirations
- domain research
- long-term opportunities and risks
- organizational mission
- existing strategic material

Missing evidence must be recorded rather than invented.

## Workflow

1. Read and preserve purpose.
2. Describe the future condition rather than current activities.
3. Identify the enduring impact sought.
4. Remove implementation and scheduling language.
5. Test ambition and credibility.
6. Define what the vision does not imply.
7. Validate that downstream choices can be assessed against it.

## Output Contract

Produce:

- `VISION.md`
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
`architecture-vision`.

## Completion Criteria

- [ ] The governing specification is identified.
- [ ] Required upstream evidence has been read.
- [ ] The document answers its primary identity question.
- [ ] Non-responsibilities are respected.
- [ ] Assumptions and open questions are visible.
- [ ] Structural, semantic, relationship, and evidence checks pass.
- [ ] Downstream review needs are reported.
