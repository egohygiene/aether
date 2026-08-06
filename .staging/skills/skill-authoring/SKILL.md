---
name: skill-authoring
description: Create, upgrade, organize, or validate portable project Agent Skills with concise SKILL.md instructions and optional scripts, references, or assets. Use when adding reusable agent capabilities under `.agents/skills`, separating procedures from agents and specs, or repairing skill metadata and progressive-disclosure structure.
---

# Skill Authoring

## Define the capability

Collect concrete requests that should trigger the skill and identify the reusable procedure required to fulfill them. Keep role identity in an agent, task requirements in a spec, repository-wide conventions in instructions, and immediate work in an issue or prompt.

## Plan resources

Include only resources that improve repeated execution:

- `scripts/` for deterministic or repeatedly rewritten operations
- `references/` for detailed domain guidance loaded only when relevant
- `assets/` for templates or files copied into outputs

Do not add a skill-local README, changelog, installation guide, or duplicated documentation. Keep references one level below `SKILL.md` and link each resource from the skill with guidance for when to use it.

## Create the skill

Place project skills at `.agents/skills/<skill-name>/SKILL.md` for cross-agent portability. Use a lowercase, hyphenated name of at most 64 characters that exactly matches the parent directory.

Use only portable frontmatter:

```yaml
---
name: skill-name
description: Describe what the skill does and the concrete requests or contexts that should trigger it.
---
```

Keep the description specific and no longer than 1024 characters. Write the body in imperative form. Put the core workflow, decision points, safety constraints, resource navigation, and validation in the body. Avoid explaining general knowledge the agent already has.

## Design progressive disclosure

Keep `SKILL.md` concise and under 500 lines. Move variants, schemas, long examples, and domain references into linked files. For references longer than 100 lines, add a compact table of contents when it materially improves navigation.

## Validate

Confirm frontmatter syntax, exact directory/name match, trigger quality, link integrity, resource necessity, lack of placeholders, and separation of concerns. Run every included script with representative inputs. Forward-test complex skills on realistic requests when practical, then refine instructions based on observed failure modes.
