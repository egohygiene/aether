---
schema: aether.skill/v1
id: orchestrate-reflective-development
title: Orchestrate Reflective Development
kind: skill
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-08-02
updated: 2026-08-02
domain: methodology
tags:
  - methodology
  - workflow
  - validation
depends_on: []
related: []
supersedes: []
implements:
  - reflector
---

# Orchestrate Reflective Development

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
