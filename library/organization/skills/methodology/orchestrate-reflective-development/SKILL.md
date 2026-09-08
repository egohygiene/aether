---
name: orchestrate-reflective-development
description: Orchestrates a bounded reflective development cycle by planning, executing, and auditing one unit of work. Use when a development cycle needs to proceed, pause, synchronize, or complete with human alignment.
license: MIT
metadata:
  aether-version: "1.1.0"
  aether-status: "draft"
  aether-spec-id: "reflector"
  aether-scope: "organization"
  aether-domain: "methodology"
  aether-owners: "egohygiene"
  aether-created: "2026-08-02"
  aether-updated: "2026-09-08"
---

# Orchestrate Reflective Development

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

For repository-scoped work, compose `maintain-repository-continuity` in
**Resume** mode before selecting work. After an authorized repository change
passes domain validation, compose **Refresh** and **Verify** immediately before
presenting the pull request, and include the reconciled root `CONTINUITY.md` in
the same change. A policy-permitted no-change or exemption result must be
documented instead of fabricating an edit.

- **Contribute:** Cycle objective, phase results, validation, human decisions, blockers, and next bounded action
- **Never claim:** An autonomous loop, human approval, or completed phase without evidence

## Purpose

Execute the reusable procedure governed by `reflector`.

Primary question:

> How should the current bounded development cycle proceed, pause, synchronize, or complete?

## Required Inputs

Resolve:

- governing specification and version
- current source or repository state
- scope and constraints
- upstream architecture or evidence
- output location
- validation expectations
- unresolved decisions

Missing evidence must remain visible.

## Workflow

1. resolve current cycle state and human alignment anchor
2. define scope, exclusions, mode, and recursion budget
3. read source specifications, issues, architecture, and prior cycles
4. plan and execute one bounded work unit
5. validate produced artifacts
6. perform or consume a reflective audit
7. detect drift and unresolved decisions
8. record state and safe resume point
9. stop at the synchronization boundary

## Output Contract

Primary output:

    reflective cycle record

Also report assumptions, evidence gaps, validation status, unresolved
questions, and downstream actions requiring separate authorization.

## Constraints

- Follow the governing specification.
- Preserve provenance and uncertainty.
- Do not invent authority, evidence, or current behavior.
- Do not silently expand scope.
- Do not claim completion when required validation is missing.
- Keep proposed downstream work separate from authorized execution.

## Completion Criteria

- [ ] Governing specification is resolved.
- [ ] Scope and constraints are explicit.
- [ ] Required evidence was inspected.
- [ ] The primary output was created.
- [ ] Validation was executed or its absence documented.
- [ ] Open questions and authorization needs are visible.
