---
schema: aether.specification/v1
id: repository-release
title: Repository Release and Changelog Specification
kind: specification
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-08-31
updated: 2026-08-31
domain: release
tags:
  - release-engineering
  - semantic-versioning
  - changelog
  - provenance
  - rollback
  - taskfile
applies_to:
  - active-repositories
  - repository-releases
  - package-releases
  - container-releases
  - site-releases
  - publication-releases
depends_on: []
related: []
supersedes: []
source_files:
  - repository-release.spec.md
---

# Repository Release and Changelog Specification

## Purpose and authority

This specification defines the provider-neutral release convention for Ego
Hygiene repositories. It governs release intent, semantic versioning,
changelogs, evidence, rollback information, and the boundary between a
repository release and its delivery adapters.

It does not prescribe a release tool. A repository may use a Taskfile, a
language-native tool, a reviewed GitHub workflow, or a future Relay action so
long as it honors this contract. Aether owns this contract and authoring
guidance. Relay owns reusable immutable execution. Hygiene owns applicability
policy, Egolint owns conformance validation, and Pace observes adoption before
it proposes any remediation.

The canonical machine-readable declaration is
`.egohygiene/release.json`, validated by
`catalog/schemas/aether.repository-release.v1.schema.json`. Its semantic
identity is `egohygiene.repository-release/v1`.

## Core invariants

1. Every active repository has a root `CHANGELOG.md` with a `## [Unreleased]`
   section and promoted, dated releases in Keep a Changelog 1.1 format.
2. A repository release tag is exact `vMAJOR.MINOR.PATCH` and immutable. A
   moving major alias is optional discovery metadata, never a production pin.
3. Every declared component has exactly one `version_authority`. A release
   plan compares every derived version to that authority; it does not select a
   convenient value from several conflicting files.
4. Conventional Commit data may recommend a semantic bump, but a reviewed
   release plan and the declared version authority decide the release. An
   ordinary pull request neither tags nor publishes.
5. A release declares unavailable, external, and not-applicable evidence
   explicitly. A GitHub Release never proves that a registry package, image,
   site deployment, DOI, or archive provider completed.
6. Immutable release artifacts are never overwritten. Recovery occurs through
   a revert, channel revocation, prior-artifact redeployment, or a corrected
   successor release.

## Release profiles and component authority

Each declaration selects one repository profile:

| Profile | Typical authoritative component source | Typical delivery boundary |
| --- | --- | --- |
| `contract` | versioned catalog or Git tag | GitHub Release evidence |
| `cli-library` | Cargo manifest or package metadata | binary/archive and optional registry |
| `python-package` | `[project].version` in `pyproject.toml` | wheel/sdist and optional PyPI |
| `npm-package` | `package.json` | tarball and optional npm registry |
| `container-image` | release tag plus immutable image digest | GitHub evidence and registry digest |
| `static-site` | workspace/package metadata or Git tag | GitHub evidence and separate deployment |
| `publication` | publication metadata or edition record | PDF/A/evidence and separate archive/DOI |
| `workspace` | declared workspace manifest/component authorities | one or more component deliveries |
| `internal-only` | explicit local authority | internal distribution or evidence only |

`archived` repositories retain their historical changelog and declaration but
set release state to `frozen`. They do not silently appear release-capable.
An `unreleased` active repository can have no prior tag; it still records the
future tag shape and release behavior.

## Versioning and changelog policy

Semantic Versioning applies to a repository's public compatibility promise, not
to every commit. Before 1.0, repositories document their compatibility policy;
breaking changes remain visible in the changelog. A component's authoritative
source may be a Git tag, Cargo manifest, Python project metadata, `package.json`,
container tag/digest record, publication metadata, catalog record, workspace
manifest, or an explicitly external system.

For a public component at 1.0 or later, an incompatible supported-interface
change requires a major-version decision and a changelog callout. Before 1.0,
the repository declares its compatibility promise and still calls out breaking
changes; `0.x` is not permission to hide them. Deprecation keeps the immutable
release record and names a replacement or removal horizon where one is known.
Removal occurs only in a later compatible release decision or a documented
retirement; it never edits historical tags, assets, or changelog entries.

The changelog has one human-maintained `Unreleased` section. A release
preparation promotes that content to `## [X.Y.Z] - YYYY-MM-DD`; it never
silently generates claims from commit text. Commit messages follow the shared
convention being aligned in `egohygiene/egohygiene#284`, but are advisory input
to the release plan rather than an unreviewed mutation authority.

## Lifecycle and authority boundaries

The required task interface is:

1. `release:plan` — read the declaration and summarize the proposed release;
2. `release:prepare` — materialize the chosen version/changelog changes in a
   reviewable release PR or working-tree handoff;
3. `release:verify` — verify the reviewed candidate, version authority,
   changelog, and selected artifact profile; and
4. `release:publish` — hand off an already reviewed default-branch release to
   an explicit manual publication workflow.

`release:publish` is not permission to publish from a local task by default.
The GitHub workflow is manually dispatched, checks the current default-branch
revision, and scopes write authority to its publication job. It delegates
immutable GitHub Release evidence to Relay where an applicable Relay profile is
available. Registry, container, site, package-manager, DOI, and archival
credentials remain repository-owned adapters.

## Evidence and rollback

Every candidate records its represented source revision, changelog decision,
selected profile, complete artifact checksums, provenance/SBOM/signature state,
and rollback instructions. `required` means the candidate must fail without
the evidence. `external` means a separate owner must attest it. `unavailable`
means the evidence is not currently produced and must not be treated as green.

When a release is wrong, never mutate its immutable tag or release asset. Use
the declaration's rollback strategy:

- `revert-and-successor-tag` for source or contract corrections;
- `revoke-channel` for package/container distribution;
- `redeploy-prior-artifact` for sites; or
- `freeze` for historical/archived repositories.

## Consumer and migration rules

New repositories begin with the declaration template and a root changelog.
Existing repositories first inventory their current tags, version sources,
changelog, workflows, and external channels. They select one profile, state
unknowns honestly, and then add the four Taskfile handoffs without replacing a
working repository-specific release process in the same change.

Read [the migration guide](../../../../docs/repository-release-convention.md)
before changing an existing release path. Use the portable
`prepare-repository-release` skill when authoring or reviewing a declaration.
Future Hygiene, Relay, Egolint, and Pace work consumes this specification by
versioned identifier; it must not fork its rules into copied workflow files.
