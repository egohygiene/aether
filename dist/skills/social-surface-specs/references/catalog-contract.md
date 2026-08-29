# Catalog contract and consumer lock

The package's `social-surface-catalog.v1.json` is a pinned copy of Aether's
canonical catalog. Its top-level `catalog` object exposes the stable catalog
identity, semantic version, source snapshot, lifecycle, rights-review state,
and release eligibility.

Each future record has a stable `surface/...` ID and separately records:

- `use`: exactly `organic` or `advertising`;
- placement, content type, media format, dimensions, and aspect ratio;
- file types and size/duration limits as explicit values or `null` when absent;
- safe-zone state and only published insets;
- verification state and review timestamp;
- original source URL/label, capture timestamp, source candidate, and snapshot
  digest;
- record lifecycle.

For a consumer lock, preserve the Aether repository release tag plus the
catalog ID, version, and `sha256-utf8-lf` catalog digest from the generated
distribution manifest. A tag alone does not identify which catalog revision a
consumer used.
