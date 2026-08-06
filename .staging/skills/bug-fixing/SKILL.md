---
name: bug-fixing
description: Diagnose and fix a concrete software defect with reproducible evidence, root-cause analysis, a minimal implementation change, regression tests, and focused validation. Use for bug reports, crashes, incorrect behavior, failing tests, error logs, regressions, or broken integrations where code changes are requested.
---

# Bug Fixing

## Establish the failure

1. Capture observed behavior, expected behavior, environment, scope, reproduction steps, logs, and recent relevant changes.
1. Inspect repository instructions and the code path before editing.
1. Reproduce the failure when feasible. If reproduction is unavailable, identify the strongest proxy signal and label the limitation.

## Find the root cause

- Trace from the visible failure through callers, state transitions, interfaces, and invariants.
- Form multiple hypotheses when evidence is ambiguous.
- Use focused diagnostics to eliminate hypotheses.
- Distinguish the root cause from triggering conditions and downstream symptoms.
- Inspect neighboring paths for the same broken invariant without broadening the fix unnecessarily.

## Implement the correction

- Choose the smallest change that restores the intended invariant.
- Preserve public behavior outside the defect.
- Add explicit validation or error handling when malformed input caused the failure.
- Avoid unrelated refactoring, dependency changes, formatter churn, and generated-file edits.
- Never suppress an error, disable a check, or weaken a type or lint rule merely to make validation pass.

## Protect against regression

Add or update the lowest-cost test that would fail under the original behavior and pass after the fix. Prefer observable behavior over private implementation details. Include boundary cases when they share the same root cause.

## Validate and report

Run the focused regression test, affected module checks, and the repository's required broader validation. Review the diff and repository status before completion. Report reproduction evidence, root cause, the exact fix, tests, commands and results, residual risk, and any validation that could not run.
