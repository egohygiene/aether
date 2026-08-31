# Repository release convention

[`egohygiene.repository-release/v1`](../library/organization/specs/release/repository-release.spec.md)
gives every active Ego Hygiene repository a small, inspectable release
contract. It standardizes the decision boundary without forcing one release
tool, package registry, hosting provider, or deployment system.

The canonical declaration is `.egohygiene/release.json`; the formal
[JSON Schema](../catalog/schemas/aether.repository-release.v1.schema.json)
defines its shape. Start from the portable
[`prepare-repository-release`](../library/organization/skills/publishing/prepare-repository-release/)
skill template when adding one.

## The release model

These are intentionally different things:

| Concept | Authority | Rule |
| --- | --- | --- |
| Repository release | Exact immutable `vMAJOR.MINOR.PATCH` Git tag | Pins a reviewed repository snapshot; never force-move it. |
| Component version | Exactly one declared `version_authority` | A manifest, catalog, or external record decides the component version. |
| Deployment build | Provider-specific commit/build identifier or digest | Evidence for a site or image deployment, not a substitute release version. |
| External channel | Explicit delivery state and receipt | Registry, archive, DOI, or distribution evidence remains external until attested. |

Commit messages can recommend a semantic bump under the shared Conventional
Commit work tracked in `egohygiene/egohygiene#284`. They do not author a
version, changelog claim, tag, or publication by themselves.

For supported public interfaces at 1.0 or later, breaking changes require an
explicit major-version decision and changelog callout. Before 1.0, a repository
states its compatibility promise and still calls out breaking changes. A
deprecation keeps its immutable historical release record, names a replacement
or removal horizon when known, and is removed only through a later reviewed
release decision.

## Minimum declaration

Every active repository records its profile, local authority, delivery state,
evidence state, rollback path, four Taskfile handoffs, and manually dispatched
GitHub workflow. A no-release or archived repository retains the declaration
with `release.state: "frozen"` and honest `not-applicable`/`unavailable`
channels rather than pretending it can publish.

```json
{
  "schema_version": "egohygiene.repository-release/v1",
  "repository": {"id": "egohygiene/example", "lifecycle": "active", "release_profile": "python-package"},
  "release": {"state": "unreleased", "tag_prefix": "v", "immutable_tags": true, "major_alias": "optional"},
  "changelog": {"path": "CHANGELOG.md", "format": "keep-a-changelog/1.1", "unreleased_heading": "Unreleased"}
}
```

The complete template adds components, delivery, evidence, and automation;
the schema requires all of them. Its root `CHANGELOG.md` always has an exact
`## [Unreleased]` heading. A dated entry is promoted through a reviewed release
PR, not generated from commits without review.

## Profile examples

Use these representative authorities and delivery statements. They are examples
of truthful declarations, not publisher configuration to copy blindly.
Schema-valid documents for every row (with the Python package in
`valid.json`) live in
[`catalog/fixtures/aether.repository-release.v1.schema/examples/`](../catalog/fixtures/aether.repository-release.v1.schema/examples/).

| Profile | Component / `version_authority` | Typical channel and evidence boundary |
| --- | --- | --- |
| Contract | `catalog` / `catalog-record` at `catalog/first-party/catalog.v1.json` | GitHub Release evidence may be `configured`; SBOM/signature may remain `unavailable`. |
| Rust tool or crate | `crate` / `cargo-manifest` at `Cargo.toml` | GitHub binary release plus a separately configured or `external` crate registry. |
| Python package | `python-package` / `pyproject-project` at `pyproject.toml` | Wheel/sdist and PyPI receipt; PyPI credentials remain repository-owned. |
| npm library or app | `npm-package` / `package-json` at `package.json` | npm receipt is separate from a GitHub Release. |
| Container image | `container-image` / `container-tag` plus immutable digest record | Registry digest and provenance record are required evidence; never overwrite an image tag. |
| Static site | `static-site` / workspace or package authority | Deployment build/URL is a separate receipt; roll back by redeploying a prior artifact. |
| Publication | `publication` / `publication-metadata` | Archive and DOI are explicitly `external` until the provider attests them. |
| Workspace | `workspace` / `workspace-manifest`, with per-component authorities | One release can have multiple channels; each is reported independently. |
| Internal-only or archived | `internal` / explicit local or `external` authority | Internal delivery is explicit; archived repositories use `frozen` and do not prepare a new tag. |

## Adoption sequence

1. Inventory existing tags, changelog, version files, workflows, registries,
   images, deployments, archives, and recovery procedures.
2. Choose one profile and one authority per component. Mark unknown,
   unavailable, external, and not-applicable states truthfully.
3. Add `.egohygiene/release.json` and `CHANGELOG.md` with `## [Unreleased]`.
4. Add the read-only `release:plan`, reviewable `release:prepare`, verification
   `release:verify`, and handoff-only `release:publish` Taskfile interface.
5. Make the publication workflow manually dispatchable from the default branch.
   Its publication job may receive scoped credentials after explicit approval;
   normal PR validation remains read-only.
6. Validate the declaration before changing a repository's actual publisher:

   ```bash
   python3 "library/organization/specs/release/validate.py" \
     --repository "." \
     --release-version "v1.2.3" \
     --format "json"
   ```

Do not replace a working repository-specific release process in the same PR
that adds the contract. First make the facts visible, then migrate individual
delivery adapters in their own reviewed changes.

## Evidence and recovery

Release evidence covers the source revision, selected changelog content,
artifact checksums, provenance, SBOM/signature state, and each external channel
receipt. `required` must block the candidate when missing; `external` means a
separate owner must provide it; `unavailable` is not success.

Tags and released assets are immutable. Correct a source/contract release with
a revert and successor tag; revoke a distribution channel when supported;
redeploy a previous artifact for a site; or freeze an archived record. Never
retag, overwrite, or silently edit a published asset.
