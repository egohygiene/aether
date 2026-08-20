---
schema: aether.architecture-document/v1
id: aether-system
title: Aether System
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-08
updated: 2026-08-19
governed_by:
  - architecture-system
depends_on:
  - aether-foundations
  - aether-ontology
related:
  - aether-purpose
  - aether-vision
  - aether-principles
  - aether-pillars
supersedes: []
---

# SYSTEM.md — How Aether's Artifacts Relate

> **Document owner:** This file  
> **Related:** [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`PURPOSE.md`](PURPOSE.md) · [`DECISIONS.md`](DECISIONS.md)

---

## 1. Scope

This document maps the relationships between Aether's artifact kinds—
specifications, skills, agents, instructions, hooks, catalogs, and releases—
and explains how canonical source becomes a deployable or installable artifact.

It describes the **data model and flow**, not the repository topology
(see [`ARCHITECTURE.md`](ARCHITECTURE.md)) and not the decision rationale
(see [`DECISIONS.md`](DECISIONS.md)).

---

## 2. Artifact Map

```
Specification (*.spec.md)
  │
  ├─► defines the behavioral contract for a Skill or Agent
  │
  └─► referenced by Skills via SKILL.md front-matter

Skill Package (SKILL.md + evals + templates + references)
  │
  ├─► consumed by AI agents at task time
  ├─► tested by evals/evals.json
  └─► assembled into Distribution Packages

Agent Source (*.agent.md)
  │
  ├─► cites one or more Skills
  ├─► deployed via egohygiene/.github (not Aether)
  └─► assembled into Distribution Packages

Schema
  │
  ├─► validates Catalog entries and Manifest files
  └─► consumed by future build tooling

Catalog (generated)
  │
  ├─► indexes available Skills, Agents, and Specifications
  ├─► generated from canonical source — not hand-edited
  └─► included in Distribution Packages

Distribution Package (generated)
  │
  ├─► assembled from canonical Skills, Agents, Schemas, and Catalogs
  ├─► versioned by repository release (see ADR-004)
  └─► published as a GitHub Release artifact

Hook (planned)
  │
  └─► lifecycle scripts triggered on canonical state transitions

Release
  │
  └─► tagged GitHub Release; wraps one or more Distribution Packages
```

---

## 3. How Canonical Source Becomes Installable

> **Current state:** No automated build process exists.  Consumers reference
> files directly from `library/organization/`.
>
> **Target state** (not yet implemented):

```
library/organization/   (canonical source)
         │
         ▼
   build process         (future; not specified here)
         │
         ▼
      dist/              (generated; never hand-edited)
         │
         ▼
   GitHub Release         (tagged; consumers download artifacts)
```

The build process is not part of this issue.  Its design will require an ADR
when proposed.

---

## 4. Specification → Skill Relationship

A Specification defines **what** behavior a skill must produce.
A Skill defines **how** that behavior is invoked.

A skill's `SKILL.md` front-matter references the specification it implements.
An eval in `evals/evals.json` tests conformance to that specification.

This is a one-to-one relationship today; future skills may implement a
composition of specifications.

---

## 5. Skill → Agent Relationship

An Agent source file (`*.agent.md`) references one or more skills by name.
The agent provides context, persona, and task orchestration; the skills
provide the reusable behavioral contracts the agent executes.

Agents are **deployed** by `egohygiene/.github` and GitHub organization
settings, not by Aether directly.  Aether provides the agent source;
deployment is a neighboring-repository concern.

---

## 6. Consumer-Local Authority

**Rule:** Consumer-local instructions and configuration are authoritative over
Aether defaults.

If a consumer repository's `.github/copilot-instructions.md` or agent
configuration overrides a default established by an Aether skill or
specification, the consumer's local version takes precedence at runtime.

Aether defaults are **strong defaults**, not mandates.

---

## 7. Instructions vs. Skills vs. Specifications

| Artifact | Governs | Authoritative? | Hand-edited? |
|---|---|---|---|
| Specification | What the output contract is | Yes (first-party) | Yes |
| Skill | How a task is invoked; evals; templates | Yes (first-party) | Yes |
| Agent source | Persona, context, task routing | Yes (first-party) | Yes |
| Consumer instructions | Local overrides and context | Yes (consumer) | Yes |
| Catalog | Index of available artifacts | No (generated) | No |
| Distribution | Installable bundle | No (generated) | No |

---

## 8. Hooks (Planned)

Hooks are lifecycle scripts that fire on artifact state transitions (e.g., when
a skill moves from `draft` to `stable`).  No hooks exist yet.  When introduced,
they will require an ADR.

---

## 9. Staged Material

`.staging/` is not part of the canonical artifact model.  Files there do not
participate in the specification → skill → agent → distribution flow until
promoted.  See [`ARCHITECTURE.md §9`](ARCHITECTURE.md#9-staged-material-lifecycle)
for the promotion gate.

---

## 10. Open Questions

- **OQ-S1 (provisional):** Whether a Catalog should be a single file or a
  per-domain index.  No decision until at least one distribution build is
  designed.
- **OQ-S2 (provisional):** Whether hooks will be implemented in Mantle (shell)
  or Relay (Actions).  Deferred to the hook design ADR.
