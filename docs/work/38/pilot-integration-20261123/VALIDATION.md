# Combined portable-pilot qualification — November 23, 2026

Issue: [Aether #38](https://github.com/egohygiene/aether/issues/38).
Parent: [draft #143](https://github.com/egohygiene/aether/pull/143),
`1473f9be497289d0a973a0980dd13e12e2accf39`.
Merged main remains `dc3549c8a23bed5fb551a458a22605e7e0777822`.
Actual final clean tested code:
`9fd9f438d08fd88a9ba2102d1205191c91afce77`.

## Outcome and source ownership

The architecture and audit source histories are integrated, with the combined
catalog and complete distributions regenerated through existing commands.
No generated artifact is hand-edited. The artifact distribution/catalog delta after parent143 is the
audit package, its two changed draft specifications and their catalog entries.
Architecture package bytes retain the exact parent selection.

The unchanged production default three-pilot CLI now passes every required
local scenario across `architecture-authoring`, `create-architecture-document`
and `audit-repository`. This is an actual standard CLI run, not the earlier
process-local reduced cohorts. All50 selected package files are bound to exact
tested Git blobs and their byte lengths/SHA-256 values in the
[qualification record](qualification.json).

Earlier domain receipts retain clean8848architecture and084audit sources;
their original histories and interpretations are not retimed or relabeled.
Approved auditor2.0.0, its read/search-only agent, all staged bytes, decisions,
global portable validator, builder and installed-host adapter remain unchanged.
Draft skill/specification versions supply no new approval or stable eligibility.

## Actual checks

| Check | Final actual outcome at clean9fd9f43 |
| --- | --- |
| `./aether test` | **440 tests:429passed,11existing optional/native skips**,20.656seconds,exit0. |
| `./aether validate --format text` | Pass; only the preserved `AETHER_PROVENANCE_009` historical staging-hash warning. |
| `./aether validate --links --json-files --format text` | Pass,zero diagnostics. |
| `./aether catalog generate --check` | Pass. |
| `./aether distribution build --check` | Pass for the complete tracked distributions. |
| `python3 -m catalog.staging_ledger check` | Pass: exact immutable reconstruction and current owner-input bindings. |
| Whole-diff whitespace and protected source comparisons | Pass. |
| Standard `python3 -m catalog.consumer_installation --scope local --output <fresh-report-directory>` | **Exit0**,unchanged default three pilots,all5required local scenarios pass. |

The existing gh2.96.0 binary is selected through command-scoped PATH only.
Default CLI, HOME and user/global skill state are not changed. Actual local
build/install/list, strict pristine validation, exact installed materialization,
structure/template checks, publish dry-run and fixture cleanup execute. The
existing harness preserves the unrelated fixture skill and removes its own
consumer tree. No host security or signer authenticity follows from CLI hashes.

The [actual sanitized consumer report](consumer-local.json) says localready and
`qualification.complete=true`. Every pristine pilot has zero portable findings.
Each installed instance matches its frozen export plus only verified host
tracking/observed separator behavior. Raw installed006/017 findings remain
visible and are not described as raw portable passes.

Overall readiness remains **not-ready** because the explicit local scope skips
pinned remote release installation and update. Actual remote
install/update/deprecation/rollback, observed agent authoring/discovery, native
host availability, eligible stable selection and immutable release/publication
remain #38's original acceptance. No hosted workflow is dispatched here.

## Resolved current-ledger drift

The first integrated code1e21 had a passing default-three-pilot local run, but
its full440-test run exposed one legitimate consistency failure. The current
residual-staging ledger still pinned old hashes for the two audit disposition
records whose history pointers were intentionally moved. No staging content or
disposition changed.

The unchanged ledger generator rebuilds the current view from immutable
`1e21edb52fc6da03b30b3a0003d21cc83e9d941b`. The exact machine delta is its source
revision and those two owner-input hashes; its Markdown summary only refreshes
the represented source and reproduction command. All734files,222units,
186current/six historical-absent skill roots, nine agent comparisons, four
pending transfers, actual staging tree, dispositions and removal authority remain
identical. No test or validator is weakened. The
[reconciliation record](ledger-reconciliation.json) preserves old/new hashes,
the original failed test/log hash and unchanged totals. The final clean9fd run
repeats the full suite and standard default-pilot CLI successfully.

Raw local logs remain private with hashes/lengths retained; the complete public
consumer report is the harness's sanitized output. Public evidence excludes
private paths, proxy values and credentials. Checks and source/file comparisons
are bounded observations, not locks against later mutation.

## Decision and roadmap impact

Reference preserved ADR-0001/0002/0004/0005. The repair preserves
canonical/generated ownership, neighboring owners, artifact-versus-release
versioning and staging review/removal authority. Historical ADR-0002/0006 and
proposed ADR-0009 remain unchanged.

Roadmap impact: **not-affected**, AET-Q01/AET-Q05. Actual local progress remains
within existing consumer work; tagged release/downstream immutable consumption
criteria are still unmet. The [single combined receipt](roadmap-impact.json)
records that disposition without changing strategy, lifecycle or human intent.
