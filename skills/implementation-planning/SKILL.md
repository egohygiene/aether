---
name: implementation-planning
description: Convert approved requirements, specifications, and architecture into an ordered, dependency-aware, implementation-ready plan. Use for technical plans, phased execution strategies, migration plans, file-level change maps, issue decomposition, delivery sequencing, validation planning, or risk analysis before code changes.
---

# Implementation Planning

## Establish inputs

1. Identify the authoritative requirements, architecture, decisions, acceptance criteria, and repository instructions.
1. Inspect affected components, interfaces, tests, automation, delivery environment, and current implementation patterns.
1. Separate approved decisions from assumptions and open questions.
1. Stop planning across a material unresolved architecture boundary; surface the decision first.

## Decompose by dependency

Build phases around independently verifiable outcomes, not arbitrary file groups. For each phase define:

- objective and requirements covered
- prerequisites and dependencies
- affected components or provisional file areas
- implementation actions in execution order
- interface, data, schema, or migration changes
- tests and validation commands
- documentation and operational updates
- completion condition
- risks and rollback or recovery needs

Prefer vertical slices when they reduce integration risk. Separate research, foundation, migration, rollout, and cleanup when each produces an independently reviewable result.

## Check completeness

Trace every requirement and acceptance criterion to at least one phase and validation step. Include compatibility, security, privacy, accessibility, observability, data migration, and release concerns only when the system requires them. Avoid fake precision: do not assign dates or effort estimates without a requested estimation method and evidence.

## Deliver

Return the requested Markdown plan or write it to the requested path. Include assumptions, open questions, dependency order, test strategy, risks, and the recommended first executable unit. Do not modify production code during a planning-only task.
