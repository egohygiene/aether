# Portable architecture governing resources — November 23, 2026

Issue: [#38](https://github.com/egohygiene/aether/issues/38). Base:
`dc3549c8a23bed5fb551a458a22605e7e0777822` after merged141→142.
Exact tested source: `8848f2f19904f5cc432d6438e8f6dedbcc17bbe8`.
Later handoff files add evidence/continuity rather than relabeling that run.

## Actual behavior and preserved contracts

The two architecture pilots now carry their actual governing resources instead
of requiring a canonical checkout at runtime. The orchestrator includes parent
`architecture-document`2.1.1, unchanged `architecture-set`1.0.0 and unchanged
structural schema. The focused skill also includes child
`architecture-architecture`1.1.1. Both skills remain draft1.2.0.

Canonical and package resources preserve the architecture hierarchy, so the
child's parent link and the parent's schema/set links resolve in both contexts.
Missing-parent/schema/set controls fail through existing strict inventory and
Markdown-link rules, including removed manifest entries. No blanket exception
or generic content rewriting was added. [Exact history and requirement mapping](HISTORY.md)
retain former paths, all six original source blobs, tagged normative paragraphs
and unresolved staged comparison identity.

The [source-bound observation](qualification.json) binds all20 package files,
the observed CLI, unchanged validator/adapter and sanitized consumer report.
The original three-pilot list remains unchanged in production. For this bounded
checkpoint only, the real harness selects its first two architecture entries in
process memory; it does not change a file or omit a required local scenario.

## Executed results

| Check | Actual result |
| --- | --- |
| Seven architecture package controls | Pass: real builder output, exact resources, complete declared governing closure, schema governance, missing-resource negatives, strict015/016 rejection and archived requirement/history preservation. |
| Eight continuity integration controls | Pass after aligning the two eval revision fields; existing cases are unchanged. |
| Full `./aether test` | **435 discovered;424 passed and11 existing optional/native skips**,20.224 seconds. |
| `./aether validate --format text` | Pass; only the historical `AETHER_PROVENANCE_009` staging-hash warning remains. |
| `./aether validate --links --json-files --format text` | Pass, zero diagnostics. |
| Catalog and complete distribution drift checks | Pass. |
| Protected source/whitespace comparisons | Pass: staged bytes, decisions, schema/set, global validator and host adapter unchanged. |
| Actual gh2.96 architecture cohort | All five required local scenarios pass; selected local readiness **ready**, qualification complete. |
| Remote/release readiness | Remote install/update skipped by explicit local scope; overall **not-ready**. |

The actual [consumer report](consumer-local.json) retains local build,
project-scope install/list, strict pristine validation and exact installed
materialization, structural/template/eval checks, publish dry-run and cleanup.
All20 exported files have exact selected hashes. Raw installed006/017
host-tracking observations remain visible; real update tracking is not removed
and those raw copies are not described as portable exports.

The already-installed gh2.96 binary was selected through command-scoped PATH.
Default gh2.46, HOME and global/user skill state were unchanged. The existing
harness removed its disposable consumer tree and preserved the unrelated fixture
skill during managed removal. Publication was only the actual publish dry-run.
Observed CLI bytes/self-reported version are not independent signer proof.

Review found and closed an incorrect inference from historical internal
“Issue016” to current GitHub issue16. The mapping now remains null/unverified;
comparison and human retirement obligations remain intact. The first full run
also caught old eval-version fields; those fields were aligned without changing
cases before the clean final435-test/actual-CLI run. Qualification records retain
that resolved failure rather than calling its earlier source successful.

Independent read-only source review confirms the corrected scope, original Git
blobs, preserved normative paragraphs and missing-resource controls. Its own
seven focused controls pass. This is local package evidence, not a proof of
model judgment, host discovery or architecture acceptance.

## Remaining work and impact

The separately owned audit pilot and combined three-pilot run remain outside
this source selection. Actual remote installation/update/rollback, stable
artifact selection, observed agent use, native host matrix, immutable release
and consumer publication retain their existing#38 acceptance. No staged source,
approved decision, human review, tag/release or deployment changes.

Decision impact: reference ADR-0001/0002/0004/0005. Canonical/derived ownership,
artifact-version boundaries, stable identifiers and human deletion authority
remain unchanged; the historic ADR conflict and proposed0009 are preserved.
Roadmap impact: **not-affected**, AET-Q01/AET-Q05. The [receipt](roadmap-impact.json)
records bounded progress inside existing work without promoting strategic state.
