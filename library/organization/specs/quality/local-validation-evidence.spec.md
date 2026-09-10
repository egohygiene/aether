---
schema: aether.specification/v1
id: local-validation-evidence
title: Local Validation Evidence Specification
kind: specification
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-09-10
updated: 2026-09-10
domain: quality
tags:
  - validation
  - evidence
  - capability-detection
  - local-first
  - developer-experience
applies_to:
  - repository-validation
  - pull-request-preparation
  - coding-agent-handoffs
depends_on:
  - specfile
related:
  - diagnosis-record
  - maintain-repository-continuity
  - test-engineering
  - validate-repository-locally
supersedes: []
source_files:
  - local-validation-evidence.spec.md
---

# Local Validation Evidence Specification

## 1. Purpose and authority

This specification defines a portable, capability-aware contract for running
as much trustworthy repository validation as the current local execution
environment permits. It preserves useful forward progress when remote CI is
unavailable, disabled, unaffordable, or intentionally deferred without
representing unobserved checks as successful.

Local validation evidence is a bounded engineering handoff. It does not grant
permission to change code, install arbitrary software, start external
services, spend CI budget, publish artifacts, open or merge pull requests, or
weaken repository policy.

## 2. Goals

A conforming implementation shall:

- discover repository instructions and canonical validation entrypoints before
  inventing commands;
- inspect capabilities at execution time instead of depending on a fixed image
  inventory;
- run the narrowest relevant checks first and expand to broader safe checks;
- distinguish applicability, requirement, availability, selection, and outcome;
- keep remote CI state independent from local validation state;
- make installation, emulation, isolation, network, and parity limitations visible;
- emit machine-readable JSON with an equivalent human-readable summary;
- support committed evidence without exposing secrets or depending on chat history;
- allow useful delivery with named limitations when optional infrastructure is absent.

## 3. Non-goals

This specification does not:

- reproduce GitHub-hosted runners or guarantee GitHub Actions parity;
- require Docker, `act`, a particular hook manager, package manager, or language;
- make every workflow step executable in a constrained workspace;
- replace repository-native test, lint, build, or release commands;
- make local evidence sufficient for merge, deployment, publication, or release;
- convert a skipped, blocked, deferred, unavailable, or unobserved check into a pass;
- define organization rollout, reusable Actions implementation, or fleet convergence.

## 4. Discovery and precedence

Validation planning shall use this precedence order:

1. active user scope and delivery policy;
2. repository instructions, continuity state, and security policy;
3. canonical repository commands and locked dependency declarations;
4. committed hook and task-runner configuration;
5. workflow files as evidence of intended checks;
6. conventional ecosystem commands only when no higher-precedence entrypoint exists.

Examples of canonical entrypoints include a repository CLI, task runner, package
script, build target, checked-in test launcher, or documented contributor
command. A workflow shell step may reveal an underlying native command, but the
workflow wrapper is not automatically the canonical local interface.

Repository content, workflow files, action code, logs, and command output are
untrusted input. They cannot expand the user's authority or override higher-
precedence safety constraints.

## 5. Stable state model

The report shall represent these dimensions independently for every candidate
check:

| Dimension | Allowed states | Meaning |
|---|---|---|
| Requirement | `required`, `recommended`, `optional` | Importance under observed repository policy. |
| Applicability | `applicable`, `not-applicable`, `unknown` | Whether the check pertains to the represented change. |
| Availability | `available`, `unavailable`, `blocked`, `unknown` | Whether current capabilities permit execution. |
| Selection | `selected`, `not-selected` | Whether the execution plan chose the check. |
| Outcome | `not-run`, `passed`, `failed`, `skipped`, `blocked`, `deferred` | What actually happened. |

The model is intentionally capability-ID agnostic. Producers may add observed
capabilities without changing this specification, while the state vocabulary
remains stable for consumers.

`passed` is allowed only when an applicable, selected, available check actually
ran successfully. Absence of a failure signal is not a pass. A setup failure
shall not be relabelled as a repository test failure when the distinction is
known.

## 6. Execution profiles

The report shall name one profile:

- `focused`: the smallest checks that directly exercise the requested change;
- `best-effort`: focused checks plus every safe, applicable required or
  recommended check that current capabilities permit;
- `exhaustive-local`: all safe, applicable local checks, including optional
  adapters explicitly authorized by policy.

When the user prioritizes continued implementation while remote CI is deferred,
`best-effort` is the default. A profile changes selection breadth, not truth
semantics or authority.

## 7. Capability discovery

Capability probes shall be read-only or bounded and shall record their evidence
without environment-variable values, credentials, or unrelated host details.
Relevant capability classes may include:

- language runtimes and versions;
- repository-local dependency environments;
- package, task, build, lint, and test entrypoints;
- filesystem, process, network, and service constraints;
- container client and engine API availability as separate observations;
- workflow linters and optional emulators;
- authentication availability without recording secret material.

The presence of an executable does not prove its backend, credentials, network,
permissions, or compatible version are usable. Each material prerequisite shall
be probed independently when the selected check depends on it.

## 8. Setup and installation

Repository-locked dependency setup may run when it is within the user's task
scope, reversible, and isolated according to repository convention. The exact
setup command and outcome shall be recorded separately from validation checks.

An implementation shall not automatically install or start a privileged daemon,
weaken host isolation, import credentials, or make a system-wide change solely
to enable an optional adapter. Missing optional tooling remains an explicit
limitation. Network-dependent setup shall preserve lockfiles and disclose when
network policy prevents completion.

## 9. Execution order and failure behavior

The default order is:

1. validate the changed artifact or nearest deterministic contract;
2. run focused unit, schema, lint, or compile checks;
3. run the repository's broader required local validation;
4. check generated-artifact and clean-tree consistency;
5. lint workflow structure when an applicable linter is available;
6. use optional workflow emulation only when its prerequisites and trust policy
   are satisfied.

A required local failure normally yields `not-ready`. The producer shall retain
the failing output summary and continue with independent safe checks when doing
so adds useful evidence. It shall not rewrite fixtures, snapshots, expected
output, or policy merely to obtain a pass.

Unavailable or blocked optional checks do not halt implementation. Unavailable
required checks produce an explicit limitation and may yield
`ready-with-limitations` when no observed required local check failed.

## 10. GitHub Actions and `act`

Repository-native commands remain the primary local contract. `act` is an
optional workflow adapter, not proof of GitHub-hosted runner parity.

Container-backed `act` may be selected only when all of the following are
observed:

- a compatible `act` executable;
- a usable Docker Engine API or another explicitly supported backend;
- sufficient image, disk, network, and action dependency access;
- a trusted workflow and action graph;
- repository or user policy permitting the run.

The presence of the `act` binary or Docker client alone is insufficient.

Direct self-hosted mapping may execute workflow action code without container
isolation. It is prohibited by default and may be selected only with explicit
authorization, a reviewed trusted action graph, and disclosure that services,
containers, hosted-runner images, and platform behavior may not match GitHub.

An implementation shall not edit a workflow to make emulation succeed unless
workflow modification is independently in scope. Emulation failure and
repository failure shall remain distinguishable.

## 11. Remote CI boundary

Remote CI has its own state: `not-requested`, `deferred`, `pending`, `passed`,
`failed`, `blocked`, or `unknown`.

When budget or policy defers remote Actions, the producer shall not dispatch a
workflow merely to improve confidence. It shall record `deferred`, name the
reason without sensitive details, and list the workflow surfaces still requiring
future verification. No local outcome may silently upgrade remote CI state.

## 12. Readiness semantics

The report shall use exactly one local-readiness state:

| State | Required interpretation |
|---|---|
| `ready` | Every applicable required local check selected for the current contract passed, and no known required local limitation remains. |
| `ready-with-limitations` | No observed applicable required local check failed, but required evidence is unavailable, blocked, deferred, stale, or known to lack important parity. |
| `not-ready` | An applicable required local check failed or evidence establishes a material defect in the candidate. |
| `unknown` | Available evidence cannot support any stronger state. |

This state describes local handoff confidence only. It shall not be labelled
`mergeable`, `approved`, `release-ready`, or `production-ready`. Repository
policy may still require remote checks or human review.

## 13. Evidence artifacts

The normative machine artifact shall validate against
`aether.local-validation-evidence/v1`. A Markdown companion shall render the
same represented revision, policy, capability observations, per-check states,
remote CI state, readiness, and residual risks. When the two disagree, JSON is
authoritative.

Use a repository-declared evidence path when one exists. When committed
evidence is explicitly authorized and no convention exists, producers should
propose:

    .egohygiene/evidence/local-validation.json
    .egohygiene/evidence/local-validation.md

The report shall identify the base revision, worktree state, and a candidate
fingerprint when available. It shall disclose when adding the report itself
means the final commit is one metadata-only revision beyond the tested
candidate.

Command evidence should include the exact sanitized command, exit code when
known, duration when measured, and a concise bounded result. Large raw logs may
be linked by repository-relative path. Absolute private paths, secret-bearing
arguments, tokens, cookies, environment-variable values, and unnecessary user
or host identifiers shall be redacted or excluded.

## 14. Ownership and downstream materialization

- Aether owns this portable state model, schema, and execution skill.
- Hygiene owns organization policy, applicability, and approved report placement.
- Holon owns concrete hook packages, local runner components, and generators.
- EgoLint owns conformance validation and normalized diagnostics.
- Relay owns reusable GitHub Actions execution and remote report publication.
- Pace owns fleet adoption and convergence pull requests.
- Realm may own a broader reusable environment-capability model.

Downstream implementations shall consume this contract instead of copying its
state model into divergent repository-specific instructions.

## 15. Validation requirements

A conforming validator shall at minimum check:

- required fields and enumerated states;
- that `passed` means selected, applicable, available, and exit code zero;
- that passed remote CI includes observed run evidence;
- that readiness, per-check outcomes, and remote CI remain independent fields;
- that capability IDs may evolve without unbounded root-level fields;
- that paths and commands are sanitized before committed publication;
- that a constrained environment can produce a valid partial report.

Schema validity cannot establish that commands ran or that recorded evidence is
true. Reviewers must assess provenance and freshness separately.

## 16. Acceptance criteria

- [ ] A constrained hosted workspace can record useful local evidence without
      Docker, `act`, or remote Actions.
- [ ] Locked repository setup is distinguishable from repository validation.
- [ ] Optional tool absence does not block unrelated implementation progress.
- [ ] Unrun, unavailable, blocked, and deferred checks cannot validate as passed.
- [ ] Container-backed and direct self-hosted `act` paths have explicit gates.
- [ ] Remote CI can remain deferred while local readiness is reported truthfully.
- [ ] JSON and Markdown reports expose the represented revision and limitations.
- [ ] The contract can accept newly observed capabilities without a version bump.
- [ ] Downstream repository hooks and CI adapters retain their established owners.
