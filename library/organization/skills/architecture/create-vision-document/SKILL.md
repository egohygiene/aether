---
schema: aether.skill/v1
id: create-vision-document
title: Create Vision Document
kind: skill
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-08-01
updated: 2026-08-01
domain: architecture
tags:
  - architecture
  - identity
  - vision
  - authoring
depends_on:
  - architecture-authoring
implements:
  - architecture-vision
recommended_agents:
  - architect
---

# Create Vision Document

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
