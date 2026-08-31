# Changelog

This repository follows release-tag based versioning for install pinning and relies on GitHub generated release notes at tag time.

## Release-notes policy

- Release notes are generated from merged pull requests when maintainers create a repository release tag.
- Installed skill pinning should use repository tags (for example `--pin "v1.0.0"`).
- Artifact-level versions remain in frontmatter/catalog metadata and may evolve independently of repository tag cadence.

## [Unreleased]

- Added the versioned organization-wide repository release and changelog
  contract, schema, migration guide, portable authoring skill, Aether
  declaration, and safe Taskfile handoffs (#61).
- Added the review-gated social campaign handoff specification, schema, and portable skill with exact Identity/catalog locks, candidate-only drafts, freshness and checklist gates, digest-bound human approval, external-adapter receipts, deterministic examples, and adversarial tests (#53).
- Documentation overhaul for product-level README, contributor workflow, provenance, release/pinning, and safety guidance.
- Added read-only PR validation and explicit tagged first-party skill release workflows with deterministic rebuild checks and release metadata generation.
- Added strict staging CI validation (`--staging --strict-staging`) to the PR workflow; any unclassified top-level `.staging/` directory now fails CI.
- Published staging evacuation status document (`docs/staging-evacuation-status.md`) covering the current disposition of all 734 staged files, precondition blockers, and bounded residual backlog.
