# ADR authoring adoption checkpoint

This implements [Aether #91](https://github.com/egohygiene/aether/issues/91).
The existing `create-decisions-document` skill v2.0.0 and governing specification
v3.0.0 remain draft. Their workflow now consumes the already ratified Hygiene ADR
policy; independent proposed contracts retain their prior authority and pins.

The portable [adoption guide](../library/organization/skills/architecture/create-decisions-document/references/adoption.md)
covers preview, immutable installation, managed instructions, upgrade, rollback,
missing tools and the first validate-first canary, Identity #69 under Pace #5.
The [source selection](../library/organization/skills/architecture/create-decisions-document/references/policy-selection.json)
records exact owner commits and policy/schema/helper digests. Installation does
not activate enforcement or establish host adoption.

## Reproduce local evidence

Use Aether's `requirements-dev.lock` and a GitHub CLI supporting `gh skill` for
the repository suite. Keep Relay's Python environment separate: its pinned
`scripts/architecture-validation-requirements.txt` differs from Aether's lock.
Prepare the offline architecture runtime with the selected Relay checkout's
documented `prepare` command and exact Hygiene, EgoLint and Holon sources.

Set the following to existing verified paths, then run from the Aether checkout:

```sh
export AETHER_ADR_HYGIENE_SOURCE="$HYGIENE_CHECKOUT"
export AETHER_ADR_RELAY_SOURCE="$RELAY_CHECKOUT"
export AETHER_ADR_RELAY_PYTHON="$RELAY_PYTHON"
export AETHER_ADR_RUNTIME="$RELAY_ARCHITECTURE_RUNTIME"
python3 -m unittest discover -s tests -p test_decision_authoring.py -v
python3 aether eval run --skill create-decisions-document --format text
python3 aether validate --format text
python3 aether catalog generate --check
python3 catalog/validate_catalog.py
python3 aether distribution build --output-directory dist --check
python3 aether test
```

The owner integration tests explicitly skip when their source/runtime variables
are absent; skipped tests are not native validation evidence. Existing title
integration tests separately use `AETHER_EGOLINT_BINARY` with their selected
validator. Do not substitute that executable for Relay's architecture runtime.

The 11 ADR tests check managed-block upgrade/repeat/removal, selection parity,
owner schema and metadata compatibility, and five native synthetic consumers:
new proposal, legacy coverage, old policy rejection, proposed replacement of an
accepted predecessor, and implementation with missing approval. Synthetic human
approval in the predecessor fixture is test input, never an agent disposition.
Native runs verify that source records remain byte-identical.

The nine deterministic skill cases cover supported history, uncertain history,
proposal, supersession, routine work, legacy migration, outcome correction,
reference and unavailable tools. These check authored examples and assertions;
they do not execute a model or demonstrate provider/host loading.

## Compatibility before the canary

- Holon blueprint 1.0.0 at the selected commit still emits the older policy pin.
  Native validation rejects it. A Holon-owned reference needs a reviewed owner
  artifact/pack upgrade before materialization; preserve its provenance and ADRs.
- Hygiene's selected `decision-set` helper expects a reciprocal backlink for a
  proposed replacement. The selected EgoLint/Relay validator supports pending
  replacement without changing the accepted predecessor. Preserve that distinction
  and report a helper failure; do not manufacture authority or effective lineage.
- Hosted architecture acceptance remains deferred under Relay #99. Release,
  required activation, fleet migration and historical backfill have separate
  checkpoints. Aether #85 owns its own later backfill.

## Decision-impact handoff

ADR not required: this change applies the ratified Hygiene ADR-002 contract within
Aether's existing source/distribution and sibling ownership boundaries (Aether
ADR-001, ADR-002 and ADR-004). It adds authoring guidance and compatibility tests;
it introduces no new policy authority, artifact kind or distribution channel.
