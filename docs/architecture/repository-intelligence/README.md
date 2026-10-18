# Repository Intelligence: architecture and rollout

A shareable explanation of the target architecture and the capability-by-capability
rollout, refreshed **October 5, 2026**. This is a program map, not evidence that
every illustrated route is live.

[Open or download the full-size infographic](architecture-and-rollout-2026-10-05.png).

![Repository sources pass through Relay collection and EgoLint validation into Observatory snapshots. Relay builds repository pages; egohygiene.io builds organization views. Hygiene, Aether and Holon provide shared foundations. Pace coordinates a pilot, reviewed consumer PRs, publication verification and continuing refresh. Decisions comes first, then Roadmap, then other capabilities.](architecture-and-rollout-2026-10-05.png)

## What each repository does

These are ownership boundaries and shared build tools. The diagram does not
require each box to be an always-running service.

| Owner | Plain-language responsibility |
| --- | --- |
| Each repository | Owns canonical ADRs, roadmap and source evidence; humans approve decisions |
| Hygiene | Defines rules, schemas, applicability, routes and state meanings |
| Aether | Supplies authoring skills and review guidance, including continuous ADR capture |
| EgoLint | Validates source conformance and reports evidence |
| Relay | Collects evidence, invokes validation and normalization, and builds reusable repository pages |
| Observatory | Produces consistent, read-only repository and fleet snapshots with provenance, freshness and explicit missing data |
| Holon | Supplies templates and visual building blocks, preserving repository-owned records |
| Pace | Coordinates pilots, reviewed consumer upgrades, adoption tracking, drift and rollback |
| `.github` | Tracks the program and organization feature specifications |
| `egohygiene.io` | Composes and hosts the organization portal using safe normalized evidence |

Relay provides reusable execution; the consumer or declared host owns site
composition, credentials and deployment. Delivery can use an existing site,
central hosting, an artifact-only profile, or an intentionally disabled route.
Applicability determines the correct choice. A missing page does not automatically
mean another deployment is needed.

The diagrams are derived views of canonical sources. Observatory does not rewrite
ADRs, and Pace is the adoption coordinator rather than the renderer. Unknown,
stale and partial coverage stays explicit; private evidence and topology stay
out of public output.

## How a capability reaches the fleet

1. Finish and validate its shared source-to-page support.
2. Prove one real consumer: populated sources, successful build, declared
   publication, working URL and repeat refresh. Identity is the planned Decisions
   pilot under [Identity #69](https://github.com/egohygiene/identity/issues/69).
3. Adopt the shared capability across applicable repositories with bounded,
   reviewed consumer PRs. Reuse the implementation and update each consumer's
   sources, configuration and immutable tool pins.
4. Verify each delivery profile and ongoing refresh; track adoption and drift in
   Pace. Close an issue only when its own acceptance criteria are complete.
5. Repeat for the next capability.

The selected order is **Decisions → Roadmap → other capabilities**, with each lane
subject to its prerequisites:

- [Pace #5](https://github.com/egohygiene/pace/issues/5): ADR / Decisions adoption.
- [Pace #31](https://github.com/egohygiene/pace/issues/31): populated Roadmap adoption
  as capability 2, after ADR.
- [Pace #15](https://github.com/egohygiene/pace/issues/15): Status adoption after its
  Hygiene policy, Observatory read model and Relay presentation prerequisites.

**A live Decisions page and completed historical ADR backfill are separate
milestones.** Repository ADR issues also require their own history review,
truthful decision states, index/lineage and continuous-capture acceptance.
Publishing a page alone does not close them. Exhaustive history catch-up can
remain a later pass while unfinished acceptance stays open and visible.

## Current checkpoint and source notes

Observed October 5: [Relay PR #135](https://github.com/egohygiene/relay/pull/135),
which integrates ADR collection into the Decisions build, remains open.
Identity #69 also remains open. Merging the shared builder alone will not deploy
Identity's page: the consumer must adopt it, supply conforming sources, publish
through its declared host and verify the result.

The [organization epic, .github #30](https://github.com/egohygiene/.github/issues/30),
is the program tracker. Its top priority update selects ADR/Decisions first;
older sections still describe Roadmap first. Pace #31 explicitly records Roadmap
as capability 2. Those older passages and historical inventory counts should not
be treated as current execution or deployment evidence. Some Pace #5 dependency
notes also predate the completed shared-foundation work; verify owning issues
before acting on that checklist. This document does not edit those trackers.

The diagram summarizes existing ownership and rollout intent; it creates no new
contract or policy authority. Detailed acceptance remains in the owning issues.

## Previous illustration

[October 3 architecture snapshot](architecture-2026-10-03.png), preserved unchanged.
Its implementation-progress strip is historical; use the current checkpoint and
live issues above when resuming work.
