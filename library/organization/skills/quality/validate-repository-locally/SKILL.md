---
name: validate-repository-locally
description: Plans and executes best-effort local repository validation, adapts to observed runtime capabilities, and writes truthful evidence when remote CI is unavailable or deferred. Use when preparing a change or pull request with as much local confidence as the current environment permits; do not use for a single narrow test-design request.
license: MIT
metadata:
  aether-version: "1.1.0"
  aether-status: "draft"
  aether-spec-id: "local-validation-evidence"
  aether-scope: "organization"
  aether-domain: "quality"
  aether-owners: "egohygiene"
  aether-created: "2026-09-10"
  aether-updated: "2026-09-10"
  aether-distribution-resources:
    - source: "catalog/schemas/aether.local-validation-evidence.v1.schema.json"
      destination: "references/aether.local-validation-evidence.v1.schema.json"
---

# Validate Repository Locally

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

For repository-scoped work, compose `maintain-repository-continuity` in
**Resume** mode before selecting work. After an authorized repository change
passes domain validation, compose **Refresh** and **Verify** immediately before
presenting the pull request, and include the reconciled root `CONTINUITY.md` in
the same change. A policy-permitted no-change or exemption result must be
documented instead of fabricating an edit.

- **Contribute:** Represented revision, capability observations, exact sanitized commands and outcomes, remote CI state, limitations, and residual risk
- **Never claim:** That an unavailable, skipped, blocked, deferred, stale, or unobserved check passed

## Purpose

Maximize trustworthy local confidence without making unavailable infrastructure
a precondition for useful implementation progress. Govern the result with
`local-validation-evidence`.

## Required inputs

Resolve as much of the following as evidence permits:

- requested change and validation scope;
- repository instructions, continuity state, and canonical commands;
- current base revision, worktree state, and changed paths;
- user policy for installation, remote CI, direct action execution, and reports;
- applicable workflows, hooks, generated artifacts, and release surfaces;
- privacy and publication boundary for committed evidence.

Use `unknown`, `not-run`, `blocked`, or `deferred` instead of guessing.

## Workflow

1. Read repository instructions and continuity state. Confirm that validation,
   any dependency setup, and any committed report are within scope.
2. Discover canonical entrypoints in precedence order: repository CLI, task or
   package scripts, documented commands, hooks, then underlying workflow commands.
3. Select `focused`, `best-effort`, or `exhaustive-local`; default to
   `best-effort` when remote CI is intentionally deferred.
4. Probe only material capabilities. Treat executables, backends, credentials,
   network, permissions, and versions as separate observations. Never record
   secret environment values.
5. Build a check matrix with independent requirement, applicability,
   availability, selection, and outcome fields. Use
   [execution-adapters.md](references/execution-adapters.md) for adapter gates.
6. If authorized, perform repository-locked setup in an isolated local
   environment and record it as its own check.
7. Run the smallest relevant deterministic check first, then broader safe and
   applicable checks. Continue independent checks after a failure when useful.
8. Prefer native commands. Use workflow linting when available. Use `act` only
   after its engine, resource, network, trust, and policy gates pass.
9. Keep remote CI independent. When budget or policy defers it, do not dispatch
   a run; record `deferred` and name the unverified workflow surfaces.
10. Derive local readiness from observed evidence. Required failure means
    `not-ready`; missing required evidence or material parity means
    `ready-with-limitations` at best.
11. Validate JSON against
    `references/aether.local-validation-evidence.v1.schema.json`, render the
    Markdown companion from
    [LOCAL_VALIDATION_REPORT.template.md](templates/LOCAL_VALIDATION_REPORT.template.md),
    and inspect both for sensitive data.
12. Commit evidence only when authorized and consistent with repository policy.
    Report the represented revision, exact checks, limitations, and next
    externally gated step.

## Execution rules

- Do not install or start a privileged container daemon for optional emulation.
- Do not use direct self-hosted `act` execution without explicit authorization
  and a reviewed trusted workflow and action graph.
- Do not edit workflows, weaken assertions, update snapshots blindly, or disable
  checks merely to obtain a pass.
- Do not treat setup, emulator, network, authentication, or billing failures as
  application-test failures when the distinction is known.
- Do not trigger remote Actions when policy says `deferred` or `disallowed`.
- Do not call local evidence merge approval, hosted-runner parity, release
  readiness, or production validation.
- Do not expose tokens, cookies, credential helpers, proxy values, private
  absolute paths, or unnecessary host identity in a committed report.

## Completion criteria

- [ ] The represented candidate and chosen profile are explicit.
- [ ] Canonical repository commands were preferred over invented wrappers.
- [ ] Material capabilities and limitations were observed at execution time.
- [ ] Every candidate check has independent state dimensions.
- [ ] Focused and broader available checks ran in risk-appropriate order.
- [ ] `act` and remote CI boundaries were applied without inventing parity.
- [ ] JSON validates and the Markdown companion agrees with it.
- [ ] Required failures, unavailable evidence, and residual risks remain visible.
- [ ] Evidence was committed only when authorized and privacy-safe.
