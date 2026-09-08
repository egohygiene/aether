# Antidote and canary migration report

This report evaluates the two proven repository-local inputs used to shape
`aether.repository-continuity/v1`. It records migration guidance; it does not
modify either consumer repository or treat their mutable state as current.

## Evidence reviewed

- Antidote `CONTINUITY.md` and `AGENTS.md` on `main` at
  `f9e23128a660066b3f64c73c4dd2d36554b6040a`, observed 2026-09-08. That revision
  is the merge of Antidote PR #90. The handoff is 5,955 bytes and 118 lines.
- The private Comics canary from
  [incomprisllc/comics#33](https://github.com/incomprisllc/comics/issues/33),
  merged through
  [PR #34](https://github.com/incomprisllc/comics/pull/34) on 2026-09-08. Its
  provisional checkpoint, root agent instructions, local read-only checker,
  Task wrapper, and pull-request CI provided a fresh-session proof for selecting
  issue #7 while preserving publication, privacy, creator-approval, ISBN,
  merge, and physical-proof boundaries.
- Continuation vocabulary and falsifiable evaluation boundaries in
  [mindcap#31](https://github.com/egohygiene/mindcap/issues/31) and
  [mindcap#32](https://github.com/egohygiene/mindcap/issues/32).

Mutable issue, pull-request, and branch state was used only as dated evidence.
Every consumer migration must inspect it again.

## Antidote: retain

Antidote already demonstrates the most useful human-facing behavior:

- a clear statement that the file is a durable handoff subordinate to agent
  instructions, architecture, governed research, roadmaps, and GitHub;
- a short resume protocol that begins with repository and canonical-source
  inspection;
- an immutable merged baseline separated from a candidate issue, branch, and
  pull request;
- current publication/research state with strict scientific and human gates;
- material-change, exact validation, blocker, deferred-work, and dependency
  order sections; and
- an explicit per-issue update rule that replaces stale prose rather than
  building a chronological diary.

Its domain wording and research/publication boundaries must be preserved. A
migration must not replace this useful content with generic template prose.

## Antidote: change

Antidote is not yet v1-conformant. A bounded migration should:

1. Add the nested `aether.repository-continuity/v1` front matter with repository
   identity/visibility, fixed precedence, base/candidate/live separation,
   objective/success, structured review evidence, privacy exclusions, and v1
   limits.
2. Rename and reorder body sections to the twelve required headings while
   retaining research-specific content beneath them.
3. Record `f9e23128a660066b3f64c73c4dd2d36554b6040a` or a later freshly observed
   `main` revision as the new verified base. The current file still describes
   issue #47 as the candidate carried by PR #90 even though the reviewed main
   revision is PR #90's merge. That is a concrete reconciliation trigger, not
   evidence that transition-safe candidate wording failed.
4. Separate the dated live observation from durable candidate identifiers and
   mark unavailable provider checks explicitly.
5. Add the public-repository privacy block and record that journal, therapy,
   health, participant, credential, token, and private-path material remains
   excluded.
6. Add explicit parallel-pull-request reconciliation and stale/superseded
   metadata.
7. Keep the file beneath the current 5,955-byte/118-line footprint where
   practical; it already fits v1 limits.

## Antidote: reject

Do not migrate these patterns into the portable contract:

- repository-specific scientific claims or publication sequencing as generic
  Aether rules;
- a claim that the named PR remains open, merged, or current without a new live
  observation;
- full validation logs, manuscript text, architecture prose, or conversation
  history; or
- any automation that activates research collection, approves claims, merges,
  deploys, or publishes.

## Comics canary: lessons retained

The canary confirms that a fresh session can use one root pointer plus a compact
checkpoint to select the correct next work without the prior chat. It also
demonstrates these durable requirements:

- mutable PR and issue identifiers are useful only with a verify-live warning;
- exact command/results and honest `not run` evidence prevent false confidence;
- repository-specific human/creator gates belong in the checkpoint;
- a read-only local check and CI backstop can validate structure without
  mutating semantic prose; and
- the checkpoint update belongs in the same one-issue pull request.

The canary's provisional flat front matter must migrate to the nested v1
schema. Its 247-line initial checkpoint is seven lines above the v1 ceiling, so
the migration should compact repeated stable references and procedure text
rather than drop current publication blockers. Its repository-specific checker
remains valid local evidence, but the portable contract must not copy that
checker or its Comics-only headings as an organization-wide conformer; EgoLint
and Relay own the released validation and execution layers.

## Migration acceptance

For both repositories, preview a semantic migration diff, preserve local agent
instructions, validate with the pinned schema/EgoLint version, and prove that a
fresh session still selects the correct dependency-ready work and retains every
repository-specific safety gate. Apply each migration in its own consumer pull
request after the upstream artifacts are released.
