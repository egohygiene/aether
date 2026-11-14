# Catalog Contribution Guide

## Canonical inputs

The first-party catalog is derived from canonical source:

- `library/organization/specs/**/*.spec.md`
- `library/organization/skills/**/SKILL.md`

Do not hand-edit generated `catalog/first-party/catalog.v1.json` fields that conflict with frontmatter authority.

Regeneration refreshes source-owned versions, lifecycle, descriptions declared
in frontmatter, licenses, owners, domains, scope, and relationships even when
a catalog record already exists. Specification descriptions without a
frontmatter declaration retain their catalog summary; new records use the
first prose line. Specification scope remains catalog-owned. Skill display
titles, tags, related/superseding links, compatibility notes, and deprecation
annotations also remain catalog-owned; `allowed-tools` supplies a skill's
required-tool list.

The approved specification lifecycle maps to `stable` with
`source_state: approved`. Regeneration preserves explicit release exclusions
and removes inclusion when source becomes non-stable; it does not approve a
release. Invalid source metadata stops generation before the catalog is written.
Catalog validation names the artifact and fields that disagree with source,
even when its stored digest has already been refreshed.

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
