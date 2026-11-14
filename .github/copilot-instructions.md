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
library/organization/agents/   # provider-neutral AGENT.md sources
library/organization/instructions/ # shared instruction source
catalog/                      # schemas, governed records and annotations
```

Do **not** treat `.staging/` or `dist/` as canonical source. Root governance
remains repository-owned; [catalog ownership](../catalog/README.md) distinguishes
source-derived fields from reviewed annotations. Read [AGENTS](../AGENTS.md),
[META](../META.md), [the tactical ledger](https://github.com/egohygiene/aether/issues/105)
and [CONTINUITY](../CONTINUITY.md) for current work. Historical ADR conflicts are
explicit in [proposed ADR-0009](../docs/decisions/ADR-0009-generated-evidence-and-local-validation.md); its disposition remains pending.

---

## Key Rules

1. **Do not move or delete `.staging/` content** without satisfying the
   deletion gate in [`DECISIONS.md ADR-0005`](../DECISIONS.md#adr-0005).
2. **Preserve owner boundaries.** Relay owns reusable CI execution and Realm
   owns environment provisioning. Existing Aether-local callers, builders and
   release declaration remain repository-owned implementation evidence; changes
   must preserve explicit authorization and reconcile historical ADR-0002
   through proposed ADR-0009 rather than silently treating it superseded.
3. **Do not promote an artifact from `draft` to `stable`** without human
   review.
4. **Label open questions explicitly** rather than inventing intent.
5. **Validate local Markdown links** before finalizing documentation changes.
6. **Consumer-local instructions override Aether defaults** for that consumer's
   context.
7. **Run the decision-impact checkpoint before code changes.** Apply the
   canonical
   [`decision-impact.AGENTS.md`](../library/organization/projections/templates/decision-impact.AGENTS.md)
   module by reference; do not copy or weaken its Hygiene contract pins.
8. **Follow the repository release declaration before changing versioning or
   publication behavior.** Read [`AGENTS.md`](../AGENTS.md),
   [`.egohygiene/release.json`](../.egohygiene/release.json), and the
   [`repository-release`](../library/organization/specs/release/repository-release.spec.md)
   specification. Release preparation is reviewable; publishing remains an
   explicit manual, repository-owned action.

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
# Existing repository-owned checks; see CONTRIBUTING.md for the complete handoff
./aether validate --links --format json
./aether validate --format json
./aether catalog generate --check
./aether distribution build --check
./aether test
```

---

## Artifact States

`draft` → `experimental` → `stable` → `deprecated` → `retired`

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
| Reusable GitHub Actions | Relay |
| Aether-local validation/release callers | Aether, with the ADR-0009 conflict explicit |
| Policy/applicability | Hygiene |
| Fleet adoption | Pace |
| Evidence/query projections | Observatory |

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
