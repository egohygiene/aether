<!-- BEGIN AETHER ROADMAP-IMPACT -->
<!-- aether-instruction {"id":"roadmap-impact","version":"1.0.0","status":"draft","skill":"reconcile-roadmap-impact","contract":"aether.roadmap-impact/v1","inherits":[{"contract":"egohygiene.organization-roadmap/v1","contract_version":"1.0.0-alpha.1","revision":"d51043f1e4d2ddc22ef4534bd0d65c0053afcbda","source_url":"https://github.com/egohygiene/hygiene/blob/d51043f1e4d2ddc22ef4534bd0d65c0053afcbda/docs/ecosystem/ORGANIZATION_ROADMAP.md","status":"proposed"}]} -->
## Roadmap-impact checkpoint

After domain validation and before PR handoff, compose
`reconcile-roadmap-impact` with `architecture-roadmap` and
`create-roadmap-document`. Inspect current canonical roadmap, real step IDs,
actual diff and executed evidence; preserve missing/stale/conflicting inputs.
Emit exactly one disposition: `updated`, `proposed`, `not-affected` or `blocked`,
with a concise reason and evidence under `aether.roadmap-impact/v1`. Silence is
not completion. A no-change result needs no ceremonial edit.

Make only authorized minimal factual updates. Read-only roles never mutate the
roadmap; they may propose an impact. Human-governed horizon, optionality,
priority and strategic intent remain proposals until reviewed. Partial work,
issue closure, a pushed branch, passing checks or this receipt do not establish
strategic completion or supply human approval.

Emit an inferred typed `organization-roadmap-impact` signal when applicable;
local repository authority does not permit writing Hygiene's organization
strategy. Preserve private context and emit no public signal from a private
receipt. If source, skill loading or validation is unavailable, record the
blocked check and next owner. Refresh continuity after domain reconciliation.

This draft shared module is static guidance, not an installed or enforced host
hook. Preserve consumer prose, scoped instructions and tool permissions.
<!-- END AETHER ROADMAP-IMPACT -->
