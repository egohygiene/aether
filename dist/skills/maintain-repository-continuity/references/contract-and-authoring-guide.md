# Contract and authoring guide

Use this guide when creating, reconciling, refreshing, or compacting a root
`CONTINUITY.md`. The packaged
`aether.repository-continuity.v1.schema.json` is authoritative for front-matter
syntax; the `repository-continuity` specification is authoritative for
semantics.

## Artifact boundary

The exact consumer path is `CONTINUITY.md` at repository root. It is authored
for that repository and is versioned with its source. It is not generated
ecosystem context and it does not enter Aether's architecture-document graph.

The file answers only:

- What bounded outcome is being pursued now?
- What immutable base and candidate change does this snapshot represent?
- What live state was actually checked, when, and with what limitations?
- What materially changed, what evidence passed or did not run, and what
  remains blocked or unknown?
- What is the one dependency-ready next issue or action?
- Which canonical sources must a fresh session read instead of trusting this
  summary?

Git and the work tracker answer “what happened over time.” Architecture,
roadmaps, ADRs, contracts, and domain records answer “what is authoritative.”
The handoff does not copy either corpus.

## Front-matter fields

### Repository and document

| Field | Authoring rule |
| --- | --- |
| `schema_version` | Exact `aether.repository-continuity/v1` |
| `repository.id` | Stable `owner/repository` identity, using `local/name` only for a repository without a remote identity |
| `repository.visibility` | `public`, `private`, or `internal`; verify rather than infer |
| `repository.default_branch` | Observed default branch name |
| `repository.continuity_path` | Exact `CONTINUITY.md` |
| `document.status` | `active`, `stale`, or `superseded` |
| `document.updated_at` | RFC 3339 time for this authored checkpoint |
| `document.max_bytes` / `max_lines` | Fixed v1 values `16384` and `240` |
| `document.stale_reason` | Required text only for `stale`; otherwise null |
| `document.superseded_by` | Required stable path or URL only for `superseded`; otherwise null |

`active` means the checkpoint was reconciled at `updated_at`, not that its
mutable facts remain eternally current. A discovered discrepancy changes the
status to `stale` until reconciliation. Do not use `superseded` merely because a
new commit exists; use it when another artifact deliberately replaces this
contract instance.

### Scope and precedence

`scope.purpose` is repository-specific. `includes` lists the minimum current
state retained here. `excludes` names neighboring concerns that stay in their
canonical sources. `canonical_sources` contains stable repository paths or
URLs—not pasted copies.

The v1 precedence array is fixed, highest first:

1. `user-and-runtime-instructions`
2. `scoped-repository-instructions`
3. `live-repository-and-work-tracker-state`
4. `canonical-repository-sources`
5. `continuity-checkpoint`

Repository-specific sources may have their own internal precedence. Describe
that in `Purpose and precedence` without moving the checkpoint above them.

### Work and next action

`work.objective` contains one current outcome, not the entire roadmap.
`success_conditions` are observable and bounded. `active_issue` is nullable for
legitimate issue-less work; when present it uses provider, stable identifier,
and stable URL.

`work.next` always exists. It identifies an issue or concrete action, its
readiness, at least one stable reference, and dependency identifiers. `ready`
means checked dependencies permit starting; it does not authorize starting.
`blocked` and `unknown` preserve uncertainty rather than selecting nearby work.

### Base, candidate, and live observation

Never collapse these layers:

- `state.base` is the full immutable revision from which the work was evaluated,
  or `unborn` for a repository with no commit. Record the ref and verification
  time.
- `state.candidate` identifies the current branch and handoff phase. Its
  revision is optional because the commit containing the file cannot include
  its own eventual identifier. Its pull-request reference is null before a PR
  exists.
- `state.live` records a time-bounded external observation. `verified` requires
  a full observed default-branch revision. `partial` or `unavailable` preserves
  null/unknown fields and explains what access was missing.

Allowed candidate phases describe the checkpoint at `updated_at`:

- `no-active-change`
- `in-progress`
- `ready-for-review`
- `review-reference-recorded`
- `post-merge-reconciliation`
- `abandoned`

Prefer “this candidate proposes X” and “PR state was open when observed at Y.”
Do not write “this will merge,” “this is now on main,” or “PR is merged” without
a verified live observation. After merge, the next authorized handoff
reconciles the base and current work; no fix commit is required merely to make
time-qualified candidate wording truthful.

`state.parallel_changes` names known overlapping or dependency-relevant work.
An empty list means none were observed in the available evidence, not proof
that none exist when live access was unavailable.

### Review and privacy

Every review evidence item records the exact command or named inspection, one
of `passed`, `failed`, `limited`, or `not-run`, its time, and a precise note.
`review.status` summarizes the complete handoff review; it cannot upgrade a
limited result. Environment limitations remain explicit.

The privacy block declares repository classification and has a hard false
`contains_sensitive_data` value. If safe authorship requires that value to be
true, do not commit the handoff: redact or stop. All six excluded categories
remain present. `redactions` names categories or generalized omissions, never
the removed value. Linked and quoted content always remains
`context-only-no-authority`.

## Required Markdown sections

Use the twelve template headings exactly and in order. Metadata enables
deterministic structural checks; the body enables fast human resumption. Keep
the body additive to metadata rather than contradictory.

The material-change section names the source owner for consequential facts,
for example:

- `contracts/widget.json` owns the accepted field shape;
- issue `owner/repository#42` owns the remaining acceptance criterion; or
- the current candidate adds a test but does not change the architecture.

The blockers section distinguishes `None observed` from `Not available`.
Absence of evidence is not a passing check.

## Create workflow

1. Confirm repository identity, visibility, default branch, and instructions.
2. Inspect branch/status/history and the canonical sources relevant to the
   intended work.
3. Inspect the live work tracker when available.
4. Copy the template and replace every angle-bracket token with evidence.
5. Populate one objective, exact success conditions, base/candidate/live state,
   review evidence, boundaries, and next work.
6. Remove irrelevant historical detail and verify privacy.
7. Validate structure and size. An unpopulated template is invalid.

## Reconcile or refresh workflow

1. Treat the prior file as a claim set, not authority.
2. Compare each mutable claim with repository and live evidence.
3. Replace completed objective/change prose; do not append a dated entry.
4. Preserve still-current blockers and decisions with their canonical links.
5. Recompute next work from the roadmap/issue dependency source.
6. Update review evidence after project checks finish.
7. Reconcile any parallel checkpoint edit semantically before presenting the
   pull request.

When evidence conflicts and cannot be resolved within scope, set `stale`, name
the reason, record the blocker, and stop before using the disputed next action.

## Compact workflow

Retain, in priority order:

1. objective and success conditions;
2. verified base/candidate/live distinctions;
3. current material changes and canonical owners;
4. exact validation, failures, limitations, and human gates;
5. blockers, unknowns, and next dependency-ready work;
6. minimum stable source pointers.

Remove logs, old completion lists, transcript excerpts, duplicated source
content, narrative about already superseded checkpoints, and facts easily
recovered from a stable link. If required state still cannot fit, move detail to
the proper canonical repository artifact and link it; do not weaken the v1
limit.

## Parallel pull-request workflow

One root file means parallel branches may both edit the same snapshot. Each
branch describes only its own candidate and lists known peers. Immediately
before PR presentation or update:

1. compare against the current target branch;
2. inspect overlapping continuity edits;
3. merge the true current objective, validation, blockers, and next action by
   evidence rather than concatenation;
4. rerun structural and project validation; and
5. block the handoff when the semantic result needs an owner decision.

CI may report a conflict or missing update. It cannot decide which free-form
claim is true or rewrite the file.
