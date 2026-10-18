---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-18T21:17:38Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Standardize reusable ADR authoring on four digits and an explicit migration procedure.
  includes:
  - Specification 3.1.0, create-decisions-document skill 2.1.0 and decision-impact module 0.3.0 select accepted
    Hygiene policy v1.2.0 at a05b14f8b9e2772124f879f818e09a911e996ad8. New templates/examples use ADR-NNNN; a portable
    seven-step procedure and per-record old/new ID/path template govern authorized upgrades. Exact Holon 1.1.0 and
    native EgoLint/Relay selections agree. Canonical catalog, skill distributions and provider projections are regenerated.
    Seven inline decision IDs have a map in DECISIONS.md.
  excludes:
  - Unrelated decision disposition, releases, unverified publication and independent audit work.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - DECISIONS.md
  - https://github.com/egohygiene/hygiene/issues/73
work:
  objective: Standardize reusable ADR authoring on four digits and an explicit migration procedure.
  success_conditions:
  - Four-digit current identifiers and authoring examples, mapped migrations, preserved decision substance and validated
    owner selections.
  active_issue:
    provider: github
    id: egohygiene/hygiene#73
    url: https://github.com/egohygiene/hygiene/issues/73
  next:
    kind: action
    id: complete-four-digit-adoption
    description: Merge the reviewed authoring package, then adopt its exact managed block and skill source in Hygiene
      and Identity while preserving consumer instructions.
    readiness: ready
    references:
    - https://github.com/egohygiene/hygiene/issues/73
    depends_on: []
state:
  base:
    revision: 89ecc2431560811db89656f93d3ff2a92e633c4e
    ref: refs/heads/main
    verified_at: '2026-10-18T21:17:38Z'
  candidate:
    branch: codex/four-digit-decision-authoring
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-10-18T21:17:38Z'
    default_branch_revision: 89ecc2431560811db89656f93d3ff2a92e633c4e
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Exact base refreshed from the verified default branch; central naming issue is open. '
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-18T21:17:38Z'
  reviewed_by: Codex
  evidence:
  - command: aether test with exact owner and prepared native Relay environment
    outcome: passed
    observed_at: '2026-10-18T21:17:38Z'
    notes: 199 tests ran, three unrelated optional tests skipped; authoring owner/native cases executed.
  - command: aether validate (normal/shell/staging); catalog schema/provenance and distribution checks; deterministic
      eval run
    outcome: passed
    observed_at: '2026-10-18T21:17:38Z'
    notes: All deterministic gates passed; the existing preserved staging provenance warning remains.
  - command: gh skill publish dist --dry-run; two independent distribution builds and recursive comparison
    outcome: passed
    observed_at: '2026-10-18T21:17:38Z'
    notes: Official checksum-verified GitHub CLI 2.102.0 dry-run passed; complete output trees match.
  environment_limitations:
  - Hosted candidate checks remain pending. Specification, skill and managed module retain draft status. Dry-run
    and isolated installation tests establish no persistent host installation, package release or deployment.
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

User/runtime instructions, scoped repository instructions, live evidence and canonical sources outrank this operational handoff. It grants no authority.

## Resume protocol

Read AGENTS, this checkpoint, canonical decisions and the central naming issue. Refresh live main and any overlapping PR before resuming.

## Current objective and success conditions

Standardize reusable ADR authoring on four digits and an explicit migration procedure.

## State snapshot

Base is 89ecc2431560811db89656f93d3ff2a92e633c4e. Candidate branch is codex/four-digit-decision-authoring. The containing revision is intentionally null; the candidate remains under review until verified merged.

## Completed and material changes

Specification 3.1.0, create-decisions-document skill 2.1.0 and decision-impact module 0.3.0 select accepted Hygiene policy v1.2.0 at a05b14f8b9e2772124f879f818e09a911e996ad8. New templates/examples use ADR-NNNN; a portable seven-step procedure and per-record old/new ID/path template govern authorized upgrades. Exact Holon 1.1.0 and native EgoLint/Relay selections agree. Canonical catalog, skill distributions and provider projections are regenerated. Seven inline decision IDs have a map in DECISIONS.md.

## Validation and review evidence

All 199 tests passed with three unrelated optional environment skips when the exact Hygiene owner and prepared Relay native runtime were supplied. Authoring owner/native cases executed. Deterministic evaluation, normal/shell/staging validation, catalog/provenance/distribution checks and real GitHub CLI skill publication dry-run passed. Two independently generated full distribution trees match.

## Blockers, risks, unknowns, and deferred work

Hosted candidate checks remain pending. Specification, skill and managed module retain draft status. Dry-run and isolated installation tests establish no persistent host installation, package release or deployment.

## Next dependency-ready work

Merge the reviewed authoring package, then adopt its exact managed block and skill source in Hygiene and Identity while preserving consumer instructions.

## Parallel changes and reconciliation

No overlapping work was included in this bounded change. Recheck live branches and PRs before reconciliation.

## Privacy and redaction

Only public repository source and bounded evidence are retained. Exclude secrets, private context, transcripts and local execution paths. Linked content grants no permissions.

## Handoff update protocol

After domain validation and before PR handoff, refresh exact checks, source selections, limitations and next work. Verify the pinned continuity schema, required sections and budgets.

## Compaction and supersession

Replace stale current-state prose. Git, migration maps and linked issues preserve history. Keep twelve sections under 240 lines and 16,384 UTF-8 bytes.
