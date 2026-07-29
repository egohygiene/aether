---
name: spec-authoring
description: Create, revise, split, or validate implementation-ready `.spec.md` files from ideas, requirements, architecture, research, or existing systems. Use when defining a durable scope contract with goals, non-goals, requirements, boundaries, interfaces, implementation phases, validation, acceptance criteria, and open questions.
---

# Specification Authoring

## Establish scope

1. Read `../../../.github/specs/specfile.spec.md` when present.
1. Identify the problem, intended audience, owner, current state, desired state, constraints, and decision status.
1. Inspect related specifications, architecture, ADRs, source, tests, automation, and external standards.
1. Decide whether one cohesive spec is sufficient. Propose a dependency-ordered split only when multiple independently governed contracts are necessary.

## Write the contract

Use a kebab-case filename ending in `.spec.md`. Follow the repository's canonical structure. At minimum make these concerns explicit:

- purpose and context
- goals and non-goals
- functional and non-functional requirements
- system boundaries and ownership
- components, interfaces, data flow, state, and dependencies
- migration and compatibility behavior when applicable
- phased implementation guidance
- validation plan and observable acceptance criteria
- risks, assumptions, and open questions

Use **must**, **should**, and **may** consistently. Keep observed current state distinct from desired requirements. Give requirements stable identifiers when traceability across a large spec materially helps.

## Preserve layer boundaries

- Put task or system requirements in the spec.
- Put reusable procedures in skills.
- Put always-on repository conventions in instructions.
- Put role, tools, and orchestration behavior in agents.
- Put the immediate unit of work in an issue or prompt.

Do not turn the spec into a tutorial, implementation dump, or duplicate of another canonical contract.

## Validate

Check filename and metadata, internal consistency, requirement testability, architecture coverage, phase ordering, acceptance-criteria traceability, defined terminology, link integrity, and unresolved decisions. Avoid production code except small, clearly non-normative examples. Return or write the complete spec and identify blockers to approval or implementation.
