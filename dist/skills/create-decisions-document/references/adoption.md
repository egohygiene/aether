# Pinned adoption and compatibility

[policy-selection.json](policy-selection.json) records the supported source matrix
and SHA-256 values of the policy, ratification, migration, schemas and owner helper.
Resolve its full commits and verify those bytes before relying on downloaded inputs.
No policy prose or validation semantics are vendored into this skill.

## Preview and installation

From the exact reviewed Aether checkout:

```sh
python3 aether distribution build --output-directory dist
python3 aether validate --format text
python3 aether distribution build --output-directory dist --check
python3 aether eval run --skill create-decisions-document --format text
```

Inspect `dist/skills/create-decisions-document` and the generated provider
instruction previews. A local development installation is:

```sh
gh skill install ./dist create-decisions-document --from-local
```

For a reviewed immutable consumer selection, use the actual reviewed Aether
commit (resolve the value before executing):

```sh
gh skill install egohygiene/aether create-decisions-document --pin "$AETHER_COMMIT"
```

Do not pass a moving branch or assume a draft package is a stable release. Record
the actual commit, artifact digest/version, host discovery path and observed load
result. Installing this skill does not install owner validators or activate a CI
hook. A missing skill requires an explicit unavailable result and a bounded draft
or evidence inventory; consequential decision handoff cannot claim completed skill
execution or conformance. Read-only roles retain their existing permissions.

## Managed instruction adoption

Preview the shared `decision-impact` marker block generated from Aether's source.
Use the existing projection merge boundary to insert or replace exactly that
block, preserving consumer prose and other modules; its boundary normalizes
separator whitespace. Malformed or
duplicate marker pairs block replacement. Do not overwrite a consumer AGENTS.md
with the generated repository fixture. Existing roles/tool allowlists remain
unchanged. The instruction calls this skill before implementation and again at
issue completion/PR handoff; a static block cannot enforce every agent or PR.

## Holon materialization compatibility

Holon blueprint 1.1.0 at the selected immutable commit emits the same Hygiene v1.2.0 policy selection as EgoLint and Relay. It preserves authored records and supplies the existing plan → render → verify → rollback mechanism.

Use **validate-first** for existing corpora. Inventory ownership/provenance and preview the per-record padding map before writing. If Holon owns a generated policy reference, re-render the reviewed upgraded pack and reconcile materializer state; do not hand-edit generated policy or falsify its recorded digest. Repository-owned records, human authority and immutable history remain outside generated ownership.

For a compatible reviewed Holon pack, follow its pinned
[materialization guide](https://github.com/egohygiene/holon/blob/a7734dba83305276b12932fcd4ce348044d9a2e9/docs/materialization-engine.md):
`plan` previews the current target and source digests; `render` applies only the
reviewed matching plan; `verify` checks ownership; `rollback` refuses to erase
post-render edits. ADR bodies remain repository-owned throughout.

## Validation boundary

The selection records EgoLint's reviewed ratified-policy validator and Relay
profile 1.0.0-alpha.4. Explicitly prepare/acquire dependencies, then validate offline
through the pinned owner tools. Both ADR contract tuples in the consumer EgoLint
policy and `docs/decisions/policy-reference.json` must agree. Do not update the
independent proposed roadmap/projection contracts merely because ADR policy is
accepted. Unsupported or mismatched pins fail. Explicit supported historical policy selections retain their own semantics; legacy adoption can remain partial despite valid syntax.

The native Relay replay demonstrates approved-policy proposals, missing approval,
old-pin rejection and legacy coverage. Hosted architecture
acceptance, release, required activation, ADR collection and public Decisions
publication have separate owners. Record unavailable checks and the precise
source revisions; a generated page or passing syntax check is not adoption.

## First canary and completion

[Identity#69](https://github.com/egohygiene/identity/issues/69), coordinated by
[Pace#5](https://github.com/egohygiene/pace/issues/5), is the first validate-first
canary. Its scheduling gate still applies. Preview existing numerical IDs across widths, inline/detailed
records, policy/index ownership and human evidence; then propose one bounded
adoption/migration PR. Preserve the accepted publication topology. Authoring
readiness does not complete historical backfill, deployment or fleet adoption.

Before the next skill/policy upgrade, compare the prior and target full pins,
preview the managed-block diff and validate all affected records. Retain prior
pins, file digests and migration/materializer state. Roll back the scoped upgrade
through the owning mechanism after checking for later edits; never delete authored
history or silently downgrade records to make an old validator pass.
