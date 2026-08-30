# External Source Review Guide

## Purpose

External skills listed in Aether must be provenance-backed and schema-valid
before review. Review does not authorize installation, execution, publishing,
or promotion into Aether's first-party library.

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

## Selection boundary and cadence

The source review register supplies one allowlisted, deferred, or rejected
decision for every captured source. The initial allowlist is deny-by-default:
listed records are only agent-assisted reference material and still require
human review.

Before selecting or updating an external artifact:

1. Confirm the exact source record, immutable pin, and normalized digest.
2. Review embedded links, tool requests, and instructions for external effects.
3. Keep installation, execution, first-party adoption, delivery, and
   publication as separately authorized actions.
4. Run the external governance validator.

Follow the routine and event-driven review schedule in the external review
cadence document. A security advisory, license change, ownership transfer,
repository archival, redirect, pin change, executable resource, or proposed
external action triggers immediate review.
