# Aether agent guidance

Read this file before changing Aether. Canonical source is under
`library/organization/` and `catalog/`; `.staging/` and `dist/` are derived or
migration evidence, not source.

## Release convention

Every active Ego Hygiene repository follows the versioned
[`repository-release`](library/organization/specs/release/repository-release.spec.md)
contract. Its local declaration is `.egohygiene/release.json`; its root
`CHANGELOG.md` retains an exact `## [Unreleased]` section.

Before changing release behavior, inspect the declaration, version authority,
changelog, existing immutable tags, and repository-owned release workflow.
Use `release:plan`, `release:prepare`, and `release:verify` to make a reviewed
candidate. `release:publish` is an explicit handoff only: do not create tags,
publish packages, deploy sites, use registry credentials, or overwrite release
assets unless the user separately authorizes that exact external action.

Commit messages may inform a semantic-version recommendation, but the reviewed
release plan and declared version authority decide the version. Follow the
shared Conventional Commit work in `egohygiene/egohygiene#284` without letting
it silently rewrite a release.

## Aether boundaries

Aether owns provider-neutral specifications, schemas, skills, and agent
guidance. Relay owns reusable immutable execution; Hygiene owns applicability
policy; Egolint owns conformance validation; Pace observes adoption before it
proposes remediation. Keep provider credentials and delivery adapters in their
consumer repository.

Run the relevant deterministic validation and regenerate `dist/` and the
first-party catalog after changing canonical source.
