# Repository release authoring guidance

The full policy is `repository-release`. Use this guide to make the narrow
decisions that a declaration records.

## Choose one profile

- Use `contract` for standards, catalogs, and reusable configuration.
- Use `cli-library`, `python-package`, or `npm-package` when a package or
  binary has an explicit public compatibility promise.
- Use `container-image` when the immutable digest is a released deliverable.
- Use `static-site` when a build is released independently from deployment.
- Use `publication` when editions, PDFs, or archival artifacts differ from
  source-code versioning.
- Use `workspace` when multiple components must name their own authorities.
- Use `internal-only` for a real internal release with a disclosed boundary.

Do not use a profile to claim a registry, deployment, DOI, or signature that is
not configured. Mark the relevant channel or evidence as `external`,
`unavailable`, or `not-applicable`.

## Preserve one authority

The version authority is the source that a release plan compares rather than
rewrites. For example, a Rust crate can use `Cargo.toml`, a Python package can
use `[project].version`, an npm package can use `package.json`, and a
publication can use its edition metadata. A Git tag identifies the immutable
repository release but does not replace a component's authority.

## Keep preparation reviewable

Prepare a release by changing the chosen authority and promoting the reviewed
`Unreleased` changelog entry in a release PR. A manual default-branch workflow
may publish the accepted candidate after verification. A conventional commit is
useful evidence for a bump but cannot silently determine a publication.
