---
schema: aether.specification/v1
id: worker-strategy
title: Bounded Worker Strategy
kind: specification
version: 0.1.0
status: draft
owners:
  - egohygiene
created: 2026-10-02
updated: 2026-10-02
domain: methodology
tags:
  - workers
  - checkpoints
  - roadmap
  - handoff
  - local-validation
applies_to:
  - repository-work-sessions
  - issue-mini-sprints
  - cross-repository-roadmap-resumption
depends_on:
  - specfile
  - repository-continuity
  - local-validation-evidence
related:
  - auditor
  - test-engineering
  - repository-cleanup
supersedes: []
---

# Bounded Worker Strategy

Run one small, resumable engineering checkpoint per worker session and preserve unfinished quality work explicitly.

## 1. Purpose, context, and boundaries

This opt-in strategy organizes existing repository issues into mini sprints.
Its goal is to reach a usable product through short implementation jobs, durable
handoffs, and separate completion passes for tests, documentation, validation,
and review. It applies to humans, Copilot, and other coding assistants.

The October 2, 2026 authoring request established the following requirements:
small implementation checkpoints; explicit deferred quality work; repository
handoffs that survive a new chat; local verification when remote CI is deferred;
and an initial report grounded in live repository and GitHub evidence. The Flow
suite is the first intended trial, with a complete comic artifact tree as its
consumer outcome. No live Flow roadmap or performance result is asserted here.

This is a workflow contract, not an autonomous scheduler, model-selection
policy, mandatory organization rollout, or replacement for consumer commands.
It does not promise a runtime or credit reduction. Five to ten minutes is an
initial scope target; measured results can inform later adjustments.

Active user and runtime instructions take precedence. Applicable consumer
instructions govern local behavior; this strategy supplies defaults. A request
to defer checks changes their scheduling, never their recorded outcome. This
specification alone grants no authority to mutate trackers, merge, publish,
dispatch CI, spend money, or process real media.

## 2. Operating model and sources of truth

| Component | Responsibility |
| --- | --- |
| This Aether specification | Reusable worker behavior, versioned and referenced |
| Consumer roadmap and GitHub issues | Scope, dependencies, acceptance, and outstanding work |
| Branch and draft PR | Reviewable implementation and evidence at known revisions |
| Sprint handoff | Current state of one issue, including its deferred work |
| Root `CONTINUITY.md` | Current repository resume entrypoint and links to active handoffs |
| Local validation evidence | Commands, actual outcomes, limitations, and revision coverage |

A worker is one bounded work session with a single primary role. A checkpoint
is its finishable scope. A mini sprint is an existing parent issue with a finite
set of implementation and completion checkpoints. Roles are sequential work
modes; they do not require separate models, multiple agents, or concurrency.

The data flow is: inspect current evidence, reconcile the next checkpoint,
perform its authorized work, persist the candidate and handoff, then report.
Each later session rechecks mutable state before resuming.

## 3. Bootstrap and roadmap reconciliation

- **WRK-001 — Invocation.** The worker MUST record the requested repositories,
  outcome, strategy version/ref, role, scope, check budget, and stopping point.
  Infer routine defaults from the request. Preserve existing authorization;
  ask only about material ambiguity that cannot be resolved from evidence.
- **WRK-002 — Bounded discovery.** Read applicable `AGENTS.md`, relevant roadmap
  and architecture contracts, and `CONTINUITY.md` when present. Verify the
  default-branch revision, open PRs, relevant issues, and dependency state.
  For a suite, inspect issue/PR summaries across the named repositories, then
  read detailed code only for the next candidate. Disclose inaccessible or
  incomplete inventories; a search result cap is not a complete inventory.
- **WRK-003 — Startup report.** Before implementation, report what is observed,
  implemented but unvalidated, blocked, or unknown; the recommended sequence;
  the next bounded checkpoint; and proposed issue changes. Include source links
  and the observation time. A bootstrap-only request ends after this report.
  An execution request proceeds within its existing authorization.
- **WRK-004 — Reuse.** Reuse current issues, sub-issues, PRs, and handoffs. Create
  or edit tracker records only when that is part of the authorized work. Keep
  acceptance criteria intact; reconcile stale claims instead of silently
  replacing them. Inspect relevant closed work before proposing a duplicate.

Default startup summary:

```text
Goal and observed refs:
Current state and evidence gaps:
Recommended order and dependencies:
Next checkpoint: repository / issue / role / scope / stop condition
Checks selected now; checks deferred and where tracked:
Proposed tracker changes, or none:
```

Discovery is sufficient when the worker can choose and explain the next
dependency-ready checkpoint. A kickoff is not an automatic fleet audit.

## 4. Mini-sprint structure and worker roles

- **WRK-005 — Scope.** Split a large issue into roughly two to four cohesive
  implementation checkpoints when useful. A small issue may need only one.
  Append applicable completion checkpoints from the table below. Use a parent
  checklist for small scopes and sub-issues for independently assignable jobs;
  avoid creating a separate issue for every checklist line.
- **WRK-006 — Contract.** Every checkpoint MUST state its outcome, included and
  excluded work, relevant interfaces/files, dependencies, acceptance criteria,
  selected checks, deferred checks, and handoff location before implementation.
  Unknown paths or commands remain explicit discovery tasks.
- **WRK-007 — Single role.** Perform only the assigned role and necessary
  supporting work. Capture discoveries outside scope for a later checkpoint.
  Do not turn one implementation job into a test, docs, CI, and refactor sprint.

| Role | Deliverable and stopping point |
| --- | --- |
| Implementation | Scoped behavior and required interface notes; stop at the checkpoint's acceptance boundary |
| Test authoring | Acceptance-linked test cases and fixtures; mark execution separately if deferred |
| Test execution | Run the selected tests and report evidence; bound diagnosis and move substantial fixes into checkpoints |
| Documentation | User-facing instructions and examples matching current behavior; identify unverified examples |
| Local validation / CI preparation | Run applicable repository-native CI commands locally; record hosted-runner gaps |
| Audit | Review the changed feature and its integration boundary; classify concrete findings and deduplicate follow-ups |
| Refactoring / repair | Address named findings within a bounded change; record the focused checks needed afterward |

Test authoring and execution MAY be combined when both fit one small session.
Simple documentation changes need review, not invented behavioral tests.
Checkpoints that do not apply are marked not applicable with a reason.

- **WRK-008 — Stop and save.** Use a five-to-ten-minute target for a small job,
  with room reserved for its handoff. If the scope grows or a command stalls,
  record partial work and the next action rather than starting an open-ended
  retry loop. Commit and push authorized, reviewable work to a branch/draft PR.
  If pushing is unavailable, report the exact saved state and delivery blocker.
  Do not discard unrelated work or start background processes without a handoff.

## 5. Implementation-first profile and completion passes

When selected by the caller, the implementation-first profile uses the following
rules. It is an explicit scheduling choice relative to the broader
`local-validation-evidence` default; its evidence semantics remain unchanged.

- **WRK-009 — Deferred checks.** Broad test runs, exhaustive test authoring,
  documentation polish, CI mirroring, and broad refactors belong to named later
  checkpoints. Record each deferred obligation before ending the current one.
  Run only cheap, directly relevant checks within the selected budget, unless
  the user has explicitly deferred those too. Never report an unrun check as
  passed or a partial implementation as validated.
- **WRK-010 — Early boundaries.** Do not expand into unrelated changes to get a
  green result. For changes involving overwrite/delete behavior, migrations,
  security boundaries, or shared interfaces, name the necessary focused check
  and perform it before relying on that behavior or using real data. If checks
  are deferred, preserve the implementation as unvalidated draft work and
  identify dependent work that cannot safely rely on it yet.
- **WRK-011 — Loop-back trigger.** Record a finite batch boundary in the roadmap.
  The initial recommendation is one parent issue, or at most three tightly
  connected parent issues, followed by their applicable completion passes.
  Run a focused integration check before stacking work on an uncertain shared
  interface. A changed batch size requires a recorded reason, not a new policy.
- **WRK-012 — Local CI evidence.** Use native repository commands and locked
  setup where available. Reuse the existing `local-validation-evidence` outcome
  and readiness model. Remote CI remains separate: do not dispatch or rerun it
  when deferred, and do not modify billing, required checks, or protections.
  State that pushes/PRs may trigger existing workflows; draft status does not
  suppress them. Any workflow-trigger change is a separate scoped change.

Workflow emulation is optional. Local runs do not establish hosted-runner parity,
remote success, merge readiness, or release readiness. Record platform, service,
credential, network, and environment gaps relevant to the selected commands.

## 6. Durable handoff and reporting contract

- **WRK-013 — Repository handoff.** Every checkpoint MUST leave a compact
  repository-owned record, including incomplete or blocked checkpoints. Reuse
  an established work-record location. Where none exists, use
  `docs/work/<parent-issue-number>/HANDOFF.md` for the sprint and link it from
  root `CONTINUITY.md` when present. The sprint record preserves deferred work
  after another issue becomes active; the root file remains one current snapshot
  under `repository-continuity`, not an expanding diary or duplicate tracker.

Minimum sprint record; headings may follow consumer conventions:

```text
Parent issue / checkpoint / role:
Strategy version and immutable source ref:
Observed at / verified base SHA / candidate branch / PR:
Outcome and acceptance criteria:
Implemented / partial / remaining work (with paths):
Interface decisions and assumptions:
Checks actually run: command, outcome, exit code if known, represented revision:
Deferred checks: behavior to prove, test/fixture needed, exact command if known,
  expected result, reason deferred, linked checkpoint and loop-back trigger:
Documentation / local CI / audit obligations:
Blockers, dependent work, and known parallel changes:
Next action: files to read, concrete edit or command, expected result, stop point:
```

Record the verified base and candidate separately; a file cannot contain its own
eventual commit SHA. Link external commit/PR evidence after it exists. On resume,
compare the handoff to live refs and reconcile concurrent changes before editing.
If interrupted before updating the handoff, inspect branch/PR history and the
working tree; do not assume the last planned action completed.

The parent issue SHOULD link the latest sprint handoff. Preserve outstanding
test obligations in that record and the existing parent checklist, even when an
implementation sub-issue closes. Do not store full logs, transcripts, credentials,
or unrelated private context in a public handoff.

- **WRK-014 — User report.** End with the checkpoint outcome, branch/PR link,
  checks actually run, explicit deferred work, handoff link, and next job.
  Use concise prose. A saved file or unpushed commit is not a pushed PR.
- **WRK-015 — Honest closure.** Track implementation completion separately from
  verification. Close an implementation sub-issue only when its scoped criteria
  are met. Keep the parent open until its agreed acceptance criteria and required
  completion checkpoints are satisfied or explicitly revised by the owner.
  Do not use an automatic closing keyword for the parent in an implementation-only
  PR. Merge authority comes from the user/repository, not this strategy.

## 7. Audit, refactoring, and a finite finish line

- **WRK-016 — Findings.** Audit the batch against acceptance criteria, changed
  interfaces, generated artifacts, and maintainability. Separate required fixes
  from optional improvements. Link evidence, impact, expected result, and the
  smallest suggested checkpoint. Search existing issues before creating any;
  publish follow-ups only within the authorized tracker scope.
- **WRK-017 — Completion.** Repairs that affect behavior reopen the relevant
  validation obligation. Optional improvements do not extend the current sprint
  automatically. A low issue count is a progress indicator, not evidence of
  correctness; preserve a reachable consumer outcome and a finite acceptance bar.

## 8. Adoption and validation plan

Start with one existing parent issue. Record its checkpoint boundaries and trial
the selected role in a fresh session. Resume from the committed handoff, execute
the deferred completion pass, and review whether the next session could recover
without chat history. Adjust scope targets using observed duration, interruptions,
rework, and provider usage only when available; do not invent cost measurements.

The following are review scenarios, not claims that runtime evaluations exist:

| Scenario / requirement | Expected evidence |
| --- | --- |
| Fresh-chat bootstrap (WRK-001–004) | Live source refs, bounded roadmap report, reused issues, one next checkpoint |
| Implementation with tests deferred (WRK-005–010) | Reviewable partial or complete code, named checks and expected results, no false pass |
| Interrupted or concurrent work (WRK-008, 013–014) | Reconciled branch state and a concrete resume action |
| Local-only completion (WRK-011–012) | Actual command outcomes, environment gaps, separate remote-CI state |
| Implementation PR merges (WRK-015) | Parent validation obligations remain open and reachable |
| Audit finds optional cleanup (WRK-016–017) | Deduplicated optional follow-up without silently extending acceptance |

Acceptance for the first consumer trial: a new session can locate the current
work, execute one checkpoint, recover all deferred obligations, and report its
evidence without replaying prior chat. Review of this document alone does not
prove the strategy's effectiveness or consumer adoption.

Open questions for the trial: which checkpoint sizes reduce rework; whether
checklists or sub-issues are clearer for a given repository; and which checks
fit the immediate budget. These do not block drafting or a bounded trial.

## 9. Related contracts

Dependencies are resolved at the same Aether ref as this specification:
`specfile`, `repository-continuity`, and `local-validation-evidence`. Reuse their
contracts; do not fork continuity or evidence schemas. Aether owns this portable
guidance. Consumers own adoption, issue state, commands, and product acceptance;
Hygiene owns organization applicability and Relay owns reusable CI execution.

This narrow strategy relates to the broader agent/cost-policy work in
[Aether #41](https://github.com/egohygiene/aether/issues/41) and instruction-library
work in [Aether #40](https://github.com/egohygiene/aether/issues/40). It completes
neither issue and does not require those larger systems for the first trial.
