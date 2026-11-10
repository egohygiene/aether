---
name: audit-repository
description: Audits an explicitly scoped repository or public organization roster through composable profiles, preserving evidence, uncertainty, strengths and suggestion-only follow-up in immutable reports and typed sidecars.
license: MIT
metadata:
  aether-version: "1.2.0"
  aether-status: "draft"
  aether-spec-id: "repository-audit-data"
  aether-scope: "organization"
  aether-domain: "quality"
  aether-owners: "egohygiene"
  aether-created: "2026-08-02"
  aether-updated: "2026-11-09"
  aether-distribution-resources:
    - source: "catalog/schemas/aether.audit-profile-registry.v1.schema.json"
      destination: "references/aether.audit-profile-registry.v1.schema.json"
    - source: "catalog/schemas/aether.repository-audit-report.v1.schema.json"
      destination: "references/aether.repository-audit-report.v1.schema.json"
---

# Audit Repository

<!-- aether-continuity-disposition: read-only -->

## Repository continuity composition

For repository-scoped work, compose `maintain-repository-continuity` in
**Resume** mode before selecting work. This skill is continuity read-only: do
not create, refresh, or otherwise mutate `CONTINUITY.md` unless a separate
authorized repository-changing workflow takes ownership of that handoff.

- **Contribute:** Audit scope, observed findings, confidence, evidence gaps, and executed checks
- **Never claim:** Permission to modify CONTINUITY.md, apply fixes, or convert recommendations into completed work

## Purpose

Execute one reusable procedure governed by approved `auditor` 2.0.0. The draft
`repository-audit-data` 1.0.0 extension supplies composable profile/data
interfaces and depends on that approved foundation; it does not change its
human lifecycle. This skill remains **draft** pending deterministic and host
qualification under [Aether #86](https://github.com/egohygiene/aether/issues/86).

Primary question:

> What does observable repository evidence show about quality, alignment, risk, and strengths?

## Required Inputs

Resolve:

- governing specification and version
- current source or repository state
- scope and constraints
- upstream architecture or evidence
- output location
- validation expectations
- unresolved decisions
- explicit profile IDs/versions or a named composite from the exact reviewed
  [profile registry](references/audit-profiles.v1.json)
- for organization scope, an explicit authorized repository/revision roster
  and the applicable owner public-admission evidence

Missing evidence must remain visible.

## Workflow

1. Resolve request, recorded defaults, scope and read-only constraints. Select
   one profile, several explicit profiles, or `holistic`; use the exact registry
   resolver and retain both requested and resolved ID/version references.
   Experimental opportunities require explicit additional selection.
2. Authenticate the supplied roster through its owner admission boundary before
   reading excluded/private findings, identities, counts or hashes. Do not
   discover an organization or silently expand the selected repository scope.
3. Inspect repository context in the approved discovery order, then existing
   audits. Record exact represented revisions, included/excluded/inspected/
   uninspected scope, tools and actual limitations. Missing context remains
   unknown, blocked or unsupported rather than guessed applicability.
4. Gather evidence within scope. Read-only diagnostics require actual host and
   user authorization; a read/search-only agent can consume supplied captured
   evidence or hand off requested diagnostics, not acquire execute authority.
5. Follow each leaf profile's focus, required evidence and exclusions using
   this same procedure. Label every finding with its original leaf ID/version
   and evidence classification; overlapping results do not erase origins.
6. Assign the approved classification, severity, confidence, status, effort and
   impact. Keep defects, policy observations, opportunities, experiments and
   strengths distinct. An absent feature or speculative recommendation is not
   a confirmed failure. State missing evidence for low-confidence claims.
7. Preserve explicit profile/run completion, uninspected scope, continuation,
   stale evidence, uncertain history and known prior-audit links. No missing
   record, later capture or changed title resolves an older finding.
8. Propose bounded validation and candidate issues as suggestions. Do not
   create issues, apply remediation, accept risk, or ratify architecture.
9. Return the canonical report and sidecar candidates to an explicitly
   authorized output writer. If this execution has new-report write authority,
   write only new unique report/sidecar files, never source/history. Bind actual
   Markdown bytes and validate the same authored model through the exact
   [machine interface](references/audit-data-contract.md). Record every unrun
   validation and downstream qualification gap.

## Output Contract

Primary output:

    audits/{audit-name}-{utc-timestamp}.md

The typed sidecar uses the same filename stem with `.json`, exact machine
schema/profile versions, canonical Markdown path/hash and source provenance.
It is a projection from the report's authored finding model, not a separately
invented assessment or prose scraper. Record assumptions, evidence gaps,
validation state, unresolved questions, positive observations or their absence,
and separately authorized downstream actions.

## Constraints

- Follow the governing specification.
- Preserve provenance and uncertainty.
- Do not invent authority, evidence, or current behavior.
- Do not silently expand scope.
- Do not claim completion when required validation is missing.
- Keep proposed downstream work separate from authorized execution.
- Complete scope is not pass, conformance, deployment or human acceptance.
- Preserve original profile/evidence classification and independent finding
  history; experiments remain informational and recommendation-only.
- Exclude credentials, private conversation, raw logs and machine-local paths.

## Completion Criteria

- [ ] Governing specification is resolved.
- [ ] Exact requested/resolved profile versions and registry digest are retained.
- [ ] Scope and constraints are explicit.
- [ ] Required evidence was inspected.
- [ ] New outputs were written through an authorized writer or returned as
  candidates with the missing host capability explicit.
- [ ] Validation was executed or its absence documented.
- [ ] Open questions and authorization needs are visible.

## Staged reconciliation and remaining maturity

A staged candidate at `.staging/skills/repository-audit/` covers similar
ground under the name `repository-audit`. The canonical skill is named
`audit-repository` and is governed by the `auditor` specification.

The [source reconciliation](references/staged-reconciliation.md) records the
meaningful staged/canonical delta under Aether #86/#68. It retains observed
diagnostics, current prior-audit checks, strengths, bounded backlog and partial
reporting while rejecting monolith paths and staged agent edit/execute tools.
Historical staged files remain migration evidence; none is promoted or deleted.
Single/multiple/holistic/experimental profile fixtures, malformed/stale/partial/
blocked/not-applicable cases, dependency closure and actual host/discovery
qualification remain unexecuted. Source reconciliation or a version bump does
not promote this draft skill.
