---
schema: aether.skill/v1
id: create-personal-model-document
title: Create Personal Model Document
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
  - domain
  - authoring
depends_on:
  - architecture-authoring
related: []
supersedes: []
implements:
  - architecture-personal-model
recommended_agents:
  - architect
---

# Create Personal Model Document

    ## Purpose

    Create or update `PERSONAL_MODEL.md` in conformance with `architecture-personal-model`.

    The document must answer:

    > How does this project understand the people it serves while preserving agency, dignity, privacy, complexity, and change?

    ## Use This Skill When

    - the canonical document is missing
    - terminology or assumptions are inconsistent
    - upstream architecture has changed
    - a repository is establishing or repairing its domain model
    - downstream architecture needs a stable canonical reference

    ## Required Inputs

    Resolve the governing specification, upstream architecture, relevant
    evidence, existing terminology or assumptions, and downstream consumers.

    Missing evidence must be recorded rather than invented.

    ## Workflow

    1. inventory explicit and implicit assumptions about people
2. separate evidence from preference and inference
3. define agency, autonomy, identity, context, and change
4. distinguish people from system representations
5. define consent, privacy, and inference boundaries
6. define correction and contestability expectations
7. challenge universal and normative assumptions
8. record limitations and unknowns
9. report downstream design and AI implications

    ## Output Contract

    Produce:

    - `PERSONAL_MODEL.md`
    - governing specification identifier and version
    - assumptions and unresolved questions
    - validation results
    - downstream migration or review recommendations

    ## Constraints

    - Preserve canonical terminology.
    - Separate evidence, assumptions, and inference.
    - Do not fabricate domain or human knowledge.
    - Do not silently resolve contradictions.
    - Do not leak implementation structure into canonical concepts.
    - Do not claim completion when required evidence is missing.

    ## Validation

    Use:

        references/validation-checklist.md

    and the acceptance criteria in:

        architecture-personal-model

    ## Completion Criteria

    - [ ] The governing specification is identified.
    - [ ] Required upstream artifacts have been read.
    - [ ] The primary question is answered.
    - [ ] Boundaries are respected.
    - [ ] Assumptions and open questions are visible.
    - [ ] Structural, semantic, relationship, and evidence checks pass.
    - [ ] Downstream impacts are reported.
