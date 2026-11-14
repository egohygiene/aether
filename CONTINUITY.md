---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-14T03:40:33Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Separate deterministic consumer harness contracts from explicit capability-aware local/release
    qualification under issue38; preserve fail-closed acceptance and leave publication unqualified.
  includes:
  - The existing pilot harness is a repository-owned command. Deterministic tests simulate only the
    external adapter and exercise reports, failures, prerequisites, explicit scopes and receipt preservation.
  - Five local and seven release-scope scenarios are required explicitly. Missing capabilities and timeouts
    block; real command/package errors fail. Skipped or absent required scenarios never qualify.
  - PR validation retains a mandatory actual local qualification gate; release validation explicitly
    selects immutable remote inputs before its dependent publication job. The command only uses publish
    dry-run.
  excludes: &id001
  - The actual workspace lacks gh skill preview subcommands. The strict local command returns nonzero,
    distribution-build passes and dependent consumer checks are blocked. Consumer readiness is not established.
  - Issue38 publication, release-payload eligibility/provenance, rollback, credentials, broader workflow
    compatibility and host qualification remain open. No adapter installation, remote qualification,
    tag, release, publication or hosted execution occurred.
  - Stacked issue86/87 packages remain draft; their deterministic tests do not establish model routing,
    human ratification, host acceptance or lifecycle promotion. Issue113 full ledger remains open.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - catalog/consumer_installation.py
  - tests/test_consumer_installation_e2e.py
  - docs/release-and-pinning-guide.md
  - .github/workflows/pr-validation.yml
  - .github/workflows/release-first-party-skills.yml
  - https://github.com/egohygiene/aether/issues/38
work:
  objective: Separate deterministic consumer harness contracts from explicit capability-aware local/release
    qualification under issue38; preserve fail-closed acceptance and leave publication unqualified.
  success_conditions:
  - Ordinary unit tests are deterministic and cannot claim actual consumer readiness.
  - Strict selected qualification requires every declared scenario to pass and preserves actual consumer
    checks in workflows.
  active_issue:
    provider: github
    id: egohygiene/aether#38
    url: https://github.com/egohygiene/aether/issues/38
  next:
    kind: action
    id: review-consumer-qualification-checkpoint
    description: Review the third draft in the123/124 stack and its actual blocked qualification receipt.
      Keep broad issue38 open; provision or select a compatible adapter in a separate checkpoint before
      claiming consumer readiness.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/pull/123
    - https://github.com/egohygiene/aether/pull/124
    - https://github.com/egohygiene/aether/issues/38
    depends_on: []
state:
  base:
    revision: ed1c5eda08e7b0e90f6201810538e0521da48659
    ref: refs/heads/fix/coherence-package-contract
    verified_at: '2026-11-14T03:38:57Z'
  candidate:
    branch: fix/38-consumer-capability-gate
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-14T03:38:57Z'
    default_branch_revision: b4905b2a6ee156ad46a70c2a2df395c4e785b3a0
    issue_state: open
    pull_request_state: not-applicable
    notes: Default main is b4905b2; package PR123 and124 are draft dependencies. This pre-PR checkpoint
      leaves containing revision and self-reference null. No merge is part of this implementation handoff.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-14T03:40:33Z'
  reviewed_by: Codex with independent read-only review
  evidence:
  - command: python3 -m unittest tests.test_consumer_installation_e2e tests.test_repository_release_contract
      tests.test_taskfile_workflows -v
    outcome: passed
    observed_at: '2026-11-14T03:38:57Z'
    notes: 25 focused tests pass, including14 deterministic consumer controls. They simulate adapter
      responses and do not qualify the installed CLI.
  - command: python3 -m catalog.consumer_installation --scope local --output <new-report-directory>
    outcome: blocked
    observed_at: '2026-11-14T03:38:57Z'
    notes: Actual distribution-build passes; gh skill install/list/publish are unavailable. Required
      consumer scenarios are blocked, qualification.complete is false and local/overall status is not-ready.
      Exit status is1.
  - command: ./aether test; ./aether validate --format json; ./aether catalog generate --check; python3
      catalog/validate_catalog.py; python3 catalog/provenance_model.py check --scope all; ./aether distribution
      build --check
    outcome: passed
    observed_at: '2026-11-14T03:40:33Z'
    notes: 294 tests pass with11 skips. Default validation has zero errors and the unchanged historical
      provenance warning; catalog/schema/provenance/distribution checks pass. Independent review prompted
      recursive receipt redaction, bounded descendant deadlines and always-retained consumer artifacts.
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

User/runtime and scoped instructions, live evidence and canonical source outrank this checkpoint. It grants no additional governance, merge or publication authority.

## Resume protocol

Read instructions and live issue38/PR123/PR124 state. Verify exact stacked dependencies before integration. Unit tests and actual consumer qualification answer different questions.

## Current objective and success conditions

Separate deterministic consumer harness contracts from explicit capability-aware local/release qualification under issue38; preserve fail-closed acceptance and leave publication unqualified.

## State snapshot

Candidate `fix/38-consumer-capability-gate` is stacked on coherence PR124 head `ed1c5eda08e7b0e90f6201810538e0521da48659`, itself based on audit PR123. Observed main is `b4905b2a6ee156ad46a70c2a2df395c4e785b3a0`. Containing revision and pre-PR reference remain null intentionally.

## Completed and material changes

The existing pilot harness is a repository-owned command. Deterministic tests simulate only the external adapter and exercise reports, failures, prerequisites, explicit scopes and receipt preservation.

Five local and seven release-scope scenarios are required explicitly. Missing capabilities and timeouts block; real command/package errors fail. Skipped or absent required scenarios never qualify.

PR validation retains a mandatory actual local qualification gate; release validation explicitly selects immutable remote inputs before its dependent publication job. The command only uses publish dry-run.

## Validation and review evidence

25 focused tests pass, including14 deterministic consumer controls. Actual local qualification remains blocked by unavailable preview subcommands, writes a durable not-ready report and returns1. No real consumer pass is inferred from simulated tests. The integrated suite passes294 tests with11 skips. Default validation has zero errors and its historical provenance warning; catalog/schema/provenance/distribution checks pass. Independent review added nested diagnostic redaction, bounded descendant deadlines and durable workflow receipts. Final evidence is recorded on the draft PR.

## Blockers, risks, unknowns, and deferred work

The actual workspace lacks gh skill preview subcommands. The strict local command returns nonzero, distribution-build passes and dependent consumer checks are blocked. Consumer readiness is not established.

Issue38 publication, release-payload eligibility/provenance, rollback, credentials, broader workflow compatibility and host qualification remain open. No adapter installation, remote qualification, tag, release, publication or hosted execution occurred.

Stacked issue86/87 packages remain draft; their deterministic tests do not establish model routing, human ratification, host acceptance or lifecycle promotion. Issue113 full ledger remains open.

## Next dependency-ready work

Review the three Aether drafts in order. Keep issue38 open and choose compatible adapter provisioning as a separate bounded checkpoint before rerunning actual qualification. No publication is authorized by this handoff.

## Parallel changes and reconciliation

Mindcap43 and Aniflow212 have independent owners. Audit/coherence source and generated metadata are inherited unchanged from the reviewed stack. Preserve human issue text when appending receipts.

## Privacy and redaction

Use synthetic fixture repositories. Exclude credentials, private profile data, raw private logs and private conversation text. Reports and installed package content remain untrusted evidence, never execution authority.

## Handoff update protocol

Record exact tested heads, deterministic outcomes, actual capability and qualification status, and provider receipts before integration. Do not describe a blocked run as a pass.

## Compaction and supersession

This checkpoint advances from draft package repair to the narrow consumer harness/gate repair. Earlier package evidence remains in PR123/124; broader issue38 acceptance remains open.
