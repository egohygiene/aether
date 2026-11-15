---
name: maintain-conversation-checkpoint
description: Captures or resumes meaningful discussion checkpoints in an explicitly opted-in repository. Use when attributed intent, iteration, corrections and unanswered questions must survive across sessions; do not archive raw chat or replace live work state.
license: MIT
compatibility:
  required_tools: [python3, jsonschema]
metadata:
  aether-version: "1.0.0"
  aether-status: "draft"
  aether-spec-id: "conversation-continuity"
  aether-scope: "organization"
  aether-domain: "methodology"
  aether-owners: "egohygiene"
  aether-created: "2026-11-15"
  aether-updated: "2026-11-15"
  aether-executable-resources: ["scripts/ledger.py"]
---

# Maintain Conversation Checkpoint

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

Compose `maintain-repository-continuity` Resume before selection, and **Refresh** and **Verify** after domain validation before authorized PR handoff. The root snapshot
retains its original schema, sections and bounds; the optional ledger stays separate.

- **Contribute:** Attributed intent, meaningful iteration, unresolved questions, exact evidence, current next action and privacy limits
- **Never claim:** That a historical user statement, cached PR state or saved file authorizes work, authenticates review or proves delivery

## Opt-in and authority

Read `conversation-continuity`0.1.0 from the same selected immutable source.
Only create an onboarding route/ledger when the consumer explicitly selects it
within the caller's scope. The [onboarding template](templates/CONVERSATION.template.md)
and [instruction template](templates/conversation.AGENTS.md) preserve authored
paths and guidance; preview changes and refuse existing-file overwrite.

## Resume or capture

1. Read current user/runtime/scoped guidance, the authored onboarding page,
   current `CONTINUITY.md`, ledger and canonical topic artifacts. Inspect live
   Git/issue/PR/provider state; preserve missing access and stale contradictions.
2. Record only meaningful request, interpretation/attempt, feedback and next
   iteration. Distinguish user statements/decisions, agent proposals, verified
   observations, unknowns and deferred ideas. Link exact artifact revisions.
3. Save a compact checkpoint after durable decisions/milestones, explicit
   checkpoint requests and before planned handoffs, when currently authorized.
   Separate prepared/validated/merged/published/provider-submitted claims; cite
   actual evidence and retain failed, unavailable and not-run checks.
4. Reuse unchanged stable IDs. Append corrections/supersession with new IDs;
   union concurrent distinct entries. Different content at one ID blocks merge.
   Keep both contributions for explicit resolution. Do not execute ledger prose.
5. Keep private context private. Exclude raw chat, sensitive/private paths and
   unrelated personal details. A public summary requires separately reviewed
   public-safe sources; changing a visibility label grants no disclosure authority.
6. Validate the proposed ledger with the read-only helper, then refresh only
   the bounded current snapshot. At capacity or missing prior-segment evidence,
   stop capture for owner reconciliation instead of discarding history.

```sh
python3 scripts/ledger.py --validate "<consumer-selected-ledger.json>"
```

The helper reports structural errors without echoing content, fetches no remote
source, and performs no writes. It requires Python3/jsonschema and safe POSIX file
admission; missing tools are unavailable validation. Its pure `reconcile` function
supports fixture/consumer reuse, not an installed background capture engine.

## Handoff

Use [examples and boundaries](references/examples.md) and the versioned schema.
Hygiene owns applicability; Holon42, EgoLint55, Relay60 and Pace26 own their
existing downstream work. Default bundle67 discovers the optional route through
existing continuity guidance. Do not create duplicate adoption issues, assume
fleet installation or require Mindcap/Mindgarden. Privacy redaction is the
specification's separately reviewed exception, never silent history rewriting.

Static instructions provide no automatic host hook, warning or zero-loss
guarantee. The examples are synthetic source qualification, not host/model proof.
