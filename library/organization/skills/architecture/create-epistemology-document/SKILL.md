---
schema: aether.skill/v1
id: create-epistemology-document
title: Create Epistemology Document
kind: skill
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-08-02
updated: 2026-08-02
domain: architecture
tags:
  - architecture
  - meta
  - epistemology
  - authoring
depends_on:
  - architecture-authoring
implements:
  - architecture-epistemology
recommended_agents:
  - architect
---

# Create Epistemology Document

## Purpose

Create or update `EPISTEMOLOGY.md` in conformance with `architecture-epistemology`.

The document must answer:

> How do we determine whether a claim is sufficiently supported, how certain we are, and how that knowledge may change?

## Use this skill when

- the canonical document does not exist
- the existing document is incomplete or inconsistent
- upstream architecture changed materially
- the repository architecture system is being established or repaired
- a repeatable, validated authoring workflow is needed

## Do not use this skill for

- treating authority as proof
- hiding disagreement
- using undefined confidence labels
- presenting decisions as facts

## Required inputs

- governing specification and version
- required upstream architecture documents
- applicable policies and decisions
- existing repository evidence
- known conflicts, assumptions, and open questions

Missing evidence must be recorded rather than invented.

## Workflow

1. inventory existing evidence, provenance, confidence, and decision practices
2. identify recurring knowledge failures and ambiguity
3. define claim states and their meanings
4. define source and evidence evaluation criteria
5. define confidence and uncertainty language
6. define conflict-resolution and canonicalization rules
7. test the model against contradictory and incomplete evidence
8. validate applicability to humans and AI systems

## Output contract

Produce:

- `EPISTEMOLOGY.md`
- governing specification identifier and version
- assumptions and unresolved questions
- validation results
- downstream review recommendations

## Constraints

- Preserve canonical terminology.
- Separate evidence, inference, proposal, and decision.
- Do not invent organizational intent or authority.
- Do not silently resolve contradictions.
- Do not claim completion when required inputs are missing.
- Keep implementation detail outside the document unless the specification
  explicitly requires it.

## Validation

Use:

    references/validation-checklist.md

and the acceptance criteria in:

    architecture-epistemology

## Completion criteria

- [ ] The governing specification is identified.
- [ ] Required upstream evidence has been read.
- [ ] The document answers its primary question.
- [ ] Responsibilities and non-responsibilities are respected.
- [ ] Assumptions and unresolved questions are visible.
- [ ] Structural, semantic, relationship, and evidence checks pass.
- [ ] Downstream review needs are reported.
