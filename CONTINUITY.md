---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-15T00:44:09Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Complete optional repository-owned Exploration Note authoring without creating implementation
    commitment, a new artifact kind or an ingestion engine.
  includes:
  - Draft exploration-note-authoring0.1.0 and author-exploration-note provide a concise editable template,
    consumer-selected paths and optional authoring guidance. Draft/parked notes do not become decisions
    or tasks.
  - The thin helper checks bounded metadata/local references and creates only a selected new file in an
    existing approved directory. Unchanged repeat is a no-op; differing authored content, duplicate identities,
    unsafe references, private-to-public sources and ambiguous metadata are refused without overwrite
    or promotion.
  - Eight native methods and eleven declared deterministic examples cover create, revise, park, graduate/link,
    duplicate, conflicting decision, missing source and public/private behavior. Actual generated helper
    executes outside Aether with Python-I and pinned PyYAML.
  - A reviewed opt-in Aether canary records a public-source agent hypothesis about onboarding discovery.
    It stays repository-owned, draft and parked; no issue, accepted decision or garden projection is created.
    Mindgarden39 is verified closed not-planned and is not treated as a dependency.
  - 'Catalog/inventory/provider manifests and generated distributions reconcile the optional package:
    37 specifications, 42 skills and 10 canonical agents. All 734 staged blobs and 6,791,350 raw bytes
    remain unchanged at the refreshed source ledger.'
  excludes: &id001
  - The convention is optional draft authoring guidance and a consumer-owned Markdown output, not a new
    first-party artifact kind or organization lifecycle policy. No fleet installation, forced migration,
    issue promotion, garden ingestion or public deployment occurs.
  - The Aether canary is reviewed by Codex for source/authority/privacy and stays draft/parked. It supplies
    no human architectural acceptance, usefulness measurement, model effectiveness or organization applicability
    decision.
  - The helper checks bounded metadata and available local source paths; external references, source truth,
    private prose classification and actual review require independent verification. Authored edits and
    normal Git review own revisions; no archive or ingestion engine is added.
  - Mindgarden39 is closed not-planned as actually observed; it is historical context, not an active prerequisite.
    Existing downstream owner work remains separate. The real consumer/release gate under38 stays not-ready,
    with 11 existing optional/native skips explicit.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - library/organization/specs/authoring/exploration-note.spec.md
  - library/organization/skills/authoring/author-exploration-note/SKILL.md
  - docs/explorations/2026-11-15-opt-in-onboarding-discovery.md
  - tests/test_exploration_notes.py
  - docs/evidence/2026-11-15-exploration-notes-qualification.json
  - https://github.com/egohygiene/aether/issues/103
work:
  objective: Complete optional repository-owned Exploration Note authoring without creating implementation
    commitment, a new artifact kind or an ingestion engine.
  success_conditions:
  - An optional brief repository-authored note preserves attribution, alternatives, uncertainty, lineage
    and a parked or separately linked next step without overriding canonical decisions.
  - Actual scaffold repetition and authored-update controls preserve existing content; missing/private/ambiguous
    inputs stay explicit.
  - Synthetic source checks and a reviewed local canary qualify the authoring path, with no automatic
    promotion, service dependency or fleet adoption claim.
  active_issue:
    provider: github
    id: egohygiene/aether#103
    url: https://github.com/egohygiene/aether/issues/103
  next:
    kind: issue
    id: egohygiene/hygiene#23
    description: Define the proposed people-first content policy at its Hygiene owner with source mappings,
      separate mechanical/human review, honest freshness/archive states and representative fixtures; preserve
      human activation and broader site-legal work.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/23
    depends_on: []
state:
  base:
    revision: c337e2642f9fa3462cf8a3fa92a7c3748a5149f1
    ref: refs/heads/main
    verified_at: '2026-11-15T00:44:09Z'
  candidate:
    branch: codex/optional-exploration-notes
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-15T00:44:09Z'
    default_branch_revision: c337e2642f9fa3462cf8a3fa92a7c3748a5149f1
    issue_state: open
    pull_request_state: not-applicable
    notes: Observed main c337e26 includes merged133;102 is closed after exact-head hosted schema/source/reproducibility
      qualification.103 remains open and this local source27ae1db has no PR yet.38 consumer readiness
      stays not-ready. Containing report/checkpoint revision remains null.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-15T00:44:09Z'
  reviewed_by: Codex
  evidence:
  - command: ./aether test under requirements-dev.lock environment
    outcome: passed
    notes: 367 full tests pass with 11 existing explicit optional/native skips.
    observed_at: '2026-11-15T00:44:09Z'
  - command: python -m unittest tests.test_exploration_notes tests.test_continuity_integration -q
    outcome: passed
    notes: 16 focused methods pass, including actual creation/no-op/overwrite refusal and source-linked
      parked canary.
    observed_at: '2026-11-15T00:44:09Z'
  - command: ./aether eval run --skill author-exploration-note --mode deterministic --format json
    outcome: passed
    notes: All 11 declared structure/assertion cases pass with zero skips or suite errors; not model behavior.
    observed_at: '2026-11-15T00:44:09Z'
  - command: Catalog/schema/provenance/source/links/strict-staging/distribution and portable helper checks
    outcome: passed
    notes: All relevant source checks pass with historical default provenance warning retained. Actual
      generated package executes outside Aether under pinned dependencies; staged blob inventory remains
      unchanged.
    observed_at: '2026-11-15T00:44:09Z'
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

Complete optional repository-owned Exploration Note authoring without creating implementation commitment, a new artifact kind or an ingestion engine.

- An optional brief repository-authored note preserves attribution, alternatives, uncertainty, lineage and a parked or separately linked next step without overriding canonical decisions.
- Actual scaffold repetition and authored-update controls preserve existing content; missing/private/ambiguous inputs stay explicit.
- Synthetic source checks and a reviewed local canary qualify the authoring path, with no automatic promotion, service dependency or fleet adoption claim.

## State snapshot

Observed default source `c337e2642f9fa3462cf8a3fa92a7c3748a5149f1`. Candidate `codex/optional-exploration-notes` is a review checkpoint; its containing revision remains null intentionally.

## Completed and material changes

Draft exploration-note-authoring0.1.0 and author-exploration-note provide a concise editable template, consumer-selected paths and optional authoring guidance. Draft/parked notes do not become decisions or tasks.

The thin helper checks bounded metadata/local references and creates only a selected new file in an existing approved directory. Unchanged repeat is a no-op; differing authored content, duplicate identities, unsafe references, private-to-public sources and ambiguous metadata are refused without overwrite or promotion.

Eight native methods and eleven declared deterministic examples cover create, revise, park, graduate/link, duplicate, conflicting decision, missing source and public/private behavior. Actual generated helper executes outside Aether with Python-I and pinned PyYAML.

A reviewed opt-in Aether canary records a public-source agent hypothesis about onboarding discovery. It stays repository-owned, draft and parked; no issue, accepted decision or garden projection is created. Mindgarden39 is verified closed not-planned and is not treated as a dependency.

Catalog/inventory/provider manifests and generated distributions reconcile the optional package: 37 specifications, 42 skills and 10 canonical agents. All 734 staged blobs and 6,791,350 raw bytes remain unchanged at the refreshed source ledger.

## Validation and review evidence

`./aether test under requirements-dev.lock environment` — passed: 367 full tests pass with 11 existing explicit optional/native skips.

`python -m unittest tests.test_exploration_notes tests.test_continuity_integration -q` — passed: 16 focused methods pass, including actual creation/no-op/overwrite refusal and source-linked parked canary.

`./aether eval run --skill author-exploration-note --mode deterministic --format json` — passed: All 11 declared structure/assertion cases pass with zero skips or suite errors; not model behavior.

`Catalog/schema/provenance/source/links/strict-staging/distribution and portable helper checks` — passed: All relevant source checks pass with historical default provenance warning retained. Actual generated package executes outside Aether under pinned dependencies; staged blob inventory remains unchanged.

ADR not required: implements the requested optional authored document output through existing specification/skill kinds; adds no public schema, global lifecycle policy, new owner, service or authorization. Roadmap impact: not-affected within existing authoring corpus. Existing ADR dispositions and all strategic identities remain unchanged.

## Blockers, risks, unknowns, and deferred work

The convention is optional draft authoring guidance and a consumer-owned Markdown output, not a new first-party artifact kind or organization lifecycle policy. No fleet installation, forced migration, issue promotion, garden ingestion or public deployment occurs.

The Aether canary is reviewed by Codex for source/authority/privacy and stays draft/parked. It supplies no human architectural acceptance, usefulness measurement, model effectiveness or organization applicability decision.

The helper checks bounded metadata and available local source paths; external references, source truth, private prose classification and actual review require independent verification. Authored edits and normal Git review own revisions; no archive or ingestion engine is added.

Mindgarden39 is closed not-planned as actually observed; it is historical context, not an active prerequisite. Existing downstream owner work remains separate. The real consumer/release gate under38 stays not-ready, with 11 existing optional/native skips explicit.

## Next dependency-ready work

Define the proposed people-first content policy at its Hygiene owner with source mappings, separate mechanical/human review, honest freshness/archive states and representative fixtures; preserve human activation and broader site-legal work.

## Parallel changes and reconciliation

Preserve merged133 conversation extension and proposed ADR0012,132 release source repair,131 worker guidance,130 roadmap composition and129 staging controls. Source integration does not establish native consumer readiness or policy ratification.

## Privacy and redaction

Public-safe source facts and synthetic fixtures only. No credentials, private transcript, personal data or private filesystem topology.

## Handoff update protocol

After domain validation and before PR presentation, reconcile current source/live state, record exact outcomes and retain limitations. Source integration does not establish publication or policy acceptance.

## Compaction and supersession

Git and linked work records retain history. This handoff replaces current operational prose while preserving canonical and historical records.
