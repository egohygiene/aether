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
updated: 2026-08-24
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

<!-- BEGIN ROADMAP EXECUTION SNAPSHOT -->
<!-- roadmap-manifest
schema: hygiene.roadmap/v1alpha1
repository: egohygiene/aether
visibility: public
publication: central
route: /roadmap/aether/
updated: 2026-08-24
-->
## 2026-08-24 execution snapshot

> This evidence-reconciled snapshot is the issue-generation and visual-roadmap handoff. The longer-horizon strategy below remains canonical context; generated HTML, JSON, progress, issue plans, and commit lists are projections.

**Lifecycle:** active pre-release authoring plane  
**Current gate:** Repair release workflow run 32672225496, which selected zero jobs, then publish the first immutable bundle release tracked by issue #38.  
**North-star outcome:** Immutable, provenance-rich AI authoring bundles made from validated specifications, skills, and agents.

### Visual roadmap publication

**Mode:** `central`  
**Route:** `/roadmap/aether/`  
**Current publication evidence:** GitHub source and validation; release publication is configured but not proven.

Publish the public-safe projection through egohygiene.io at /roadmap/aether/. This repository owns intent and acceptance evidence; it does not add a second site deployment.

### Quest line

<!-- roadmap-step
id: AET-Q01
status: complete
depends_on: []
issues: []
-->
#### AET-Q01 — Build the authoring corpus

**State:** `complete`  
**Depends on:** None

**Outcome:** A substantial, structured corpus exists for authoring and validating AI behavior.

**Exit criteria:**

- [x] Specifications, skills, and agents are present in declared locations.
- [x] Pull-request validation covers the corpus.

**Current evidence:**

- The audit counted 23 specifications, 29 skills, and 9 agents.
- PR #47 merged at ce8308fdc230 with green PR validation.

<!-- roadmap-step
id: AET-Q02
status: blocked
depends_on: [AET-Q01]
issues: []
-->
#### AET-Q02 — Repair release job selection

**State:** `blocked`  
**Depends on:** `AET-Q01`

**Outcome:** A release invocation reliably schedules the intended build, attest, and publish jobs.

**Exit criteria:**

- [ ] A release dry run schedules at least one expected job.
- [ ] The workflow fails explicitly when no releasable bundle is selected.

**Current evidence:**

- Release run 32672225496 failed with zero jobs.

<!-- roadmap-step
id: AET-Q03
status: ready
depends_on: [AET-Q01]
issues: []
-->
#### AET-Q03 — Reconcile documentation with the corpus

**State:** `ready`  
**Depends on:** `AET-Q01`

**Outcome:** Published documentation accurately inventories the current authoring surface.

**Exit criteria:**

- [ ] Counts and supported artifact types are generated or checked automatically.
- [ ] Stale authoring and release instructions are removed.

**Current evidence:**

- The audited documentation was stale relative to the repository corpus.

<!-- roadmap-step
id: AET-Q04
status: planned
depends_on: [AET-Q02, AET-Q03]
issues: []
-->
#### AET-Q04 — Version bundle provenance

**State:** `planned`  
**Depends on:** `AET-Q02`, `AET-Q03`

**Outcome:** Every bundle identifies its source specifications, validation results, and immutable digest.

**Exit criteria:**

- [ ] The manifest and provenance schema are versioned.
- [ ] Verification succeeds without trusting mutable branch state.

**Current evidence:**

- Immutable provenance is the stated target; no published bundle proof was observed.

<!-- roadmap-step
id: AET-Q05
status: planned
depends_on: [AET-Q04]
issues: [38]
-->
#### AET-Q05 — Publish and consume the first release

**State:** `planned`  
**Depends on:** `AET-Q04`

**Outcome:** Issue #38 closes with a tagged bundle used successfully by a downstream repository.

**Exit criteria:**

- [ ] A tagged release contains verified immutable artifacts.
- [ ] A downstream consumer pins and validates the release.

**Current evidence:**

- Issue #38 tracks the first release.
- No GitHub release was observed.

<!-- roadmap-step
id: AET-Q06
status: planned
depends_on: [HYG-Q06, AET-Q04]
issues: []
-->
#### AET-Q06 — Publish the roadmap authoring kit

**State:** `planned`  
**Depends on:** `HYG-Q06`, `AET-Q04`

**Outcome:** Versioned Aether guidance, templates, and evaluations help authors improve ROADMAP.md while leaving policy ownership in Hygiene.

**Exit criteria:**

- [ ] The kit generates stable IDs, outcomes, dependencies, issue hints, and exit criteria against the pinned Hygiene contract.
- [ ] Evaluation fixtures reject invented completion evidence and accidental private publication.

**Current evidence:**

- Aether already owns reusable AI artifacts; roadmap authoring support is assigned there by the visual-roadmap specification.

### Roadmap-to-issue handoff

- A step is complete only when its exit criteria and required evidence are satisfied; commit count never determines progress.
- Ready steps without an issue are candidates for the private, duplicate-aware roadmap.issue-plan.json dry run. Planned steps remain preview-only unless a reviewer explicitly opts them in with issue_policy: propose.
- Issue creation or reconciliation requires human approval or an explicitly authorized Pace operation and returns issue references through a reviewable roadmap pull request.
- Pull requests and commits should include Roadmap-Step: <ID>; historical evidence may be linked through existing issue and pull-request relationships.
- Public rendering uses only allowlisted build-time evidence and never places a GitHub token or private issue plan in the browser artifact.

<!-- END ROADMAP EXECUTION SNAPSHOT -->

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
