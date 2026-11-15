---
schema: aether.specification/v1
id: exploration-note-authoring
title: Optional Repository Exploration Note Authoring
kind: specification
version: 0.1.0
status: draft
owners: [egohygiene]
created: 2026-11-15
updated: 2026-11-15
domain: authoring
tags: [exploration, notes, provenance, privacy]
applies_to: [opt-in-repository-exploration-notes]
depends_on: [architecture-epistemology, repository-continuity]
related: [architecture-decisions, repository-journal, conversation-continuity]
supersedes: []
source_files: [exploration-note.spec.md]
---

# Optional Repository Exploration Note Authoring

## Purpose and boundary

An Exploration Note preserves a worthwhile tentative idea before it becomes an
RFC, spike, ADR, specification or issue. It is a consumer-authored Markdown
document output, not a new first-party catalog kind, organization lifecycle
policy, knowledge ontology, ingestion engine or implementation commitment.
Use the existing specification/skill catalog and portable package conventions.

The default suggestion is `docs/explorations/YYYY-MM-DD-short-slug.md`; a consumer
may select another supported authored location or existing layout. Create no
empty directories or notes unless that repository opts in within current user
authority. Do not migrate existing notes, move canonical storage to `/garden/`,
or install the convention across the fleet.

## Minimal editable format

The small optional template uses an identity/title, existing `draft` document
status, public/private classification, and `authority: exploratory-only`.
Created/updated dates may be null when unknown; never invent them. Sources carry
stable references and visibility; related links point to authoritative artifacts.
Optional consumer extensions remain authored data, not new shared semantics.

Suggested sections are Context and sources; Ideas and attribution; Alternatives
and uncertainty; Relationships; Next step; and Revisions. A consumer can omit an
inapplicable section or adapt headings. Keep enough information to distinguish:

- observation: what source/evidence actually establishes;
- user direction: an attributed request or preference;
- agent suggestion/hypothesis: an explicitly tentative interpretation;
- human-approved decision: a reference to independently verified canonical ADR
  or domain authority, never authority supplied by this note;
- actionable task: an already authorized issue/work reference, not an automatic
  promotion from brainstorming.

Include context, competing approaches, assumptions, tradeoffs, questions and
experiments as useful. A null `next_step` means explicitly parked/no action;
parking has no deadline and requires no follow-up issue. Keep status draft after
parking or linking a downstream artifact. Existing `superseded` status requires
an explicit replacement relationship, preserving the old identity and provenance.
These are authoring conventions, not a new global lifecycle state machine.

## Revision, duplication and graduation

Revise in Git with a concise Revisions note, source/correction links and the same
stable identity. Preserve earlier uncertainty rather than retroactively claiming
the idea was accepted. Link supersession, split-from, merged-from and resulting
issues/ADRs/specifications in Relationships; retain original IDs and source links.
Never merge/split/delete authored notes automatically. Inspect stable identities
and source/topic overlap before creating a duplicate; different filenames do not
make the same identity a different idea. A suspected duplicate is a proposal to
link/reconcile, not permission to overwrite either contribution.

The thin helper creates only a caller-selected new file in an existing approved
directory. An identical repeat is unchanged. Any differing existing content,
symlink or special file is refused. It offers no revise, archive, promotion or
remote-write command. Authored revisions use the normal authorized editing/review
workflow; template reruns never overwrite those edits.

## Composition and ownership

Aether78 retains free-form brain-dump triage and optional issue promotion;
repository-journal records historical repository evidence; conversation-continuity
preserves meaningful interaction/resume context. Link these when applicable
without copying their records into the note. `architecture-decisions` and the
accepted Hygiene ADR policy continue to govern actual architectural decisions.

Mindgarden may later discover a reviewed visibility-safe note as a linked garden
candidate. Its index/projection must retain the repository note as canonical and
use current owner provenance/review/synapse contracts. Mindgarden39 is closed
not-planned (observed 2026-11-15), so it is historical context, not an active
dependency or authorization to build a competing skeleton/ontology here.

Holon owns separate opt-in scaffold materialization with pinned Aether inputs,
preview/conflict/upgrade/rollback and authored-content preservation. Hygiene
decides applicability; Pace may later propose reviewed adoption. Existing
backlog owners keep their work; no downstream issue or fleet mutation is created
without evidence of distinct uncovered implementation work. `/garden/` discovery,
ingestion, search and public publishing remain future owner work.

## Privacy and evidence

Default privately derived ideas to private. Exclude raw chat, credentials,
personal/financial/employment details, private paths and sensitive source text.
Public fixtures are entirely synthetic or use actual authorized public repository
facts. Explicitly private sources cannot enter a public note; labels cannot
detect sensitive prose or authenticate declassification. Review before sharing.

Missing sources remain partial/unknown. A structural/local-reference check never
proves a claim true, an external link current, an ADR accepted or a user decision
authenticated. A proposed alternative conflicting with accepted architecture
stays an exploration and identifies that conflict; it cannot override the source.

## Qualification

Exercise create, authored revision, park, graduate/link, duplicate identity,
conflicting decision, missing source and public/private behavior. Demonstrate
idempotent creation and refusal to overwrite an authored revision. A reviewed
opt-in repository canary remains repository-owned and exploratory, with future
garden discovery only by reference. Record actual checks and unavailable tooling;
passing fixtures do not establish adoption, usefulness or model effectiveness.
