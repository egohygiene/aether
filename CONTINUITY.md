---
schema_version: aether.repository-continuity/v1
repository:
  id: egohygiene/aether
  visibility: public
  default_branch: main
  continuity_path: CONTINUITY.md
document:
  status: active
  updated_at: '2026-11-03T05:37:45Z'
  max_bytes: 16384
  max_lines: 240
  stale_reason: null
  superseded_by: null
scope:
  purpose: Make deterministic evaluation share structural preflight and fail honestly on invalid suites,
    selections and unexecuted assertion requirements.
  includes: &id001
  - Reject invalid schema/empty cases/duplicate IDs and mismatched identities through the same admission
    path in validator and runner.
  - Record missing assertion evidence, run-level errors, rejected suites and actual case counts separately;
    keep filesystem assertions independent of goldens.
  - Preserve explicit skipped/unsupported scope and execute no model or paid provider.
  excludes:
  - Model/routing/subjective evaluation, source catalog work in draft115, release/publication and issue
    closure.
  - Evaluation execution, regression suites and hosted CI.
  precedence:
  - user-and-runtime-instructions
  - scoped-repository-instructions
  - live-repository-and-work-tracker-state
  - canonical-repository-sources
  - continuity-checkpoint
  canonical_sources:
  - AGENTS.md
  - aether_validator.py
  - tests/test_aether_validator.py
  - docs/deterministic-evaluations.md
  - catalog/schemas/aether.skill-evaluations.v2.schema.json
  - README.md
  - DECISIONS.md
  - https://github.com/egohygiene/aether/issues/109
work:
  objective: Make deterministic evaluation share structural preflight and fail honestly on invalid suites,
    selections and unexecuted assertion requirements.
  success_conditions: *id001
  active_issue:
    provider: github
    id: egohygiene/aether#109
    url: https://github.com/egohygiene/aether/issues/109
  next:
    kind: action
    id: review-draft-and-qualify
    description: Review the fail-closed evaluator draft; qualify its selection/schema/evidence/counting
      regressions in the deferred pass, and preserve parallel catalog115/distribution110 source and checkpoint
      work.
    readiness: ready
    references:
    - https://github.com/egohygiene/aether/issues/109
    depends_on: []
state:
  base:
    revision: 87e0277d1c99187464516899e57e2285b8f7a015
    ref: refs/heads/main
    verified_at: '2026-11-03T05:37:45Z'
  candidate:
    branch: codex/109-fail-closed-evaluation
    revision: null
    pull_request: null
    handoff_state: ready-for-review
  live:
    status: verified
    observed_at: '2026-11-03T05:37:45Z'
    default_branch_revision: 87e0277d1c99187464516899e57e2285b8f7a015
    issue_state: open
    pull_request_state: not-applicable
    notes: Main87e0277 contains merged distribution PR116. Issue109 is open; catalog draft115 and audit106
      remain open and untouched. This independent candidate has no merge/publication or passing evaluation
      claim.
  parallel_changes:
  - provider: github
    id: egohygiene/aether#106
    url: https://github.com/egohygiene/aether/pull/106
  - provider: github
    id: egohygiene/aether#115
    url: https://github.com/egohygiene/aether/pull/115
  - provider: github
    id: egohygiene/aether#110
    url: https://github.com/egohygiene/aether/issues/110
review:
  status: partial
  reviewed_at: '2026-11-03T05:37:45Z'
  reviewed_by: Codex
  evidence:
  - command: AST parse aether_validator.py and tests/test_aether_validator.py; git diff --check
    outcome: passed
    observed_at: '2026-11-03T05:37:45Z'
    notes: Both sources parse; seven new regression methods are authored but unexecuted. The existing
      missing-fixture expectation now distinguishes a rejected suite from executed case failures.
  - command: ./aether distribution build --output-directory dist; ./aether catalog generate
    outcome: passed
    observed_at: '2026-11-03T05:37:45Z'
    notes: Both commands exit0 and leave tracked derived/catalog bytes unchanged. These commands do not
      execute evaluations or tests.
  - command: Pinned continuity metadata/schema/formats, twelve headings, privacy and size inspection
    outcome: passed
    observed_at: '2026-11-03T05:37:45Z'
    notes: One bounded source handoff within the existing budgets; official EgoLint conformance is unexecuted.
  - command: Evaluation commands, regression suites, model/provider checks and hosted CI
    outcome: not-run
    observed_at: '2026-11-03T05:37:45Z'
    notes: No evaluator or regression case was executed. Static and generation evidence does not establish
      correct runtime evaluation behavior.
  environment_limitations:
  - All new and existing evaluation regressions remain unexecuted; issue109 stays open.
  - Deterministic case success qualifies structure and declared assertions only; prose, routing and model
    behavior remain unexecuted.
  - Catalog draft115 shares the validator/test files; preserve its existing changes during eventual integration.
  - Official released EgoLint conformance, hosted CI and broader qualification remain deferred.
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

Keep this issue109 source handoff below user/runtime instructions, scoped policy, live evidence and canonical sources. It grants no merge/publication authority.

## Resume protocol

Read AGENTS, the evaluator evidence guide, validator/runner and issue109. Verify main and peers; PR116 is already merged, and original catalog draft115 remains separate.

## Current objective and success conditions

Share structural admission, reject empty/invalid requested work, execute filesystem assertions independently of goldens and report evidence/counts honestly without running a model.

## State snapshot

Base main87e0277d1c99187464516899e57e2285b8f7a015 includes merged116. Issue109 is open. Candidate codex/109-fail-closed-evaluation has null self-revision/PR before creation.

## Completed and material changes

aether_validator.py now shares suite preflight, rejects duplicate JSON keys/invalid schema and identity, reports unmatched selection/unsupported mode/no executable cases, requires golden evidence for text assertions and counts suite errors separately. The guide defines deterministic scope and seven regression methods cover the new boundaries.

## Validation and review evidence

Both Python sources parse and whitespace checks pass. Actual distribution build and catalog regeneration exit0 with unchanged derived bytes. Continuity metadata/schema/formats, headings and size/privacy checks pass. No evaluation or test runs.

## Blockers, risks, unknowns, and deferred work

The new cases and existing suites remain unexecuted, as do evaluator commands and official EgoLint/hosted CI. A source implementation and regenerated artifacts do not qualify assertion execution or a real task. Issue109 remains open.

## Next dependency-ready work

Review and qualify the source draft during the deferred checks phase. Preserve independent distribution110 and catalog115 changes while selecting the next bounded source work.

## Parallel changes and reconciliation

Audit106 and catalog115 remain untouched. Issue110 is separate. Validator/test and root checkpoint overlaps must be reconciled semantically; do not replace the dirty original catalog worktree.

## Privacy and redaction

Only scoped public source facts and synthetic fixture inputs are retained. No private workbook data, credentials, personal context or machine-local paths enter this repository.

## Handoff update protocol

Refresh after actual qualification/review. ADR not required: routine correctness repair of the existing deterministic evaluator and evidence counts, with no model/provider/release authority. No new lifecycle disposition, merge or issue closure is claimed.

## Compaction and supersession

Keep twelve required sections and existing budgets. Canonical schema, evaluator guide, Git and issue109 retain detailed contract/history.
