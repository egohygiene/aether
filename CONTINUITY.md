---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-15T00:32:31Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Complete the optional conversation-onboarding/checkpoint-ledger source extension while preserving
    bounded current continuity, privacy and current authority.
  includes:
  - Draft conversation-continuity0.1.0 composes unchanged repository-continuity1.0.0 and worker-strategy0.2.0.
    Authored opt-in AGENTS/onboarding templates route to current snapshot, separate meaningful discussion
    ledger and canonical artifacts. No new required files or first-party artifact kind.
  - The schema and read-only portable helper preserve stable attributed requests, decisions/proposals,
    interpretations/attempts/feedback, exact revisions, unknowns, questions and next action. Prepared/validated/merged/published/provider-submitted
    remain separate evidence claims.
  - Native controls exercise unchanged capture, append correction, deterministic concurrent union/collision
    refusal, missing/future/cyclic links, unsafe references, classified private inputs, bounded regular-file
    admission and source-withholding diagnostics. No helper writes or network requests occur.
  - One isolated fresh process reads authored route, a schema-valid bounded current snapshot, saved ledger,
    exact committed artifact and actual Git branch/head/worktree without prior chat. Generated portable
    package validates outside Aether with Python-I. These are mechanical proofs only.
  - Existing continuity skill1.2.0 discovers the optional route for default-bundle67 without enabling
    it. Canonical inventory, schema mirror, catalog and generated distributions are reconciled; corpus36specs/41skills/10agents.
    ADR0012 stays proposed/null.734 retained staging files and raw bytes are unchanged.
  - Initial hosted schema-resolution failure under pinnedjsonschema4.10.3 is repaired with an absolute
    schema identifier. An isolated environment from requirements-dev.lock passes catalog/schema,16 focused
    and359 full tests with11 existing skips. New hosted exact-head proof remains pending.
  excludes: &id001
  - The extension, ledger schema and ADR0012 remain draft/proposed with null approval. Source integration
    does not authenticate user decisions, human review, private prose classification or downstream policy/adoption.
  - No repository is opted in or receives a live ledger/onboarding installation. Static guidance installs
    no background memory, context warning, saving hook or zero-loss guarantee. Isolated-process recovery
    proves mechanical file/Git access, not model/host effectiveness.
  - The helper does not load prior segments, resolve cross-segment identities, fetch live provider state,
    write files or redact history. Missing access/prior context is explicit. Public admission rejects
    classified private sources but still needs content review.
  - 'Existing38 real consumer qualification remains not-ready: no real release-eligible skills, no installed
    gh skill adapter and no actual publication or remote acceptance. Eleven existing optional/native test
    skips remain explicit.'
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - library/organization/specs/methodology/conversation-continuity.spec.md
  - library/organization/skills/methodology/maintain-conversation-checkpoint/SKILL.md
  - library/organization/skills/methodology/maintain-repository-continuity/SKILL.md
  - catalog/schemas/aether.conversation-ledger.v1.schema.json
  - tests/test_conversation_continuity.py
  - docs/decisions/ADR-0012-optional-conversation-evidence-extension.md
  - docs/evidence/2026-11-15-conversation-continuity-qualification.json
  - https://github.com/egohygiene/aether/issues/102
work:
  objective: Complete the optional conversation-onboarding/checkpoint-ledger source extension while preserving
    bounded current continuity, privacy and current authority.
  success_conditions:
  - Opt-in authored discovery recovers active topic/artifacts/questions/next action without replaying
    chat or replacing root continuity.
  - Repeated and concurrent captures preserve source identity/provenance; corrections, unavailable state,
    privacy and current role limits remain explicit.
  - Canonical spec/skill/schema, generated portable resources and deterministic examples agree; no runtime/adoption/publication
    proof is inferred.
  active_issue:
    provider: github
    id: egohygiene/aether#102
    url: https://github.com/egohygiene/aether/issues/102
  next:
    kind: issue
    id: egohygiene/aether#103
    description: Define optional repository-owned exploration notes as authored document outputs; compose
      brain-dump/continuity boundaries and qualify a reviewed local opt-in canary without new artifact
      kind, automatic promotion or fleet rollout.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/103
    depends_on: []
state:
  base:
    revision: 919bb4874dd9376944f6459474c01e9f3a4d93ef
    ref: refs/heads/main
    verified_at: '2026-11-15T00:32:31Z'
  candidate:
    branch: codex/conversation-continuity-extension
    revision: null
    pull_request:
      provider: github
      id: egohygiene/aether#133
      url: https://github.com/egohygiene/aether/pull/133
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-15T00:32:31Z'
    default_branch_revision: 919bb4874dd9376944f6459474c01e9f3a4d93ef
    issue_state: open
    pull_request_state: open
    notes: Observed main919bb48 includes merged132.133 is open at priorhead6a2c921 and initial hosted43658350782
      exposed pinned-jsonschema relative-ID resolution failure. Local sourceb5bb6032c0fbdc2a43443ee0ebbb0344a377dd29
      repairs both canonical/portable schema IDs; pinned catalog,16 focused and359 full tests pass with11
      existing skips. Updated hosted proof remains pending; no source failure is attributed to the baseline
      consumer gate.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-15T00:32:31Z'
  reviewed_by: Codex
  evidence:
  - command: ./aether test
    outcome: passed
    notes: 359 full tests pass under both available and repository-pinned dependencies, with11 existing
      optional/native skips. Native pinned catalog/schema check passes after correcting relative-ID resolution.
    observed_at: '2026-11-15T00:32:31Z'
  - command: python -m unittest tests.test_conversation_continuity tests.test_continuity_integration -q
    outcome: passed
    notes: 16 focused methods pass, including actual isolated saved-file/Git recovery with schema-valid
      bounded checkpoint.
    observed_at: '2026-11-15T00:32:31Z'
  - command: ./aether eval run --skill maintain-conversation-checkpoint --mode deterministic --format
      json
    outcome: passed
    notes: 12 declared structure/golden assertion cases pass withzero skips/suite errors; not model judgment.
    observed_at: '2026-11-15T00:32:31Z'
  - command: Catalog/schema/provenance/source/links/strict-staging/distribution, portable helper and proposed
      ADR metadata checks
    outcome: passed
    notes: Actual generated package executes outside Aether with Python-I and bundled schema. Default
      source keeps only historical provenance warning.734 staging files/222units/6,791,350 raw bytes remain
      unchanged.
    observed_at: '2026-11-15T00:32:31Z'
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

Complete the optional conversation-onboarding/checkpoint-ledger source extension while preserving bounded current continuity, privacy and current authority.

- Opt-in authored discovery recovers active topic/artifacts/questions/next action without replaying chat or replacing root continuity.
- Repeated and concurrent captures preserve source identity/provenance; corrections, unavailable state, privacy and current role limits remain explicit.
- Canonical spec/skill/schema, generated portable resources and deterministic examples agree; no runtime/adoption/publication proof is inferred.

## State snapshot

Observed default source `919bb4874dd9376944f6459474c01e9f3a4d93ef`. Candidate `codex/conversation-continuity-extension` is a review checkpoint; its containing revision remains null intentionally.

## Completed and material changes

Draft conversation-continuity0.1.0 composes unchanged repository-continuity1.0.0 and worker-strategy0.2.0. Authored opt-in AGENTS/onboarding templates route to current snapshot, separate meaningful discussion ledger and canonical artifacts. No new required files or first-party artifact kind.

The schema and read-only portable helper preserve stable attributed requests, decisions/proposals, interpretations/attempts/feedback, exact revisions, unknowns, questions and next action. Prepared/validated/merged/published/provider-submitted remain separate evidence claims.

Native controls exercise unchanged capture, append correction, deterministic concurrent union/collision refusal, missing/future/cyclic links, unsafe references, classified private inputs, bounded regular-file admission and source-withholding diagnostics. No helper writes or network requests occur.

One isolated fresh process reads authored route, a schema-valid bounded current snapshot, saved ledger, exact committed artifact and actual Git branch/head/worktree without prior chat. Generated portable package validates outside Aether with Python-I. These are mechanical proofs only.

Existing continuity skill1.2.0 discovers the optional route for default-bundle67 without enabling it. Canonical inventory, schema mirror, catalog and generated distributions are reconciled; corpus36specs/41skills/10agents. ADR0012 stays proposed/null.734 retained staging files and raw bytes are unchanged.

Initial hosted schema-resolution failure under pinnedjsonschema4.10.3 is repaired with an absolute schema identifier. An isolated environment from requirements-dev.lock passes catalog/schema,16 focused and359 full tests with11 existing skips. New hosted exact-head proof remains pending.

## Validation and review evidence

`./aether test` — passed: 359 full tests pass under both available and repository-pinned dependencies, with11 existing optional/native skips. Native pinned catalog/schema check passes after correcting relative-ID resolution.

`python -m unittest tests.test_conversation_continuity tests.test_continuity_integration -q` — passed: 16 focused methods pass, including actual isolated saved-file/Git recovery with schema-valid bounded checkpoint.

`./aether eval run --skill maintain-conversation-checkpoint --mode deterministic --format json` — passed: 12 declared structure/golden assertion cases pass withzero skips/suite errors; not model judgment.

`Catalog/schema/provenance/source/links/strict-staging/distribution, portable helper and proposed ADR metadata checks` — passed: Actual generated package executes outside Aether with Python-I and bundled schema. Default source keeps only historical provenance warning.734 staging files/222units/6,791,350 raw bytes remain unchanged.

Proposed ADR0012 records the optional separate evidence output choice. Approval remains null; integration supplies no human policy disposition. Roadmap impact: not-affected within existing authoring corpus.

## Blockers, risks, unknowns, and deferred work

The extension, ledger schema and ADR0012 remain draft/proposed with null approval. Source integration does not authenticate user decisions, human review, private prose classification or downstream policy/adoption.

No repository is opted in or receives a live ledger/onboarding installation. Static guidance installs no background memory, context warning, saving hook or zero-loss guarantee. Isolated-process recovery proves mechanical file/Git access, not model/host effectiveness.

The helper does not load prior segments, resolve cross-segment identities, fetch live provider state, write files or redact history. Missing access/prior context is explicit. Public admission rejects classified private sources but still needs content review.

Existing38 real consumer qualification remains not-ready: no real release-eligible skills, no installed gh skill adapter and no actual publication or remote acceptance. Eleven existing optional/native test skips remain explicit.

## Next dependency-ready work

Define optional repository-owned exploration notes as authored document outputs; compose brain-dump/continuity boundaries and qualify a reviewed local opt-in canary without new artifact kind, automatic promotion or fleet rollout.

## Parallel changes and reconciliation

Preserve132 release source repairs and its not-ready consumer gate,131 worker guidance,130 roadmap module and129 staging controls. Historical audit and source-rights dispositions remain unchanged.

## Privacy and redaction

Public-safe source facts and synthetic fixtures only. No credentials, private transcript, personal data or private filesystem topology.

## Handoff update protocol

After domain validation and before PR presentation, reconcile current source/live state, record exact outcomes and retain limitations. Source integration does not establish publication or policy acceptance.

## Compaction and supersession

Git and linked work records retain history. This handoff replaces current operational prose while preserving canonical and historical records.
