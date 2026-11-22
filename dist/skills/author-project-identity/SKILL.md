---
name: author-project-identity
description: Authors or updates consumer-owned project identity, collects real brand facts, prepares explicit v1 candidates and delegates checks to a pinned Identity implementation. Use when authoring, initializing, adopting or reviewing project identity; not for generic specification writing or automatic brand approval/publication.
license: MIT
compatibility: Use an immutable compatible Identity implementation for execution; its current embedded v1 validator requires Python 3.11+.
metadata:
  aether-version: "1.0.0"
  aether-status: "draft"
  aether-spec-id: "project-identity-authoring"
  aether-scope: "organization"
  aether-domain: "authoring"
  aether-owners: "egohygiene"
  aether-created: "2026-11-22"
  aether-updated: "2026-11-22"
  aether-executable-resources:
    - "scripts/verify_identity_source.py"
  aether-distribution-resources:
    - source: "library/organization/specs/authoring/project-identity-authoring.spec.md"
      destination: "references/project-identity-authoring.spec.md"
---

# Author Project Identity

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

Compose `maintain-repository-continuity` in **Resume** mode before selecting
repository work. After authorized source changes pass domain checks, compose
**Refresh** and **Verify** before PR handoff and include the reconciled root
`CONTINUITY.md`; record a policy-permitted no-change/exemption instead of an
invented edit. Check-only work stays read-only unless separately authorized.

- **Contribute:** Identity source choices, exact subjects/pins, applicability, actual validation evidence and remaining owner decisions.
- **Never claim:** Invented rights/approvals, producer support, comprehensive kit readiness, installation, publication or policy activation from a source pass.

## Resolve the task and authority

Follow `project-identity-authoring`; its packaged copy is
`references/project-identity-authoring.spec.md`. Read the exact Identity sources
identified by [the source lock](references/identity-source-lock.json) when
available through authorized preparation. Missing references stay unavailable;
do not fetch or install them implicitly. Identity owns field/schema semantics;
this skill owns the agent procedure, not a replacement validator.

Inspect local instructions, existing `.identity/`, selected output roots and
allowed operations. Distinguish absent, v0-only and v1 source. Collect existing
facts, profile choices, masters, rights, reviewer evidence and tool/runtime pins.
Keep canonical intent, candidates and generated output separate.

## Workflow

1. Resolve the actual Identity implementation and matching scripts/schemas/
   profile versions using [CLI/capability guidance](references/identity-cli-and-capabilities.md).
   A schema ID, package version or mutable branch is not compatibility proof.
2. Interview the owner in small batches using the optional
   [intake worksheet](templates/OWNER_INTAKE.template.md). Reuse known answers; compute byte
   hashes mechanically. Preserve unknown creator/reference/license/reviewer
   facts instead of borrowing approvals or inferring rights from code licenses.
3. Select profiles for real consumer surfaces. Propose optional material only
   for a concrete need; distinguish a local token baseline from an approved
   organization default. Record decisions against exact subjects and evidence.
4. Prepare the authorized review candidate through explicit `identity v1-init`
   or the supported manual route. `identity init` is legacy v0. Never silently
   migrate, overwrite existing source, promote candidates or invent approvals.
5. Delegate source validation to the matching authoritative validator. Preserve
   structured diagnostics, actual command/exit and the source/tool revision.
   An incomplete starter remains incomplete; do not claim `v1-validate` exists.
6. Separately establish selected producer support. When generation is authorized,
   generate only the selected outputs through documented publication boundaries.
   For checking, use read-only verification; never regenerate or recover as a fix.
7. Keep source validity, producer capability, selected-output freshness and
   complete public-kit readiness distinct. Do not rename unsupported material,
   strip its governance or classify arbitrary stderr/nonzero exit as drift.
8. For updates, preserve old source/pins/approvals and review changed subjects,
   selected output differences and rollback together. Validate the actual new
   candidate rather than relabeling old execution evidence.
9. Apply [the validation checklist](references/validation-checklist.md). Report
   exact changes, prepared/checked/generated/verified scope, actual outcomes,
   missing facts, unsupported/unrun checks and the next owner/action.

## Boundaries and completion

Source and output checks are read-only. Tool installation, network acquisition,
canonical adoption, recovery, publication and external delivery are separate
operations under existing authorization; the skill grants none implicitly.
Keep private payloads, transcripts and credentials out of public source/reports.
Passing checks do not create human approval or accept an ADR.

Return a reviewable candidate or evidence-backed update and truthful check
results. Missing runtime or references remain blocked/unavailable; unresolved
facts stay explicit. Keep the skill draft until its actual maturity gates pass.
Do not claim `gh skill` support from the existence/version of `gh`, and do not
publish a skill, Rust binary, release or site without the applicable reviewed
publication action. This is first-party Aether procedure; Identity remains the
domain implementation and each consumer retains its own creative authority.
