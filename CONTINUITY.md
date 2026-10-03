---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-10-03T17:45:57Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Bounded handoff for ratified-policy ADR authoring (#91).
  includes:
  - 'Aether #91 authoring candidate, native checks, and canary compatibility'
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
  - docs/adr-authoring-adoption.md
  - library/organization/specs/architecture/governance/decisions.spec.md
  - library/organization/skills/architecture/create-decisions-document/SKILL.md
  - library/organization/skills/architecture/create-decisions-document/references/policy-selection.json
work:
  objective: Align the existing ADR skill and decision-impact guidance with ratified Hygiene policy.
  success_conditions:
  - Consistent proposed authoring, historical evidence, lineage, and two decision-impact checkpoints
  - Exact policy authority with draft Aether artifacts and independent proposed contracts preserved
  - Passing native owner validation and explicit canary compatibility limits
  active_issue:
    provider: github
    id: egohygiene/aether#91
    url: https://github.com/egohygiene/aether/issues/91
  next:
    kind: action
    id: review-adr-authoring-candidate
    description: 'Review the #91 candidate; resolve the documented Holon policy-reference upgrade before
      canary materialization.'
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/91
    - https://github.com/egohygiene/identity/issues/69
    depends_on: []
state:
  base:
    revision: 087bceccd936922371155e69dc92ff802aa8a029
    ref: refs/heads/main
    verified_at: '2026-10-03T17:45:57Z'
  candidate:
    branch: codex/adr-authoring-91
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: partial
    observed_at: '2026-10-03T17:45:57Z'
    default_branch_revision: 087bceccd936922371155e69dc92ff802aa8a029
    issue_state: open
    pull_request_state: not-applicable
    notes: 'Main and issue #91 were checked through GitHub; no open Aether PRs were observed before publication.
      Candidate PR and its CI do not yet exist in this snapshot; discover them through #91. Host-specific
      adoption remains unverified.'
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-10-03T17:45:57Z'
  reviewed_by: Codex
  evidence:
  - command: python3 aether test
    outcome: passed
    observed_at: '2026-10-03T17:45:57Z'
    notes: 199 tests passed, zero skips. ADR owner/runtime variables and AETHER_EGOLINT_BINARY were configured;
      all 11 ADR tests and existing native title tests ran.
  - command: python3 aether eval run --mode deterministic --format text
    outcome: passed
    observed_at: '2026-10-03T17:45:57Z'
    notes: 205 cases passed across 36 skills, including nine ADR cases. Checks authored examples; does
      not execute a model.
  - command: python3 aether validate --format text
    outcome: passed
    observed_at: '2026-10-03T17:45:57Z'
    notes: No errors. Existing preserved staging-hash provenance warning remains. Shell and strict staging
      checks also passed.
  - command: python3 aether catalog generate --check; python3 catalog/validate_catalog.py; python3 catalog/provenance_model.py
      check --scope all
    outcome: passed
    observed_at: '2026-10-03T17:45:57Z'
    notes: Catalog, schemas, fixtures, coverage, relationships and provenance checks passed.
  - command: python3 aether distribution build --output-directory dist --check
    outcome: passed
    observed_at: '2026-10-03T17:45:57Z'
    notes: Generated skill, spec and provider artifacts are current.
  - command: Two clean distribution builds; gh skill publish dist --dry-run
    outcome: passed
    observed_at: '2026-10-03T17:45:57Z'
    notes: Distribution byte equality and publish-payload validation passed; no publication occurred.
  environment_limitations:
  - Relay native execution requires its separately pinned Python environment; Aether dependencies alone
    are insufficient.
  - No host-specific skill loading, hosted architecture acceptance, publication or fleet adoption evidence
    is claimed.
  - No released continuity conformer was run; structural schema and semantic review are recorded separately.
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

Resume #91 using the front-matter precedence. This replaces the stale #98
checkpoint after PR #99 merged; Git preserves that earlier handoff. The current
change grants no new policy, lifecycle, merge or publication authority.

## Resume protocol

1. Read scoped instructions, canonical sources above, branch status and history.
2. Recheck issue #91, the resulting PR and exact main/head revisions on GitHub.
3. Reconcile parallel changes and owner compatibility before applying anything.
4. Keep authoring readiness, human disposition, validation and adoption separate.

## Current objective and success conditions

Make historical reconstruction, proposal, correction, reference and proposed
replacement consistent across the skill, specification, templates and managed
guidance. Preserve human authority, source history and read-only role permissions.

## State snapshot

The base and branch are recorded above; pre-publication candidate SHA and PR are
intentionally null. Hygiene policy v1.1.0 is already ratified at the selected
commit. Relay PR #121 is merged at 33e1fc78727269bd3821dea53f6541f769cf4319;
this candidate selects its advisory architecture profile 1.0.0-alpha.2.
The authoring skill/spec/module remain draft; Intelligence remains proposed.

## Completed and material changes

- Aligned existing authoring sources and generated packages with Hygiene policy.
- Added evidence-preserving history, migration, correction and lineage guidance.
- Routed both decision-impact checkpoints to the shared skill; retained permissions.
- Added owner-backed template/native tests and nine deterministic example cases.
- Documented pinned adoption, compatibility, upgrade, rollback and canary limits.

## Validation and review evidence

The full 199-test suite passed without skips, including all native integrations.
All 205 deterministic cases passed. Required catalog/distribution/validation
checks passed; generated outputs reproduce byte-for-byte. The earlier #98 gh
environment error is resolved. Native tests preserve source bytes and prove that
implementation without approval and the old materializer policy pin are rejected.
See front matter and the adoption checkpoint for commands and evidence limits.

## Blockers, risks, unknowns, and deferred work

Holon's selected blueprint still emits the older policy pin. A reviewed owner
upgrade is required before materializing a ratified-policy canary. Hygiene's old
decision-set helper also disagrees on pending reciprocal lineage; the selected
EgoLint/Relay consumer supports proposed replacements without changing the old
accepted record. Do not fake approval or edit generated hashes to bypass either.
Hosted architecture acceptance remains deferred under Relay #99. Aether's own
backfill (#85), the default bundle (#67), releases and fleet adoption remain open.

## Next dependency-ready work

Review the #91 candidate and its CI. Identity #69 under Pace #5 remains the first
validate-first canary, subject to its scheduling gate and owner compatibility.
Use its existing corpus to preview a bounded adoption; do not begin bulk backfill
or deployment from this handoff.

## Parallel changes and reconciliation

No open Aether PR was observed in the pre-publication check. Recheck at review
time; a dependency merge does not silently upgrade this candidate's pinned inputs.

## Privacy and redaction

Public repository handoff with synthetic test examples. No private paths,
credentials, personal conversations or protected source content are included.

## Handoff update protocol

Refresh after domain validation and before the next PR update. Reconcile live
head, issue and CI state rather than treating this snapshot as current proof.
Keep the handoff in the same bounded change; do not accumulate a transcript.

## Compaction and supersession

Remain below 16,384 UTF-8 bytes and 240 lines. Replace stale operational state;
canonical documents, Git and issue/PR history retain durable facts and chronology.
