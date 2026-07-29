---
name: repository-cleanup
description: Clean and standardize repository structure, configuration, formatting, documentation, generated artifacts, and project hygiene while preserving intended behavior. Use for cleanup passes, stale-file review, configuration consistency, formatter or linter hygiene, documentation polish, ignored artifacts, or low-risk technical-debt removal.
---

# Repository Cleanup

## Define the invariant

State the exact cleanup scope and the behavior, public interfaces, generated outputs, and user-owned changes that must remain unchanged.

## Classify before editing

Inspect repository status, ignore rules, formatters, linters, generators, task automation, ownership metadata, and neighboring conventions. Classify each candidate:

- safe mechanical cleanup
- safe documentation or configuration correction
- behavior-affecting change requiring separate authorization
- uncertain ownership or usage
- generated or externally managed artifact
- unrelated change outside scope

Edit only the first two categories during routine cleanup.

## Apply reviewable changes

- Group changes by purpose.
- Prefer repository automation for formatting and generated outputs.
- Preserve compatibility and existing public behavior.
- Remove duplication only after identifying the canonical source.
- Delete files only when ownership, obsolescence, references, and recovery are understood.
- Keep dependency upgrades, architectural refactors, and feature work separate.

## Validate

Run applicable formatting, linting, schema or configuration validation, documentation checks, and focused tests. Compare behavior-sensitive outputs when configuration changes may alter builds. Review the final diff for semantic changes, mass churn, secrets, generated files, and unrelated user edits.

Report cleaned areas, behavior-preservation evidence, validation results, and uncertain candidates intentionally left unchanged.
