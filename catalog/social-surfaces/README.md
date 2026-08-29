# Social-surface specifications catalog

This directory is the canonical, versioned boundary for cross-platform social
and advertising creative-surface requirements. It is intentionally separate
from Identity: Aether stores reusable evidence, query behavior, freshness
rules, provenance, and release pinning; Identity may later select an approved
and pinned subset for a Brand Kit.

## Source and rights boundary

`catalog.v1.json` records the supplied 2026-08-28 source snapshot by exact
SHA-256 digest, capture timestamp, and inventory counts. The source candidate
is registered in `../external/source-candidates.v1.json` with a pending rights
review; [#54](https://github.com/egohygiene/aether/issues/54) owns that
decision. The archive and its SVG templates are deliberately absent from this
repository.

No source-derived surface records may be added while the catalog's
`rights_review.state` is `pending` or `rejected`. A review decision must name
the permitted use and its evidence before changing the catalog to stable or
release-included.

## Contract and unknowns

The schema is `../schemas/aether.social-surface-catalog.v1.schema.json`.
Every record must state organic versus advertising use and retain its source
candidate, original source URL/label, capture time, snapshot digest, and
verification state. Unavailable values use explicit `null` or `unknown` states;
they are never guessed from neighboring placements.

Run deterministic validation and an offline query:

```bash
python3 catalog/social-surfaces/validate.py
python3 catalog/social-surfaces/query.py --use "organic" --output-format "markdown"
```

## Distribution and pinning

Build the governed catalog package with:

```bash
./aether distribution build --output-directory "dist"
```

The resulting `dist/catalogs/social-surface-specs/distribution-manifest.v1.json`
contains the catalog identity, semantic version, and canonical digest. A stable,
rights-approved catalog is included in Aether's release manifest; consumers pin
both that repository tag and those manifest values.
