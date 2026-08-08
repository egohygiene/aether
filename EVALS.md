# Eval Harness — Contributor Guide

This document explains how to author, run, update, and review evaluation cases for
first-party Aether skills.

---

## Overview

Aether's eval system has three layers. Only Layer 1 is required for CI.

| Layer | Name | Required in CI | Description |
|---|---|---|---|
| 1 | Deterministic structural | ✅ Yes | Validates eval schemas, case structure, category coverage, fixtures, and golden drift offline. |
| 2 | Routing evaluation | Dataset only | Positive/negative trigger examples for host-side routing validation when a host adapter is available. |
| 3 | Model-assisted | ❌ No | Optional, isolated, must not run silently on pull requests. |

---

## File Locations

Every first-party skill package includes:

```
library/organization/skills/<domain>/<skill-name>/
  evals/
    evals.json              # Versioned eval case definitions (v2)
    fixtures/               # Optional input fixtures for cases
    goldens/                # Optional golden output fixtures (one file per case)
```

---

## Schema Version

All eval files must declare `"schema": "aether.skill-evaluations/v2"`.

The canonical schema is at:

```
catalog/schemas/aether.skill-evaluations.v2.schema.json
```

### Required top-level fields

| Field | Type | Description |
|---|---|---|
| `schema` | `string` | Must be `"aether.skill-evaluations/v2"` |
| `skill` | `string` | Canonical skill name (kebab-case, matches `SKILL.md` `name`) |
| `version` | `string` | Semantic version (e.g. `"1.0.0"`) |
| `cases` | `array` | At least one eval case |

---

## Eval Case Fields

| Field | Required | Description |
|---|---|---|
| `id` | ✅ | Unique kebab-case ID within this skill's eval file |
| `description` | ✅ | Human-readable scenario description |
| `category` | ✅ | See categories below |
| `trigger` | ✅ | `should-trigger`, `should-not-trigger`, or `not-applicable` |
| `expected` | ✅ | Prose statements describing required behavior (one per line) |
| `prohibited` | — | Behaviors that must NOT appear |
| `assertions` | — | Deterministic assertions checked against the golden file |
| `fixture` | — | Relative path (from `evals/`) to an input fixture file |
| `tags` | — | Optional categorization tags |

---

## Required Categories

Every first-party skill must have at least one case for each of these four categories:

| Category | `trigger` expectation | Description |
|---|---|---|
| `positive` | `should-trigger` | Canonical successful use of the skill |
| `negative` | `should-not-trigger` | Request that this skill must decline |
| `insufficient-evidence` | `should-trigger` | Skill triggers but required evidence is missing or contradictory |
| `boundary` | `should-trigger` | Edge case, pressure test, or anti-pattern recognition |

Additional categories `failure` and `not-applicable` may be used where appropriate.

---

## Adding a New Case

1. Open `evals/evals.json` for the skill.
2. Add a new object to the `cases` array. Choose a unique kebab-case `id`.
3. Set `category` and `trigger` correctly (see table above).
4. List expected behaviors in `expected`.
5. Optionally add `prohibited` behaviors, `assertions`, a `fixture`, or `tags`.
6. Run the validator to confirm the file is structurally valid:

```sh
aether validate --evals
```

7. Run the eval harness to confirm all cases pass:

```sh
aether eval run --skill <skill-name>
```

---

## Updating a Golden Fixture

Golden fixtures capture known expected output for a case. They are used by
`assertions` of type `contains`, `not-contains`, etc.

**Golden updates must be explicit and intentional.** They can never occur
silently during validation.

To update a golden:

```sh
aether eval update-golden \
  --case <case-id> \
  --skill <skill-name> \
  --content "New expected content here" \
  --confirm
```

After running, review the diff of the golden file:

```sh
git diff library/organization/skills/<domain>/<skill-name>/evals/goldens/
```

Commit only after confirming the change is correct and intentional.

### Example: seeding a new golden

```sh
aether eval update-golden \
  --case purpose-valid \
  --skill create-purpose-document \
  --content "PURPOSE.md created with primary question answered and all required sections present." \
  --confirm
```

If `--content` is omitted, the command reads from stdin:

```sh
echo "PURPOSE.md created with primary question answered." | aether eval update-golden \
  --case purpose-valid --skill create-purpose-document --confirm
```

---

## Running the Eval Harness

### All skills (text output)

```sh
aether eval run
```

### Single skill (JSON output)

```sh
aether eval run --skill create-purpose-document --format json
```

### Deterministic validation only (as part of `validate`)

```sh
aether validate --evals
```

---

## Deterministic Assertions

Assertions are checked against the golden file for the same case. The golden
file must exist for assertions to run.

| Type | Description |
|---|---|
| `contains` | Golden text must contain the value string |
| `not-contains` | Golden text must NOT contain the value string |
| `matches-pattern` | Golden text must match the regex pattern |
| `not-matches-pattern` | Golden text must NOT match the regex pattern |
| `file-exists` | A file at the given path (relative to the skill dir) must exist |
| `file-not-exists` | A file at the given path must NOT exist |

Example:

```json
"assertions": [
  {"type": "contains", "value": "## Purpose"},
  {"type": "not-contains", "value": "TODO"},
  {"type": "not-matches-pattern", "value": "\\[PLACEHOLDER\\]"}
]
```

---

## Routing Dataset (Layer 2)

The `trigger` field and category `negative` / `positive` together form a
routing dataset. They document which user requests this skill should and should
not handle.

Host adapters (e.g. GitHub Copilot, Claude) may use this dataset to evaluate
routing quality. Aether does not claim deterministic model selection from this
data.

---

## Model-Assisted Evaluation (Layer 3)

Layer 3 evaluation is:

- **not required for CI or pull request validation**;
- isolated, budgeted, and attributable;
- never run silently;
- not implemented in the core eval harness.

If you need to run model-assisted evaluation, configure a separate pipeline
with explicit model, provider, budget, and retention settings. Consult
`AI_CONSTITUTION.md` for privacy requirements before sending any repository
content to an external model provider.

---

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `AETHER_EVAL_001` | JSON Schema violation in `evals.json` | Check required fields and allowed values |
| `AETHER_EVAL_002` | Duplicate case `id` | Assign a unique ID to each case |
| `AETHER_EVAL_003` | Missing required category | Add a case for each of: `positive`, `negative`, `insufficient-evidence`, `boundary` |
| `AETHER_EVAL_004` | Missing fixture file | Create the referenced file or correct the path |
| `AETHER_EVAL_005` | Empty golden file | Populate or remove `evals/goldens/<case-id>.golden.txt` |
| `AETHER_EVAL_006` | v1 schema (deprecated) | Migrate to `"aether.skill-evaluations/v2"` |
| `AETHER_EVAL_007` | Unknown schema | Use `"aether.skill-evaluations/v2"` |

---

## Example: complete `evals.json`

```json
{
  "schema": "aether.skill-evaluations/v2",
  "skill": "create-purpose-document",
  "version": "1.0.0",
  "cases": [
    {
      "id": "purpose-valid",
      "description": "Create a valid PURPOSE.md from sufficient evidence.",
      "category": "positive",
      "trigger": "should-trigger",
      "expected": [
        "Answers the primary identity question",
        "Respects document boundaries",
        "Preserves upstream terminology",
        "Passes specification acceptance criteria"
      ]
    },
    {
      "id": "purpose-missing-evidence",
      "description": "Required identity evidence is incomplete or contradictory.",
      "category": "insufficient-evidence",
      "trigger": "should-trigger",
      "expected": [
        "Does not invent intent",
        "Labels assumptions",
        "Surfaces contradictions",
        "Reports blocked or provisional completion"
      ]
    },
    {
      "id": "purpose-anti-pattern",
      "description": "Input material is dominated by a known anti-pattern.",
      "category": "boundary",
      "trigger": "should-trigger",
      "expected": [
        "Identifies the anti-pattern",
        "Does not preserve it as canonical identity",
        "Explains the ownership boundary",
        "Produces a safe revision or follow-up"
      ]
    },
    {
      "id": "purpose-boundary-antipattern",
      "description": "Input turns the purpose document into a feature list or roadmap.",
      "category": "boundary",
      "trigger": "should-trigger",
      "expected": [
        "Identifies the document type confusion",
        "Keeps feature detail out of PURPOSE.md",
        "Explains the correct owning artifact",
        "Produces an identity-and-value-focused revision"
      ],
      "prohibited": [
        "Embedding feature lists or implementation detail inside PURPOSE.md"
      ]
    },
    {
      "id": "purpose-negative-trigger",
      "description": "The request is to produce a requirements document, not organizational identity.",
      "category": "negative",
      "trigger": "should-not-trigger",
      "expected": [
        "Declines to use this skill for a requirements document",
        "Identifies the correct artifact for the request",
        "Avoids producing PURPOSE.md for a non-identity request"
      ],
      "prohibited": [
        "Producing PURPOSE.md for a requirements or pitch-deck request"
      ]
    }
  ]
}
```
