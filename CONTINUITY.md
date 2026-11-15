---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-15T00:11:34Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Repair existing first-party release source selection, payload and metadata without publishing
    or promoting an unqualified stable set.
  includes:
  - Existing release workflow removes invalid job-level steps context and adds a read-only PR source qualification
    job. Tagged validation and protected publication remain dispatch-only. GH_TOKEN is mapped on CLI steps
    and checkout credentials are not persisted.
  - catalog/release_source.py binds the existing remote lightweight/annotated tag to full selected commit
    and current default-branch ancestry. Publication checks out the validated commit and refuses moved
    tags before rebuilding and immediately before publication.
  - Release tooling selects only stable/release-included skill inventories and eligible governed catalogs.
    Channel payload and deterministic archive share exact paths; draft/provider/unlisted/prior-output
    data is excluded without deleting development distributions.
  - Metadata uses acyclic checksums/provenance, requires full source SHA, recognizes canonical bracketed
    Unreleased, rejects unsafe input/output paths and refuses stale payload hashes. Synthetic stable-selection
    fixtures do not approve real artifacts.
  excludes: &id001
  - Actual Aether catalog has no release-eligible first-party skills; metadata preparation refuses the
    candidate. No lifecycle/rights status, reviewed stable set, tag or release is created or promoted.
  - Installed GitHub CLI has no skill command. Native consumer acceptance remains blocked/not-ready; portable
    pilot governing dependencies and remote install/update/deprecation/rollback remain issue38 obligations.
  - Actionlint validates workflow expressions and native disposable-Git/metadata fixtures qualify source
    behavior. Hosted PR source-job creation is pending; dispatch-only tagged jobs and publication are
    not exercised. Token mapping is source wiring, not credential or publication proof.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - .egohygiene/release.json
  - CHANGELOG.md
  - ROADMAP.md
  - .github/workflows/release-first-party-skills.yml
  - catalog/release_source.py
  - library/organization/skills/build-release-artifacts.py
  - docs/release-and-pinning-guide.md
  - docs/evidence/2026-11-15-release-source-qualification.json
  - docs/evidence/2026-11-15-release-source-roadmap-impact.json
  - https://github.com/egohygiene/aether/issues/38
work:
  objective: Repair existing first-party release source selection, payload and metadata without publishing
    or promoting an unqualified stable set.
  success_conditions:
  - Workflow parses and a read-only PR source job can execute without entering dispatch-only publication.
  - Native disposable-Git tests reject moved tags, wrong source and non-default ancestry while provenance
    uses the selected immutable commit.
  - Exact selected channel/archive inventories and final checksums agree; repeated metadata/archive output
    is stable and canonical changelog notes are retained.
  active_issue:
    provider: github
    id: egohygiene/aether#38
    url: https://github.com/egohygiene/aether/issues/38
  next:
    kind: issue
    id: egohygiene/aether#102
    description: After source qualification, compose optional conversation checkpoint/evidence extension
      with continuity; release38 stays open for a reviewed real stable set, available adapter, portable
      package dependencies and actual authorized remote proof.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/102
    - https://github.com/egohygiene/aether/issues/38
    depends_on: []
state:
  base:
    revision: aefd467e00906f6ee95a6bc27dd96ab97db3f545
    ref: refs/heads/main
    verified_at: '2026-11-15T00:11:34Z'
  candidate:
    branch: codex/release-source-integrity
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-15T00:11:34Z'
    default_branch_revision: aefd467e00906f6ee95a6bc27dd96ab97db3f545
    issue_state: open
    pull_request_state: not-applicable
    notes: Observed mainaefd467 includes merged131 and92 is closed.38 remains open. This implementation
      sourcef3f6cf3 has no PR yet; its later evidence/handoff commit cannot contain its own identifier.
      Remote tags are empty and installed gh skill is unavailable.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-15T00:11:34Z'
  reviewed_by: Codex
  evidence:
  - command: ./aether test
    outcome: passed
    notes: 351 full tests pass with11 existing explicit optional/native skips; no gate weakened.
    observed_at: '2026-11-15T00:11:34Z'
  - command: python -m unittest tests.test_release_artifacts tests.test_release_workflow tests.test_repository_release_contract
      -q
    outcome: passed
    notes: 24 focused tests include actual disposable Git origins and selected-payload/hash/archive controls.
    observed_at: '2026-11-15T00:11:34Z'
  - command: actionlint1.7.7 -shellcheck= -pyflakes= .github/workflows/release-first-party-skills.yml
    outcome: passed
    notes: Checksum-verified official binary reproduced the prior invalid steps context and accepts changed
      source. Optional external lint integrations disabled; every workflow shell body separately passes
      bash -n.
    observed_at: '2026-11-15T00:11:34Z'
  - command: Source/catalog/links/shell/distribution, release-declaration and staging ledger checks
    outcome: passed
    notes: Canonical source checks pass; existing default provenance warning retained. Actual catalog
      metadata candidate deliberately fails with no eligible skills; no tag is created.
    observed_at: '2026-11-15T00:11:34Z'
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

Repair existing first-party release source selection, payload and metadata without publishing or promoting an unqualified stable set.

- Workflow parses and a read-only PR source job can execute without entering dispatch-only publication.
- Native disposable-Git tests reject moved tags, wrong source and non-default ancestry while provenance uses the selected immutable commit.
- Exact selected channel/archive inventories and final checksums agree; repeated metadata/archive output is stable and canonical changelog notes are retained.

## State snapshot

Observed default source `aefd467e00906f6ee95a6bc27dd96ab97db3f545`. Candidate `codex/release-source-integrity` is a review checkpoint; its containing revision remains null intentionally.

## Completed and material changes

Existing release workflow removes invalid job-level steps context and adds a read-only PR source qualification job. Tagged validation and protected publication remain dispatch-only. GH_TOKEN is mapped on CLI steps and checkout credentials are not persisted.

catalog/release_source.py binds the existing remote lightweight/annotated tag to full selected commit and current default-branch ancestry. Publication checks out the validated commit and refuses moved tags before rebuilding and immediately before publication.

Release tooling selects only stable/release-included skill inventories and eligible governed catalogs. Channel payload and deterministic archive share exact paths; draft/provider/unlisted/prior-output data is excluded without deleting development distributions.

Metadata uses acyclic checksums/provenance, requires full source SHA, recognizes canonical bracketed Unreleased, rejects unsafe input/output paths and refuses stale payload hashes. Synthetic stable-selection fixtures do not approve real artifacts.

## Validation and review evidence

`./aether test` — passed: 351 full tests pass with11 existing explicit optional/native skips; no gate weakened.

`python -m unittest tests.test_release_artifacts tests.test_release_workflow tests.test_repository_release_contract -q` — passed: 24 focused tests include actual disposable Git origins and selected-payload/hash/archive controls.

`actionlint1.7.7 -shellcheck= -pyflakes= .github/workflows/release-first-party-skills.yml` — passed: Checksum-verified official binary reproduced the prior invalid steps context and accepts changed source. Optional external lint integrations disabled; every workflow shell body separately passes bash -n.

`Source/catalog/links/shell/distribution, release-declaration and staging ledger checks` — passed: Canonical source checks pass; existing default provenance warning retained. Actual catalog metadata candidate deliberately fails with no eligible skills; no tag is created.

No new architectural choice: implements existing explicit/manual first-party release path, owner boundaries and stable-selection rules. No replacement preparation engine, catalog lifecycle decision or public schema is introduced. Roadmap impact: updated factual partial evidence on AET-Q02/AET-Q04 only; both broader release gates remain unmet.

## Blockers, risks, unknowns, and deferred work

Actual Aether catalog has no release-eligible first-party skills; metadata preparation refuses the candidate. No lifecycle/rights status, reviewed stable set, tag or release is created or promoted.

Installed GitHub CLI has no skill command. Native consumer acceptance remains blocked/not-ready; portable pilot governing dependencies and remote install/update/deprecation/rollback remain issue38 obligations.

Actionlint validates workflow expressions and native disposable-Git/metadata fixtures qualify source behavior. Hosted PR source-job creation is pending; dispatch-only tagged jobs and publication are not exercised. Token mapping is source wiring, not credential or publication proof.

## Next dependency-ready work

After source qualification, compose optional conversation checkpoint/evidence extension with continuity; release38 stays open for a reviewed real stable set, available adapter, portable package dependencies and actual authorized remote proof.

## Parallel changes and reconciliation

Preserve131 checkpoint guidance,130 roadmap controls,129 staging guard and unchanged734 staging blobs. Original audit history and proposed ADR disposition remain unchanged.

## Privacy and redaction

Public-safe source facts and synthetic fixtures only. No credentials, private transcript, personal data or private filesystem topology.

## Handoff update protocol

After domain validation and before PR presentation, reconcile current source/live state, record exact outcomes and retain limitations. Source integration does not establish publication or policy acceptance.

## Compaction and supersession

Git and linked work records retain history. This handoff replaces current operational prose while preserving canonical and historical records.
