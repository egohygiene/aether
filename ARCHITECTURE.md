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

```
aether/
├── library/
│   └── organization/          # Canonical source tree
│       ├── skills/            # First-party skill packages
│       │   ├── architecture/
│       │   ├── authoring/
│       │   ├── methodology/
│       │   ├── publishing/
│       │   └── quality/
│       └── specs/             # First-party specifications
│           ├── architecture/
│           ├── authoring/
│           ├── methodology/
│           ├── publishing/
│           └── quality/
├── .staging/                  # Unreviewed incoming material (not canonical)
│   ├── agents/
│   ├── instructions/
│   ├── manifests/
│   └── specs/
├── PURPOSE.md
├── ARCHITECTURE.md
├── SYSTEM.md
├── AI_CONSTITUTION.md
├── DECISIONS.md
├── ROADMAP.md
├── README.md
└── LICENSE
```

**Target state** adds the following directories (not yet created):

```
aether/
├── dist/                      # Generated distribution artifacts (see ADR-001)
├── docs/
│   └── adr/                   # Architecture Decision Records
└── schemas/                   # JSON/YAML schemas for catalog entries
```

---

## 3. Canonical Source

`library/organization/` is the **sole authoritative source** for all
first-party artifacts.  Any file outside this tree is either:

- **Staged material** (`.staging/`) — unreviewed and non-authoritative.
- **Generated distribution** (`dist/`) — assembled from canonical source; not
  hand-edited after generation (see [ADR-001](DECISIONS.md#adr-001)).
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

`SKILL.md` is the only required file.  The other directories are present when
the skill is sufficiently mature to include them.

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
| Agent source (`*.agent.md`) | Custom-agent definition | `library/organization/` (planned) | Yes |
| Schema | Structured data contract | `schemas/` (planned) | Yes |
| Catalog | Index of available artifacts | `dist/` (planned, generated) | No — generated |
| Distribution package | Versioned installable bundle | `dist/` (planned, generated) | No — generated |
| Staged material | Unreviewed incoming content | `.staging/` | No |

---

## 5. Artifact State Transitions

Every first-party artifact (specification or skill) carries a `status` field.

```
draft ──► stable ──► deprecated ──► retired
           │
           └──► (may be released)
```

| State | Meaning | May Be Released? |
|---|---|---|
| `draft` | Actively being authored; may change at any time | No |
| `stable` | Reviewed, accepted, and ready for consumer use | Yes |
| `deprecated` | Superseded; existing consumers should migrate | Yes (with warning) |
| `retired` | Removed from active index; file kept for history | No |

Staged material in `.staging/` does **not** carry a recognized status until
it is promoted into `library/organization/`.

---

## 6. Canonical Source vs. Generated Distribution

See [ADR-001](DECISIONS.md#adr-001) for the full decision record.

**Summary rule:** Canonical source lives in `library/organization/`.  Generated
distributions are assembled by a future build process and placed in `dist/`.
Generated files are never edited by hand.  Until the build process exists,
`dist/` does not exist and distributions are release-only (see
[ADR-006](DECISIONS.md#adr-006)).

---

## 7. First-Party vs. External Artifacts

| Classification | Definition |
|---|---|
| First-party | Authored and governed in `library/organization/` by Ego Hygiene contributors |
| External | Imported from outside the organization; stored in a dedicated external subtree (not yet created) |
| Staged | In `.staging/`; ownership and provenance not yet confirmed |

See [ADR-003](DECISIONS.md#adr-003) for the ownership rule.

---

## 8. Consumer Installation

**Current state:** Consumers clone or copy files from `library/organization/`
directly.  No automated distribution mechanism exists.

**Target state:** Consumers reference a versioned `dist/` package or a
GitHub Release artifact, installing only the artifacts they need.  The
installation mechanism is not specified in this document; it will be defined
when the distribution build process is designed.

See [ADR-004](DECISIONS.md#adr-004) for the versioning decision.

---

## 9. Staged Material Lifecycle

`.staging/` is a holding area for material that was generated, imported, or
contributed before a canonical review process existed.

**Deletion gate:** No file may be removed from `.staging/` until:

1. Its content has been reviewed against the relevant specification.
2. It has been either promoted to `library/organization/` or explicitly
   rejected with a recorded reason.
3. The [`DECISIONS.md` ADR-005](DECISIONS.md#adr-005) deletion-gate rule is satisfied.

See [ADR-005](DECISIONS.md#adr-005) for the full rule.

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
- **OQ-A2 (provisional):** Whether agent source files belong in
  `library/organization/agents/` or in a top-level `agents/` directory.
  Holding at `library/organization/` pending more agent candidates.
