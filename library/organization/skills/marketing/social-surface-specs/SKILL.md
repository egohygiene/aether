---
name: social-surface-specs
description: Select and explain pinned social-media or advertising creative surfaces from a provenance-governed offline catalog. Use when work needs platform placement, dimensions, media limits, safe zones, or organic-versus-advertising distinctions.
license: MIT
metadata:
  aether-version: "1.0.0"
  aether-status: "experimental"
  aether-scope: "organization"
  aether-domain: "marketing"
  aether-owners: "egohygiene"
  aether-created: "2026-08-29"
  aether-updated: "2026-08-29"
  aether-executable-resources:
    - "scripts/query-social-surfaces.py"
  aether-distribution-resources:
    - source: "catalog/social-surfaces/catalog.v1.json"
      destination: "references/social-surface-catalog.v1.json"
    - source: "catalog/social-surfaces/query.py"
      destination: "scripts/query-social-surfaces.py"
---

# Social-surface specifications

Use the pinned offline catalog to choose a creative surface. It is a dated
reference, not a claim that a platform's policy is currently unchanged.

## Select a surface

Start with the exact platform and distinguish organic from advertising work.
Then constrain the placement, media format, or content type only when they
materially change the output.

```bash
python3 scripts/query-social-surfaces.py \
  --catalog "references/social-surface-catalog.v1.json" \
  --platform "Example Network" \
  --use "organic" \
  --output-format "markdown"
```

The query is deterministic and offline. It returns the catalog ID, version,
and digest with every result so a consumer can compare it to its lockfile.
No result is better than guessing: report that the pinned catalog lacks the
requested placement and direct the requester to an approved update path.

## Interpret the result

- Preserve organic and advertising as separate use cases.
- Report dimensions, aspect ratio, file types and limits only when present.
- Treat a `safe_zone.state` of `unknown` as unknown; it is not permission to
  place important content near an edge.
- Preserve the source URL, label, verification state, capture time, and
  snapshot digest when communicating a selected surface.

Read [catalog-contract.md](references/catalog-contract.md) for record fields,
provenance, and consumer locks. Read [freshness-and-rights.md](references/freshness-and-rights.md)
before making a paid, high-impact, or policy-sensitive delivery.

## Freshness and rights boundary

Never describe a dated catalog record as current platform policy. For changed,
consequential, paid, or production requirements, verify the record's linked
official source and say that a live check occurred. Do not copy source-pack
templates, inject unpublished source data, or change rights/review status.

The current catalog is experimental and rights-pending. Its empty records list
is intentional: the source archive is registered by digest but is not
redistributed through this skill until an explicit review authorizes that use.
