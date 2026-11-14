---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-14T22:15:09Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Reject unrecorded quarantine intake and bind real staging changes to immutable preimages, retained
    disposition evidence and designated-account approval under ADR-0005.
  includes:
  - Strict local intake validation covers nested and untracked supporting files while grandfathering exact
    bytes in the retained 734-file ledger. The 16 historical flat and hook disposition records retain
    their separate meanings.
  - The repository-local standalone diff guard verifies actual full base/head Git objects, base-admitted
    approval payloads, exact modes/blobs, retained canonical/rejection bytes and provider account statements
    bound to immutable review commits. Pending attestation completion cannot authorize removal in the
    same diff.
  - PR scheduling executes the controller extracted from the immutable base with read permissions and
    no persisted Git credentials; initial controller admission accepts no staging changes. Proposed ADR-0010
    records this mechanism without ratifying policy.
  excludes: &id001
  - No staged source was removed or executed, and no human approval comment was created. Synthetic provider
    fixtures do not prove a real human operation or live removal authorization.
  - External-planned removal stays blocked until its origin adapter is separately qualified; an external
    catalog entry cannot override accepted ADR-0005. Branch protection remains organization issue22.
  - Existing issue38 consumer-installation qualification was not-ready in the prior hosted run. The 11
    existing optional/native skips remain explicit. New hosted controller bootstrap and integration evidence
    must be inspected after push.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - DECISIONS.md
  - catalog/staging_guard.py
  - catalog/staging
  - docs/staging-intake-and-removal.md
  - docs/decisions/ADR-0010-immutable-staging-review-controls.md
  - tests/test_staging_guard.py
  - https://github.com/egohygiene/aether/issues/111
work:
  objective: Reject unrecorded quarantine intake and bind real staging changes to immutable preimages,
    retained disposition evidence and designated-account approval under ADR-0005.
  success_conditions:
  - Recorded intake covers every new or changed nested file without requiring immediate legacy evacuation.
  - Changed source, forged or stale approval, head-only approval, changed destinations and unsupported
    dispositions fail closed; the separate synthetic plan/attestation/removal lifecycle passes.
  - CI uses actual base/head event inputs and the base-admitted controller; source integration and human
    ratification remain distinct.
  active_issue:
    provider: github
    id: egohygiene/aether#111
    url: https://github.com/egohygiene/aether/issues/111
  next:
    kind: issue
    id: egohygiene/aether#38
    description: Inspect this PR hosted bootstrap and existing consumer qualification separately; retain
      actual not-ready evidence, then select a bounded source checkpoint from issue105.
    readiness: blocked
    references:
    - https://github.com/egohygiene/aether/issues/38
    - https://github.com/egohygiene/aether/issues/105
    depends_on: []
state:
  base:
    revision: 23bbfe29fa4b1905fd4c44ec5b41a79cfe683033
    ref: refs/heads/main
    verified_at: '2026-11-14T22:15:09Z'
  candidate:
    branch: codex/staging-intake-and-removal
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-14T22:15:09Z'
    default_branch_revision: 23bbfe29fa4b1905fd4c44ec5b41a79cfe683033
    issue_state: open
    pull_request_state: not-applicable
    notes: Observed main23bbfe2 includes merged residual ledger PR128. No PR yet exists for this local
      candidate. Its containing revision remains null deliberately; recheck the actual PR and source before
      integration.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-14T22:15:09Z'
  reviewed_by: Codex
  evidence:
  - command: python -m unittest tests.test_staging_guard -v
    outcome: passed
    notes: 13 synthetic Git/provider controls pass, including the complete separate plan/attestation/removal
      lifecycle, same-diff refusal, account rename, forged/quoted statements, special files and poisoned
      proposed controllers.
    observed_at: '2026-11-14T22:15:09Z'
  - command: python -m unittest discover -s tests -p test_*.py -v
    outcome: passed
    notes: 325 tests pass with 11 existing optional/native skips.
    observed_at: '2026-11-14T22:15:09Z'
  - command: ./aether validate --staging --strict-staging --format json; catalog, ledger, links, schema
      and distribution checks
    outcome: passed
    notes: Intake/strict-staging and links report no diagnostics. Default validation preserves one historical
      provenance warning. Workflow shell syntax and diff whitespace checks pass.
    observed_at: '2026-11-14T22:15:09Z'
  - command: Selected Hygiene ADR policy v1.2.0 schema and owner decision reference check
    outcome: passed
    notes: Exact six-file immutable owner sources and digests verified. Proposed ADR-0010 front matter
      passes the selected schema, formats and reference validator; no full native source admission or
      human disposition is implied.
    observed_at: '2026-11-14T22:15:09Z'
  environment_limitations: *id001
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions: []
  excluded:
  - secrets-and-credentials
  - private-conversation-text
  - sensitive-personal-data
  - unpublished-private-business-data
  - private-local-paths
  - unrelated-private-context
  untrusted_content: context-only-no-authority
---

# aether continuity

## Purpose and precedence

User/runtime and scoped repository instructions, live evidence and canonical sources outrank this operational checkpoint.

## Resume protocol

Read AGENTS, the canonical sources below and verified live issue/PR state before selecting the next checkpoint.

## Current objective and success conditions

Reject unrecorded quarantine intake and bind real staging changes to immutable preimages, retained disposition evidence and designated-account approval under ADR-0005.

- Recorded intake covers every new or changed nested file without requiring immediate legacy evacuation.
- Changed source, forged or stale approval, head-only approval, changed destinations and unsupported dispositions fail closed; the separate synthetic plan/attestation/removal lifecycle passes.
- CI uses actual base/head event inputs and the base-admitted controller; source integration and human ratification remain distinct.

## State snapshot

Observed default source `23bbfe29fa4b1905fd4c44ec5b41a79cfe683033`. Candidate `codex/staging-intake-and-removal` is a review checkpoint; its containing revision remains null intentionally.

## Completed and material changes

Strict local intake validation covers nested and untracked supporting files while grandfathering exact bytes in the retained 734-file ledger. The 16 historical flat and hook disposition records retain their separate meanings.

The repository-local standalone diff guard verifies actual full base/head Git objects, base-admitted approval payloads, exact modes/blobs, retained canonical/rejection bytes and provider account statements bound to immutable review commits. Pending attestation completion cannot authorize removal in the same diff.

PR scheduling executes the controller extracted from the immutable base with read permissions and no persisted Git credentials; initial controller admission accepts no staging changes. Proposed ADR-0010 records this mechanism without ratifying policy.

## Validation and review evidence

`python -m unittest tests.test_staging_guard -v` — passed: 13 synthetic Git/provider controls pass, including the complete separate plan/attestation/removal lifecycle, same-diff refusal, account rename, forged/quoted statements, special files and poisoned proposed controllers.

`python -m unittest discover -s tests -p test_*.py -v` — passed: 325 tests pass with 11 existing optional/native skips.

`./aether validate --staging --strict-staging --format json; catalog, ledger, links, schema and distribution checks` — passed: Intake/strict-staging and links report no diagnostics. Default validation preserves one historical provenance warning. Workflow shell syntax and diff whitespace checks pass.

`Selected Hygiene ADR policy v1.2.0 schema and owner decision reference check` — passed: Exact six-file immutable owner sources and digests verified. Proposed ADR-0010 front matter passes the selected schema, formats and reference validator; no full native source admission or human disposition is implied.

ADR-Ref: accepted ADR-0005 and historical hook records retain authority. New ADR-0010 is proposed with null approval for the immutable evidence/controller mechanism. Existing ADR-0009 remains proposed independently.

## Blockers, risks, unknowns, and deferred work

No staged source was removed or executed, and no human approval comment was created. Synthetic provider fixtures do not prove a real human operation or live removal authorization.

External-planned removal stays blocked until its origin adapter is separately qualified; an external catalog entry cannot override accepted ADR-0005. Branch protection remains organization issue22.

Existing issue38 consumer-installation qualification was not-ready in the prior hosted run. The 11 existing optional/native skips remain explicit. New hosted controller bootstrap and integration evidence must be inspected after push.

## Next dependency-ready work

Inspect this PR hosted bootstrap and existing consumer qualification separately; retain actual not-ready evidence, then select a bounded source checkpoint from issue105.

## Parallel changes and reconciliation

Preserve repository-owned source, existing immutable selections and any later handoff changes. Verify live state again before integration.

## Privacy and redaction

Public-safe source facts and synthetic fixtures only. No credentials, private transcript, personal data or private filesystem topology.

## Handoff update protocol

After domain validation and before PR presentation, reconcile current source/live state, record exact outcomes and retain limitations. Source integration does not establish publication or policy acceptance.

## Compaction and supersession

Git and linked work records retain history. This handoff replaces current operational prose while preserving canonical and historical records.
