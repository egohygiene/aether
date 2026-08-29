# Campaign handoff contract

## Source roles

| Input | Authority |
| --- | --- |
| Identity package | Approved assets, brand metadata, selectors, approvals, and provenance |
| Aether catalog | Dated platform/placement facts and source evidence |
| Campaign brief | User-supplied objective, audience, context, candidate copy, claims, links, and attribution intent |
| Human approval | Exact reviewed packet's authorization for immutable export |
| External receipt | Evidence that a separately authorized adapter published an exported packet |

The brief cannot replace Identity facts or Aether constraints. The packet
copies and locks those sources so a reviewer can see the whole handoff without
creating a new authority.

## Digest rules

- Catalog locks use `sha256-utf8-lf`: normalize CRLF/CR to LF, encode UTF-8,
  then hash.
- Identity package locks use `sha256-canonical-json`: serialize parsed JSON
  with sorted keys and compact separators, encode UTF-8, then hash.
- Review approvals bind to the canonical JSON digest of the complete packet in
  `reviewed` state before approval is inserted.

Any semantic edit changes the reviewed digest and requires a new approval.

## Brief rules

The brief is closed. Each selection names one target already present in the
Identity package. Copy and claims are candidates. A claim may include an
evidence reference for review, but evidence does not itself create approval.

Attribution marked `required` needs non-empty text. A required link must be an
HTTPS URL. Duplicate selection or target IDs fail validation.

Credential-like keys and well-known secret values fail before packet creation.
Account authentication belongs only in a separately authorized adapter's
secret store, never in the packet.

## Packet validation

Structural validation uses
`aether.social-campaign-handoff/v1`. Semantic validation additionally proves:

- unique channels and checklist items;
- append-only, contiguous lifecycle history ending in the current state;
- candidate-only copy before export approval;
- approval IDs and reviewed packet digest agree;
- every required checklist item is complete before export;
- required freshness verification and attribution have evidence;
- publication is never implied without an external receipt; and
- no credentials or direct-publish authority are embedded.

Unknown constraints remain unknown. A renderer must interpret them
conservatively and may not infer a safe zone or media limit.
