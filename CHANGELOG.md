# Changelog

This repository follows release-tag based versioning for install pinning and relies on GitHub generated release notes at tag time.

## Release-notes policy

- Release notes are generated from merged pull requests when maintainers create a repository release tag.
- Installed skill pinning should use repository tags (for example `--pin "v1.0.0"`).
- Artifact-level versions remain in frontmatter/catalog metadata and may evolve independently of repository tag cadence.

## Unreleased

- Documentation overhaul for product-level README, contributor workflow, provenance, release/pinning, and safety guidance.
- Added read-only PR validation and explicit tagged first-party skill release workflows with deterministic rebuild checks and release metadata generation.
