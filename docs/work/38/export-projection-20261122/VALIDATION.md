# Build-only skill metadata projection — 2026-11-22

Base: Aether `e5a67e581857122a8131fe8a24d1c7e6c1fa1170`.
Owner: [#38](https://github.com/egohygiene/aether/issues/38).

## Concrete repair

The distribution builder already copied the Identity governing specification
into its declared package-local destination. It also copied the canonical
`metadata.aether-distribution-resources` build instruction into exported
`SKILL.md`, retaining its repository-only source path. The unchanged strict
portable validator rejected that field with `AETHER_PORTABLE_015`.

The builder now consumes and validates that declaration before omitting only
the build-only key from generated frontmatter. Opted-in headers use
deterministic YAML serialization; every other field value and the complete
normalized Markdown body are retained. The explicit narrow exception to
verbatim copying is documented in the builder and canonical frontmatter
contract. Ordinary skills remain exact UTF-8/LF copies.

Canonical skill files are untouched. The existing manifest `source_digest`
still hashes canonical source rather than pretending it hashes the projected
export. All resource bytes, manifests, generated inventories, versions,
maturity and release selection remain unchanged. No arbitrary manifest-v1
field, validator exception or installed-host normalization is introduced.

## Corpus and regression checks

The [observation](projection-observation.json) binds the changed builder hash,
all ten opted-in canonical/projected skill hashes, unchanged body hashes and
declared resource hashes. Actual base-to-generated comparison finds exactly
ten changed generated paths, each an opted-in `SKILL.md`. All 33 ordinary skill
exports and every manifest/resource retain their prior bytes. All 43 canonical
skills match the immutable base.

The five new regression methods cover:

- actual resource bundling plus pristine validation outside canonical source,
  canonical byte preservation, ordinary metadata/body preservation,
  deterministic output and canonical-versus-projected source digests;
- continued strict rejection of genuine runtime canonical paths and installer
  local paths rather than indiscriminate text scrubbing;
- empty/null declarations and flow-style metadata, retaining empty ordinary
  metadata maps where appropriate;
- invalid declarations and resource/output collisions failing before export;
- the actual complete corpus: every current declaring skill is exercised, and
  every ordinary skill remains a verbatim normalized copy.

Existing traversal, canonical/companion/output symlink, output confinement,
partial-generation failure and unexpected-output retention controls also pass.

## Executed results

| Check | Actual result |
| --- | --- |
| Focused `test_build_distributions.py` discovery | 42 tests pass. |
| `./aether test` | 410 discovered: 399 passed, 11 existing optional/native skips. |
| `./aether catalog generate` | Pass; catalog bytes unchanged because canonical skill content is unchanged. |
| Distribution build and `--check` | Pass, all generated families current. |
| `./aether validate --format text` | Pass; the existing `AETHER_PROVENANCE_009` staging warning remains unchanged. |
| Pristine `author-project-identity` strict portability | Pass with zero diagnostics and the existing validator unchanged. |
| Roadmap receipt, continuity structure and staged whitespace | Validated separately at handoff; no official released EgoLint conformance claim. |

Eight of the ten declaring packages now pass pristine strict portability.
`audit-repository` retains separate historical `015`/`016` findings, and
`create-repository-journal` retains a separate `015` finding. These are actual
remaining runtime/provenance content findings, not the removed build directive;
the observation records their file/rule identities. This checkpoint neither
erases those sources nor relabels them passed.

## Remaining acceptance and decision impact

The installed-host adapter must still distinguish verified CLI-injected
tracking from a pristine portable artifact. Historical pilot dependencies,
actual installation/update/release qualification, stable promotion and remote
consumer acceptance remain separate #38 work. A pristine source pass is not
observed agent behavior or full readiness. No global installation, hosted
workflow, tag, release or publication was performed.

Decision impact: reference preserved ADR-0001/ADR-0002 for canonical/generated
ownership. The documented build-only projection implements those existing
boundaries and the already-selected #38 repair; no new architecture or ADR
lifecycle is selected. Historical decisions and proposed ADR-0009 are preserved.

Roadmap impact: **not-affected**, AET-Q01/AET-Q05. The bounded repair advances
existing work without strategic resequencing or completing release milestones.
