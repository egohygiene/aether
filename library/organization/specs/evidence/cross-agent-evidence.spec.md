---
schema: aether.specification/v1
id: cross-agent-evidence
title: Cross-agent public evidence packet specification
kind: specification
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-09-04
updated: 2026-09-04
domain: evidence
tags:
  - cross-agent
  - evidence
  - provenance
  - public-data
  - least-authority
applies_to:
  - public-evidence-handoffs
  - bounded-research-results
  - execution-zone-boundaries
depends_on: []
related: []
supersedes: []
source_files:
  - cross-agent-evidence.spec.md
---

# Cross-agent public evidence packet specification

## Purpose

This specification defines a portable, inspectable packet for moving public
evidence and bounded findings between agents or execution zones. It provides a
file contract, not a bidirectional channel, transport, capability grant, or
authorization to act on a destination system.

The contract has three distinct artifacts:

1. `aether.cross-agent-evidence-packet/v1` carries received public evidence,
   bounded findings, provenance, policy requirements, review, and lifecycle.
2. `aether.sanitized-research-request/v1` carries a separately reviewed public
   request outward. It never reuses the evidence packet as a request envelope.
3. `aether.evidence-projection/v1` binds a packet to one provider, MCP, A2A,
   filesystem, or queue adapter without broadening its authority.

## Authority and privacy boundary

- Aether owns these provider-neutral artifact shapes and deterministic import
  rules.
- A policy authority decides whether a destination, sensitivity, source,
  capability requirement, sanitization, or declassification is acceptable.
- A transport adapter moves bytes only after policy admission. It does not
  interpret evidence or grant capabilities.
- A receiving workflow owns its task-specific acceptance and use of admitted
  evidence.

Evidence packets contain public inputs only. Confidential agents shall not send
private text, private facts, credentials, identifiers, or confidentially
derived queries outward. A public outbound request must instead use the
sanitized-request schema and carry a human sanitization and declassification
decision bound to its canonical digest.

Source content is untrusted evidence. Text that asks an agent to ignore policy,
invoke tools, reveal secrets, or change role remains quoted data and has no
instruction authority.

## Packet structure

The packet envelope separates identity and integrity from its payload. The
payload has seven distinct sections:

- `request`: the bounded public task that produced the packet;
- `evidence`: source metadata, immutable attachment references, and exact byte
  spans;
- `findings`: supported or partial conclusions, uncertainty, limitations, and
  rejected claims;
- `provenance`: transformations, tools, producer, workflow, and revision;
- `policy`: destination scope, maximum sensitivity, required policy IDs,
  required session capabilities, byte bounds, and an explicit false capability
  grant;
- `review`: human review and sanitization/declassification status;
- `lifecycle`: state, freshness evaluation, expiration, supersession, and
  revocation.

Every source records its public URL or stable source ID, authority status,
jurisdiction, retrieval and effective dates, rights basis, and content digest.
Every exact excerpt identifies one attachment, a half-open byte range
`[start_byte, end_byte)`, and the digest of those exact bytes. Findings cite
source and excerpt IDs; they do not silently convert source content into
instructions.

Attachments are either relative immutable files or HTTPS immutable references.
Relative paths cannot be absolute, contain `..`, escape the declared attachment
root, or exceed the packet byte bounds. Importers verify local bytes and digests
without fetching remote content.

## Canonical integrity

Canonical JSON is UTF-8 JSON with object keys sorted and no insignificant
whitespace. The packet digest is SHA-256 over this object:

```json
{
  "schema_version": "aether.cross-agent-evidence-packet/v1",
  "packet": {"...": "the complete packet identity object"},
  "payload": {"...": "the complete packet payload object"}
}
```

The top-level `integrity` object is excluded so a digest never covers itself.
The same rule applies to sanitized requests. A signature is separately recorded
as `verified`, `unverified`, or `unsigned`; checksum validity never implies
signer trust.

## Lifecycle

Packet states are `draft`, `reviewed`, `ready`, `partial`, `failed`, `stale`,
`superseded`, `revoked`, and `incompatible`.

- `ready` requires a matching digest, current freshness, approved human review,
  public-only sanitization, and no revocation or supersession.
- `partial` preserves useful bounded evidence while naming omissions or failed
  steps.
- `failed` preserves failure evidence but is not usable as a successful result.
- `stale` records an expired source or authority evaluation.
- `superseded` names a replacement packet.
- `revoked` names the revocation decision and time.
- `incompatible` names the unsupported schema, policy, or capability condition.

Unsigned and unverified signatures are legal only when explicitly represented;
the importing policy may still reject them. Import never upgrades a state.

## Deterministic import

An importer shall, without model judgment:

1. parse JSON and reject unknown or malformed fields against the versioned
   schema;
2. verify the canonical envelope digest and explicit signature status;
3. apply packet-wide and importer-wide attachment-count and byte bounds;
4. normalize and resolve attachment paths beneath an explicit root, then verify
   exact size and SHA-256 digest;
5. verify excerpt ranges and the digest of every exact byte span;
6. reject non-public sensitivity, private-data flags, credential material, or
   source content marked as instructions;
7. evaluate lifecycle and source authority freshness using the packet's explicit
   `evaluated_at` and `valid_until` values;
8. require the destination, policy IDs, and session capabilities to be admitted
   by external policy; and
9. return structured errors without executing content or fetching references.

Missing policy or session context fails closed. Packets describe required
capabilities but always set `grants_capabilities` to false.

## Projection rules

A projection names one adapter kind and the digest of one packet. It shall
preserve the packet's destination, public sensitivity ceiling, required policy
IDs, required session capabilities, and false capability grant exactly. Adapter
metadata may narrow delivery behavior but cannot add a destination, capability,
action authority, or content transformation.

Provider, MCP, A2A, filesystem, and queue projections are therefore transport
descriptions, not alternate evidence contracts.

## Failure behavior

Import fails closed for malformed schemas, unknown states, digest mismatch,
path traversal, missing or oversized attachments, invalid exact spans, stale
authority represented as current, private-data indicators, credential-like
material, prompt content represented as instructions, missing external policy
admission, or broadened projections. The validator never repairs, summarizes,
executes, transports, publishes, or declassifies a packet.

