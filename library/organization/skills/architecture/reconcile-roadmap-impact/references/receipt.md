# Roadmap-impact receipt

Output identity: `aether.roadmap-impact/v1`, version `1.0.0`, draft.
The canonical [portable JSON Schema](receipt.schema.json)
validates a handoff record, not roadmap strategy or authority. The current source
and permissions must be inspected independently. Preserve original evidence
clocks; do not call stale context current because the receipt is new.

Required fields describe the repository, visibility, actual role ceiling,
disposition, concise reason, materiality/intent change, canonical roadmap
path/revision/availability, known steps, changed paths, proposed changes,
evidence and optional organization signals. Paths are relative; source revisions
are full immutable commits or explicit null when blocked.

| Disposition | Required meaning |
| --- | --- |
| `updated` | Reader-writer role, material factual change, current roadmap, evidence, exact changed roadmap path; an intent delta additionally needs independently verified human-review evidence. |
| `proposed` | Material or unresolved impact, a concrete proposal, no changed roadmap path; read-only roles remain nonmutating. |
| `not-affected` | Nonmaterial impact, a concise reason and no roadmap edits/proposals. |
| `blocked` | Missing, stale, inaccessible or conflicting roadmap input; unknown materiality and no fabricated edit. |

`changed_paths` records only roadmap mutations in this receipt; it is not the
whole PR file inventory. A role label is descriptive and cannot grant rights.
Evidence references are inspectable source/check/work URLs or repository paths;
schema success does not establish that a claimed check actually passed.

Every organization signal has type `organization-roadmap-impact`, owner
`egohygiene/hygiene`, canonical source `organization/roadmap.v1.json`, a real
initiative ID or explicit null, proposed `evidences`, `blocks`, `depends-on` or
`informs` relation, original source reference, bounded reason and assertion
`inferred`. Private receipts have no public organization signals. A separate
authorized Hygiene workflow decides whether to apply the proposal.

Human rendering can be three lines, plus a typed organization signal when needed:

```text
Roadmap impact: not-affected
Roadmap step: AET-Q07
Reason: bounded maintenance within an already-active capability; release acceptance is unchanged.
```

The [synthetic case inventory](../evals/fixtures/cases.json) supplies explicit
inputs and receipts; deterministic checks validate schema branches, role
ceilings and module projections. Read the skill for judgment, unavailable
evidence, privacy, upgrade and recovery limitations.

The portable schema is byte-identical to the canonical catalog schema, checked during Aether validation. When the selected runtime provides jsonschema, run `python3 scripts/validate_receipt.py RECEIPT.json` from the skill directory. The script validates shape and exact changed-roadmap-path equality; it authenticates no source or authorization and changes no file. Otherwise report schema execution unavailable without inventing a pass.
