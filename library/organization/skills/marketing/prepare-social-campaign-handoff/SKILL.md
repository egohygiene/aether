---
name: prepare-social-campaign-handoff
description: Prepares and reviews deterministic social campaign handoff packets from approved Identity social artifacts and a pinned Aether catalog. Use when platform-specific candidate copy and creative inputs need a human approval gate before export; do not use for posting, scheduling, account access, ad buying, or analytics.
license: MIT
compatibility:
  required_tools:
    - python3
metadata:
  aether-version: "1.0.0"
  aether-status: "experimental"
  aether-spec-id: "social-campaign-handoff"
  aether-scope: "organization"
  aether-domain: "marketing"
  aether-owners: "egohygiene"
  aether-created: "2026-08-29"
  aether-updated: "2026-08-29"
  aether-executable-resources:
    - "scripts/campaign-handoff.py"
  aether-distribution-resources:
    - source: "catalog/schemas/aether.social-campaign-handoff.v1.schema.json"
      destination: "references/aether.social-campaign-handoff.v1.schema.json"
---

# Prepare a social campaign handoff

Build a reviewable packet without becoming a publisher or a second source of
brand/platform truth.

## Inputs

Require all three local inputs:

- an approved `identity.social-surface-package/v1`;
- the exact `aether.social-surface-catalog/v1` locked by that package; and
- a user-supplied campaign brief based on
  [campaign-brief.template.json](templates/campaign-brief.template.json).

Do not request or accept platform credentials, tokens, cookies, scheduler
secrets, direct-post instructions, or ad-spend authority. Do not fetch current
platform requirements while compiling.

## Prepare

```bash
python3 scripts/campaign-handoff.py prepare \
  --identity-package "path/to/social-surfaces.json" \
  --catalog "path/to/catalog.v1.json" \
  --brief "path/to/campaign-brief.json" \
  --output "path/to/campaign-handoff.json"
```

Preparation verifies the Identity and catalog locks, exact selected surfaces,
rights/release state, provenance, and closed brief. It emits only `draft`
copy/claims and preserves unknown constraints and freshness requirements.

## Review lifecycle

Use the deterministic commands in
[review-and-export-safety.md](references/review-and-export-safety.md). The
allowed skill-owned progression is:

`draft -> reviewed -> approved-for-export`

Approval requires every required checklist item plus a human approval record
whose digest matches the exact reviewed packet. The tool may also supersede a
packet. It shall refuse a transition to `published`.

A platform or scheduler adapter may later append a published receipt under its
own explicit authorization. That adapter is outside this skill.

## Interpret and hand off

- Preserve dimensions, media limits, safe-zone state, source evidence, and
  null/unknown values exactly.
- Keep user objective, audience, context, candidate copy, and claims labeled by
  source and review status.
- Do not call a draft or reviewed packet approved.
- Treat `approved-for-export` as authorization to hand off an immutable file,
  not authorization to publish it.
- Re-run validation immediately before handoff.

Read [campaign-handoff-contract.md](references/campaign-handoff-contract.md)
when authoring a brief, integrating a consumer, or investigating validation.
