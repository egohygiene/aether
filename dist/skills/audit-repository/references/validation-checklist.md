# Audit Repository Validation Checklist

## Governance

- [ ] `auditor` is identified.
- [ ] The governing version is known.
- [ ] Scope and constraints are explicit.
- [ ] The approved base specification and draft machine extension retain their
  independent lifecycle states.
- [ ] Requested/composed profiles resolve through one exact registry; every
  finding preserves its original leaf profile/version.

## Evidence

- [ ] Required sources were inspected.
- [ ] Facts, assumptions, inference, and proposals are distinguishable.
- [ ] Missing evidence is acknowledged.
- [ ] Contradictions remain visible.
- [ ] Opportunities, experiments, policy findings and observed defects remain
  distinct; experimental recommendations are not production failures.
- [ ] Prior-audit identities and reported deltas have actual evidence; absence
  or unknown state has not been converted into resolution.

## Execution

- [ ] Work remained within authorized scope.
- [ ] Required artifacts were produced.
- [ ] No prohibited side effects occurred.
- [ ] Downstream work was not silently authorized.
- [ ] A read/search-only agent has not acquired edit/execute permission from a
  profile. An authorized output writer owns new immutable report/sidecar files.
- [ ] Candidate issues remain suggestions and no historical report is altered.

## Validation

- [ ] Actual checks and their limits are recorded separately from unrun
  acceptance criteria; no missing validation is labelled passing.
- [ ] Partial or blocked state is recorded when applicable.
- [ ] Unsupported, not-applicable and unknown profile scope remains explicit.
- [ ] Markdown and sidecar project the same authored model and bind actual
  Markdown bytes; raw file, semantic JSON and upload hashes are distinguished.
- [ ] Canonical ownership is clear.
- [ ] Another reviewer can reproduce the conclusion.

Deterministic scenario fixtures, package dependency closure and actual
host/discovery qualification remain separate maturity evidence. Static schema
inspection or catalog/distribution regeneration does not promote this draft.
