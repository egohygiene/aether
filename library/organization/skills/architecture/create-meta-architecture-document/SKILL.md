---
name: create-meta-architecture-document
description: Creates or updates META.md describing the architecture of the architecture system itself. Use when a project needs to define or review the meta-level rules governing its architecture documentation.
license: MIT
metadata:
  aether-version: "1.1.0"
  aether-status: "draft"
  aether-spec-id: "architecture-meta"
  aether-scope: "organization"
  aether-domain: "architecture"
  aether-owners: "egohygiene"
  aether-created: "2026-08-02"
  aether-updated: "2026-09-08"
---

# Create Meta Architecture Document

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

For repository-scoped work, compose `maintain-repository-continuity` in
**Resume** mode before selecting work. After an authorized repository change
passes domain validation, compose **Refresh** and **Verify** immediately before
presenting the pull request, and include the reconciled root `CONTINUITY.md` in
the same change. A policy-permitted no-change or exemption result must be
documented instead of fabricating an edit.

- **Contribute:** Architecture-document ownership, relationships, precedence, validation, and governance gaps
- **Never claim:** That proposed documentation governance or ownership is approved without evidence

## Purpose

Create or update `META.md` in conformance with `architecture-meta`.

The document must answer:

> How is this architecture-document system organized, navigated, validated, and evolved?

## Use this skill when

- the canonical document does not exist
- the existing document is incomplete or inconsistent
- upstream architecture changed materially
- the repository architecture system is being established or repaired
- a repeatable, validated authoring workflow is needed

## Do not use this skill for

- duplicating every architecture document
- relying only on directory order
- hiding missing documents
- making META.md an upstream dependency for everything

## Required inputs

- governing specification and version
- required upstream architecture documents
- applicable policies and decisions
- existing repository evidence
- known conflicts, assumptions, and open questions

Missing evidence must be recorded rather than invented.

## Workflow

1. discover all applicable architecture documents and metadata
2. resolve specifications and stable identifiers
3. classify categories and canonical ownership
4. build and validate the relationship graph
5. derive reading and authoring order
6. record lifecycle, gaps, omissions, and conflicts
7. write concise navigation without duplicating document content
8. reconcile the prose with generated catalog data

## Output contract

Produce:

- `META.md`
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

    architecture-meta

## Completion criteria

- [ ] The governing specification is identified.
- [ ] Required upstream evidence has been read.
- [ ] The document answers its primary question.
- [ ] Responsibilities and non-responsibilities are respected.
- [ ] Assumptions and unresolved questions are visible.
- [ ] Structural, semantic, relationship, and evidence checks pass.
- [ ] Downstream review needs are reported.
