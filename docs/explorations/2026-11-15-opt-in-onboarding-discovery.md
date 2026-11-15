---
id: exp-opt-in-onboarding-discovery
title: Explore opt-in onboarding discovery placement
status: draft
authority: exploratory-only
visibility: public
created: '2026-11-15'
updated: '2026-11-15'
sources:
- reference: library/organization/specs/methodology/conversation-continuity.spec.md
  visibility: public
- reference: docs/decisions/ADR-0012-optional-conversation-evidence-extension.md
  visibility: public
- reference: https://github.com/egohygiene/aether/issues/103
  visibility: public
related:
- https://github.com/egohygiene/aether/pull/133
next_step: null
extensions:
  canary_review:
    by: Codex
    date: '2026-11-15'
    scope: Authorship, public source provenance, tentative authority and no automatic
      promotion; not human architectural acceptance.
---

# Explore opt-in onboarding discovery placement

This is an explicitly selected Aether authoring canary, not a required repository
surface. No architecture is accepted and no implementation task is created.

## Context and sources

Observation: [the optional conversation extension](../../library/organization/specs/methodology/conversation-continuity.spec.md)
uses authored scoped guidance to discover onboarding, current state and discussion
evidence. [ADR-0012](../decisions/ADR-0012-optional-conversation-evidence-extension.md)
remains proposed with no human approval. Source integration in PR133 did not
install a host hook or opt a consumer into a live ledger.

## Ideas and attribution

Agent hypothesis: a consumer might discover its optional onboarding through a
short README link as well as scoped AGENTS guidance. Another possibility is to
keep one local AGENTS route and avoid a second navigation link. This note records
an agent suggestion, not a user choice or accepted architectural requirement.
The user-authorized source task permits this bounded authoring canary; it supplies
no organization adoption or publication decision.

## Alternatives and uncertainty

- Keep one authored AGENTS route: less navigation to maintain, but humans may miss it.
- Add a README link where useful: easier human discovery, but another source pointer
  needs review after paths move.
- Rely on a future garden index: potentially useful discovery, currently unqualified
  here and never a prerequisite for the minimal local workflow.

No comparative usefulness, model effectiveness or maintenance-cost measurement
has been performed. Applicability to other repositories is unknown.

## Relationships

Canonical source stays in this repository. A future reviewed visibility-safe
Mindgarden `/garden/` view may link this stable identity and immutable revision;
it must not become a second authored copy or infer an approved decision. No
Mindgarden ingestion or new backlog item is created. Accepted ADRs and current
consumer instructions retain authority; this note supersedes neither.

## Next step

Parked; no action, deadline or follow-up issue is required. A consumer may later
propose a comparison under its own scope, preserving the current opt-in boundary.

## Revisions

2026-11-15: initial public-source canary; Codex reviewed the actual note for source
links, attribution, privacy and tentative status. This is not human ratification.

