# Contributing to Aether

## Scope

Contribute to canonical first-party source only:

- `library/organization/specs/`
- `library/organization/skills/`
- `library/organization/agents/`
- `catalog/` contracts, schemas, fixtures, and reports

Do not treat `.staging/` or `dist/` as canonical source.

## Workflow

1. Create a focused branch/PR for one concern.
2. Edit canonical source.
3. Run validation/build checks.
4. Regenerate derived artifacts when canonical source changed.
5. Re-run checks and include results in the PR description.

## Required local checks

```sh
./aether validate --format "text"
./aether catalog generate --check
python3 catalog/validate_catalog.py
python3 library/organization/skills/build-distributions.py --check
python3 library/organization/agents/build-projections.py --check
./aether test
```

## Common contributor tasks

- Catalog records and provenance: `docs/catalog-contribution-guide.md`
- First-party skill authoring: `docs/first-party-skill-authoring-guide.md`
- External-source review: `docs/external-source-review-guide.md`
- Release and pinning: `docs/release-and-pinning-guide.md`
- Agent/hook safety: `docs/agent-and-hook-safety-guide.md`

## Governance constraints

- Do not remove staged content until ADR-005 deletion-gate conditions are met.
- Do not promote `draft` to `stable` without human review.
- Do not add CI/release automation owned by neighboring repositories.

See `DECISIONS.md`, `PURPOSE.md`, and `ARCHITECTURE.md`.
