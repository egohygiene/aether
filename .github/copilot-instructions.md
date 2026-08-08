# Copilot Instructions for Aether

These instructions give Copilot and custom agents the repository-specific
context needed to inspect, validate, and change Aether correctly.

For full architectural intent, read the governance documents:
[`PURPOSE.md`](../PURPOSE.md) · [`ARCHITECTURE.md`](../ARCHITECTURE.md) ·
[`SYSTEM.md`](../SYSTEM.md) · [`AI_CONSTITUTION.md`](../AI_CONSTITUTION.md) ·
[`DECISIONS.md`](../DECISIONS.md) · [`ROADMAP.md`](../ROADMAP.md)

---

## What Aether Is

Aether is the canonical library of reusable AI specifications, skills, agent
source, schemas, catalogs, and distribution artifacts for the Ego Hygiene
organization.

---

## Canonical Source Location

```
library/organization/skills/   # first-party skill packages
library/organization/specs/    # first-party specifications
```

Do **not** treat `.staging/`, `dist/`, or any other path as canonical source.

---

## Key Rules

1. **Do not move or delete `.staging/` content** without satisfying the
   deletion gate in [`DECISIONS.md ADR-005`](../DECISIONS.md#adr-005).
2. **Do not add CI workflows, toolchain setup, or release automation** to this
   repository — those belong to Relay, Realm, and egohygiene/.github.
3. **Do not promote an artifact from `draft` to `stable`** without human
   review.
4. **Label open questions explicitly** rather than inventing intent.
5. **Validate local Markdown links** before finalizing documentation changes.
6. **Consumer-local instructions override Aether defaults** for that consumer's
   context.

---

## How to Inspect the Repository

```sh
# List all canonical specifications
find library/organization/specs -name "*.spec.md" | sort

# List all canonical skills
find library/organization/skills -name "SKILL.md" | sort

# Count staged files
find .staging -type f | wc -l

# Verify governance documents exist
find . -maxdepth 1 -type f \
  \( -name "PURPOSE.md" \
  -o -name "ARCHITECTURE.md" \
  -o -name "SYSTEM.md" \
  -o -name "AI_CONSTITUTION.md" \
  -o -name "DECISIONS.md" \
  -o -name "ROADMAP.md" \) \
  -print
```

---

## How to Validate Changes

```sh
# Check for broken local Markdown links (manual scan for now; no link checker installed)
grep -rn '\](\./' library/organization/ *.md .github/ | grep -v '.git'

# Confirm spec front-matter has required fields
find library/organization/specs -name "*.spec.md" | xargs grep -l "^schema: aether.specification/v1"
```

---

## Artifact States

`draft` → `stable` → `deprecated` → `retired`

Only `stable` artifacts may be released.  Only human review may promote
`draft` to `stable`.

---

## Responsibility Split (Summary)

| Concern | Owner — not Aether |
|---|---|
| Org agent deployment | `egohygiene/.github` |
| Repository baseline | Empathy |
| Repository templates | Holon |
| Dev environment | Realm |
| Shell commands | Mantle |
| Lint implementation | Egolint |
| GitHub Actions | Relay |
| Conformance | PACE |

See [`PURPOSE.md §4`](../PURPOSE.md#4-what-aether-is-not) for the full table.

---

## Commit Convention

```
docs(architecture): <summary>
feat(skills): <summary>
feat(specs): <summary>
fix(<scope>): <summary>
```

Follow [Conventional Commits](https://www.conventionalcommits.org/).
