---
schema: aether.specification/v1
id: social-campaign-handoff
title: Review-gated social campaign handoff specification
kind: specification
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-08-29
updated: 2026-08-29
domain: marketing
tags:
  - social-media
  - campaign-handoff
  - human-approval
  - provenance
  - deterministic-builds
applies_to:
  - social-campaign-drafts
  - external-publisher-handoffs
depends_on: []
related: []
supersedes: []
source_files:
  - social-campaign-handoff.spec.md
---

# Review-gated social campaign handoff specification

## Purpose

This specification defines a deterministic handoff between approved Identity
artifacts, pinned Aether platform facts, human campaign intent, and a separately
authorized publishing adapter. It permits candidate drafting and reviewed
export. It does not authorize account access, scheduling, posting, advertising
spend, targeting, or analytics.

## Authority boundaries

- Identity owns approved brand assets, copy facts, links, attribution,
  provenance, and the social-surface projection that maps them.
- Aether owns the reusable social-surface fact contract and this handoff
  workflow.
- The user supplies campaign objective, audience, context, and candidate copy.
- A named human reviewer owns approval for export.
- An external adapter owns any later platform interaction under separate,
  explicit authorization.

No layer may silently assume another layer's authority.

## Required inputs

A draft compiler shall consume only:

1. an immutable `identity.social-surface-package/v1` artifact;
2. the exact local `aether.social-surface-catalog/v1` artifact named by that
   package's ID, version, and digest lock; and
3. a closed `aether.social-campaign-brief/v1` supplied by the user.

The compiler shall make no network request. The catalog shall be stable,
rights-approved, and release-included. Every selected Identity target shall
resolve to the same catalog record and preserve its constraints exactly.

## Packet states

The state machine is:

```text
draft -> reviewed -> approved-for-export -> published
   \         \               \                \
    +---------+---------------+----------------> superseded
```

- `draft` contains candidate copy and is not export-authorized.
- `reviewed` records human inspection but is still not export-authorized.
- `approved-for-export` requires a human approval record bound to the canonical
  digest of the exact reviewed packet. Candidate copy and claims become
  approved only through that transition.
- `published` is an observation imported from a separately authorized adapter.
  The Aether skill shall never create this transition.
- `superseded` names its replacement and cannot return to an active state.

Every transition appends an actor, time, previous state, new state, and reason.
History is append-only and shall begin with the null-to-draft creation event.

## Draft contents

Each packet shall record:

- stable packet ID and version;
- exact Identity schema, projection version, source digest, and package digest;
- exact catalog ID, version, normalized text digest, capture time, source URLs,
  freshness notice, and live-verification state;
- user-supplied objective, audience, and context with explicit source labels;
- selected channel and placement records with dimensions, media constraints,
  safe-zone state, verification, and provenance;
- approved Identity source asset path, digest, accessibility text, license,
  origin, copy/link selectors, and related approval IDs;
- candidate copy and claims, never represented as approved at draft time;
- required attribution and links;
- a review record, publishing checklist, export authorization, publication
  status, and lifecycle history.

Unknown surface constraints shall remain unknown or null. A packet shall never
invent dimensions, file limits, duration limits, safe-zone geometry, source
evidence, claims, attribution, or approvals.

## Review and export gate

Before approval for export, every required checklist item shall be completed
with evidence. The minimum checklist covers Identity integrity, catalog lock,
catalog freshness, candidate copy and claims, required links and attribution,
safe-zone handling, final creative inspection, and credential-free export.

An export approval shall contain the exact reviewed packet digest, decision,
reviewer, time, and evidence reference. Editing the packet after review changes
the digest and invalidates that approval.

An approved packet authorizes an immutable file handoff only. It does not
authorize a scheduler, platform account, or publication action.

## Publishing adapter boundary

Credentials, tokens, cookies, account identifiers intended for authentication,
or direct-publish instructions are prohibited in briefs and packets. Future
platform adapters shall be separate artifacts with their own authorization,
credential isolation, audit log, dry-run behavior, and revocation boundary.

A published packet is valid only when it preserves the prior export approval
and adds a receipt naming the adapter, authorization approval, platform event
ID, publication time, and immutable exported packet digest.

## Determinism and rollback

Canonical JSON serialization, stable ordering, explicit timestamps supplied by
the caller, and content digests make repeated operations reproducible. The
compiler shall never write over an input artifact.

Rollback does not erase history. A withdrawn or replaced packet transitions to
`superseded`, names the replacement, and remains available as evidence.

## Failure behavior

Validation shall fail closed for unsupported surfaces, stale or mismatched
catalog locks, incomplete Identity provenance, invented approved claims,
missing attribution, incomplete checklists, invalid transitions, embedded
credentials, direct-publish requests, or publication records without an
authorized external receipt.
