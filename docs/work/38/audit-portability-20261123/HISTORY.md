# Audit portability source history

Issue: [Aether #38](https://github.com/egohygiene/aether/issues/38).
Immutable pre-change source:
`dc3549c8a23bed5fb551a458a22605e7e0777822`.

This repository-only record preserves the full source layout and exact bytes
that are unnecessary in an installed audit workflow. It is not another skill,
governing specification, source promotion or installed execution input. The
[inventory](source-history.json) binds every original/archive pair by actual
bytes and SHA-256. Git retains the same originals at the immutable baseline.

## Historical migration mapping

The original reconciliation inspected baseline
`5077797448d32a59b06eabe4b38f091137d58052`. Its source mapping stays explicit:

| Portable source identity | Original source path | SHA-256 |
| --- | --- | --- |
| `staged-repository-audit-skill` | `.staging/skills/repository-audit/SKILL.md` | `af9f21603e9f99f9e732083fd3a1f673234162155f9fc37cef212f9bb047a7ef` |
| `staged-auditor-agent` | `.staging/agents/auditor.agent.md` | `0ae0ca6b156c6dc1a5764a2d7d53f45075ba4b0849e5cdcdbb1f4e351b214928` |
| `auditor` | `library/organization/specs/quality/auditor.spec.md`, approved2.0.0 | `f9f4d56673cefac4233fad4d53c78d1ba0726201b7e097bb78f67a721b81e62f` |

The [exact original reconciliation](history/staged-reconciliation-before.md)
retains every original path and behavior disposition. The installed summary
keeps these source identities/hashes and all per-behavior dispositions, including
the rejected edit/execute tools and monolith paths. The two staging disposition
records now point here for the full mapping. Their original records are retained
in [the archive](history/), with `preserve-migration-evidence`, reconstructed
hash status and restricted trust classification unchanged. No staged file or
approved source is deleted, edited or promoted.

## Draft source editions

| Source | Before | Candidate | Disposition |
| --- | --- | --- | --- |
| `audit-repository` | draft1.2.1 | draft1.2.2 | Add exact package-local governing resources and portable historical summary. |
| `repository-audit-data` | draft1.0.1 | draft1.0.2 | Keep both machine contracts1.0.0; identify their owners and complete governing resource mapping without requiring the source checkout. |
| `specfile` | draft2.0.0 | draft2.0.1 | Preserve naming/canonical-placement obligations; distinguish repository layout from installed projections. |
| `auditor` | approved2.0.0 | same exact bytes | Preserve status, behavior, metadata and its declared `specfile` dependency. |

Artifact versions record authored source revisions; they do not create a
repository release or override release eligibility. These are current draft
editions, not edits to an immutable published tag or release asset. No old Git
object, approval or historical source version is replaced. The approved auditor
continues to declare `specfile` by stable ID; the package resolves that dependency
to the exact selected draft authoring standard without assigning it approval.

## Specfile Section 4 before/after requirements map

The [exact draft2.0.0](history/specfile-2.0.0.spec.md) is retained. Section 4's
four explicit `shall` bullets stay byte-identical:

| Original requirement | Candidate preservation |
| --- | --- |
| `use lowercase kebab-case` | Unchanged. |
| `end with .spec.md` | Unchanged, including code formatting. |
| `have one canonical location` | Unchanged; installed copies are explicitly projections, not additional canonical locations. |
| `avoid conflicting duplicate copies` | Unchanged. |

The repository-local example `.github/specs/` stays unchanged. The two
publisher-layout examples `library/organization/specs/` and
`library/community/specs/` remain exact in the archived source and remain the
owning repository's source placement. No canonical source moves: the existing
`ARCHITECTURE.md` topology and catalog path selection are untouched. The new
paragraph explicitly retains those first-party/community locations and forbids
relaxing their placement; it identifies owner architecture/catalog as the
source-layout authority. It does not encode those paths in order to evade a
validator.

The clarification addresses a different concern: an installed audit package
must resolve its exact governing ID/version through its declared local resource
mapping without cloning the publisher's repository. The package includes
byte-identical `specfile`, approved `auditor` and `repository-audit-data`, closing
the extension's two dependencies and the foundation's `specfile` dependency.
Related-artifact IDs are not silently turned into governing prerequisites.

All text outside Section 4 and version/update metadata in `specfile` remains
unchanged. All text outside the source-mapping section and version/update
metadata in `repository-audit-data` remains unchanged. No approved requirement,
profile schema, helper, read-only agent tool ceiling or lifecycle is rewritten.

## Decision and roadmap impact

Reference preserved ADR-0001/0002/0004/0005 for canonical/generated ownership,
neighboring owners, artifact-versus-release versions and staging preservation.
No new source location, artifact kind, distribution channel, approval boundary
or versioning scheme is introduced. The known ADR-0002/0006 conflict and proposed
ADR-0009 remain unchanged.

The existing #38 consumer gate and AET-Q01/AET-Q05 own this partial portability
repair. A local audit package pass does not establish whole-pilot, remote
install/update/rollback, stable maturity, observed model behavior or release
acceptance. The separate checkpoint handoff retains actual validation outcomes.
