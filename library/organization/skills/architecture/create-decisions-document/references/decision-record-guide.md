# Decision record guide

Read the exact Hygiene policy, ratification and migration documents named by
[policy-selection.json](policy-selection.json). This guide applies those sources
to authoring; it does not create an alternative policy.

## Separate the evidence questions

| Question | Useful evidence | What it does not prove |
| --- | --- | --- |
| What changed? | Reachable commits, tags, merged PRs, releases | Original rationale or human disposition |
| Why was it chosen? | Contemporary ADR/proposal, issue discussion, explicit design review | Implementation or verification |
| Who disposed of it? | Explicit human disposition with identity, date and durable evidence URL | Merge alone is insufficient |
| Was it implemented? | Source/PR/release evidence tied to the decision | Acceptance or successful verification |
| Was it verified? | Named validation evidence at a specific revision | Broader correctness or approval |

Retain existing human-authored disposition and approval verbatim when preserving
an established record. Automated authors create new records as proposed even
when historical evidence is strong; present the evidence for human disposition.
A legacy accepted label without durable authority stays an unresolved migration
claim. Preserve it in the source inventory; do not silently relabel the old file
or manufacture a schema-valid approval object.

## Historical reconstruction

1. Establish authorized repository/visibility, current immutable revision and
   available history boundaries. Inspect existing ADRs/logs first. Missing or
   shallow history, inaccessible PRs and unavailable releases are evidence gaps.
2. Read reachable Git history and tags, merged PRs, issues, releases, architecture
   documents and existing records. Use immutable source/line links where possible;
   provider observations carry their inspection date. Do not run consumer code.
3. Group consequential choices by durable boundary, not by commit or issue count.
   Link multiple changes to one record where they implement the same decision.
4. Preserve IDs, prefixes, filenames, status claims, rationale, citations and
   historical blame links. Map inline extraction and aliases before edits.
   Collisions and ambiguous canonical sources require human resolution.
5. Record what contemporaneous evidence establishes. State missing rationale or
   alternatives as unknown. Current code can establish implementation but never
   supplies motives, approval or a historical choice date by inference.
6. Record the reconstruction date separately in a Markdown note after the seven
   required sections. Preserve a proven historical date; if none is proven, use
   the new record's date in front matter and explicitly label historical date
   unknown. Never add unregistered reconstruction metadata keys to the schema.
7. Keep new historical drafts proposed; use migration-only implementation unknown
   when evidence cannot establish delivery. Link proof for implemented or verified
   states. Preserve later corrections/outcomes as dated notes, not rewritten history.

Use [the migration map](../templates/MIGRATION.template.md). A map can document an
unresolved record without pretending that the repository has completed adoption.
Private sources and protected links stay inside their authorized audience.

## Proposed supersession

Create the replacement as proposed with the predecessor in `supersedes`, a new
unused ID and an index row. Preserve the old record's status/body and do not add
an effective replacement backlink while approval is pending. When a human
records the replacement's acceptance and the old record's superseded disposition,
verify both directions, authority evidence and absence of cycles with the owning
validator. An agent does not perform those lifecycle transitions autonomously.

The selected EgoLint validator supports this two-stage proposal. The older
Hygiene `tools/decisions.py decision-set` at the policy pin requires a reciprocal
backlink even before approval; report that compatibility finding if using that
helper. Do not alter old authority, invent a backlink, or accept a proposal to
make an older helper pass. Use the selected EgoLint/Relay boundary for the real
consumer replay, and retain any differing owner-validator results explicitly.

## Index and legacy migration

`docs/decisions/README.md` owns the canonical index, with one numeric-order row
per canonical record: ID, title, decision status, date and relative link.
`DECISIONS.md` becomes compatibility navigation only after a reviewed extraction
preserves its inline records and inbound links. Do not install an empty index or
pointer over existing history. Preserve historical ID widths/prefixes through
the policy's exception process; new records use unused `ADR-NNN` identifiers.
No exception or migration map grants missing human authority.

The policy reference is a version/full-commit reference, not copied policy prose.
An authorized policy upgrade revalidates existing records and preserves the old
pin in Git. Repository-owned ADRs and rationale are never managed output.

## PR handoff examples

```text
ADR-Ref: egohygiene/example#ADR-012
Operation: create; proposed; approval pending.
Evidence: source revisions and authoring validation linked in the PR.
```

```text
ADR-Ref: egohygiene/example#ADR-004
Operation: reference; implements the existing accepted boundary without a new choice.
```

```text
ADR-Ref: egohygiene/example#ADR-013
Operation: supersede; proposed replacement of ADR-004; old record preserved.
Human disposition and effective reciprocal lineage remain pending.
```

```text
ADR not required: this localized parser fix implements the existing input contract.
```

Repeat the classification against the completed diff before issue completion or
PR handoff. A late architectural change must not retain an earlier no-ADR claim.
Use real IDs in consumer work; the examples above are synthetic, not evidence.
