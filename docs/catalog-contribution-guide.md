# Catalog Contribution Guide

## Canonical inputs

The first-party catalog is derived from canonical source:

- `library/organization/specs/**/*.spec.md`
- `library/organization/skills/**/SKILL.md`

Do not hand-edit generated `catalog/first-party/catalog.v1.json` fields that conflict with frontmatter authority.

## Update flow

1. Edit canonical spec/skill frontmatter and body.
2. Regenerate/check the catalog:

```sh
./aether catalog generate --check
./aether catalog generate
```

3. Validate catalog contracts:

```sh
python3 catalog/validate_catalog.py
```

## Required invariants

- Artifact IDs are unique.
- Source paths/digests map 1:1 to canonical files.
- Relationship targets resolve.
- Release inclusion remains lifecycle-compliant (only stable releasable).
