---
schema: aether.architecture-document/v1
id: aether-ontology
title: Aether Ontology
kind: architecture-document
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-08-19
updated: 2026-08-19
governed_by:
  - architecture-ontology
depends_on:
  - aether-purpose
  - aether-vision
  - aether-principles
  - aether-epistemology
related:
  - aether-pillars
  - aether-manifesto
  - aether-ai-constitution
  - aether-personal-model
supersedes: []
---

# Aether Ontology

## Domain scope

Aether models the concepts needed for make AI behavior contracts reusable, inspectable, versioned, testable, and installable across the organization. The ontology names conceptual entities and relationships; it is not a source-code class model, API schema, or database design.

## Canonical concepts

| Concept | Meaning |
| --- | --- |
| Specification | A canonical concept in the Aether domain whose exact fields belong to specifications or schemas, not this ontology. |
| Skill | A canonical concept in the Aether domain whose exact fields belong to specifications or schemas, not this ontology. |
| Agent | A canonical concept in the Aether domain whose exact fields belong to specifications or schemas, not this ontology. |
| Instruction | A canonical concept in the Aether domain whose exact fields belong to specifications or schemas, not this ontology. |
| Evaluation | A canonical concept in the Aether domain whose exact fields belong to specifications or schemas, not this ontology. |
| Catalog record | A canonical concept in the Aether domain whose exact fields belong to specifications or schemas, not this ontology. |
| Distribution | A canonical concept in the Aether domain whose exact fields belong to specifications or schemas, not this ontology. |
| Provenance | A canonical concept in the Aether domain whose exact fields belong to specifications or schemas, not this ontology. |
| Consumer override | A canonical concept in the Aether domain whose exact fields belong to specifications or schemas, not this ontology. |

## Core relationships

- A repository or person provides source context to one or more domain artifacts.
- A specification constrains how an artifact is interpreted or produced.
- A plan separates proposed action from execution.
- Evidence supports a claim; a decision authorizes a durable direction.
- Provenance connects derived artifacts to their inputs and processing context.
- A consumer integrates through an explicit interface rather than internal structure.

## Boundaries

- Conceptual identity is distinct from filesystem path, database identifier, or display label.
- Observed state is distinct from desired state.
- Proposed relationships are not accepted facts.
- Neighboring repositories retain ownership of their domain concepts.

## Evidence and uncertainty

- **Observed:** The repository README and checked-in implementation establish the canonical first-party library of reusable AI specifications, skills, agent source, schemas, catalogs, and distributions.
- **Decided for this draft:** The repository owns the bounded concern described here and participates through versioned contracts.
- **Proposed:** Target systems and later roadmap phases remain proposals until accepted and implemented.
- **Open question:** Which parts of this draft should become active in the first independently versioned release?
