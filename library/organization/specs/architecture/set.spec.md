---
schema: aether.specification/v1
id: architecture-set
title: Architecture Document Set Specification
kind: specification
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
domain: architecture
tags:
  - architecture
  - applicability
  - materialization
  - validation
applies_to:
  - architecture-document-sets
  - consumer-repositories
depends_on:
  - architecture-document
related:
  - architecture-meta
  - architecture-authoring
supersedes: []
---

# Architecture Document Set Specification

## Introduction

This specification defines how a repository selects, materializes, inventories,
and validates an applicable set of architecture documents from the Aether
architecture-document system.

It answers:

> Which architecture documents does this scope need, why are they applicable,
> and how is the set governed as one dependency graph?

## 1. Purpose and scope

The specification governs selection profiles, applicability evidence, canonical
filenames, materialized metadata, identifier namespacing, set completeness,
intentional omissions, dependency closure, and cross-document validation.

It does not define the substantive content of an individual architecture
document, replace its document-specific specification, or require every
repository to use every document.

## 2. Conceptual model

```text
repository evidence
    + reusable Aether specifications
    + applicability decision
        -> selected document set
        -> repository-specific materializations
        -> dependency graph and META inventory
        -> validation evidence
```

Selection is an architectural decision. A profile is a starting heuristic, not
proof that each document applies.

## 3. Responsibilities

An architecture set owns:

- the list of applicable architecture documents;
- justification for conditional documents;
- canonical filename and artifact identifier mapping;
- dependency closure;
- lifecycle status across the set;
- intentional omissions, missing nodes, and blocked nodes;
- cross-document terminology and ownership consistency;
- set-level validation and change propagation.

## 4. Non-responsibilities

An architecture set does not own:

- the content concern assigned to an individual document;
- implementation topology beyond what `ARCHITECTURE.md` owns;
- accepted decision content beyond `DECISIONS.md`;
- generated architecture portals as a competing source of truth;
- organization policy owned by Hygiene.

## 5. Applicability profiles

| Profile | Typical documents | Use when |
| --- | --- | --- |
| Core | Purpose, vision, principles, epistemology, foundations, system, architecture, methodology, decisions, roadmap, meta | The repository has durable system and governance concerns |
| Human-facing | Core plus personal model, design, design system | People use, operate, contribute to, or are materially affected by its surfaces |
| AI-participating | Core plus AI constitution | AI agents or AI product capabilities act in scope |
| Domain-rich | Core plus ontology | Stable concepts and relationships need canonical ownership |
| Public identity | Core plus pillars and manifesto | The repository communicates strategic capabilities and public commitments |
| Complete reference | All 18 documents | Every category is genuinely applicable and the repository can maintain the full graph |

Profiles may be composed. Applicability must be recorded in `META.md`.

## 6. Materialized metadata

Every selected document shall contain:

- `schema: aether.architecture-document/v1`;
- a stable, scope-prefixed `id`;
- `title`;
- `kind: architecture-document`;
- semantic `version`;
- lifecycle `status`;
- `owners`;
- `created` and `updated` dates;
- one or more `governed_by` specification identifiers;
- `depends_on`, `related`, and `supersedes` identifier arrays.

The schema in `architecture-document.schema.json` is the structural authority
for extracted frontmatter.

## 7. Requirements

- **REQ-001:** Every selected document shall have one canonical path.
- **REQ-002:** Every selected document shall have a stable, unique identifier.
- **REQ-003:** Every selected document shall name its governing specification.
- **REQ-004:** Required dependencies shall be selected or explicitly recorded
  as missing or blocked.
- **REQ-005:** Dependency edges shall resolve and remain acyclic.
- **REQ-006:** `META.md` shall inventory selected, intentionally omitted,
  missing, blocked, and provisional documents distinctly.
- **REQ-007:** Conditional documents shall have an applicability rationale.
- **REQ-008:** Materializations shall remain repository-specific rather than
  copied generic placeholders.
- **REQ-009:** Existing detailed documents shall be migrated without discarding
  accepted decisions, history, or repository evidence.
- **REQ-010:** Generated projections shall identify the canonical source set.
- **REQ-011:** Cross-document terminology conflicts shall be surfaced.
- **REQ-012:** A material upstream change shall trigger downstream review.
- **REQ-013:** The set shall distinguish observed, decided, inferred, proposed,
  assumed, unverified, and open-question claims where relevant.
- **REQ-014:** Complete-reference claims shall pass complete-reference
  validation rather than relying on file count alone.

## 8. Constraints

- **CON-001:** Do not create empty files to satisfy a profile.
- **CON-002:** Do not silently duplicate a concern across documents.
- **CON-003:** Do not invent repository intent to complete the graph.
- **CON-004:** Do not treat an intentional omission as a missing artifact.
- **CON-005:** Do not overwrite detailed existing architecture with generic
  generated prose.
- **CON-006:** Do not use generated diagrams or sites as the only canonical
  representation.
- **CON-007:** Do not activate a provisional set without human review.
- **CON-008:** Do not let path placement replace explicit identifier metadata.

## 9. Authoring contract

### Inputs

- repository source and configuration;
- README, documentation, specifications, schemas, and existing decisions;
- applicable organization architecture and policy;
- current implementation evidence;
- known product, human, AI, and publication surfaces;
- existing architecture documents and history.

### Process

1. Discover current architecture evidence.
2. Resolve this specification and every candidate document specification.
3. Select profiles and individual documents from applicability evidence.
4. Build the dependency graph and detect missing nodes.
5. Author in dependency order with focused skills.
6. Preserve existing decisions and evidence during migration.
7. Create `META.md` after the set is known.
8. Run structural, relationship, semantic, and evidence validation.
9. Record omissions, conflicts, and open questions honestly.

### Outputs

- repository-specific canonical architecture documents;
- a complete `META.md` inventory and graph;
- validation evidence;
- a report of created, migrated, omitted, blocked, and unresolved artifacts.

## 10. AI authoring strategy

AI systems shall inspect repository evidence before selecting documents, avoid
generic placeholders, preserve accepted historical content, distinguish target
architecture from current implementation, report conflicting evidence, and
leave drafts provisional when organizational intent requires human acceptance.

## 11. Validation

Validation covers:

- schema-valid materialized frontmatter;
- canonical filenames and stable identifiers;
- governing specification resolution;
- dependency closure and acyclicity;
- one H1 and valid heading progression;
- relative-link integrity;
- `META.md` inventory coverage;
- duplicate concern ownership;
- evidence and uncertainty labeling;
- complete-reference coverage when claimed.

## 12. Acceptance criteria

- [ ] Applicable documents are justified.
- [ ] Intentional omissions are distinct from missing dependencies.
- [ ] Materialized metadata passes the canonical schema.
- [ ] Identifiers are unique and scope-prefixed.
- [ ] Dependencies resolve and the graph is acyclic.
- [ ] Existing architecture history and accepted decisions are preserved.
- [ ] `META.md` inventories the complete set and lifecycle state.
- [ ] Repository-specific content replaces generic placeholders.
- [ ] Current, target, proposed, and unknown states remain distinguishable.
- [ ] Structural, relationship, semantic, and evidence checks pass or have
  explicit exceptions.

## 13. Related artifacts

- `architecture-document`
- `architecture-meta`
- `architecture-authoring`
- `architecture-document.schema.json`
- `validate.py`

