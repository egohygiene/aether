---
schema: aether.architecture-document/v1
id: aether-architecture
title: Aether Architecture
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-08
updated: 2026-11-13
governed_by:
  - architecture-architecture
depends_on:
  - aether-foundations
  - aether-system
related:
  - aether-purpose
  - aether-vision
  - aether-principles
  - aether-pillars
supersedes: []
---

# ARCHITECTURE.md — How Aether Is Structured

> **Document owner:** This file  
> **Related:** [`PURPOSE.md`](PURPOSE.md) · [`SYSTEM.md`](SYSTEM.md) · [`DECISIONS.md`](DECISIONS.md) · [`ROADMAP.md`](ROADMAP.md) · [`AI_CONSTITUTION.md`](AI_CONSTITUTION.md)

---

## 1. Scope

This document describes Aether's repository topology, the boundary between
canonical source and generated distribution, the lifecycle of every artifact
kind, and the rules that govern how artifacts move between states.

It does **not** describe neighboring repositories, runtime deployment, or
organization policy—those belong to the systems named in [`PURPOSE.md §4`](PURPOSE.md#4-what-aether-is-not).

---

## 2. Repository Topology (Current State)

```text
aether/
├── library/organization/       # Canonical artifact content
│   ├── skills/                # Domain/SKILL.md packages and resources
│   ├── specs/                 # Domain/*.spec.md contracts
│   ├── agents/                # <agent>/AGENT.md + derived source catalog
│   ├── instructions/          # Shared instruction/disposition source
│   └── projections/           # Provider registry, templates and builder
├── catalog/                   # Canonical schemas/fixtures/governed records
│   ├── first-party/           # Generated spec/skill index + annotations
│   ├── external/              # Restricted upstream provenance/reviews
│   └── schemas/
├── dist/                      # Tracked generated outputs; never hand-edit
├── .staging/                  # Retained unreviewed migration evidence
├── docs/decisions/            # Canonical new ADRs and legacy index
├── tests/                     # Deterministic source/contract regressions
├── aether                     # Repository-owned command entry point
├── AGENTS.md                  # Shared local instructions
├── CONTINUITY.md              # Compact operational checkpoint
└── README.md                  # Human starting path
```

The tracked generated tree conflicts with the historical release-only rule in
[ADR-0006](DECISIONS.md#adr-0006). The distinction above describes observed
source, not a newly accepted policy. [Proposed ADR-0009](docs/decisions/ADR-0009-generated-evidence-and-local-validation.md)
records this conflict and the local-versus-reusable workflow boundary for human
review. Preserve the original decisions and generated evidence pending review.

---

## 3. Canonical Source

`library/organization/` owns first-party artifact content. `catalog/` owns
structured schemas, governed external records and reviewed annotations; generated
source fields are refreshed from artifact frontmatter. Other paths include:

- **Staged material** (`.staging/`) — unreviewed and non-authoritative.
- **Generated distribution** (`dist/`) — assembled from canonical source; not
  hand-edited after generation (see [ADR-0001](DECISIONS.md#adr-0001)).
- **Repository governance documents** (`*.md` at root, `.github/`) —
  authoritative for repository behavior but not for skill or specification
  content.

### 3.1 Skill Package Layout

Every skill lives at:

```
library/organization/skills/<domain>/<skill-name>/
├── SKILL.md              # Authoritative skill contract
├── evals/
│   └── evals.json        # Evaluation cases
├── references/
│   └── *.md              # Supporting guidance documents
└── templates/
    └── *.template.md     # Output templates
```

The current [first-party package contract](docs/first-party-skill-authoring-guide.md)
requires `SKILL.md`, `references/`, `templates/` and `evals/evals.json`, including
load-trigger and executable-resource declarations where applicable. Draft
status does not exempt a package from structural validation.

### 3.2 Specification Layout

Every specification lives at:

```
library/organization/specs/<domain>/<name>.spec.md
```

Each `*.spec.md` begins with a YAML front-matter block under the
`aether.specification/v1` schema.

---

## 4. Artifact Kinds

| Kind | Description | Location | Authoritative? |
|---|---|---|---|
| Specification (`*.spec.md`) | Behavior contract for a document, agent, or process | `library/organization/specs/` | Yes |
| Skill package | Reusable AI task package | `library/organization/skills/` | Yes |
| Agent source (`AGENT.md`) | Provider-neutral agent definition | `library/organization/agents/` | Yes |
| Schema | Structured data contract | `catalog/schemas/` and artifact-owned schemas | Yes |
| Catalog | Source-derived indexes with reviewed annotations | `catalog/first-party/`, agent catalog | Source fields derived; annotations retain their declared owner |
| Distribution package | Generated package/projection | `dist/` | No — generated; presence is not release evidence |
| Staged material | Unreviewed incoming content | `.staging/` | No |

---

## 5. Artifact State Transitions

Every first-party artifact (specification or skill) carries a `status` field.

```
draft ──► experimental ──► stable ──► deprecated ──► retired
```

| State | Meaning | May Be Released? |
|---|---|---|
| `draft` | Actively being authored; may change at any time | No |
| `experimental` | Bounded evaluation with explicit limits | No |
| `stable` | Reviewed source lifecycle; release provenance/selection gates also apply | Eligible only with complete provenance and explicit release inclusion |
| `deprecated` | Superseded; existing consumers should migrate | Historical immutable releases remain; new selection is separately governed |
| `retired` | Removed from active index; file kept for history | No |

Staged material in `.staging/` does **not** carry a recognized status until
it is promoted into `library/organization/`.

---

## 6. Canonical Source vs. Generated Distribution

See [ADR-0001](DECISIONS.md#adr-0001) for the full decision record.

**Observed implementation:** `./aether distribution build` invokes existing
specification, skill and provider builders. `dist/` is tracked and verified by
drift/reproducibility checks; generated content is never hand-edited.
[ADR-0006](DECISIONS.md#adr-0006) still records the conflicting historical
release-only choice. [Proposed ADR-0009](docs/decisions/ADR-0009-generated-evidence-and-local-validation.md)
asks for explicit disposition; a factual documentation correction does not
accept that proposal or rewrite history.

---

## 7. First-Party vs. External Artifacts

| Classification | Definition |
|---|---|
| First-party | Authored and governed in `library/organization/` by Ego Hygiene contributors |
| External | Governed references under `catalog/external/`; captured material remains migration evidence with explicit rights/use limits |
| Staged | In `.staging/`; ownership and provenance not yet confirmed |

See [ADR-0003](DECISIONS.md#adr-0003) for the ownership rule.

---

## 8. Consumer Installation

Builders produce selective portable skill packages and provider projections.
The [release/pinning guide](docs/release-and-pinning-guide.md) documents preview
`gh skill` adapters and explicit local/release qualification. Actual adapter
availability and receipt status decide readiness: deterministic unit tests,
tracked packages and catalog presence do not establish a compatible installed
consumer, approved release, or remote upgrade/rollback proof. Issue38 retains
that acceptance work.

See [ADR-0004](DECISIONS.md#adr-0004) for the versioning decision.

---

## 9. Staged Material Lifecycle

`.staging/` is a holding area for material that was generated, imported, or
contributed before a canonical review process existed.

**Deletion gate:** No file may be removed from `.staging/` until:

1. Its content has been reviewed against the relevant specification.
2. It has been either promoted to `library/organization/` or explicitly
   rejected with a recorded reason.
3. The [`DECISIONS.md` ADR-0005](DECISIONS.md#adr-0005) deletion-gate rule is satisfied.

See [ADR-0005](DECISIONS.md#adr-0005) for the full rule.

---

## 10. Changes That Require an ADR

An Architecture Decision Record is required before implementing any of the
following:

- Changing the canonical source tree location.
- Adding or removing an artifact kind.
- Defining a new state in the artifact lifecycle.
- Establishing or changing a distribution channel.
- Moving a responsibility boundary between Aether and a neighboring repository.
- Introducing committed generated content (`dist/` in version control).
- Changing the versioning scheme (per-artifact vs. repository-release).

---

## 11. Open Questions

- **OQ-A1 (provisional):** Whether `library/organization/` should be flattened
  to `library/` as artifact kinds grow.  No migration is planned until evidence
  requires it.
- **OQ-A2 (historical):** Implemented source now lives at
  `library/organization/agents/<id>/AGENT.md`. The provider projection registry
  owns generated host paths; no file move is proposed by this reconciliation.
