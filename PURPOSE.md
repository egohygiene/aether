---
schema: aether.architecture-document/v1
id: aether-purpose
title: Aether Purpose
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-08
updated: 2026-08-19
governed_by:
  - architecture-purpose
depends_on:
  []
related:
  - aether-vision
  - aether-principles
  - aether-pillars
  - aether-manifesto
supersedes: []
---

# PURPOSE.md — Why Aether Exists

> **Document owner:** `ARCHITECTURE.md`  
> **Related:** [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`SYSTEM.md`](SYSTEM.md) · [`DECISIONS.md`](DECISIONS.md) · [`ROADMAP.md`](ROADMAP.md)

---

## 1. Statement of Purpose

Aether is the **canonical library of reusable AI specifications, skills, agent
source, schemas, catalogs, and distribution artifacts** for the Ego Hygiene
organization.

It exists so that every repository, agent, and consumer within the organization
can reference a single authoritative source of AI behavior contracts instead of
duplicating intent ad hoc across private configuration files.

## 2. Problem Solved

Before Aether, AI behavior intent existed only as ephemeral prompts, undocumented
conventions, or scattered per-repository copies.  There was no shared vocabulary,
no versioned contract for what a skill does, no governed boundary between
first-party and external artifacts, and no distribution model that let consumers
receive updates without copying the entire source tree.

Aether makes the following possible:

- A human or agent reading a skill or specification understands exactly what
  behavior is expected, what inputs are required, what outputs are guaranteed,
  and what quality bar must be met.
- Consumers can install discrete, versioned artifacts without pulling in
  unrelated canonical source.
- First-party intent can be distinguished from third-party extensions and from
  staged material that has not yet been reviewed.
- Architectural decisions are recorded and accessible, so later issues and
  pull requests can treat them as authoritative rather than re-litigating them.

## 3. What Aether Is

| What Aether provides | Examples |
|---|---|
| Specifications (`*.spec.md`) | Behavior contracts for documents, agents, processes |
| Skills (`SKILL.md` + evals + templates + references) | Reusable AI task packages |
| Agent source (`*.agent.md`) | Custom-agent definition files |
| Schemas | Structured data contracts for catalog and manifest entries |
| Catalogs | Indexes of available skills, agents, and specifications |
| Distribution artifacts | Versioned, installable packages assembled from canonical source |

## 4. What Aether Is Not

Aether does not own the following; each belongs to a named neighboring
repository or system:

| Concern | Not Aether — see instead |
|---|---|
| Organization custom-agent deployment and Copilot policy | `egohygiene/.github` and GitHub organization settings |
| Universal repository baseline (`.gitignore`, `CODEOWNERS`, …) | Empathy |
| Repository creation and customization | Holon |
| Development environment and installed toolchain | Realm |
| Portable shell commands | Mantle |
| Lint and static-check implementation | Egolint |
| Reusable GitHub Actions | Relay |
| Conformance measurement and drift detection | PACE |
| Mind Garden domain contracts | Mindgarden |
| Flutter application contracts | `egohygiene` application repositories |
| Video/animation compiler contracts | Aniflow or Flow |

## 5. Primary Consumers

- **Human contributors** authoring architecture documents or skills.
- **Copilot and custom agents** executing tasks that reference canonical
  skill or specification files.
- **Downstream repositories** that consume versioned Aether distributions.
- **Future tooling** (not yet built) that validates conformance or publishes
  release packages.

## 6. Success Condition

Aether succeeds when:

1. A new contributor can understand what a skill does without reading source
   code or chat history.
2. A consumer can install a specific skill version without cloning this
   repository.
3. Agents operating in any repository can cite an Aether specification as an
   authoritative behavioral contract.
4. Architectural decisions are recorded before implementation begins.

## 7. Open Questions

- **OQ-P1 (provisional):** Whether ArXiv publication is a first-class Aether
  distribution channel or a downstream concern.  Currently treated as a
  publishing skill candidate.
- **OQ-P2 (provisional):** Whether Mindgarden and Aniflow domain contracts will
  eventually move into Aether or remain in their own repositories.
