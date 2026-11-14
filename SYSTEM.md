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
updated: 2026-11-13
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

Agent Source (<id>/AGENT.md)
  │
  ├─► cites one or more Skills
  ├─► deployed via egohygiene/.github (not Aether)
  └─► assembled into Distribution Packages

Schema
  │
  ├─► validates Catalog entries and Manifest files
  └─► consumed by existing validators and builders

Catalog (source-derived fields + reviewed annotations)
  │
  ├─► indexes available Skills, Agents, and Specifications
  ├─► source fields generated; declared catalog annotations preserved
  └─► included in Distribution Packages

Distribution Package (generated)
  │
  ├─► assembled from canonical Skills, Agents, Schemas, and Catalogs
  ├─► versioned by repository release (see ADR-0004)
  └─► eligible publication is a separately authorized release handoff

Hook (planned)
  │
  └─► lifecycle scripts triggered on canonical state transitions

Release
  │
  └─► tagged GitHub Release; wraps one or more Distribution Packages
```

---

## 3. How Canonical Source Becomes Installable

The repository command `./aether distribution build` already assembles
specifications, portable skills, provider projections and selected catalog
outputs. Canonical artifact content lives under `library/organization/`;
`catalog/` owns schemas, provenance records and declared annotations.

```text
canonical content + catalog contracts
                  ↓
repository-owned deterministic builders/validators
                  ↓
tracked dist/ + manifests/projections (derived)
                  ↓
explicit consumer qualification and reviewed release selection
                  ↓
separately authorized immutable publication / downstream install
```

Tracked generated output and local CI/release callers exist, while historical
ADR-0006 and ADR-0002 contain conflicting rules. [Proposed ADR-0009](docs/decisions/ADR-0009-generated-evidence-and-local-validation.md)
records this for human review; source existence is not acceptance. Actual
consumer qualification remains not-ready when the preview adapter is missing.
See [release/pinning](docs/release-and-pinning-guide.md) and [the tactical ledger](https://github.com/egohygiene/aether/issues/105).

---

## 4. Specification → Skill Relationship

A Specification defines **what** behavior a skill must produce.
A Skill defines **how** that behavior is invoked.

A skill's `SKILL.md` front-matter references the specification it implements.
An eval in `evals/evals.json` tests conformance to that specification.

Skills already compose governing contracts, references and other skills.
Declared metadata and packaged resource checks establish those relationships;
deterministic evals exercise declared assertions only and do not run a model.

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
| Catalog | Source-derived index plus declared annotations | Fields retain their documented owner | Regenerate source fields; review annotations |
| Distribution | Installable bundle | No (generated) | No |

---

## 8. Hooks (Planned)

Historical hook prototypes remain staged and excluded from first-party
execution/distribution under [ADR-0007](DECISIONS.md#adr-0007). The delivered
decision-impact and continuity instruction blocks are guidance, not proof of an
automatically installed runtime hook. New executable hook adoption still needs
its own review and permitted source disposition.

---

## 9. Staged Material

`.staging/` is not part of the canonical artifact model.  Files there do not
participate in the specification → skill → agent → distribution flow until
promoted.  See [`ARCHITECTURE.md §9`](ARCHITECTURE.md#9-staged-material-lifecycle)
for the promotion gate.

---

## 10. Open Questions

- **OQ-S1 (historical):** The implemented catalog families have explicit
  responsibilities in [catalog/README.md](catalog/README.md); no index split or
  new canonical registry is proposed here.
- **OQ-S2 (provisional):** Whether hooks will be implemented in Mantle (shell)
  or Relay (Actions).  Deferred to the hook design ADR.
