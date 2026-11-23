---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T18:34:37.754559+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Qualify strict pristine exports and verified local installed-host materialization without rewriting
    tracking or weakening portability.
  includes:
  - Freeze and strictly validate selected pristine exports before installation; compare exact bounded
    no-follow installed inventories/resources and typed semantic frontmatter/body.
  - Admit only exact verified gh local-path tracking and the observed single blank separator; preserve
    raw installed diagnostics and actual source mutation failures.
  - Actual direct companion local readiness with gh 2.96.0, retained historical pilot failures and complete
    remote/stable-release limits.
  excludes:
  - No global portable-validator rule change, installed tracking rewrite, host/path blanket allowance,
    or generated content beyond the projection parent.
  - No remote installation/update, user/global configuration, hosted workflow, stable promotion, tag,
    release or deployment.
  - No observed agent authoring, automatic discovery, binary authentication or OS-matrix qualification.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - catalog/consumer_installation.py
  - tests/test_consumer_installation_e2e.py
  - library/organization/skills/SKILL-CONTRACT.md
  - docs/release-and-pinning-guide.md
  - docs/identity-companion.md
  - docs/work/38/host-materialization-20261122/VALIDATION.md
  - docs/work/38/host-materialization-20261122/consumer-companion.json
  - docs/work/38/host-materialization-20261122/consumer-pilots.json
  - docs/work/38/host-materialization-20261122/package-and-adapter-observation.json
  - docs/work/38/host-materialization-20261122/roadmap-impact.json
work:
  objective: Qualify strict pristine exports and verified local installed-host materialization without
    rewriting tracking or weakening portability.
  success_conditions:
  - Keep pristine export validation strict and separate from exact verified host materialization and raw
    installed observations.
  - Reject wrong tracking, changed bodies/resources/fields, ambiguous metadata, links and vacuous inventories
    without changing real installed state.
  - Retain actual direct local success, original pilot failures, skipped remote scenarios and draft/release
    exclusion.
  active_issue:
    provider: github
    id: egohygiene/aether#38
    url: https://github.com/egohygiene/aether/issues/38
  next:
    kind: action
    id: review-host-materialization-and-repair-original-pilot-dependencies
    description: 'Review this child after projection PR #141. Repair the original three pilots’ governing-resource/provenance
      references without masking paths or deleting history, then rerun their real local gate. Keep release
      eligibility and remote/publication acceptance separate.'
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/pull/141
    - https://github.com/egohygiene/aether/issues/38
    depends_on: []
state:
  base:
    revision: 26a8ff90feb4344a7a5836540c55d872da3736a9
    ref: refs/heads/codex/38-build-metadata-projection-20261122
    verified_at: '2026-11-22T18:34:37.754559+00:00'
  candidate:
    branch: codex/aether-38-host-materialization-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T18:34:37.754559+00:00'
    default_branch_revision: e5a67e581857122a8131fe8a24d1c7e6c1fa1170
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Provider verified main e5a67e5, issue #38 open and parent draft #141 open. Prior #140 is merged.
      No PR exists yet for this host-materialization child; no release selection or publication occurred.'
  parallel_changes:
  - provider: github
    id: egohygiene/aether#141
    url: https://github.com/egohygiene/aether/pull/141
review:
  status: partial
  reviewed_at: '2026-11-22T18:34:37.754559+00:00'
  reviewed_by: Codex
  evidence:
  - command: Focused adapter suite and final ./aether test
    outcome: passed
    observed_at: '2026-11-22T18:34:37.754559+00:00'
    notes: '32 focused controls pass; full 428 tests: 417 passed / 11 existing optional-native skips.
      Anchored multiline semantic-drift regression rejects exact old parser.'
  - command: Actual gh 2.96 direct companion local harness
    outcome: passed
    observed_at: '2026-11-22T18:34:37.754559+00:00'
    notes: All 5 required local scenarios pass; strict pristine diagnostics empty, source and actual installed
      inventory/resources/semantic values match; raw 006/017 retained; remote skipped/overall not-ready.
  - command: Actual standard three-pilot local consumer CLI
    outcome: limited
    observed_at: '2026-11-22T18:34:37.754559+00:00'
    notes: Exit 1 / not-ready preserves original pristine 015/016 governing-resource/provenance findings.
      Their exact materialization passes; no failed scenario is relabeled passed.
  - command: ./aether validate --format text; distribution build --check --output-directory dist
    outcome: passed
    observed_at: '2026-11-22T18:34:37.754559+00:00'
    notes: Only historical AETHER_PROVENANCE_009 warning; generated distributions match projection parent.
      No canonical skill/runtime validator or maturity change.
  - command: Roadmap-impact receipt schema and independent core/documentation reviews
    outcome: passed
    observed_at: '2026-11-22T18:34:37.754559+00:00'
    notes: Not-affected within AET-Q01/AET-Q05. Independent review reproduced and cleared anchored parser
      false-pass; selected scopes and no global validator waiver retained. A second independent reviewer
      confirmed final report/readiness scopes, all package hashes and retained pilot failures.
  - command: ./aether validate --links --json-files --format text; pinned continuity schema/headings/budgets;
      public receipt hashes and path/secret scan
    outcome: passed
    observed_at: '2026-11-22T18:34:37.754559+00:00'
    notes: Documentation/link/JSON validation has zero diagnostics. All 25 package files and adapter,
      unchanged validator and observed CLI hashes match; continuity structure and public evidence scans
      pass.
  environment_limitations:
  - 'Original three-pilot portability, eligible stable payload selection and actual remote install/update/deprecation/rollback/publication
    remain open under issue #38.'
  - Actual local CLI commands are not observed model authoring, automatic discovery, host OS matrix or
    independent binary authenticity.
  - Companion remains draft 1.0.0 and excluded from stable payloads; no Identity source/tool pin or installation
    authority changes.
  - Qualification snapshots are bounded observations, not locks against later filesystem mutation.
  - Official released EgoLint continuity conformance is not claimed; pinned schema/headings/budget supply
    structural evidence.
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

User/runtime and scoped instructions, live state and canonical source outrank this bounded operational handoff. It records a proposed consumer adapter checkpoint, not stable release or policy promotion.

## Resume protocol

Read AGENTS, the selected source/evidence above and actual parent draft #141. Preserve unrelated dirty checkouts and previous receipts. This branch follows the export projection; do not infer the older #140 failure was secretly repaired retroactively.

## Current objective and success conditions

Qualify strict pristine exports and verified local installed-host materialization without rewriting tracking or weakening portability.

## State snapshot

Base is projection 26a8ff90feb4344a7a5836540c55d872da3736a9 on codex/38-build-metadata-projection-20261122. Current main remains e5a67e581857122a8131fe8a24d1c7e6c1fa1170. Child candidate has null containing revision/PR at this pre-PR checkpoint; issue #38 remains open.

## Completed and material changes

The adapter validates/freeze-captures pristine packages before any installer, verifies unchanged sources and exact installed inventories/resources/typed frontmatter/body, and admits only verified local tracking plus one observed blank separator. Anchored whole-line metadata parsing closes a reproduced intermediate false-pass for literal delimiters in multiline descriptions. No real installation is normalized or rewritten. Raw installed diagnostics stay visible.

## Validation and review evidence

See docs/work/38/host-materialization-20261122/VALIDATION.md. Actual direct companion local gate passes all 5 scenarios; standard 3 pilots retain original export errors and exit 1. Full 428 tests pass with 11 existing skips; 32 focused controls, source/distribution drift, roadmap receipt and independent review pass. No fresh external publication or remote scenario is inferred.

## Blockers, risks, unknowns, and deferred work

Historical pilot governing-resource/provenance 015/016 findings remain. Raw installed 006/017 are observed host tracking, not a raw portable pass. Remote and stable-release gates, observed agent behavior and OS/binary-authenticity qualification remain incomplete. Snapshot reads do not lock files after verification.

## Next dependency-ready work

Review/merge projection #141 before this child when authorized, then repair the original portable pilot resources/provenance without blanket allowances or erased history. Rerun actual selected local gates and retain remote/release/maturity gates separately. No new issue or automatic next-checkpoint authority is supplied.

## Parallel changes and reconciliation

Parent #141 owns build-only metadata projection and its contract exception. This child owns installed-host verification and source-bound local receipts. Preserve both exact source histories and reconcile continuity semantically. Identity source/engineering work remains separately owned.

## Privacy and redaction

Public-safe source facts, synthetic tests and sanitized fixture/report paths only. No HOME repurposing, user/global skill state changes, private transcript, proxy values or credentials. Observed exact CLI/package hashes do not establish signer authenticity.

## Handoff update protocol

After domain checks, reverify live state, apply pinned schema / 12 headings / byte-line budgets and whitespace before PR handoff. Reference preserved ADR-0001 / ADR-0002; no new private-path policy, manifest schema or ADR disposition. Roadmap: not-affected AET-Q01/AET-Q05, with actual local progress distinct from strategy completion.

## Compaction and supersession

Git, the existing issue and dated reports retain earlier state. Replace current operational prose and preserve the historical 2.46/2.96 observations, earlier failed receipts, stable exclusion and unrun release acceptance.
