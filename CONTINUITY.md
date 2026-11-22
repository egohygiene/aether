---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-22T18:20:33.900407+00:00'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Repair build-only metadata leakage in portable skill exports while preserving canonical source,
    provenance and strict validation.
  includes:
  - Narrow generated-frontmatter projection consumes only aether-distribution-resources after resource
    validation/copying.
  - All ten declaring packages, unchanged canonical bytes/resources/manifests and ordinary exports, plus
    meaningful regression evidence.
  - Existing source/generated contract clarification, roadmap-impact disposition and bounded continuity.
  excludes:
  - No installed-host adapter, strict-validator, manifest-schema, canonical skill/specification or maturity/version
    changes.
  - No stable promotion, remote install/update, hosted CI, tag, release or publication.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - ROADMAP.md
  - library/organization/skills/build-distributions.py
  - library/organization/skills/SKILL-CONTRACT.md
  - tests/test_build_distributions.py
  - docs/work/38/export-projection-20261122/VALIDATION.md
  - docs/work/38/export-projection-20261122/projection-observation.json
  - docs/work/38/export-projection-20261122/roadmap-impact.json
  - https://github.com/egohygiene/aether/issues/38
work:
  objective: Repair build-only metadata leakage in portable skill exports while preserving canonical source,
    provenance and strict validation.
  success_conditions:
  - Pristine Identity companion passes unchanged strict portability without canonical paths from a build-only
    field.
  - All canonical skill bytes, ordinary field values/body bytes, resource/manifests and 33 ordinary skill
    exports remain unchanged.
  - Invalid resources and genuine runtime/private paths still fail; release and installed-host readiness
    stay separate.
  active_issue:
    provider: github
    id: egohygiene/aether#38
    url: https://github.com/egohygiene/aether/issues/38
  next:
    kind: action
    id: qualify-verified-installed-host-materialization
    description: Integrate the separately owned installed-host verification checkpoint, then rerun actual
      local companion qualification. Retain historical pilot runtime/provenance findings and all stable/remote-release
      gates.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/38
    depends_on: []
state:
  base:
    revision: e5a67e581857122a8131fe8a24d1c7e6c1fa1170
    ref: refs/heads/main
    verified_at: '2026-11-22T18:20:33.900407+00:00'
  candidate:
    branch: codex/38-build-metadata-projection-20261122
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-22T18:20:33.900407+00:00'
    default_branch_revision: e5a67e581857122a8131fe8a24d1c7e6c1fa1170
    issue_state: open
    pull_request_state: not-applicable
    notes: Fresh provider reads verify main e5a67e5, issue38 open and zero open Aether PRs. Earlier companion139
      and host140 are merged. This source candidate has not been pushed or opened as a PR.
  parallel_changes: []
review:
  status: partial
  reviewed_at: '2026-11-22T18:20:33.900407+00:00'
  reviewed_by: Codex
  evidence:
  - command: Focused test_build_distributions.py discovery
    outcome: passed
    observed_at: '2026-11-22T18:20:33.900407+00:00'
    notes: 42 tests pass, including five new projection methods and existing confinement/failure controls.
  - command: ./aether test
    outcome: passed
    observed_at: '2026-11-22T18:20:33.900407+00:00'
    notes: 410 discovered:399 passed and11 existing optional/native skips.
  - command: ./aether catalog generate; distribution build and --check; validate --format text
    outcome: passed
    observed_at: '2026-11-22T18:20:33.900407+00:00'
    notes: Catalog bytes unchanged; generated families current; source validation passes with the unchanged
      historical AETHER_PROVENANCE_009 warning.
  - command: Complete corpus source/export/resource/hash observation and pristine companion validation
    outcome: passed
    observed_at: '2026-11-22T18:20:33.900407+00:00'
    notes: Ten declaring headers project only the build key;33 ordinary exports,43 canonical skills and
      all manifests/resources retain bytes. Identity companion returns zero strict diagnostics; two other
      declaring packages retain separate runtime/provenance findings.
  - command: Roadmap receipt, continuity schema/headings/budgets and whitespace
    outcome: passed
    observed_at: '2026-11-22T18:20:33.900407+00:00'
    notes: Not-affected within AET-Q01/AET-Q05; structural checks do not establish official released EgoLint,
      strategy or release acceptance.
  environment_limitations:
  - Installed-host tracking is a separate adapter checkpoint; no installed instance is declared portable
    by this repair.
  - audit-repository retains strict015/016 and create-repository-journal retains015; actual corpus observations
    preserve those failures.
  - The11 existing optional/native skips, actual agent behavior, stable maturity, remote consumption and
    release acceptance remain separate.
  - No official released EgoLint continuity conformance is claimed; existing schema/headings/budget checks
    provide structural evidence.
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

Runtime/user and scoped instructions, verified live state and canonical sources outrank this operational handoff. This is a source/export checkpoint under existing issue38, not stable release acceptance.

## Resume protocol

Read AGENTS, builder/contract/tests and the dated export observation. Recheck main and issue38. Preserve the unrelated dirty Aether checkout, canonical skills and historical host receipts; use the isolated candidate branch.

## Current objective and success conditions

Repair build-only metadata leakage in portable skill exports while preserving canonical source, provenance and strict validation. Omit only compile-time build metadata after validation; retain every actual runtime/private-path check.

## State snapshot

Base/main is e5a67e581857122a8131fe8a24d1c7e6c1fa1170. Candidate codex/38-build-metadata-projection-20261122 has no containing-revision or pre-PR self-reference. Earlier139/140 are merged; this checkpoint is not pushed/merged/published.

## Completed and material changes

The builder consumes the resource declaration and deterministically projects opted-in headers without it. Canonical bytes, body bytes, ordinary field values, resource bytes and canonical source_digest remain intact. Contract/docs state the narrow exception; ordinary skills remain exact UTF8/LF copies. Ten generated SKILL headers change and no manifest/resource/catalog record changes.

## Validation and review evidence

42 focused tests and the full410-test suite succeed with11 existing skips. Catalog generation, distribution build/drift and source validation pass with the historical staging warning. The complete corpus observation verifies43 unchanged canonical skills,33 unchanged ordinary exports,10 projected headers and unchanged manifests/resources. Pristine Identity companion passes strict portability with zero diagnostics. See docs/work/38/export-projection-20261122/VALIDATION.md and its source-bound observation.

## Blockers, risks, unknowns, and deferred work

This repairs pristine export only. The actual installed-host tracking problem remains for the separately owned adapter. audit-repository retains015/016 and create-repository-journal retains015 from other content. Historical three-pilot, stable-selection, remote/release and observed-agent behavior gates stay open; no failed scenario is relabeled passed.

## Next dependency-ready work

Integrate the installed-host materialization comparison, requalify actual local companion commands with the selected compatible CLI, and retain separate raw/pristine/host outcomes. Resolve historical pilot governing resources/provenance within existing38 rather than weakening strict path validation. Keep draft artifacts release-excluded.

## Parallel changes and reconciliation

A peer owns consumer_installation.py and its tests on a separate unpublished checkpoint. This branch owns the builder/contracts/generated headers only; root will stack the commits and reconcile continuity. Reference preserved ADR0001/ADR0002 canonical/generated and neighboring-owner boundaries; no new lifecycle or strategic decision is selected.

## Privacy and redaction

Public repository facts, relative source/destination identities and content hashes only. Exclude private local topology, credentials, personal context and conversation transcripts. Repository content remains context-only with no authority.

## Handoff update protocol

After domain reconciliation refresh this checkpoint, verify pinned schema/twelve headings/byte-line budgets and staged whitespace before PR handoff. Roadmap disposition is not-affected for AET-Q01/AET-Q05, with no source roadmap edit or organizational signal. Preserve accepted historical labels and proposed ADR0009.

## Compaction and supersession

Git and dated issue38 records retain earlier checkpoints. This replaces current operational prose without rewriting historical CLI failures, canonical skills or release evidence.
