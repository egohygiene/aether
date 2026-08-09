# External Source Review Guide

## Purpose

External skills listed in Aether must be provenance-backed and schema-valid before approval.

## Evidence sources

- `.staging/manifests/skills-lock.json` (migration lock evidence)
- `catalog/external/approved-skills.v1.json` (approved external records)
- `catalog/schemas/aether.external-source-record.v1.schema.json` (record schema)

## Review checklist

1. Confirm upstream repository and skill path match staged evidence.
2. Confirm install examples are pinned and reproducible.
3. Validate external catalog and staging inventory tests:

```sh
./aether test
./aether validate --provenance --format "text"
```

4. Keep unresolved provenance questions explicit; do not infer ownership/history.
