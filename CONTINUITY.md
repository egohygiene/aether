---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T06:16:17.396416+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Prepare the Identity-specific authoring workflow specification and portable companion skill,
    with bounded source-hash verification and honest host qualification.
  includes:
  - Draft project-identity-authoring specification and author-project-identity skill, pinned Identity
    resource lock, capability/checklist guides and small-batch intake template.
  - Optional read-only helper, eight authored evaluation scenarios, generated standalone package and meaningful
    portability/failure controls.
  - Bounded distribution-builder compatibility-text repair with three regression cases; no distribution
    schema change.
  excludes:
  - Actual gh skill installation/publication and agent behavior are unqualified; installed gh 2.46.0 has
    no skill command.
  - No Identity field semantics, human approvals, repository enforcement, binary release, stable skill
    promotion or org strategy changes.
  - No hosted CI dispatch, tool installation, tag, release, registry publication or site deployment.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - library/organization/specs/authoring/project-identity-authoring.spec.md
  - library/organization/skills/authoring/author-project-identity/SKILL.md
  - library/organization/skills/authoring/author-project-identity/references/identity-source-lock.json
  - docs/identity-companion.md
  - docs/work/identity-companion-20261122/VALIDATION.md
  - docs/work/identity-companion-20261122/roadmap-impact.json
work:
  objective: Prepare the Identity-specific authoring workflow specification and portable companion skill,
    with bounded source-hash verification and honest host qualification.
  success_conditions:
  - Provide a packaged Identity-specific workflow with explicit v0/v1, Python, source/output and human-decision
    boundaries.
  - Exercise the copied helper outside Aether with real declared source bytes and failure controls without
    executing or changing them.
  - Retain draft release exclusion and the actual not-ready consumer gate; do not substitute authored
    evaluations for observed agent behavior.
  active_issue:
    provider: github
    id: egohygiene/aether#105
    url: https://github.com/egohygiene/aether/issues/105
  next:
    kind: action
    id: review-identity-companion-and-qualify-host
    description: 'Review this draft companion and use a genuinely compatible gh skill adapter to qualify
      actual installation and observed authoring before stable promotion. Retain the existing #38 release
      and consumer gates.'
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/38
    - https://github.com/egohygiene/identity/issues/98
    depends_on: []
state:
  base:
    revision: 3c836942bc2af10baaaf8936b114d4c9f4f59be8
    ref: refs/heads/main
    verified_at: '2026-11-22T06:16:17.396416+00:00'
  candidate:
    branch: codex/identity-companion-skill-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T06:16:17.396416+00:00'
    default_branch_revision: 3c836942bc2af10baaaf8936b114d4c9f4f59be8
    issue_state: open
    pull_request_state: not-applicable
    notes: Main and tactical tracker105 rechecked through the provider. Identity155 and156 remain open
      drafts; its separate distribution plan is in progress. No PR exists for this candidate at this checkpoint.
  parallel_changes:
  - provider: github
    id: egohygiene/identity#155
    url: https://github.com/egohygiene/identity/pull/155
  - provider: github
    id: egohygiene/identity#156
    url: https://github.com/egohygiene/identity/pull/156
review:
  status: partial
  reviewed_at: '2026-11-22T06:16:17.396416+00:00'
  reviewed_by: Codex
  evidence:
  - command: ./aether catalog generate; ./aether distribution build --output-directory dist; --check
    outcome: passed
    observed_at: '2026-11-22T06:16:17.396416+00:00'
    notes: Generated catalogs and package, checked drift; the two new 1.0.0 records remain draft and excluded
      from stable payloads.
  - command: ./aether validate --format text; ./aether test
    outcome: passed
    observed_at: '2026-11-22T06:16:17.396416+00:00'
    notes: Validation succeeds with the existing staging provenance warning. Full suite:405 tests,394
      passed and11 existing optional/native skips.
  - command: Copied generated package under Python -I; declared Identity resource verification
    outcome: passed
    observed_at: '2026-11-22T06:16:17.396416+00:00'
    notes: Eleven helper/package controls pass. Nine actual pinned resource byte/hash checks pass, without
      source execution/mutation; scope excludes binary, Git HEAD and release authenticity.
  - command: ./aether eval run --skill author-project-identity --mode deterministic --format json
    outcome: passed
    observed_at: '2026-11-22T06:16:17.396416+00:00'
    notes: Eight authored structural/golden scenarios pass declared assertions; no observed routing, model
      reasoning or real brand authoring is claimed.
  - command: python3 -m catalog.consumer_installation --scope local
    outcome: limited
    observed_at: '2026-11-22T06:16:17.396416+00:00'
    notes: 'Actually executed: distribution build passes, required local gh skill host scenarios are blocked
      by installed gh2.46.0. Exit1/not-ready retained; no remote scope selected.'
  - command: Roadmap-impact receipt and independent package review
    outcome: passed
    observed_at: '2026-11-22T06:16:17.396416+00:00'
    notes: Receipt is not-affected within AET-Q01; no strategic change. Independent read-only review finds
      no blockers in the package, helper, tests and bounded builder repair.
  environment_limitations:
  - Actual gh skill installation/publication and agent behavior are unqualified; installed gh 2.46.0 has
    no skill command.
  - No Identity field semantics, human approvals, repository enforcement, binary release, stable skill
    promotion or org strategy changes.
  - No hosted CI dispatch, tool installation, tag, release, registry publication or site deployment.
  - Official released EgoLint continuity conformance is not claimed; structural validation uses the existing
    pinned schema.
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

Runtime/user and scoped repository instructions, live evidence and canonical sources outrank this operational checkpoint. This is a draft source/package handoff.

## Resume protocol

Read AGENTS, the canonical companion sources, validation record and live branches/issues before acting. Preserve the unrelated dirty checkout and historical decisions; work on this isolated candidate branch.

## Current objective and success conditions

Prepare the Identity-specific authoring workflow specification and portable companion skill, with bounded source-hash verification and honest host qualification. Preserve Identity authority and actual approval, runtime and publication boundaries.

## State snapshot

Base/main is 3c836942bc2af10baaaf8936b114d4c9f4f59be8. Candidate codex/identity-companion-skill-20261122 has no self-referential revision/PR at this pre-PR checkpoint. The Identity stack155->156 and its new release-plan child are separate.

## Completed and material changes

Added the draft workflow spec, companion skill, pinned nine-resource lock, CLI/checklist guides, intake template, optional read-only hash helper and eight authored evaluations. Generated distribution carries the governing spec. Three builder regressions cover standard compatibility prose, legacy mapping preservation and invalid types; eleven portability/failure controls exercise the copied package.

## Validation and review evidence

See docs/work/identity-companion-20261122/VALIDATION.md and its source-lock/consumer receipts. Full suite405 succeeds with11 existing skips; source/catalog/distribution and eight declared eval checks pass. Independent package review reports no blockers. Real consumer gate stays not-ready on gh2.46.0. Earlier compatibility and wrapped-continuity defects were corrected and actual tests rerun without weakening assertions. Roadmap disposition:not-affected within AET-Q01.

## Blockers, risks, unknowns, and deferred work

Actual gh skill install/list/publish-dry-run qualification needs a compatible adapter; the harness used existing pilot skills, not direct installation of this companion. Actual model behavior, stable promotion and remote release proof remain unqualified. The helper checks only declared resource bytes; it does not authenticate a binary, Git HEAD, complete checkout, human review or release. Existing #38 gates and unrelated owner-release prerequisites remain.

## Next dependency-ready work

Review the authored package and qualify actual use on a compatible host; maintain draft status until its maturity and release gates pass. Revisit the Identity source pin only after reviewing changed schemas/CLI and real runtime evidence. Identity #98/#116 own broader binary and self-source completion.

## Parallel changes and reconciliation

Aether canonical/generated ownership and neighboring-owner boundaries remain governed by preserved ADR-0001/ADR-0002. No new ADR is required for this bounded addition/compatibility-shape repair. Preserve proposed ADR-0009 and historical decision conflict without inferring human disposition. Reconcile concurrent continuity edits semantically and preserve all unrelated working-tree edits.

## Privacy and redaction

Public-safe source facts, declared upstream hashes and synthetic cases only. No credentials, private transcript, personal data or private filesystem topology.

## Handoff update protocol

Recheck current source and live state after domain validation and before PR presentation. Validate schema, twelve headings, byte/line budgets and whitespace; retain exact failures, skips and blocked host checks. This handoff grants no new external authority.

## Compaction and supersession

Git and linked work records retain earlier checkpoints. Replace current operational prose rather than append stale state; do not rewrite historical evidence or canonical policies.
