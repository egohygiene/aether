---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T07:04:17Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Record actual local Identity companion command qualification with preinstalled gh 2.96.0,
    retaining strict portability failures and complete release limits.
  includes:
  - Actual local install/list, generated-package validation, publish dry-run and cleanup receipts for
    the historical pilots and direct Identity companion.
  - Separate pristine export metadata failure from CLI-injected installed-host tracking, with exact
    CLI/package hashes and existing issue 38 next repair.
  - Documentation-only evidence, roadmap-impact reconciliation and bounded root continuity refresh.
  excludes:
  - No production code, canonical skill/specification, generated payload, maturity, version or release-policy
    changes.
  - No user-scope/global installation or configuration, remote install/update, publication, tag, release,
    hosted CI or stable promotion.
  - No observed agent authoring, automatic discovery, native OS-matrix or new Identity runtime/source
    qualification.
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
  - library/organization/skills/authoring/author-project-identity/SKILL.md
  - library/organization/skills/authoring/author-project-identity/references/identity-source-lock.json
  - docs/identity-companion.md
  - docs/work/identity-companion-host-20261122/VALIDATION.md
  - docs/work/identity-companion-host-20261122/package-observation.json
  - docs/work/identity-companion-host-20261122/consumer-companion-observation.json
  - docs/work/identity-companion-host-20261122/consumer-pilot-observation.json
  - docs/work/identity-companion-host-20261122/roadmap-impact.json
  - https://github.com/egohygiene/aether/issues/38
work:
  objective: Record actual local Identity companion command qualification with preinstalled gh 2.96.0,
    retaining strict portability failures and complete release limits.
  success_conditions:
  - Run actual local commands with the selected compatible CLI and exact draft generated package in
    disposable project scope.
  - Retain raw failed portable checks and not-ready status without weakening validators, rewriting source
    or inferring remote/stable acceptance.
  - Bind sanitized receipts to immutable source/package/CLI observations and the existing issue 38 repair
    owner.
  active_issue:
    provider: github
    id: egohygiene/aether38
    url: https://github.com/egohygiene/aether/issues/38
  next:
    kind: action
    id: align-export-and-installed-portability-under-38
    description: Review the docs-only host evidence; align package-build metadata projection with the
      existing verbatim-copy contract, then qualify explicitly verified installer tracking separately.
      Preserve strict validation and historical pilot findings; rerun local gates before any selected
      remote/release work.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/38
    depends_on: []
state:
  base:
    revision: 625aa5389473e05d5317fa7181db48117ef0cc42
    ref: refs/heads/main
    verified_at: '2026-11-22T07:04:17Z'
  candidate:
    branch: codex/identity-companion-host-qualification-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T07:04:17Z'
    default_branch_revision: 625aa5389473e05d5317fa7181db48117ef0cc42
    issue_state: open
    pull_request_state: not-applicable
    notes: Fresh remote main observed at 625aa53 at07:04:17Z; provider reads at06:58:46Z confirm issue38
      and tracker105 open. Companion PR139 is included in this base. No PR or release selection exists
      for this independent docs-only candidate.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-22T07:04:17Z'
  reviewed_by: Codex
  evidence:
  - command: Compatible gh 2.96.0 --version; skill install/list/publish --help; actual standard local
      harness
    outcome: failed
    observed_at: '2026-11-22T07:01:15Z'
    notes: Existing pilot build/install/list/publish-dry-run/cleanup pass; strict portability fails
      with existing canonical/staging prose plus installed tracking. CLI gate exits 1/not-ready; remote
      cases skipped.
  - command: Direct author-project-identity process-local pilot selection; unchanged consumer harness
      API
    outcome: failed
    observed_at: '2026-11-22T07:01:15Z'
    notes: Actual Codex project install/list, manifest/resources/template/eval structure, dry-run and
      cleanup pass. Raw installed portability fails 006/015/017; qualification.complete=false and overall
      not-ready.
  - command: validate_portable_skill_package on pristine dist/skills/author-project-identity
    outcome: failed
    observed_at: '2026-11-22T07:01:15Z'
    notes: 'AETHER_PORTABLE_015: verbatim SKILL frontmatter retains canonical aether-distribution-resources
      source. This is separate from installer-injected local-path.'
  - command: ./aether validate --links --json-files --format text; distribution build --check --output-directory
      dist
    outcome: passed
    observed_at: '2026-11-22T07:01:15Z'
    notes: Zero link/JSON diagnostics; all distribution drift checks pass. No canonical or generated
      artifacts changed.
  - command: Roadmap-impact receipt schema; root continuity schema/headings/budgets; staged whitespace
    outcome: passed
    observed_at: '2026-11-22T07:01:15Z'
    notes: Draft receipt is not-affected within AET-Q01/AET-Q05. Structural checks only; official released
      EgoLint conformance is not claimed.
  - command: Independent read-only docs/evidence review and exact 25-package-file hash/size comparison
    outcome: passed
    observed_at: '2026-11-22T07:04:17Z'
    notes: No blockers; failed pristine015/installed006-015-017 and not-ready receipts remain distinct
      from actual successful local commands. Public receipts pass private-path and credential-marker
      review.
  environment_limitations:
  - Strict pristine export and installed-instance portability remain failed; historical three-pilot
    canonical/staging findings remain.
  - Observed gh 2.96.0 file hash/self-reported version does not establish independent binary authenticity;
    default 2.46.0 was not upgraded.
  - No real agent authoring, automatic discovery, remote install/update, hosted CI, stable promotion,
    release or native OS-matrix qualification.
  - Draft 1.0.0 companion remains excluded from stable payloads; Identity source lock stays afc3680
    and its binary/runtime release is separate.
  - Only documentation/evidence checks were run for this checkpoint; historical broad suite results
    are not relabeled as a fresh run.
  - Official released EgoLint continuity conformance is unavailable; existing local schema/heading/budget
    checks supply structural evidence.
privacy:
  classification: public-repository
  contains_sensitive_data: false
  redactions:
  - Private local source/fixture/user paths and credential values sanitized by the existing report harness.
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

Runtime/user and scoped repository instructions, verified live state and canonical sources outrank this snapshot. This is a docs-only local host qualification handoff, not release readiness or promotion.

## Resume protocol

Read AGENTS, docs/identity-companion.md, the new dated validation/receipts and issue #38. Recheck main and live scope. Preserve unrelated working-tree edits and old receipts; select new exclusive report paths for any rerun.

## Current objective and success conditions

Record actual local author-project-identity install/list, strict validation, publish dry-run and cleanup with the already installed gh 2.96.0. Keep failures, draft status, immutable source/package pins and unrun remote/behavioral gates explicit.

## State snapshot

Base/main is 625aa5389473e05d5317fa7181db48117ef0cc42, containing companion PR #139. Candidate codex/identity-companion-host-qualification-20261122 is an independent docs-only child with no pre-commit revision/PR self-reference. Issues #38/#105 remain open.

## Completed and material changes

Added sanitized standard-pilot and direct-companion host receipts plus exact CLI/package hash and pristine validation observation. Updated the companion guide and linked the earlier historical checkpoint. No code, canonical skill/spec, generated payload, maturity or release boundary changed.

## Validation and review evidence

See docs/work/identity-companion-host-20261122/VALIDATION.md. Real gh 2.96.0 local install/list, dry-run and cleanup pass; both harness profiles remain not-ready. Pristine companion fails 015; its raw installed instance adds 006/017 for CLI tracking. Link/JSON, distribution drift, roadmap receipt and continuity structural checks pass; independent read-only review found no blockers. This checkpoint does not rerun the historical broad suite.

## Blockers, risks, unknowns, and deferred work

The new CLI is available without replacing default 2.46.0, but local command success is not portable acceptance. Build-resource metadata retained by verbatim copying and installer local-path tracking need separate handling under #38. Historical pilot provenance failures, actual agent behavior, native matrix, stable promotion and remote/release acceptance remain unresolved.

## Next dependency-ready work

Review this evidence, then align package-build metadata projection with the existing verbatim-copy contract and requalify pristine output. Separately constrain verified installed-host tracking without blanket path allowances or validator weakening. Reuse issue #38; no duplicate issue or remote action is authorized by this record.

## Parallel changes and reconciliation

This candidate is independent of Identity's engineering PR stack; root coordinates that separate handoff. Preserve unrelated Aether changes. ADR-0001/ADR-0002 retain canonical/generated and owner boundaries; no new ADR disposition. Roadmap impact:not-affected for existing AET-Q01/AET-Q05, with intent and release gates unchanged.

## Privacy and redaction

Receipts contain public source facts, package hashes and sanitized command evidence. Exclude credentials, private conversation, personal data and private local topology. No user-scope install or global configuration action was selected.

## Handoff update protocol

After domain checks, refresh this snapshot and validate exact schema, twelve headings and 16384-byte/240-line budgets; reverify live state before PR presentation. Preserve failed/not-run cases. Structural conformance cannot authenticate source, approvals or release readiness.

## Compaction and supersession

Git and dated receipts retain history. Replace current operational prose instead of appending logs; keep the earlier 2.46.0 observation as historical and the new 2.96.0 run time-qualified. Neither supplies stable publication or actual model-behavior evidence.
