# First-Party Skill Authoring Guide

## Location and shape

Create new skills only under:

`library/organization/skills/<domain>/<skill-name>/SKILL.md`

Include companion directories as needed:

- `references/`
- `templates/`
- `evals/evals.json`

## Contract

Follow `library/organization/skills/SKILL-CONTRACT.md`.

Key requirements:
- `name` and `description` required.
- `name` must match parent directory (kebab-case).
- Aether metadata belongs under `metadata`.
- Do not include install-tracking metadata keys (`metadata.github-*`) in canonical source.

## Validation/build

```sh
./aether validate --skills --format "text"
./aether validate --evals --format "text"
python3 library/organization/skills/build-distributions.py --check
```
