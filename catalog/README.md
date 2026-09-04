# Catalog contracts (v1)

This directory defines machine-readable contracts for Aether cataloging,
provenance, lifecycle, and distribution.

## Files

- `schemas/` — versioned JSON Schemas
- `fixtures/` — valid/invalid examples per schema
- `schemas/aether.social-campaign-handoff.v1.schema.json` — closed review,
  approval, immutable-export, and external-publication receipt contract
- `schemas/aether.cross-agent-evidence-packet.v1.schema.json` — public evidence,
  exact-span, provenance, review, lifecycle, and least-authority packet contract
- `schemas/aether.sanitized-research-request.v1.schema.json` — separately
  reviewed public request contract for outbound research boundaries
- `schemas/aether.evidence-projection.v1.schema.json` — provider, MCP, A2A,
  filesystem, and queue projection authority ceiling
- `evidence-packets/` — deterministic importer, usage, and synthetic legal and
  software fixtures with adversarial mutation cases
- `schemas/aether.repository-release.v1.schema.json` — repository profile,
  semantic-version, changelog, delivery, evidence, and manual-handoff contract
- `first-party/catalog.v1.json` — canonical compatibility catalog for the current specification and skill corpus
- `external/approved-skills.v1.json` — governed external skill catalog entries reconstructed from staged provenance
- `external/source-candidates.v1.json` — non-publishable external source candidates, including their rights-review state
- `social-surfaces/` — versioned social-surface contract, offline catalog, query tool, and deterministic distribution builder
- `PROVENANCE.md` — shared lifecycle, trust, provenance, and stable-publication policy
- `provenance_model.py` — deterministic normalized provenance projection across first-party specs/skills/agents and reviewed external artifacts
- `reports/first-party-coverage.v1.json` — coverage report for the canonical spec/skill corpus
- `reports/staged-skills-inventory.v1.json` — complete staged-skill inventory with per-item migration disposition
- `validate_catalog.py` — v1 specification/skill catalog validator

## Authority when fields overlap

Canonical first-party source lives under `library/organization/`.

Current source-specific catalogs have different responsibilities:

- specification and skill frontmatter is authoritative for `first-party/catalog.v1.json`;
- canonical agent source and `library/organization/agents/catalog.json` own agent-specific capability metadata;
- reviewed external source records own their upstream provenance and redistribution evidence.

The normalized provenance model is a **derived policy view**, not a second hand-edited source of truth. It gives these artifact kinds one common vocabulary for source, revision, digest, license, trust, lifecycle, compatibility, maintainer ownership, and publication readiness.

## Lifecycle and versioning rules

Canonical lifecycle vocabulary:

```text
draft -> experimental -> stable -> deprecated -> retired
```

Only `stable` artifacts with complete publishable provenance are eligible for release. Stable lifecycle alone does not override missing revision, digest, license, trust, or maintainer evidence.

`deprecated` artifacts should name a replacement when one exists. `retired` artifact IDs are never reused.

Repository release tags and artifact content revisions are distinct:

- repository tag pins a release-manifest snapshot;
- artifact version records the source artifact's revision inside that snapshot.

## Artifact-kind coverage

The normalized provenance contract supports:

- specifications;
- skills;
- agents;
- prompts;
- instructions.

The current repository has canonical specs, skills, and agents. Prompt/instruction source can be added later without inventing a separate provenance lifecycle. Rich agent catalog/cost-control work remains separate from the generic provenance contract.

## First-party and external separation

First-party and external artifacts are never conflated:

- first-party canonical source receives `first-party` trust;
- reviewed external source preserves its upstream repository/revision, license, digest, and external trust classification;
- a pending external source candidate remains external, non-publishable, and cannot silently populate a stable first-party catalog;
- external review does not silently reclassify content as first-party;
- restricted, unknown, or untrusted source cannot enter stable publication.

## Canonical serialization and digest rules

- text-source digests use `sha256-utf8-lf`;
- digest input is UTF-8 bytes after line-ending normalization to LF;
- deterministic JSON serialization is `json.dumps(sort_keys=True, separators=(',', ':'))`;
- provenance records are sorted by stable artifact ID.

## Staging lock preservation

`.staging/manifests/skills-lock.json` is preserved strictly as migration
provenance evidence. Its historical `computedHash` values are not treated as
cryptographically valid until the algorithm is reconstructed.

## Validation commands

Validate existing v1 catalog coverage and relationships:

```bash
python3 catalog/validate_catalog.py
```

Validate the shared lifecycle/provenance model and deterministic first-party + external projections:

```bash
python3 catalog/provenance_model.py check --scope "all"
```

Generate review-only normalized catalogs:

```bash
python3 catalog/provenance_model.py generate \
  --scope "first-party" \
  --output "/tmp/aether-first-party-provenance.json"

python3 catalog/provenance_model.py generate \
  --scope "external" \
  --output "/tmp/aether-external-provenance.json"
```

Generated review files are not canonical source and should not be edited as a substitute for the underlying artifact/catalog records.

## External source selection

The reviewed external catalog is not an execution allowlist. The source review
register covers every captured upstream source with an allowlisted, deferred,
or rejected decision. The initial allowlist is deny-by-default and grants only
human-reviewed, agent-assisted reference use for its exact immutable records.

Run the external cross-catalog check with:

    python3 catalog/external/validate.py
