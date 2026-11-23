# Portable audit governing resources — November 23, 2026

Issue: [#38](https://github.com/egohygiene/aether/issues/38). Base/main:
`dc3549c8a23bed5fb551a458a22605e7e0777822` (merged #141/#142).
Actual tested clean source:
`084adf4234f7f97a16891069b42f7dbfae8b9e28`.

## Outcome and preserved authority

The draft audit package now includes exact byte copies of draft `specfile`
2.0.1, unchanged approved `auditor`2.0.0 and draft `repository-audit-data`1.0.2.
All declared governing dependencies resolve inside the package. Existing schema,
registry and reference-helper bytes remain unchanged. Runtime instructions name
package-local resources instead of requiring the publisher's source tree.

The installed reconciliation retains staged source IDs/names, hashes,
uncertainty, restrictions and every per-behavior disposition. The full original
paths, eight exact pre-change files and before/after requirement map remain in
[repository-only history](HISTORY.md) and its [inventory](source-history.json).
No source/staging deletion, approved-byte change, agent-tool expansion or
lifecycle promotion occurs. The portable validator itself is unchanged.

Specfile's four explicit Section4 naming/canonical-location requirements and
repository-local example remain intact. Its source-placement clarification
retains the same first-party/community owner locations and distinguishes
distributed projections from canonical authority. Existing architecture/catalog
path selection is unchanged. Independent source review found no requirement or
authority relaxation; the exact original edition remains inspectable.

## Executed checks

- `python3 -m unittest tests.test_audit_package_contract tests.test_audit_report_contract tests.test_audit_portable_governance -v`:
  **33 tests pass**, including five new actual-export/governing-closure controls.
  They verify resource bytes and versions, reject missing governing resources,
  retain strict canonical/staging runtime-path refusal, compare all historical
  archives to actual immutable Git objects, preserve staging restrictions and
  compare the original Section4 requirements and owner architecture.
- `./aether validate --skills --specifications --evals --links --json-files --staging --format text`:
  **zero diagnostics**. This selected source check does not claim current
  combined catalog/distribution drift qualification.
- Independent read-only review reruns the five new controls and confirms exact
  approved auditor, read/search-only agent and staged bytes against the base.
- Public receipt scan, JSON parsing and whitespace checks pass. The
  [observation](observation.json) binds the qualified CLI/unchanged validator,
  raw report hash and all30 deterministically reproduced package files.

The final handoff tightens only test-side archive-membership assertions and
reruns the same33 tests successfully. All30 package files remain byte-identical
to the clean084adf4 selection; later test/documentation changes are not relabeled
as another actual CLI execution.

## Actual compatible CLI qualification

The existing gh2.96.0 binary was selected only through command-scoped PATH.
The existing consumer harness ran in `local` scope with a process-local
single-pilot selection for `audit-repository`; the production three-pilot list
is unchanged. Actual project-scope installation/listing, strict pristine
validation, exact installed-instance comparison, publish dry-run and cleanup
execute. No user/global skill configuration or default CLI changes.

| Required local scenario | Actual outcome |
| --- | --- |
| Distribution build | Pass |
| Clean project-local install/list | Pass |
| Strict pristine export and exact installed-host materialization | Pass |
| Publish validation (`--dry-run`) | Pass |
| Cleanup preserving the unrelated fixture skill | Pass |

The [actual sanitized report](consumer-audit.json) says `local_status=ready`
and local `qualification.complete=true`. Its complete30-file materialization
matches the frozen export, admitting only the existing verified local tracking
field and observed one-blank-LF separator. Raw installed `006`/`017` diagnostics
remain observations; they are not called a raw portable pass.

The report remains **overall not-ready**: pinned remote release install and
update are skipped. This selects one pilot, not all three. Deterministic package
tests and actual local CLI behavior do not establish observed model auditing,
automatic discovery, binary signature authenticity, stable promotion or release.
Private harness fixtures were cleaned by the existing harness after the run.

## Parent integration and remaining work

The parent owns combined architecture/audit catalog and distribution regeneration,
full repository checks, all-three-pilot qualification and the new draft PR stack.
No stale generated file is hand-edited in this checkpoint. Actual source-bound
local acceptance remains tied to084adf4; later integration is not relabeled as
that execution. Remote install/update/deprecation/rollback, eligible stable
selection and actual publication remain #38's original acceptance.

Decision impact: reference preserved ADR-0001/0002/0004/0005. This supplies
existing portable inputs and retains staging history without a new source
location, artifact kind, channel, permission boundary or versioning scheme.
Known historical ADR-0002/0006 conflict and proposed ADR-0009 remain untouched.

Roadmap impact: **not-affected**, AET-Q01/AET-Q05. This is partial local progress
inside the existing consumer/release work, without a strategic/maturity change.
The [single receipt](roadmap-impact.json) retains that disposition and scope.
