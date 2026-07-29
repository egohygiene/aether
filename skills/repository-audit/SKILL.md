---
name: repository-audit
description: Perform an evidence-based, non-destructive repository audit and write a structured report. Use for holistic or focused reviews of architecture, code quality, testing, security, CI/CD, dependencies, documentation, developer experience, maintainability, accessibility, performance, or repository hygiene.
---

# Repository Audit

## Resolve the request

Determine the audit strategy, included and excluded scope, focus areas,
depth, and constraints.

Read repository-level audit specifications, agent definitions, architecture
documents, and instructions when present. Apply documented defaults and record
every inferred value in the resulting report.

## Inspect systematically

1. Read the repository overview, architecture, decisions, and applicable specifications.
1. Review existing audits before recording new findings.
1. Inspect automation, manifests, workflows, source, tests, and documentation relevant to scope.
1. Run read-only diagnostics when they provide reproducible evidence.
1. Record material files, tools, commands, or environments that were unavailable.

## Maintain evidence integrity

- Label statements as observed, inferred, recommended, or unverified.
- Cite repository-relative paths, symbols, configuration keys, or command results precisely.
- Assign lower confidence when evidence is incomplete.
- Separate the observation, its significance, and the recommendation.
- Record strengths and effective practices, not only defects.
- Avoid repeating prior findings without checking their current state.
- Never present an unavailable or blocked check as completed.

## Write the report

Follow the repository's audit specification and output conventions when they
exist.

Otherwise, create a uniquely named Markdown report under `audits/`. Never
overwrite an existing report.

During a normal audit, modify only the new audit report. Do not apply fixes,
update dependencies, reformat files, open issues, create commits, or alter
repository configuration unless the request explicitly expands the scope.

## Validate

Confirm that the report documents:

- scope and exclusions
- evidence sources
- commands executed
- positive observations
- findings
- severity and confidence
- uncertainties
- blocked checks
- recommended follow-up work
- a prioritized backlog

When the audit cannot be completed, produce a truthful partial or blocked
report and identify the next evidence required.
