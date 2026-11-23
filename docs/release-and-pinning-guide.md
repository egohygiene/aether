# Release and Pinning Guide

## Repository release policy

- Repository tags (`vMAJOR.MINOR.PATCH`) are the installable release contract for
  `gh skill install --pin`.
- Artifact frontmatter/catalog versions remain per-artifact metadata and do not
  replace repository tags.
- Breaking changes require a major artifact-version bump and release-note callout.
- Only catalog records with `lifecycle.state: stable` and `release.included: true`
  may appear in a release manifest.
- Deprecation keeps the artifact installable but must name a replacement;
  deletion is reserved for retired IDs and must not rewrite an existing tag.

## Workflow entry points

| Workflow | Trigger | Permissions | Purpose |
| --- | --- | --- | --- |
| `.github/workflows/pr-validation.yml` | `pull_request` | `contents: read` | Deterministic tests and explicit local consumer qualification; no publish credentials |
| `.github/workflows/release-first-party-skills.yml` | Changed release tooling PR, or manual dispatch from the default branch with an existing `release_tag` | PR source qualification and tagged validation are read-only; `contents: write` only in dispatch-only gated publish job | Qualify source independently; explicit immutable tagged publication remains gated |

The publication job targets the `first-party-skill-release` environment. Configure
required reviewers there so publication remains deliberate and reviewable.

## PR validation checks

The pull-request workflow runs:

```sh
./aether distribution build --output-directory "dist"
./aether distribution build --output-directory "dist" --check
./aether validate --format "text"
./aether validate --shell --format "text"
./aether catalog generate --check
python3 catalog/validate_catalog.py
./aether eval run --mode "deterministic" --format "text"
./aether test
python3 -m catalog.consumer_installation --scope local \
  --output ".artifacts/pr-validation/consumer-installation"
```

It also rebuilds `dist/` twice and diffs the results to enforce reproducibility.
Failure uploads contain only command logs and diffs from `.artifacts/`.

## Explicit consumer qualification

`./aether test` uses a simulated external adapter to exercise harness status,
reporting and failure controls deterministically. Passing those tests does not
qualify a real consumer. Run the separate command above with an unused output
directory to test the actual installed GitHub CLI. It builds a temporary
distribution, installs three pilot packages into disposable Git repositories,
validates those packages, runs `gh skill publish --dry-run`, and checks manual
cleanup preserves an unrelated fixture skill. It never publishes.

The report is `consumer-installation-readiness.v1.json` with a diagnostic bundle
when overall readiness is incomplete. Both validation workflows retain the
sanitized consumer receipt on success or failure. The command requires a POSIX
workspace so its per-command deadline can stop the entire process group; stdout
and stderr are drained with bounded buffers.
Missing commands, unsupported preview subcommands or command timeouts are
`blocked`; actual build/install/list/package-validation failures remain failures.
Either prevents qualification. Exit codes are 0 for all required selected
scenarios passing, 1 for incomplete qualification and 2 for invalid arguments or
an unavailable output directory. Existing receipts are never overwritten.

The `portable-package-validation` scenario distinguishes two contracts. It
strictly validates and freezes every pristine export before any installer runs,
then verifies the installed instance's complete inventory/resources, typed
semantic frontmatter and body against that snapshot. Local gh source tracking
must identify the exact selected package; only that verified `metadata.local-path`
field and the observed single blank-LF separator omission are admitted. Source
mutation, links, unexpected fields/files, changed content and ambiguous YAML
fail qualification. A nonempty, unique manifest must account for every file.

Raw installed portability diagnostics remain in `installed_observations` and
`validation_results`. They can report absolute host tracking while the strict
pristine export and verified materialization checks pass. The adapter neither
rewrites the real installation nor globally allows private paths; tracking
remains available to the actual update mechanism. This is local materialization
acceptance, not a claim that the raw installed tree is a portable export.

Local scope requires all five local scenarios. It leaves remote scenarios
explicitly skipped and `overall_status: not-ready`, even if `local_status: ready`.
Use `qualification.complete` together with its `scope` and required scenario list
to assess the selected gate. No skipped or absent required scenario counts as a
pass. Ambient `AETHER_E2E_REMOTE_*` variables cannot select remote work.

For the additional remote install/update checks, explicitly select release scope
and a reviewed existing immutable tag plus its full commit:

```sh
python3 -m catalog.consumer_installation --scope release \
  --remote-repository "egohygiene/aether" --remote-tag "v1.2.3" \
  --remote-commit "<full 40-character commit>" \
  --output ".artifacts/release-consumer-qualification"
```

That scope installs by tag and commit and checks pinned updates preserve a local
modification in disposable repositories. It requires every local and remote
scenario; the release validation job runs this gate explicitly before its
publication dependency. It only qualifies the named pilot scenarios. Release
provenance, payload eligibility, rollback, credentials, host/model compatibility
and actual publication remain separate acceptance work under issue38. This
checkpoint does not provision a compatible `gh skill` adapter or establish that
the broader release workflow can run successfully.

## Release validation and publication flow

1. Create the exact immutable tag from reviewed default-branch history, then
   manually dispatch the workflow from the default branch with `release_tag`.
2. Resolve the existing remote tag to its full commit, check out that commit in a clean runner, and verify it is on current default-branch history. Lightweight and annotated tags are supported. The publication job checks out the validated commit and rechecks the remote tag before rebuilding and immediately before publishing; a moved tag is refused. Workflow-dispatch `GITHUB_SHA` is never the selected release authority.
3. Rebuild `dist/`, rerun deterministic validation/tests/evals and the explicit release-scope consumer gate, and verify two-build reproducibility.
4. Generate release metadata with:

   ```sh
   python3 library/organization/skills/build-release-artifacts.py \
     --release-tag "v1.2.3" \
     --output-directory "dist" \
     --commit-sha "<full 40-character selected source commit>" \
     --payload-directory ".artifacts/release-candidate/payload" \
     --archive ".artifacts/release-candidate/aether-v1.2.3-dist.tar.gz"
   ```

5. Confirm `dist/release/release-manifest.v1.json` matches the approved tag.
6. Run `gh skill publish ".artifacts/release-candidate/payload" --dry-run` only with a compatible adapter. The payload is an unused directory outside `dist/`, built from selected stable skill and eligible governed-catalog inventories plus exactly five release metadata files. Draft skills, unselected provider projections, unlisted files, and prior release outputs are excluded. Manifest escapes, symlinks and special files are refused. The archive has the same exact inventory; nothing is archived by sweeping all of `dist/`.
7. After explicit publication authorization and environment approval, rebuild from the validated full commit, recheck the unchanged tag, rerun the dry-run, and publish the selected payload with:

   ```sh
   gh skill publish ".artifacts/release-candidate/payload" --tag "v1.2.3"
   ```

8. Attach the release bundle archive plus:
   - `dist/release/release-manifest.v1.json`
   - `dist/release/checksums.txt`
   - `dist/release/release-provenance.v1.json`
   - `dist/release/LICENSE.notices.txt`
   - `dist/release/release-notes.md`

The workflow refuses an existing GitHub release or release asset for the tag;
it never replaces a published asset. Tags are never rewritten.

## Release metadata contents

- `release-manifest.v1.json` — repository tag plus release-eligible first-party skills
- `release-manifest.v1.json` may also list release-eligible governed catalogs, with their exact version and digest
- `checksums.txt` — SHA-256 digests for the exact selected payload, including the final provenance file; excludes itself to avoid a hash cycle
- `release-provenance.v1.json` — selected immutable source commit, included artifacts, and digests of selected distribution files plus manifest/license/notes; excludes generated provenance and checksums to avoid self-reference
- `LICENSE.notices.txt` — repository license plus included artifact license summary
- `release-notes.md` — included artifacts plus the current canonical `## [Unreleased]` changelog excerpt (legacy unbracketed input remains recognized)

Repeated metadata generation overwrites only its five named outputs, retains unknown
prior files without including them, and is byte-identical for identical selected
inputs. Before staging the payload, final checksums/provenance must match its
actual bytes. The tar/gzip archive normalizes names, timestamps, ownership and
permission bits while preserving whether a selected resource is executable.
Payload/archive destinations must be unused; no unrelated output is overwritten.

The read-only PR job runs native disposable-Git tag/commit controls and synthetic
stable-selection, archive-inventory, checksum and repeatability cases. It proves
that GitHub parses this workflow and creates its source-qualification job at the
changed revision. It never enters the release validation/publication jobs. This
is not tagged-release job completion or consumer acceptance. `GH_TOKEN` is mapped
explicitly only on CLI steps, with the containing job's scoped token; checkout
does not persist credentials. Secret availability is not asserted by source.

## Preview GitHub CLI compatibility

`gh skill` is an unqualified preview adapter here. The installed CLI may not provide it; missing capabilities keep consumer qualification blocked. These are the existing adapter assumptions to validate before publication:

- `gh skill publish "<selected-payload>" --dry-run` validates without publishing
- `gh skill publish "<selected-payload>" --tag "<tag>"` publishes non-interactively

If GitHub CLI changes the preview contract, update the workflows and this guide in the
same pull request.

## Consumer pinning, updating, and rollback

Install from a pinned release tag:

```sh
gh skill install "egohygiene/aether" \
  "create-purpose-document" \
  --pin "v1.0.0"
```

Inspect or update installed skills:

```sh
gh skill list --json skillName,path,scope,pinned
gh skill update --dry-run
gh skill update --all
gh skill update --unpin
```

Rollback or supersede by publishing a newer repository tag (for example `v1.0.1`)
and asking consumers to repin or update. Do not delete or retag a bad release; mark
the bad tag deprecated in release notes and publish the corrective tag.

### Catalog lockfiles

When a consumer uses a governed catalog, record the repository tag **and** the
catalog identity, version, and digest from `dist/catalogs/<name>/distribution-manifest.v1.json`:

```json
{
  "repository": "egohygiene/aether",
  "repository_release_tag": "v1.2.3",
  "catalog_id": "catalog/social-surface-specs",
  "catalog_version": "1.0.0",
  "catalog_digest": {
    "algorithm": "sha256-utf8-lf",
    "value": "<digest from the release manifest>"
  }
}
```

Only catalogs marked stable, rights-approved, and release-included may appear
in release metadata. An experimental catalog can be evaluated from source but
must not be represented as a published policy snapshot.

## Deprecation versus deletion

- **Deprecate** when a skill should remain discoverable/installable long enough to
  guide consumers to a replacement artifact ID.
- **Retire** only after the replacement/deprecation window is complete.
- **Delete nothing from `.staging/`** unless ADR-0005 conditions are satisfied.

## Relay extraction boundary

These workflows are local to Aether so the repository can validate and publish
independently now. Future Relay extraction candidates are limited to generic,
reusable pieces such as Python setup, deterministic build scaffolding, and common
artifact-upload patterns. Aether-specific validation commands, release-manifest
generation, and skill publication rules stay in this repository.
