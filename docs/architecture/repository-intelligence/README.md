# Repository Intelligence architecture

A shareable target-architecture snapshot, captured **October 3, 2026**. The bottom
strip records implementation progress on that date; destination cards describe
the intended system and do not establish that every page is deployed.

[Open or download the full-size PNG](architecture-2026-10-03.png).

![Repository sources flow through Relay collection, EgoLint validation, Observatory snapshots, and Relay site composition into repository experiences and an organization overview. Hygiene, Aether, and Holon supply shared foundations; Pace coordinates adoption.](architecture-2026-10-03.png)

## Flow and ownership

| Owner | Responsibility |
| --- | --- |
| Each repository | Canonical ADRs, roadmaps and source evidence; humans retain decision authority |
| Hygiene | Policy, contracts and projection semantics |
| Aether | Authoring skills and decision-impact guidance |
| Holon | Scaffolds and migration that preserves repository-owned records |
| Relay | Collection, orchestration, shared views and site composition |
| EgoLint | Conformance validation |
| Observatory | Deterministic repository and fleet read models |
| Pace | Canaries, adoption tracking and fleet rollout |

Approved publication workflows deliver the generated artifacts to composed
repository sites or central hosting, and to the organization overview. Insights
feed reviewed issues and source updates. Status has its own delivery track.
Source ownership, provenance and unknown coverage remain explicit throughout.

## Implementation checkpoint

- [Relay PR #121](https://github.com/egohygiene/relay/pull/121) merged at
  `33e1fc78727269bd3821dea53f6541f769cf4319`.
- [Aether PR #100](https://github.com/egohygiene/aether/pull/100) merged at
  `8ef3bd34d5fec835da54eb8acd0d074b79ee8fe2`; #91 is closed. See the
  [ADR authoring adoption guide](../../adr-authoring-adoption.md).
- Next: [Observatory #25](https://github.com/egohygiene/observatory/issues/25)
  distinguishes uncollected domains from observations with no records.
- Then: [Relay #115](https://github.com/egohygiene/relay/issues/115) collects
  existing canonical ADRs and integrates them with the Decisions build.
- First planned ADR canary: [Identity #69](https://github.com/egohygiene/identity/issues/69)
  under [Pace #5](https://github.com/egohygiene/pace/issues/5), subject to its shared
  foundation and publication gates. Holon's selected scaffold needs a reviewed
  policy-pin upgrade before canary materialization.
- Fleet pages and the org portal follow; exhaustive historical ADR catch-up is
  scheduled last in the reviewed execution sequence.

The [organization Intelligence epic](https://github.com/egohygiene/.github/issues/30)
and owning issues retain detailed scope, compatibility and publication gates.
This illustration creates no new contract or policy authority.
