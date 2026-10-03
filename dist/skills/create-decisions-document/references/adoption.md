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

Holon blueprint 1.0.0 at the selected commit preserves records and provides the
existing plan → render → verify → rollback mechanism. Its emitted policy reference
still selects `f598ed659a43dd759d4ede41c27f9e5daf991aa7`. The selected ratified
EgoLint/Relay profile requires `c589587395750cd1c79c6fa0bef010189c547249` for both ADR
contract pins and the consumer policy reference. These revisions are not interchangeable.

Use **validate-first** for Identity and other existing decision corpora. Inventory
ownership/provenance and propose the consumer-owned policy upgrade against the
selected policy-reference template. If Holon owns that file, an updated reviewed
Holon artifact/pack and state reconciliation are required before materialization;
do not hand-edit generated policy or falsify its recorded hash. The old blueprint
is not a ready-to-apply ratified-policy baseline. Report this owner compatibility
gap without silently upgrading unrelated source pins.

For a compatible reviewed Holon pack, follow its pinned
[materialization guide](https://github.com/egohygiene/holon/blob/660b941f99618806fcadd589bcdae61c519f96e4/docs/materialization-engine.md):
`plan` previews the current target and source digests; `render` applies only the
reviewed matching plan; `verify` checks ownership; `rollback` refuses to erase
post-render edits. ADR bodies remain repository-owned throughout.

## Validation boundary

The selection records EgoLint's reviewed ratified-policy validator and Relay
profile 1.0.0-alpha.2. Explicitly prepare/acquire dependencies, then validate offline
through the pinned owner tools. Both ADR contract tuples in the consumer EgoLint
policy and `docs/decisions/policy-reference.json` must agree. Do not update the
independent proposed roadmap/projection contracts merely because ADR policy is
accepted. Old pins fail; legacy adoption can remain partial despite valid syntax.

The native Relay replay demonstrates approved-policy proposals, missing approval,
old-pin rejection and legacy coverage. Hosted architecture
acceptance, release, required activation, ADR collection and public Decisions
publication have separate owners. Record unavailable checks and the precise
source revisions; a generated page or passing syntax check is not adoption.

## First canary and completion

[Identity#69](https://github.com/egohygiene/identity/issues/69), coordinated by
[Pace#5](https://github.com/egohygiene/pace/issues/5), is the first validate-first
canary. Its scheduling gate still applies. Preview existing IDs, inline/detailed
records, policy/index ownership and human evidence; then propose one bounded
adoption/migration PR. Preserve the accepted publication topology. Authoring
readiness does not complete historical backfill, deployment or fleet adoption.

Before the next skill/policy upgrade, compare the prior and target full pins,
preview the managed-block diff and validate all affected records. Retain prior
pins, file digests and migration/materializer state. Roll back the scoped upgrade
through the owning mechanism after checking for later edits; never delete authored
history or silently downgrade records to make an old validator pass.
