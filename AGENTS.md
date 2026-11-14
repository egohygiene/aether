# Aether agent guidance

Read this file before changing Aether. Canonical source is under
`library/organization/` and `catalog/`; `.staging/` and `dist/` are derived or
migration evidence, not source.

## Release convention

Every active Ego Hygiene repository follows the versioned
[`repository-release`](library/organization/specs/release/repository-release.spec.md)
contract. Its local declaration is `.egohygiene/release.json`; its root
`CHANGELOG.md` retains an exact `## [Unreleased]` section.

Before changing release behavior, inspect the declaration, version authority,
changelog, existing immutable tags, and repository-owned release workflow.
Use `release:plan`, `release:prepare`, and `release:verify` to make a reviewed
candidate. `release:publish` is an explicit handoff only: do not create tags,
publish packages, deploy sites, use registry credentials, or overwrite release
assets unless the user separately authorizes that exact external action.

Commit messages may inform a semantic-version recommendation, but the reviewed
release plan and declared version authority decide the version. Follow the
shared Conventional Commit work in `egohygiene/egohygiene#284` without letting
it silently rewrite a release.

## Aether boundaries

Aether owns provider-neutral specifications, schemas, skills, and agent
guidance. Relay owns reusable immutable execution; Hygiene owns applicability
policy; Egolint owns conformance validation; Pace observes adoption before it
proposes remediation. Keep provider credentials and delivery adapters in their
consumer repository.

## Issue authoring

For Aether issue authoring, explicitly read the
[`github-issue-authoring` skill](library/organization/skills/authoring/github-issue-authoring/SKILL.md)
and its [canonical-title guide](library/organization/skills/authoring/github-issue-authoring/references/canonical-issue-titles.md).
This repository selects that guide's pinned candidate contract in observe mode
for this pilot. Local proposals are not proof of provider label availability or
enforcement. The organization repository's instructions do not inherit here
automatically; this local pointer makes discovery explicit. Preserve scoped
instructions and existing role permissions.

## Current navigation and unresolved decisions

[README](README.md) starts the human path; [META](META.md) and
[ARCHITECTURE](ARCHITECTURE.md) map source ownership. [Issue105](https://github.com/egohygiene/aether/issues/105)
is the tactical ledger; [ROADMAP](ROADMAP.md) preserves strategic IDs and
[CONTINUITY](CONTINUITY.md) records the current operational checkpoint.

[Proposed ADR-0009](docs/decisions/ADR-0009-generated-evidence-and-local-validation.md)
exposes the historical ADR-0002/ADR-0006 conflict with tracked generated output
and local workflow callers. Preserve historical decisions; a factual correction,
merge, passing check or this proposal does not supply human disposition.

Run the relevant deterministic validation and regenerate `dist/` and the
first-party catalog after changing canonical source.

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

<!-- BEGIN AETHER WORKER-STRATEGY -->
<!-- aether-instruction {"id":"worker-strategy","version":"1.0.0","status":"draft","skill":"execute-issue-checkpoint","spec":"worker-strategy","spec_version":"0.2.0"} -->
## Bounded issue execution

For authorized repository issue work, compose `execute-issue-checkpoint` with
the selected `worker-strategy`, continuity, local-validation and roadmap-impact
contracts. Keep small issues unsplit; preserve a larger parent with the smallest
useful checkpoints; reuse existing stable checkpoint/PR identities. Parent links
group scope and do not create false blockers. Preserve all original acceptance.

Execute one bounded checkpoint at a time within the caller's authorized batch.
Save meaningful progress and the exact resume action before planned handoffs;
commit/push/update the existing draft PR only when current authority permits.
Reverify actual branch, working tree, issue/PR and checks on fresh-session resume.
Prepared, validated, review-ready, merged and delivered remain separate; retain
failed/unrun/unavailable checks and parent obligations. Read-only roles gain no
writes. Missing access, unpushed work and abrupt-loss limits stay explicit.

This draft module supplies guidance, not a scheduler, installed recovery hook,
guaranteed context warning, zero-loss promise or fleet-adoption evidence.
<!-- END AETHER WORKER-STRATEGY -->
