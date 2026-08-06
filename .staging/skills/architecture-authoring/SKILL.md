---
name: architecture-authoring
description: Design or revise software and system architecture artifacts, including boundaries, components, interfaces, data flow, dependencies, tradeoffs, and decisions. Use for architecture documents, system designs, technical direction, platform decomposition, ADR preparation, or architecture review before implementation planning.
---

# Architecture Authoring

## Establish the contract

1. Identify the requested artifact and the decision it must enable.
1. Locate repository instructions, existing architecture, ADRs, applicable specifications, and implementation evidence.
1. Select the most specific contract under `../../../.github/specs/architecture/` when present.
1. Record material unknowns instead of silently treating them as decisions.

## Build the architecture model

Define only the views needed for the decision:

- context and stakeholders
- scope and system boundary
- components and ownership
- interfaces and data contracts
- data or control flow
- dependencies and integration points
- state, lifecycle, or failure behavior
- security, privacy, accessibility, operations, and developer experience
- alternatives, tradeoffs, and consequential decisions
- migration and compatibility boundaries

Distinguish observed current state, approved target state, recommendations, assumptions, and open questions.

## Author the artifact

- Give each concept one canonical owner.
- Link to related documents instead of duplicating their content.
- Use normative terms consistently: **must** for requirements, **should** for strong recommendations, and **may** for optional behavior.
- Prefer a small table or Mermaid diagram only when relationships are clearer visually.
- Keep implementation examples non-normative unless the architecture explicitly standardizes them.
- Avoid speculative components that do not satisfy a stated requirement.

## Validate

Check that:

- every goal maps to an architectural responsibility
- boundaries and ownership do not overlap ambiguously
- interfaces identify direction, inputs, outputs, and failures
- consequential tradeoffs are explicit
- requirements do not contradict applicable specifications
- the architecture can be decomposed into implementation work
- unresolved decisions and risks are visible

Return or write the requested artifact, then summarize decisions, assumptions, open questions, and the recommended next workflow stage.
