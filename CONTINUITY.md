---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-03T02:00:47Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Bounded handoff for the issue-title authoring checkpoint (#98).
  includes:
  - 'Aether #98 candidate implementation, local checks, and dependency state'
  excludes:
  - conversation transcripts
  - duplicated architecture, roadmap, and changelog content
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - docs/issue-title-authoring-pilot.md
  - library/organization/skills/authoring/github-issue-authoring/SKILL.md
  - library/organization/skills/authoring/github-issue-authoring/references/issue-title-contract/selection.v1.json
work:
  objective: Make the existing issue authoring skill discover and consume the pinned title contract.
  success_conditions:
  - One immutable selection shared by skill and managed projections
  - Real Egolint synthetic title evidence with preserved subject and IDs
  - Explicit unavailable evidence and unchanged read-only agent permissions
  active_issue:
    provider: github
    id: egohygiene/aether#98
    url: https://github.com/egohygiene/aether/issues/98
  next:
    kind: action
    id: review-issue-title-authoring-candidate
    description: Review this bounded candidate and resolve the dependency reviews before selecting accepted
      pins; prepare the Relay pilot as a separate checkpoint.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/98
    - https://github.com/egohygiene/.github/issues/24
    depends_on: []
state:
  base:
    revision: 1072a0fafe145f919b3f83bbbc6daee2cb946030
    ref: refs/heads/main
    verified_at: '2026-10-03T02:00:47Z'
  candidate:
    branch: codex/issue-title-authoring-98
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: partial
    observed_at: '2026-10-03T02:00:47Z'
    default_branch_revision: 1072a0fafe145f919b3f83bbbc6daee2cb946030
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Main and issue #98 were checked through GitHub. Could not verify provider label availability
      or remote CI. Candidate PR has not yet been created; find its live head through issue #98. Dependency
      PRs were observed open/unmerged during this session.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-03T02:00:47Z'
  reviewed_by: Codex
  evidence:
  - command: python3 -m unittest discover -s tests -p test_issue_title_authoring.py -v
    outcome: passed
    observed_at: '2026-10-03T02:00:47Z'
    notes: 11 tests passed with AETHER_EGOLINT_BINARY set to the declared consumer build; includes 18
      upstream cases and two reviewed migrations in the final full run.
  - command: python3 aether test
    outcome: limited
    observed_at: '2026-10-03T02:00:47Z'
    notes: 'Final run: 188 tests, 187 passed, one error. Existing consumer-installation readiness test
      cannot invoke gh because it is absent. No title integration tests skipped; AETHER_EGOLINT_BINARY
      was set.'
  - command: python3 aether validate --format text
    outcome: passed
    observed_at: '2026-10-03T02:00:47Z'
    notes: No errors; existing preserved staging-hash provenance warning remains.
  - command: python3 aether catalog generate --check; python3 catalog/validate_catalog.py
    outcome: passed
    observed_at: '2026-10-03T02:00:47Z'
    notes: Catalog is current; schema, fixtures, coverage, relationships, and digest checks passed.
  - command: python3 aether distribution build --output-directory dist --check
    outcome: passed
    observed_at: '2026-10-03T02:00:47Z'
    notes: Generated skill/spec/provider outputs are current. Python bytecode caches no longer affect
      generated packages.
  - command: Fresh-context synthetic GitHub Issue Creator exercise
    outcome: passed
    observed_at: '2026-10-03T02:00:47Z'
    notes: Discovered the portable skill through local AGENTS.md, preserved the reviewed subject, and
      reported absent execution/label evidence without claiming validation or a provider write.
  - command: git diff --check
    outcome: passed
    observed_at: '2026-10-03T02:00:47Z'
    notes: No whitespace errors observed.
  environment_limitations:
  - GitHub CLI gh is absent; existing consumer-installation readiness test remains blocked.
  - Python jsonschema 4.25.1 was supplied through a temporary PYTHONPATH.
  - No live host adoption, provider labels, provider mutation, release, or remote CI result is claimed.
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

# Aether continuity

## Purpose and precedence

Resume the bounded #98 change using the front-matter precedence. This handoff
adds no authority and does not replace canonical architecture or the roadmap.
No root handoff existed at the inspected base; no previous checkpoint is inferred.

## Resume protocol

1. Read local AGENTS.md, canonical sources above, branch status, and recent history.
2. Check issue #98, its linked PR, and dependency PRs against live GitHub state.
3. Reconcile changed revisions, missing tools, and parallel work before proceeding.
4. Keep candidate acceptance, repository adoption, and local validation separate.

## Current objective and success conditions

Connect existing authoring guidance to one pinned issue-title contract. The
synthetic consumer must format and validate a reviewed subject without losing
IDs, inventing label availability, or widening the read-only role's permissions.

## State snapshot

Base and candidate branch are recorded above. Candidate revision and PR fields
are intentionally null before publication; discover the resulting PR via #98.
Dependency contract PR .github#45 and Egolint PR #79 were observed open/unmerged.
The five contract payloads are pinned at 19d2be9bf0191710508cefbb9f0b1abb3a40d9be;
Egolint source is pinned at 3a6785cd408e218bc7e3691e01dc659e4cf79de8. Both selections
remain candidate. A dependency merge does not silently promote the embedded pin.

## Completed and material changes

- Extended the existing skill, checklist, template, evals, and issue-creator agent.
- Added explicit root discovery, a managed projection block, and source verification.
- Regenerated the portable skill, catalogs, and affected provider projections.
- Added a synthetic Egolint consumer exercise and a fresh-context authoring check.
- Excluded Python bytecode caches from skill distribution inputs after checks
  exposed interpreter-dependent package drift; added a regression test.
- Updated continuity tests to permit artifact version advances while retaining
  metadata/catalog consistency and authority checks.

## Validation and review evidence

Exact commands, results, and limitations are recorded in front matter. All 11
issue-title tests passed with the real Egolint candidate, including upstream
examples and reviewed migrations. The full suite has one environment error from
missing gh; do not describe the entire suite as passing. Generated-output checks
and catalog validation passed. The fresh-context check returned an unvalidated
draft with correct provenance and explicitly unavailable provider/tool evidence.

## Blockers, risks, unknowns, and deferred work

- Blocker to complete full-suite evidence: install the required gh tooling and
  rerun the existing consumer-installation readiness test in a suitable environment.
- Candidate dependency acceptance remains external to this checkpoint.
- Live provider labels, remote CI, and actual host loading are unknown.
- Relay execution, label provisioning, fleet adoption/migration, and future-title
  enforcement remain under .github#24; the broader Aether #67 bundle is incomplete.

## Next dependency-ready work

Review the #98 candidate and its dependency PRs. Once accepted source revisions
are verified, deliberately update pins/authority. Then scope the Relay pilot:
preview/apply, current-state checks, receipts, rollback, and a no-op repeat before
any fleet sweep. This checkpoint authorizes none of those provider operations.

## Parallel changes and reconciliation

No other open Aether PR was observed at initial inspection. Recheck before merge;
other repositories' dependency PRs do not establish acceptance of this candidate.

## Privacy and redaction

Public repository handoff. No credentials, personal conversation text, private
paths, or unrelated personal context is included. Synthetic examples only.

## Handoff update protocol

Refresh after relevant validation and before the next PR update. Recheck live
state instead of interpreting this pre-publication snapshot as current proof.
Include changes to this handoff with the bounded repository change.

## Compaction and supersession

Keep below 16,384 UTF-8 bytes and 240 lines. Replace stale state instead of
accumulating a transcript; Git and issue/PR history own chronology.
