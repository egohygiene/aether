# Changelog

This repository follows release-tag based versioning for install pinning and relies on GitHub generated release notes at tag time.

## Release-notes policy

- Release notes are generated from merged pull requests when maintainers create a repository release tag.
- Installed skill pinning should use repository tags (for example `--pin "v1.0.0"`).
- Artifact-level versions remain in frontmatter/catalog metadata and may evolve independently of repository tag cadence.

## [Unreleased]

- Corrected staged skill inventory checks to distinguish retained current
  evidence from removed copies, with Git membership and negative controls;
  preserved staged source and the broader ledger follow-up (#113).

- Completed source-authoritative agent catalog regeneration and semantic drift
  checks, preserving catalog annotations and source lifecycle while correcting
  local CI continuity metadata consistency (#107).

- Added a draft local CI triage spec, portable skill and bounded agent, with a
  Realm report adapter, diagnosed root-cause grouping, stable duplicate markers,
  sanitized issue proposals and explicit provider handoffs.

- Added draft composable audit profiles and typed checkpoint reports, with
  evidence-bound classifications, immutable report handoffs, and a read-only
  auditor procedure; preserved the approved auditor 2.0.0 specification (#86,
  #68).
- Added a draft architecture coherence review skill, draft portable
  assessment contract, and exact Hygiene governance binding with separately
  trusted human evidence. AI recommendations, human claims, applicability and
  material freshness remain distinct; no architecture is ratified (#87).

- Aligned ADR authoring and decision-impact guidance with ratified Hygiene policy
  v1.1.0, including proposed records, evidence-preserving historical reconstruction,
  legacy index migration, completion handoffs and explicit canary compatibility (#91).

- Connected issue authoring to the pinned candidate title contract and Egolint
  through explicit local discovery, source verification, and managed instruction
  projections; preserved read-only agent permissions and added a synthetic
  consumer check (#98).
- Added the draft bounded worker strategy and Flow suite bootstrap guide for
  small implementation checkpoints, durable handoffs, explicit deferred quality
  work, local validation, and finite audit/refactoring passes.
- Added the capability-aware local validation evidence specification, schema,
  constrained-workspace fixtures, and portable skill for maximizing trustworthy
  local checks while keeping optional emulation and remote CI explicitly deferred
  when unavailable; also reconciled the post-rollout diagnosis skill with the
  repository continuity contract (#83).
- Integrated repository continuity across every canonical first-party skill
  and agent through a reviewed disposition inventory, compact composition
  contracts, managed Codex/Copilot/Claude instruction projections, and
  deterministic resume/completion lifecycle evaluations (#80).
- Added the provider-neutral repository continuity specification, schema,
  bounded root Markdown template, maintenance skill, prototype migration
  report, deterministic fixtures, and downstream integration map (#79).
- Added the versioned organization-wide repository release and changelog
  contract, schema, migration guide, portable authoring skill, Aether
  declaration, and safe Taskfile handoffs (#61).
- Added the review-gated social campaign handoff specification, schema, and portable skill with exact Identity/catalog locks, candidate-only drafts, freshness and checklist gates, digest-bound human approval, external-adapter receipts, deterministic examples, and adversarial tests (#53).
- Documentation overhaul for product-level README, contributor workflow, provenance, release/pinning, and safety guidance.
- Added read-only PR validation and explicit tagged first-party skill release workflows with deterministic rebuild checks and release metadata generation.
- Added strict staging CI validation (`--staging --strict-staging`) to the PR workflow; any unclassified top-level `.staging/` directory now fails CI.
- Published staging evacuation status document (`docs/staging-evacuation-status.md`) covering the current disposition of all 734 staged files, precondition blockers, and bounded residual backlog.
