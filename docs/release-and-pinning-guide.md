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
| `.github/workflows/pr-validation.yml` | `pull_request` | `contents: read` | Deterministic PR validation only; no publish credentials |
| `.github/workflows/release-first-party-skills.yml` | tag push `v*` or manual dispatch with `release_tag` | read-only validation job, `contents: write` only in gated publish job | Explicit tagged publication |

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
gh skill publish "dist" --dry-run
```

It also rebuilds `dist/` twice and diffs the results to enforce reproducibility.
Failure uploads contain only command logs and diffs from `.artifacts/`.

## Release validation and publication flow

1. Resolve an explicit tag from `workflow_dispatch.release_tag` or the pushed tag.
2. Check out the tagged commit in a clean runner.
3. Rebuild `dist/`, rerun deterministic validation/tests/evals, and verify two-build reproducibility.
4. Generate release metadata with:

   ```sh
   python3 library/organization/skills/build-release-artifacts.py \
     --release-tag "v1.2.3" \
     --output-directory "dist" \
     --commit-sha "<sha>"
   ```

5. Confirm `dist/release/release-manifest.v1.json` matches the approved tag.
6. Run `gh skill publish "dist" --dry-run`.
7. After environment approval, rebuild from the same tag, rerun the dry-run, and publish with:

   ```sh
   gh skill publish "dist" --tag "v1.2.3"
   ```

8. Attach the release bundle archive plus:
   - `dist/release/release-manifest.v1.json`
   - `dist/release/checksums.txt`
   - `dist/release/release-provenance.v1.json`
   - `dist/release/LICENSE.notices.txt`
   - `dist/release/release-notes.md`

If a GitHub release already exists for the tag, the workflow skips `gh skill publish`
and only refreshes attached assets with `gh release upload --clobber`. Tags are never rewritten.

## Release metadata contents

- `release-manifest.v1.json` — repository tag plus release-eligible first-party skills
- `checksums.txt` — SHA-256 digests for generated release payload files
- `release-provenance.v1.json` — source commit, included artifacts, and output digests
- `LICENSE.notices.txt` — repository license plus included artifact license summary
- `release-notes.md` — included artifacts plus the current `## Unreleased` changelog excerpt

## Preview GitHub CLI compatibility

`gh skill` is currently preview functionality. The workflows assume the current CLI contract:

- `gh skill publish "dist" --dry-run` validates without publishing
- `gh skill publish "dist" --tag "<tag>"` publishes non-interactively

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

## Deprecation versus deletion

- **Deprecate** when a skill should remain discoverable/installable long enough to
  guide consumers to a replacement artifact ID.
- **Retire** only after the replacement/deprecation window is complete.
- **Delete nothing from `.staging/`** unless ADR-005 conditions are satisfied.

## Relay extraction boundary

These workflows are local to Aether so the repository can validate and publish
independently now. Future Relay extraction candidates are limited to generic,
reusable pieces such as Python setup, deterministic build scaffolding, and common
artifact-upload patterns. Aether-specific validation commands, release-manifest
generation, and skill publication rules stay in this repository.
