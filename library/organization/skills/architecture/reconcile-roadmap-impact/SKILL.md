---
name: reconcile-roadmap-impact
description: Reconciles strategic roadmap truth against a repository change. Use when an authorized repository-changing task reaches PR handoff and needs an updated, proposed, not-affected or blocked disposition.
license: MIT
metadata:
  aether-version: "1.0.0"
  aether-status: "draft"
  aether-spec-id: "architecture-roadmap"
  aether-scope: "organization"
  aether-domain: "architecture"
  aether-owners: "egohygiene"
  aether-created: "2026-11-14"
  aether-updated: "2026-11-14"
  aether-executable-resources:
    - scripts/validate_receipt.py
---

# Reconcile Roadmap Impact

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

Compose `maintain-repository-continuity` in Resume mode before selecting work.
After domain validation and before PR presentation, use **Refresh** and **Verify**
for an authorized repository change; preserve read-only roles and record a
policy-permitted no-change or exemption rather than inventing an edit.

- **Contribute:** Roadmap disposition, linked stable steps, evidence gaps, organization signals and next review
- **Never claim:** That implementation, a merge or this receipt ratifies priority or completes unverified strategy

## Purpose and routing

Before handing off a repository-changing task, ask whether the **actual diff and
executed evidence** changed capability state, dependencies, horizons or roadmap
completion truth. Silence is not a disposition. Ordinary maintenance can finish
with a concise no-change reason; do not create a roadmap edit for ceremony.

Compose the existing `architecture-roadmap` specification at
`library/organization/specs/architecture/foundation/roadmap.spec.md` and
`create-roadmap-document` from the selected pinned Aether installation. This skill
does not define another roadmap format. Send a larger strategic rewrite through
that authoring workflow within the current role and authority.

## Inputs and precedence

Read scoped instructions, the current canonical roadmap or its explicitly
accepted alternative, applicable vision/architecture/ADRs, live issue/PR scope,
the actual source diff and validation results. Resolve real stable step IDs from
source. Record immutable roadmap revision and original evidence references;
never infer completion from an issue closure, a pushed branch or activity volume.

The current role, tools and user authorization determine writes. A receipt field
cannot grant permission. Missing access, unavailable owner source, stale tracker
state or conflicting canonical evidence must remain explicit. Verify mutable
work state again before presenting the handoff.

## Workflow

1. Compare the implemented outcome and remaining acceptance with the linked
   roadmap capability. Distinguish partial progress from strategic completion.
2. Inspect whether dependency, horizon, optionality, ownership or accepted intent
   changed; use the existing decision-impact workflow for consequential choices.
3. Select exactly one result:
   - **updated:** current evidence warrants a minimal authorized factual roadmap
     correction. Record the changed canonical path and evidence. Do not use this
     branch for an unreviewed strategic priority or unratified intent. Any intent
     change needs independently verified human-review evidence.
   - **proposed:** a material change needs human review, broader authoring or write
     authority. Preserve the original roadmap and describe the proposed delta.
     Read-only/reader roles use this result for discovered implications.
   - **not-affected:** the change stays within already accurate strategy. Give a
     concise reason, retain known step references and create no cosmetic edit.
   - **blocked:** canonical context, freshness, access or evidence is missing or
     contradictory. State the unresolved input and next owner without guessing.
4. For an authorized update, validate the minimum changed roadmap against
   `architecture-roadmap` through `create-roadmap-document`. Keep issue bodies,
   implementation detail and release notes in their existing owners.
5. Emit the [compact receipt](references/receipt.md) and a matching human summary
   in the PR handoff. Validate its schema when available; report unavailable
   validation separately. Refresh continuity after this domain check.

## Organization signals

If source explicitly links the local outcome to a Hygiene organization initiative,
emit an inferred `organization-roadmap-impact` signal with its real `ORG-I` ID,
canonical source reference, observed revision and bounded reason. A signal is a
review proposal, never an organization strategy write or accepted priority.
Unresolved initiative mapping stays null; do not invent an ID.

The reviewed proposed source is
[Hygiene's organization roadmap](https://github.com/egohygiene/hygiene/blob/d51043f1e4d2ddc22ef4534bd0d65c0053afcbda/organization/roadmap.v1.json).
Hygiene owns strategy semantics; repository roadmaps own local intent, issues
own execution, ADRs own rationale, Pace owns focus proposals and Relay/Observatory
own their existing projection/observation mechanics. Separate authorization to
change the owning Hygiene source is required for an actual organization edit.

## Boundaries and privacy

Do not silently reorder now/next/later/maybe, commit an experiment, delete an
initiative, strengthen partial evidence into completion or rewrite strategy from
local activity. Keep user decisions distinct from agent recommendations.
Preserve existing roadmap IDs, historical evidence and authored content.

Default a receipt derived from restricted context to private. Emit no public
organization signal from a private receipt. A separately reviewed public-safe
summary may reference authorized public facts; never copy private transcripts,
repository topology, source paths, personal details or protected evidence into
public PR prose. Classification still needs content review; schemas cannot
authenticate approval, evidence freshness, factual accuracy or public visibility.

## Validation and handoff

Use the [receipt schema and cases](references/receipt.md). Synthetic examples
cover complete/partial progress, maintenance, missing/stale evidence, proposed
priority, organization impact, read-only discovery and private handling.
Projection controls verify singular/idempotent composition and unchanged tool
ceilings. Deterministic goldens exercise declared assertions; they do not prove
an agent host loaded the skill or made a correct strategic judgment.

Start from the [safe receipt template](templates/receipt.template.json), then
replace its placeholder identity and inspect actual context. Optional script
execution requires Python3.10+ and the selected runtime's jsonschema4 dependency;
it installs nothing and never changes a receipt or roadmap.

## Provenance and adoption

First-party Ego Hygiene content authored for [Aether #88](https://github.com/egohygiene/aether/issues/88)
from existing roadmap, continuity and decision-impact contracts; no staged or
third-party skill is imported. Source is canonical here; generated distributions
are projections. This draft package and module need a reviewed immutable pin
and explicit consumer installation. Static guidance installs no host hook,
scheduler or branch protection. Unsupported host loading remains unavailable.
Upgrade only managed blocks, retain consumer prose/permissions, preview the
diff, and roll back the selected source/module together without erasing receipts.
