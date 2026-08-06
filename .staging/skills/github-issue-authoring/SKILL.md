---
name: github-issue-authoring
description: Convert ideas, brain dumps, specifications, audits, bugs, research, migrations, and implementation goals into scoped, repository-aware, copy-ready GitHub issues or dependency-ordered roadmaps. Use when drafting, revising, decomposing, or validating GitHub issue content rather than implementing it.
---

# GitHub Issue Authoring

## Select the governing format

Read `../../../.github/specs/github-issue-creator.spec.md` when present. If the user requests the repository's exact two-code-block copy format, also apply `../../../.github/specs/github-issue-authoring.spec.md`. Inspect `.github/ISSUE_TEMPLATE/` and use a template only when it clearly fits.

## Extract durable intent

Identify the problem, motivation, current state, desired state, affected system, constraints, sequencing, unresolved questions, and explicit future work. Remove repetition while preserving context that explains why the work matters.

## Inspect before prescribing

Use available repository evidence to confirm architecture, files, dependencies, commands, workflows, tests, labels, and related work. When access is incomplete, describe expected areas provisionally and record assumptions. Never fabricate exact paths or conventions.

## Classify and size

Choose one primary issue type and one observable outcome. Prefer a focused, independently reviewable vertical slice. Create a roadmap when foundation, multiple subsystems, migration phases, or separately valuable outcomes require ordering. Do not mix discovery and production implementation unless a bounded proof of concept is the stated outcome.

## Write the issue

Include the sections required by the governing specification. Make requirements normative, scope explicit, exclusions visible, implementation guidance evidence-backed, validation executable, and acceptance criteria observable. Include dependencies, risks, migration, security, privacy, accessibility, and documentation only when relevant.

## Validate the contract

Confirm that another engineer can determine what to change, what not to change, how to verify it, and when the issue is complete. Check title clarity, internal consistency, acceptance-criteria traceability, Markdown correctness, and copy readiness. Return only the requested issue, roadmap, comment, or batch format; do not implement the work.
