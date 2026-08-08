# Catalog contracts (v1)

This directory defines machine-readable contracts for Aether cataloging and
provenance, plus the initial first-party catalog.

## Files

- `schemas/` — versioned JSON Schemas
- `fixtures/` — valid/invalid examples per schema
- `first-party/catalog.v1.json` — canonical first-party artifact catalog (23 specs + 29 skills)
- `reports/first-party-coverage.v1.json` — coverage report for canonical corpus
- `validate_catalog.py` — deterministic validator

## Authority when fields overlap

Authoritative source files are:

- `library/organization/specs/**/*.spec.md`
- `library/organization/skills/**/SKILL.md`

When frontmatter and catalog overlap, frontmatter is authoritative and the
catalog is derived. Any mismatch is a validation error.

## Lifecycle and versioning rules

- Lifecycle vocabulary: `draft -> experimental -> stable -> deprecated -> retired`
- Only `stable` artifacts are releasable.
- `deprecated` artifacts must name a replacement artifact ID.
- `retired` artifact IDs are never reused.
- Breaking changes require major `artifact_version` increment and inclusion in a
  new repository release manifest.

Repository release tags (used by `gh skill install --pin`) and artifact versions
are distinct:

- Repository tag pins a release manifest snapshot.
- Artifact version tracks one artifact record.

## Canonical serialization and digest rules

- Source digests use `sha256-utf8-lf`.
- Digest input is UTF-8 bytes after line-ending normalization to LF.
- Deterministic JSON serialization is `json.dumps(sort_keys=True, separators=(',', ':'))`.

## Staging lock preservation

`.staging/manifests/skills-lock.json` is preserved strictly as migration
provenance evidence. Its historical `computedHash` values are not treated as
cryptographically valid until the algorithm is reconstructed.

## Deferred scope for later issues

Later issues can extend these contracts to:

- first-party `agent`, `instruction`, and `hook` records,
- generated distribution inventories,
- external-source ingestion coverage,
- release manifests for published tags.

## Validation command

From repository root:

```sh
python3 catalog/validate_catalog.py
```
