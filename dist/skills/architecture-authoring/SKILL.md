---
name: architecture-authoring
description: Guides selection, sequencing, authoring, updating, and validation of
  architecture documents for a repository, product, platform, or organization. Use
  when establishing, repairing, or planning a set of architecture documents.
license: MIT
metadata:
  aether-version: 1.2.0
  aether-status: draft
  aether-spec-id: architecture-document
  aether-scope: organization
  aether-domain: architecture
  aether-owners: egohygiene
  aether-created: '2026-08-01'
  aether-updated: '2026-11-23'
---

# Architecture Authoring

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

For repository-scoped work, compose `maintain-repository-continuity` in
**Resume** mode before selecting work. After an authorized repository change
passes domain validation, compose **Refresh** and **Verify** immediately before
presenting the pull request, and include the reconciled root `CONTINUITY.md` in
the same change. A policy-permitted no-change or exemption result must be
documented instead of fabricating an edit.

- **Contribute:** Selected architecture contracts, cross-document effects, validation, and unresolved decisions
- **Never claim:** That proposed architecture is accepted or implemented without evidence

## Purpose

Guide a human or AI agent through selecting, sequencing, authoring, updating,
and validating architecture documents for a repository, product, platform, or
organization.

This is an orchestrator skill. It does not replace focused document-specific
skills such as `create-purpose-document` or `create-system-document`.

## Use This Skill When

Use this skill when the task involves:

- establishing an architecture-document set
- deciding which architecture documents are necessary
- authoring multiple related architecture documents
- repairing inconsistent architecture documentation
- validating architecture dependencies
- planning the order of architecture work
- assessing whether a repository is missing canonical architecture artifacts

## Required Inputs

Resolve as much of the following as possible:

- repository or system scope
- applicable Aether bundle
- existing architecture documents
- existing decisions and constraints
- repository source and configuration
- product or organizational context
- applicable architecture specifications
- known unresolved questions

When required evidence is unavailable, record the limitation instead of
inventing context.

## Workflow

### 1. Discover Existing Architecture

Inspect canonical architecture directories, root documents, decisions,
specifications, implementation plans, repository documentation, source
boundaries, and runtime configuration.

### 2. Resolve Applicable Specifications

Read the bundled `architecture-document` 2.1.1 parent contract at
`references/architecture/document.spec.md`, `architecture-set` 1.0.0 at
`references/architecture/set.spec.md`, and their structural schema at
`references/architecture/architecture-document.schema.json`.

Then resolve each selected document-specific specification by identifier and
version from the applicable bundle or catalog. A canonical-source invocation
may resolve the same resources through the declared build-resource mapping;
installed use needs only the package-local files. Missing governing resources
or document-specific specifications are blocked inputs, not permission to
invent their requirements or claim complete set validation.

### 3. Build the Architecture Graph

Capture identifiers, categories, dependencies, consumers, related artifacts,
supersession, missing nodes, and unresolved edges.

### 4. Select the Necessary Document Set

Choose only the documents justified by the repository's complexity and needs.

### 5. Determine Authoring Order

Use dependency metadata as the source of truth.

### 6. Invoke Focused Skills

Use focused skills such as:

    create-purpose-document
    create-vision-document
    create-principles-document
    create-system-document
    create-architecture-document
    create-roadmap-document

### 7. Validate Cross-Document Consistency

Check terminology, ownership, dependency direction, duplicated concepts,
conflicting decisions, hidden assumptions, unsupported claims, unresolved
references, superseded concepts, and implementation drift.

### 8. Validate Each Document

Perform structural, relationship, semantic, and evidence validation.

### 9. Report Results

Report documents created, updated, omitted, blocked, or requiring follow-up.

## Constraints

- Do not invent organizational intent.
- Do not hide contradictory architecture.
- Do not duplicate canonical ownership.
- Do not create unnecessary placeholder documents.
- Do not treat implementation state as automatically authoritative.
- Do not rewrite unrelated documents without explicit scope.
- Do not expose private reasoning as evidence.
- Do not claim completeness when required dependencies are missing.

## Completion Criteria

The skill is complete when the applicable specifications are resolved, the
necessary document set is justified, authoring order is explicit, focused skills
are selected, changed documents pass validation, and unresolved work is visible.

## Staged Variant

A historical staged candidate carries the same `architecture-authoring` name.
The canonical skill owns architecture-document selection, sequencing and
validation; the candidate may contain additional detail or divergent framing.
This portable edition does not promote, retire or delete that candidate.

[Issue 16](https://github.com/egohygiene/aether/issues/16) retains the comparison
and review obligation. Repository-only source history records the exact former
locator and bytes. Compare unique guidance before any separately authorized
retirement; do not replace canonical source with the candidate wholesale.
