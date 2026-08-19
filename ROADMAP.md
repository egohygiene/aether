---
schema: aether.architecture-document/v1
id: aether-roadmap
title: Aether Roadmap
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-08
updated: 2026-08-19
governed_by:
  - architecture-roadmap
depends_on:
  - aether-vision
  - aether-pillars
  - aether-architecture
  - aether-decisions
related:
  - aether-purpose
  - aether-principles
  - aether-manifesto
  - aether-epistemology
supersedes: []
---

# ROADMAP.md — Aether Phased Work Plan

> **Document owner:** This file  
> **Related:** [`PURPOSE.md`](PURPOSE.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`DECISIONS.md`](DECISIONS.md)

---

## 1. Reading This Document

This roadmap describes the **sequence of structural work** required to move
Aether from its current state (a canonical library without a distribution
pipeline, without a staging review process, and without a schema layer) to its
target state.

It distinguishes:
- **Current state** — what exists today in the repository.
- **Target state** — what this document plans, but does not implement.
- **Non-goals** — work explicitly out of scope for Aether.

No implementation work is added by this document.  Phases become actionable
when individual issues are opened that reference the ADRs in
[`DECISIONS.md`](DECISIONS.md).

---

## 2. Current State

| Asset | State |
|---|---|
| Canonical specifications | 23+ in `library/organization/specs/` — `draft` status |
| Canonical skills | 23+ in `library/organization/skills/` — `draft` status |
| Staged material | 936+ files in `.staging/` — unreviewed, non-canonical |
| Distribution pipeline | Does not exist |
| Schema layer | Does not exist |
| Catalogs | Do not exist |
| Releases | None published |
| Governance documents | Created by this issue (issue 001) |

---

## 3. Phase 0 — Architecture and Governance (This Issue)

**Goal:** Establish the documents every later issue treats as authoritative.

**Deliverables:**
- [x] `PURPOSE.md`
- [x] `ARCHITECTURE.md`
- [x] `SYSTEM.md`
- [x] `AI_CONSTITUTION.md`
- [x] `DECISIONS.md` with ADR-001 through ADR-006
- [x] `ROADMAP.md`
- [x] `.github/copilot-instructions.md`

**Non-goals for this phase:**
- Normalizing skill or specification metadata.
- Building validators or release automation.
- Moving or deleting `.staging/` material.

---

## 4. Phase 1 — Canonical Source Stabilization

**Goal:** Promote all current `draft` specifications and skills to `stable`
status after review.

**Planned work (not yet scoped into issues):**
- Review each specification against its own spec (e.g., `purpose.spec.md`
  applied to `PURPOSE.md`).
- Promote reviewed artifacts from `draft` to `stable`.
- Document any artifact that does not meet the bar for `stable` and record
  the gap.

**Dependency:** Phase 0 complete.

---

## 5. Phase 2 — Schema Layer

**Goal:** Define JSON or YAML schemas for skill front-matter, specification
front-matter, catalog entries, and manifest files.

**Planned work:**
- Create `schemas/` directory.
- Publish at least one schema per canonical artifact kind.
- Validate all canonical artifacts against their schemas.

**Dependency:** Phase 1 complete (stable artifacts are the schema validation target).

---

## 6. Phase 3 — Staging Review

**Goal:** Process `.staging/` according to the deletion gate in
[ADR-005](DECISIONS.md#adr-005).

**Planned work:**
- Triage each `.staging/` file: promote, reject, or defer.
- Promoted files enter Phase 1 review.
- Rejected files are documented and removed in a dedicated PR.

**Dependency:** Phase 1 complete (review criteria require stable specifications).

---

## 7. Phase 4 — Distribution Pipeline

**Goal:** Define and build the process that assembles `dist/` packages from
canonical source and publishes them as GitHub Release artifacts.

**Planned work:**
- Design build process (requires ADR).
- Implement catalog generation.
- Implement distribution bundle assembly.
- Add `dist/` to `.gitignore`.
- Publish first versioned release.

**Dependency:** Phase 2 complete (schemas are needed to validate distribution content).

**Note:** The implementation of GitHub Actions for this pipeline belongs to
Relay, not Aether.  Aether defines the artifacts; Relay provides the workflow.

---

## 8. Phase 5 — Consumer Installation Model

**Goal:** Document and validate the consumer installation path so that a
downstream repository can install a specific Aether release without cloning
this repository.

**Planned work:**
- Define installation instructions in `README.md`.
- Validate the path end-to-end with at least one downstream consumer.

**Dependency:** Phase 4 complete.

---

## 9. Non-Goals (Permanent)

The following are **not** on this roadmap regardless of phase, as they belong
to neighboring repositories:

- CI workflow implementation (Relay).
- Toolchain installation (Realm).
- Organization deployment of agents (egohygiene/.github).
- Conformance measurement (PACE).
- Repository template management (Holon).
- Lint implementation (Egolint).

---

## 10. Open Questions

- **OQ-R1 (provisional):** Whether Phase 3 (staging review) should precede or
  follow Phase 2 (schema layer).  Current ordering assumes schemas are needed
  to validate staged material; this may be adjusted.
- **OQ-R2 (provisional):** Timeline for each phase.  No dates are committed;
  phases become active when issues are opened.
