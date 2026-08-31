---
name: prepare-repository-release
description: Authors or reviews a versioned repository release declaration and changelog plan. Use when establishing, migrating, or checking a semantic release convention; do not use to publish packages, tags, images, sites, or archives.
license: MIT
compatibility:
  required_tools:
    - python3
metadata:
  aether-version: "1.0.0"
  aether-status: "draft"
  aether-spec-id: "repository-release"
  aether-scope: "organization"
  aether-domain: "publishing"
  aether-owners: "egohygiene"
  aether-created: "2026-08-31"
  aether-updated: "2026-08-31"
  aether-executable-resources:
    - "scripts/validate-release-declaration.py"
  aether-distribution-resources:
    - source: "catalog/schemas/aether.repository-release.v1.schema.json"
      destination: "references/aether.repository-release.v1.schema.json"
    - source: "library/organization/specs/release/validate.py"
      destination: "scripts/validate-release-declaration.py"
---

# Prepare Repository Release

Create or review a repository release plan governed by `repository-release`.
This skill makes the release decision inspectable; it does not grant tag,
registry, deployment, signing, or archival authority.

## Inspect first

Read the repository's `.egohygiene/release.json`, `CHANGELOG.md`, version
authority files, current immutable tags, and release workflow before proposing
a change. Treat commit messages as bump recommendations only. The declared
version authority and a reviewed release plan decide the version.

Use the [declaration template](templates/repository-release.json) for a new
repository and [authoring guidance](references/release-authoring.md) for a
migration. The packaged schema is authoritative for the declaration shape.

## Plan and prepare

1. Select one repository profile and record any independent components.
2. Give every component exactly one version authority; do not synchronize
   conflicting files by guesswork.
3. Keep `## [Unreleased]` in the root changelog and draft the dated promoted
   release entry for human review.
4. State each delivery/evidence condition as configured, external,
   unavailable, or not-applicable. Do not imply external publication occurred.
5. Record rollback instructions that preserve immutable tags and assets.

Validate a local candidate with the portable reference validator:

```bash
python3 "scripts/validate-release-declaration.py" \
  --repository "." \
  --release-version "v1.2.3" \
  --format "json"
```

## Handoff boundaries

Use `release:plan`, `release:prepare`, and `release:verify` to create and
check a reviewed candidate. `release:publish` hands off only an approved,
current-default-branch candidate to the repository-owned manual workflow.
Relay can preserve immutable GitHub Release evidence, but registry, container,
site, DOI, archive, and signing adapters remain separately authorized.

Never force-update an exact version tag, overwrite release assets, publish
from an ordinary pull request, or treat missing external evidence as success.
