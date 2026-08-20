# Aether Artifact Lifecycle and Provenance

This document defines the shared lifecycle and provenance model used across Aether artifact kinds and ownership classes.

## Why a normalized model exists

Aether already has mature source-specific catalogs:

- `catalog/first-party/catalog.v1.json` for canonical specifications and skills;
- `library/organization/agents/catalog.json` for reusable agent source;
- `catalog/external/approved-skills.v1.json` for reviewed external skills.

Those sources evolved at different times and therefore use different field names. They remain valid compatibility/source catalogs. `catalog/provenance_model.py` projects them into one normalized model for policy decisions without making a provider format or a generated report canonical.

Future `prompt` and `instruction` source uses the same normalized contract when those canonical directories are introduced.

## Normalized record

Every normalized artifact records:

- stable artifact identifier and kind;
- first-party or external ownership class;
- source repository/location;
- immutable content revision;
- cryptographic digest;
- license;
- trust classification;
- lifecycle state;
- compatibility requirements;
- maintainers;
- whether stable publication is currently allowed;
- explicit blocking reasons when it is not.

The JSON contract is `catalog/schemas/aether.provenance-catalog.v1.schema.json`.

## Supported artifact kinds

The normalized model covers:

- `specification`
- `skill`
- `agent`
- `prompt`
- `instruction`

Hooks remain a separate executable trust-boundary concern until their lifecycle is deliberately unified; adding them to this model requires a new reviewed schema version rather than silently treating them as passive artifacts.

## Lifecycle

The canonical lifecycle is:

```text
draft → experimental → stable → deprecated → retired
```

### Draft

The artifact is actively authored or incomplete. It may have unresolved provenance or compatibility questions and is not publishable.

### Experimental

The artifact is coherent enough to evaluate in bounded consumers, but its API, evidence, provenance, compatibility, or trust posture may still change. Experimental does not imply stable distribution support.

### Stable

The artifact has an approved public contract and is eligible for release **only when every provenance gate also passes**.

### Deprecated

The artifact remains understandable for compatibility/migration but should not be selected for new use. A replacement should be recorded when one exists.

### Retired

The artifact is no longer an active distribution candidate. Its identifier and provenance remain reserved for historical traceability.

Legacy source vocabularies are mapped explicitly. For example, source `approved` maps to normalized `stable`; reviewed external artifacts map to `experimental` rather than silently becoming first-party stable content.

## Trust

Normalized trust classifications are:

- `first-party` — canonical Ego Hygiene source under organization ownership;
- `trusted` — external source explicitly approved for the relevant use boundary;
- `restricted` — reviewed external source that remains bounded or requires additional review before stable publication;
- `untrusted` — known unsuitable for automatic consumption/publication;
- `unknown` — insufficient evidence.

Moving an external artifact into `library/organization/` is a separate adoption decision. Review alone never changes external material into first-party work.

## Publication gate

An artifact is not publishable merely because its lifecycle says `stable`.

Stable publication requires all of the following:

1. lifecycle state is `stable`;
2. source revision is an immutable commit or semantic version;
3. digest uses an approved SHA-256 content/tree algorithm and has a valid value;
4. license is resolved;
5. trust is `first-party` or explicitly `trusted`;
6. at least one maintainer is recorded;
7. external redistribution requirements are satisfied where applicable.

If any condition is missing, the normalized record must expose the blocking reason and CI must reject a stable-but-unpublishable state.

This distinction lets draft and experimental research exist without pretending it is release-ready while making stable publication fail closed.

## Source revision semantics

For first-party source today, the artifact's semantic `artifact_version` / `aether-version` is the content revision inside the repository snapshot. Repository release manifests provide the immutable repository-level revision used by consumers.

For external source, use the upstream commit digest whenever available. A tag alone is acceptable only when it is the immutable evidence available and the surrounding source record preserves that limitation.

The repository-release and artifact-revision concepts remain distinct per Aether ADR-004.

## Determinism

The normalized catalogs are derived views. They are sorted by artifact ID and use canonical JSON serialization for two-build reproducibility checks.

Run:

```bash
python3 catalog/provenance_model.py check --scope "all"
```

Generate a reviewable view without changing canonical source:

```bash
python3 catalog/provenance_model.py generate \
  --scope "first-party" \
  --output "/tmp/aether-first-party-provenance.json"
```

And separately:

```bash
python3 catalog/provenance_model.py generate \
  --scope "external" \
  --output "/tmp/aether-external-provenance.json"
```

`check` builds each requested view twice, validates it against the schema, checks unique/sorted IDs, verifies current canonical agent/external coverage, and enforces the stable publication gate.

## Canonical-source rule

The normalized provenance view does not replace source ownership:

- canonical first-party content remains under `library/organization/`;
- the existing first-party and external source catalogs remain the inputs they already own;
- generated provider projections remain generated;
- future publication tooling consumes normalized policy rather than copying source records into a provider-specific format.

This preserves Aether ADR-001 and ADR-003 while giving all artifact kinds one lifecycle/provenance vocabulary.
