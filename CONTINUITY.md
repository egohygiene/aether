---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-03T05:48:35Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Confine current skill/spec distribution inputs and outputs to declared trees before payload
    reads or writes.
  includes: &id001
  - Parse semantic YAML identifiers from one normalized spec snapshot and reject unsafe IDs before output
    paths are constructed.
  - Reject implicit canonical/companion source symlinks; preserve explicitly declared contained resources
    and deterministic valid bytes.
  - 'Anchor output reads/writes to the selected resolved base, reject redirects within owned subtrees
    and preserve #108 failure/inventory behavior.'
  excludes:
  - Filesystem sandboxing against concurrent adversarial writers, host installation, source cleanup and
    publication.
  - Regression suites, hosted CI, issue closure and independent evaluator/catalog implementation.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - library/organization/skills/build-distributions.py
  - library/organization/specs/build-distributions.py
  - aether_validator.py
  - tests/test_build_distributions.py
  - tests/test_build_spec_distributions.py
  - tests/test_aether_validator.py
  - docs/distribution-paths.md
  - README.md
  - https://github.com/egohygiene/aether/issues/110
work:
  objective: Confine current skill/spec distribution inputs and outputs to declared trees before payload
    reads or writes.
  success_conditions: *id001
  active_issue:
    provider: github
    id: egohygiene/aether#110
    url: https://github.com/egohygiene/aether/issues/110
  next:
    kind: action
    id: review-draft-and-qualify
    description: Review source/output containment and qualify the harmless sentinel, identifier, resource
      and symlink cases in the deferred checks pass; reconcile with evaluator117 and catalog115 before
      later integration.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/110
    depends_on: []
state:
  base:
    revision: 87e0277d1c99187464516899e57e2285b8f7a015
    ref: refs/heads/main
    verified_at: '2026-11-03T05:48:35Z'
  candidate:
    branch: codex/110-confined-distribution-paths
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-03T05:48:35Z'
    default_branch_revision: 87e0277d1c99187464516899e57e2285b8f7a015
    issue_state: open
    pull_request_state: not-applicable
    notes: Main87e0277 contains merged distribution PR116. Issue110 is open; evaluator draft117, catalog115
      and audit106 are separately open. The original dirty catalog source is untouched. This candidate
      is not merged, installed or published.
  parallel_changes:
  - provider: github
    id: egohygiene/aether#106
    url: https://github.com/egohygiene/aether/pull/106
  - provider: github
    id: egohygiene/aether#115
    url: https://github.com/egohygiene/aether/pull/115
  - provider: github
    id: egohygiene/aether#117
    url: https://github.com/egohygiene/aether/pull/117
review:
  status: partial
  reviewed_at: '2026-11-03T05:48:35Z'
  reviewed_by: Codex
  evidence:
  - command: AST parse six changed Python sources and git diff --check
    outcome: passed
    observed_at: '2026-11-03T05:48:35Z'
    notes: Both builders, validator and three regression files parse. Seven new regression methods are
      authored but unexecuted.
  - command: ./aether distribution build --output-directory dist; ./aether distribution build --output-directory
      dist --check; ./aether catalog generate
    outcome: passed
    observed_at: '2026-11-03T05:48:35Z'
    notes: All commands exit0 against current valid canonical source. Tracked dist/catalog bytes remain
      unchanged, including manifest path ordering. No regression or sentinel case executes.
  - command: Pinned continuity schema/formats, twelve headings, size and privacy inspection
    outcome: passed
    observed_at: '2026-11-03T05:48:35Z'
    notes: One bounded source handoff meets metadata/size/privacy checks; official EgoLint conformance
      is unexecuted.
  - command: Identifier/symlink/sentinel/resource/portable regressions and hosted CI
    outcome: not-run
    observed_at: '2026-11-03T05:48:35Z'
    notes: All newly authored negative-path cases remain unexecuted. Positive generation does not establish
      their behavior.
  environment_limitations:
  - Seven new negative/positive regression methods and existing suites remain unexecuted; issue110 stays
    open.
  - Guards assume a quiescent local filesystem; they do not claim race-free sandboxing against concurrent
    directory substitution.
  - Explicit resources retain their governed contained-source mechanism; implicit companion/source redirects
    are rejected.
  - Official EgoLint conformance and broader owner/host/release qualification remain deferred.
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

Record the bounded issue110 source/output guard draft below user/runtime, scoped instructions, live evidence and canonical source. It grants no installation/publication authority.

## Resume protocol

Read AGENTS, both builders, the path-boundary guide and issue110. Main already contains merged116; preserve evaluator117 and the original catalog115 work.

## Current objective and success conditions

Reject unsafe semantic identifiers and implicit source/output redirects before payload I/O while preserving valid deterministic packages, explicit resources and #108 inventory/failure semantics.

## State snapshot

Base main87e0277d1c99187464516899e57e2285b8f7a015 includes merged116. Issue110 and peer drafts106/115/117 are open. Candidate codex/110-confined-distribution-paths has null self-revision/PR before creation.

## Completed and material changes

Spec frontmatter is parsed once with existing PyYAML from the same normalized bytes copied. Stable-ID admission is added to the validator. Builders reject implicit canonical/companion symlinks, verify contained sources, capture one skill source snapshot and reject redirected output reads/writes. Valid manifest order is preserved. Seven new regressions use synthetic IDs and harmless temporary sentinels.

## Validation and review evidence

Six Python sources parse and whitespace checks pass. Actual distribution build, --check and catalog regeneration exit0 with unchanged tracked derived bytes. Continuity metadata/schema/formats/heading/privacy/budget checks pass. No regression or sentinel case executes.

## Blockers, risks, unknowns, and deferred work

Negative-path, custom-output and resource regressions remain unexecuted. Quiescent guards do not establish sandbox/race guarantees. Official EgoLint and wider CI/host/release checks remain deferred. No install, release or publication occurs.

## Next dependency-ready work

Review and qualify issue110 during the deferred checks pass, preserving evaluator117 and catalog115. Keep the issue open until required negative/portable acceptance has actual proof.

## Parallel changes and reconciliation

Audit106, catalog115 and evaluator117 remain separate. Validator/test and checkpoint edits may overlap; reconcile their source scopes and one current handoff during later integration without replacing the dirty original worktree.

## Privacy and redaction

Only scoped public source facts and synthetic harmless sentinel tests are retained. No private host files, secrets, personal context, workbook contents or machine-local paths are included.

## Handoff update protocol

Refresh after review and actual qualification. ADR not required: enforce the existing canonical-to-derived containment contract and reuse the existing PyYAML dependency; no new owner, format, installation or publication authority.

## Compaction and supersession

Keep twelve required sections and existing budgets. Canonical builders, path guide, Git and issue110 retain detailed contract/history.
