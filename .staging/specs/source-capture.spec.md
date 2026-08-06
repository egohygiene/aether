---
title: Process Specification — Source Capture Pipeline
version: 1.1
date_created: 2026-07-18
last_updated: 2026-07-18
owner: Ego Hygiene
tags: [process, capture, sources, conversations, chatgpt, mindgarden]
---

# Introduction

This specification defines a source-agnostic capture pipeline that retrieves,
preserves, normalizes, verifies, and versions source material before knowledge
extraction. Its first implementation target is ChatGPT conversations, while its
interfaces remain extensible to documents, webpages, repositories, media, and
other source types.

The capture layer establishes a durable ground truth. It does not interpret the
meaning of a source, extract knowledge, create synapses, route knowledge into the
Mind Garden, or publish content.

## 1. Purpose and Scope

The pipeline accepts a source URL, provider identifier, or previously exported
artifact and produces a verified Source Artifact Bundle suitable for downstream
processing.

This specification covers:

- Capture request validation and canonical identifier resolution
- Provider-specific retrieval through isolated adapters
- Authentication isolation and safe handling of retrieval credentials
- Preservation of provider payloads and paginated response boundaries
- Canonical normalization without semantic summarization
- Human-readable transcript rendering
- Conversation trees, regenerated responses, edits, and alternate branches
- Attachment discovery, retrieval, hashing, and failure reporting
- Integrity hashing and semantic change detection
- Immutable source versions and idempotent recapture
- Sensitivity propagation, security redaction, and redaction accounting
- Partial recovery, resumable processing, batch capture, and structured reports
- Handoff to `knowledge-extract.spec.md`

This specification does not cover:

- Knowledge extraction, synthesis, or synapse derivation
- Vault-native source-note rendering or semantic folder routing
- Obsidian wikilink generation
- Publishing, remote deletion, or mutation of the original source
- Final visual or editorial artifacts

Those responsibilities belong to `knowledge-extract.spec.md`,
`synapse-create.spec.md`, `gardenize.spec.md`, and downstream publishing
specifications.

## 2. Architectural Boundaries

The required flow is:

```text
capture request
    -> source adapter
    -> provider response units
    -> private source artifact bundle
    -> canonical normalized source
    -> capture result
    -> knowledge extraction
    -> gardenization
    -> Mind Garden source note
```

The source archive and the Mind Garden source note are different artifacts:

- The **Source Artifact Bundle** is a private, versioned fidelity archive.
- The **Source Note** is a vault-native Markdown record created later by
  `gardenize.spec.md` from the bundle manifest and capture result.
- The artifact storage root must be configurable and private by default.
- Raw archives must not be assumed publishable or safe to commit to Git.
- Colocating archives inside an Obsidian vault requires explicit configuration
  and exclusion from Git, Quartz, search indexing, and publication as required
  by the applicable sensitivity policy.

## 3. Definitions

- **Capture Request**: Structured input that initiates one source capture.
- **Capture Run**: One execution attempt, identified by a stable `run_id`,
  whether it succeeds, fails, or finds unchanged content.
- **Source Identifier**: Provider-native identifier or resolvable reference to a
  source. A ChatGPT conversation identifier is UUID-shaped but must not be
  restricted to UUID version 4.
- **Source ID**: Stable internal identifier derived from provider and canonical
  provider identifier, such as `chatgpt-<conversation-id>`.
- **Capture Adapter**: Replaceable provider-specific component responsible for
  authentication, retrieval, pagination, and conversion into safe response
  units. Core pipeline logic must not embed provider endpoints.
- **Provider Response Unit**: One response body or exported record returned by
  the adapter, preserving its original response boundary and order.
- **Raw Archive**: Stored provider response units after mandatory removal of
  transport credentials and other prohibited authentication material. It is
  otherwise fidelity-preserving and is immutable after finalization.
- **Raw Response Index**: Manifest describing every stored response unit,
  retrieval order, pagination relationship, hash, and status.
- **Normalized Source**: Provider-independent structured representation derived
  from the raw archive without summarization.
- **Normalized Conversation**: Canonical message-tree representation of a
  captured conversation.
- **Transcript**: Human-readable Markdown rendering of the normalized
  conversation, including clear branch structure.
- **Canonical Content Hash**: Hash of a deterministic, volatility-filtered
  normalized representation used to decide whether source meaning changed.
- **Raw Content Hash**: Hash used only to verify the exact stored bytes of a raw
  response unit or raw response index.
- **Capture Version**: Immutable bundle version created when canonical source
  content materially changes or when explicitly forced by policy.
- **Branch**: Divergent continuation from a shared message ancestor.
- **Branch Index**: Derived navigation data over the canonical message tree. It
  must never override or contradict the tree.
- **Attachment**: Referenced or embedded asset associated with a source message.
- **Coverage Record**: Accounting of captured, omitted, inaccessible,
  truncated, unsupported, and uncertain source regions.
- **Redaction Record**: Non-secret audit entry describing a security
  transformation without retaining the removed value.
- **Sensitivity Classification**: `public`, `normal`, `sensitive`, or
  `restricted`.
- **Finalized Bundle**: Complete or explicitly partial bundle atomically moved
  from staging to its immutable version directory after validation.

## 4. Requirements, Constraints, and Guidelines

### 4.1 Functional Requirements

- **REQ-001**: The pipeline shall accept a full ChatGPT conversation URL, a bare
  ChatGPT conversation identifier, or a supported local export.
- **REQ-002**: Provider identifiers shall be validated using adapter-specific
  rules. ChatGPT identifiers shall not be rejected solely because their UUID
  version nibble is not version 4.
- **REQ-003**: The pipeline shall normalize all accepted identifier forms to one
  canonical provider identifier and stable Source ID.
- **REQ-004**: Retrieval shall occur only through a versioned Capture Adapter.
- **REQ-005**: The core pipeline shall not depend on a specific documented or
  undocumented provider endpoint.
- **REQ-006**: Each paginated response, export record, or independently returned
  response body shall be stored as a separate Provider Response Unit. Pagination
  units must not be merged and then described as an unmodified raw response.
- **REQ-007**: The pipeline shall write a Raw Response Index recording the
  ordered response units and their relationships.
- **REQ-008**: The pipeline shall normalize raw response units into one canonical
  representation before transcript rendering or downstream extraction.
- **REQ-009**: Normalization shall preserve all representable source content,
  message relationships, content parts, provider identifiers, timestamps,
  attachments, and available metadata except explicitly documented security
  redactions.
- **REQ-010**: The pipeline shall render a human-readable Markdown transcript
  that does not silently flatten or discard alternate branches.
- **REQ-011**: The parent/children message graph shall be the canonical branch
  representation. Any branch list shall be derived and verifiably consistent.
- **REQ-012**: The pipeline shall discover attachment references and attempt
  retrieval when authorized by request policy.
- **REQ-013**: Unavailable attachments shall not block an otherwise usable
  capture. Their status and failure reasons shall be recorded.
- **REQ-014**: Every finalized bundle shall contain a manifest, response index,
  normalized source, transcript when renderable, capture report, and redaction
  ledger when redactions occurred.
- **REQ-015**: Every capture run shall produce a run-level report, including
  runs that fail before a Source ID or bundle version can be finalized.
- **REQ-016**: The pipeline shall support incremental processing of long sources
  and explicitly report partial recovery.
- **REQ-017**: A Capture Result shall be emitted for downstream extraction only
  when status is `complete` or policy permits extraction from `partial`.
- **REQ-018**: Batch capture shall isolate failure by source and emit one batch
  report plus independent per-source run reports.

### 4.2 Integrity and Versioning Requirements

- **INT-001**: SHA-256 shall be used to hash each stored raw response unit,
  attachment, normalized file, and finalized manifest-defined artifact.
- **INT-002**: Raw hashes verify stored bytes only. They shall not determine
  whether source meaning changed.
- **INT-003**: Semantic change detection shall use `canonical_content_hash` over
  deterministic normalized content.
- **INT-004**: Canonical hashing shall exclude capture timestamps, adapter
  diagnostics, local paths, run IDs, pagination transport metadata, expiring
  signatures, temporary download URLs, and other documented volatile values.
- **INT-005**: Canonical hashing shall preserve message order, tree structure,
  content-part order, meaningful timestamps, attachment identities, and other
  source semantics.
- **INT-006**: Canonical serialization rules shall be versioned and deterministic
  across supported platforms. Object keys shall be sorted, arrays shall retain
  semantic order, text shall use UTF-8, and line endings shall be normalized.
- **INT-007**: An unchanged canonical content hash shall not create a new content
  version. The run shall return `unchanged` and reference the latest verified
  bundle.
- **INT-008**: A changed canonical content hash shall create a new immutable
  version while retaining all previous versions.
- **INT-009**: An explicit `force_new_version` request may create an identical
  content version for audit or migration purposes and shall record the reason.
- **INT-010**: `latest.yaml` or an equivalent portable manifest pointer shall be
  the normative latest-version mechanism. Symlinks may be optional conveniences
  but must not be required.

### 4.3 Security and Privacy Requirements

- **SEC-001**: User-supplied credentials, session tokens, cookies, authorization
  headers, and adapter authentication configuration shall never be written to
  artifacts, reports, manifests, filenames, command output, or logs.
- **SEC-002**: Credentials shall be resolved from an approved runtime source,
  remain in the narrowest practical scope, never be serialized, and have
  references released after adapter execution. Managed runtimes shall not claim
  guaranteed physical memory zeroization; clearing is best effort where
  supported.
- **SEC-003**: Conversation captures shall default to `sensitive` unless the
  request or policy explicitly assigns a stricter classification.
- **SEC-004**: Authentication material introduced by transport or retrieval shall
  be removed before a Provider Response Unit is persisted.
- **SEC-005**: Source-authored credential-like text and provider-returned
  ephemeral access values shall be handled according to sensitivity policy.
  When removed, they shall be replaced by stable placeholders and recorded in
  the redaction ledger without retaining the secret value.
- **SEC-006**: A stored Raw Archive is fidelity-preserving subject to mandatory
  security transformations. The manifest shall never claim byte identity with
  the network response when a security transformation occurred.
- **SEC-007**: Derived normalized files and transcripts shall undergo secret
  scanning before finalization.
- **SEC-008**: Attachment filenames shall be sanitized against traversal,
  reserved names, control characters, and collisions.
- **SEC-009**: Attachment scanning shall be content-type aware. A binary file
  must not be quarantined solely because arbitrary bytes accidentally match a
  text credential pattern.
- **SEC-010**: Quarantined attachments shall be isolated, excluded from ordinary
  downstream processing, and represented by metadata only.
- **SEC-011**: Raw bundles shall be private and non-publishable by default.
- **SEC-012**: Sensitivity classification and redaction history shall propagate
  through the Capture Result.

### 4.4 Quality Requirements

- **QLT-001**: Capture shall preserve meaning and structure without compression,
  summarization, or interpretation.
- **QLT-002**: Missing provider fields shall be represented as `null`, `unknown`,
  or an explicit absence status rather than invented.
- **QLT-003**: Unknown roles, content types, and provider metadata shall be
  preserved through extensible fields instead of discarded.
- **QLT-004**: Regenerated responses, edited prompts, nested branches, synthetic
  roots, and multiple roots shall be represented without inventing a single
  authoritative path.
- **QLT-005**: Transcript rendering shall identify the selected provider path
  when known while still exposing all captured alternatives.
- **QLT-006**: Capture reports shall distinguish failure, omission, unsupported
  content, policy exclusion, and genuine absence.

### 4.5 Operational Constraints

- **CON-001**: The capture layer shall not perform semantic knowledge extraction.
- **CON-002**: Previously finalized bundle versions shall never be modified or
  deleted by capture operations.
- **CON-003**: Processing shall occur in a run-specific staging directory and be
  atomically finalized when supported by the filesystem.
- **CON-004**: Failed staging content shall be clearly marked and either retained
  for recovery or safely cleaned according to policy. It shall never appear to
  be a verified bundle.
- **CON-005**: A partial capture shall never be labeled complete.
- **CON-006**: Final Mind Garden paths and Markdown source-note formatting remain
  the responsibility of Gardenization.

### 4.6 Guidelines and Processing Pattern

- **GUD-001**: Use Source IDs shaped as `<provider>-<provider-id>`.
- **GUD-002**: Use ISO 8601 timestamps with explicit UTC offset.
- **GUD-003**: Prefer explicit nullable fields in stable machine contracts.
- **GUD-004**: Record adapter, schema, normalizer, transcript renderer, security
  policy, and canonicalization versions.
- **GUD-005**: Use relative paths inside bundles and absolute paths only in
  runtime results when necessary.
- **PAT-001**: Process stages shall be: validate → resolve authentication →
  retrieve → sanitize transport material → persist response units → index raw
  units → normalize → discover attachments → render transcript → scan and record
  redactions → hash → validate → finalize → emit result.
- **PAT-002**: Each stage shall emit structured status and checkpoint data.

## 5. Interfaces and Data Contracts

### 5.1 Capture Request

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `request_id` | string | Yes | Unique request identifier |
| `source_type` | enum | Yes | `chatgpt_conversation \| document \| webpage \| repository \| media \| other` |
| `identifier` | string | Yes | Provider URL, provider ID, or local export path |
| `provider` | string | No | Explicit provider override |
| `adapter` | string | No | Requested adapter name or automatic selection |
| `adapter_config` | object | No | Non-secret adapter settings or credential references; inline credentials prohibited |
| `artifact_root` | path | No | Configured private artifact root |
| `sensitivity` | enum | No | `public \| normal \| sensitive \| restricted` |
| `attachment_policy` | enum | No | `metadata_only \| download \| skip`; default `metadata_only` |
| `partial_policy` | enum | No | `reject \| retain \| allow_extraction`; default `retain` |
| `force_retrieve` | boolean | No | Bypass local unchanged assumptions and retrieve again |
| `force_new_version` | boolean | No | Create an identical content version for an explicit recorded reason |
| `force_reason` | string | Conditional | Required when `force_new_version=true` |
| `batch_id` | string | No | Parent batch identifier |
| `requested_by` | string | No | User or agent audit label |

### 5.2 Adapter Capture Result

The adapter returns this in memory to the core. Authentication state is never
part of this contract.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `provider` | string | Yes | Provider name |
| `canonical_identifier` | string | Yes | Provider-native stable identifier |
| `canonical_url` | string/null | Yes | Stable URL when available |
| `response_units` | array[object] | Yes | Ordered response bodies plus safe retrieval metadata |
| `attachments` | array[object] | Yes | Discovered attachment references |
| `provider_metadata` | object | Yes | Non-secret source metadata |
| `coverage` | object | Yes | Adapter-level capture coverage |
| `warnings` | array[string] | Yes | Non-fatal adapter warnings |

Each response unit contains a sequence number, media type, body bytes or a
structured payload, pagination relationship, source timestamp when available,
and non-secret diagnostics. Authentication headers and cookies are prohibited.

### 5.3 Raw Response Index

Stored as `raw/index.yaml`.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `schema` | string | Yes | Raw index schema version |
| `source_id` | string | Yes | Stable Source ID |
| `capture_version` | integer | Yes | Bundle version |
| `units` | array[object] | Yes | Ordered response-unit records |
| `combined_hash` | string | Yes | Hash over ordered unit hashes and index semantics |
| `security_transformations` | integer | Yes | Number of transformations applied before persistence |

Each unit record includes `unit_id`, `sequence`, `path`, `media_type`,
`byte_size`, `sha256`, `previous_unit_id`, `next_unit_id`, `pagination_token`
only when non-secret and stable, `status`, and applicable redaction-record IDs.

### 5.4 Source Artifact Manifest

Stored as `manifest.yaml`.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `schema` | string | Yes | Manifest schema version |
| `source_id` | string | Yes | Stable internal Source ID |
| `source_type` | string | Yes | Canonical source-type vocabulary |
| `provider` | string | Yes | Provider name |
| `provider_id` | string | Yes | Canonical provider identifier |
| `canonical_url` | string/null | Yes | Canonical source URL |
| `capture_version` | integer | Yes | Immutable content version |
| `capture_status` | enum | Yes | `complete \| partial` for finalized bundles |
| `captured_at` | datetime | Yes | Finalization timestamp |
| `sensitivity` | enum | Yes | Propagated classification |
| `raw_index_path` | path | Yes | Relative raw response index path |
| `normalized_path` | path | Conditional | Required when normalization succeeded |
| `transcript_path` | path/null | Yes | Null when rendering did not succeed |
| `capture_report_path` | path | Yes | Relative bundle report path |
| `redaction_ledger_path` | path/null | Yes | Null when no redactions occurred |
| `raw_combined_hash` | string | Yes | Integrity hash from raw index |
| `normalized_content_hash` | string/null | Yes | Stored normalized-file hash |
| `canonical_content_hash` | string/null | Yes | Semantic version-detection hash |
| `previous_version` | integer/null | Yes | Prior content version |
| `versions` | object | Yes | Adapter, schemas, normalizer, renderer, policy, canonicalizer |
| `conversation` | object/null | Yes | Conversation metadata when applicable |

### 5.5 Normalized Conversation

Stored as `normalized/conversation.json`.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `schema` | string | Yes | Normalized schema version |
| `source_id` | string | Yes | Parent Source ID |
| `capture_version` | integer | Yes | Bundle content version |
| `provider` | string | Yes | Source provider |
| `provider_conversation_id` | string | Yes | Provider conversation identifier |
| `canonical_url` | string/null | Yes | Conversation URL |
| `title` | string/null | Yes | Provider title |
| `created_at` | datetime/null | Yes | Provider creation time |
| `updated_at` | datetime/null | Yes | Provider modification time |
| `participants` | array[object] | Yes | Participant records |
| `root_message_ids` | array[string] | Yes | Zero or more canonical roots |
| `messages` | object | Yes | Map of message ID to Message Record |
| `branch_index` | array[object] | Yes | Derived navigation index |
| `selected_path` | array[string]/null | Yes | Provider-selected path when known |
| `attachments` | array[object] | Yes | Attachment records |
| `integrations` | array[object] | Yes | Models, tools, plugins, apps, or connectors when available |
| `provider_metadata` | object | Yes | Preserved non-secret unmapped metadata |
| `redactions` | array[string] | Yes | Redaction-record IDs affecting normalized content |

### 5.6 Participant, Message, and Content Part

**Participant Record**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `participant_id` | string | Yes | Stable conversation-local identifier |
| `role` | enum | Yes | `user \| assistant \| system \| developer \| tool \| unknown` |
| `display_name` | string/null | Yes | Display label when available |
| `provider_id` | string/null | Yes | Non-secret provider identifier |
| `provider_metadata` | object | Yes | Extensible safe metadata |

**Message Record**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `message_id` | string | Yes | Provider ID or deterministic generated ID |
| `provider_message_id` | string/null | Yes | Original provider ID |
| `parent_id` | string/null | Yes | Parent message ID |
| `children_ids` | array[string] | Yes | Ordered child IDs |
| `role` | enum | Yes | `user \| assistant \| system \| developer \| tool \| unknown` |
| `participant_id` | string/null | Yes | Related participant |
| `content` | array[object] | Yes | Ordered Content Part records |
| `created_at` | datetime/null | Yes | Message timestamp |
| `updated_at` | datetime/null | Yes | Edit timestamp when available |
| `status` | enum | Yes | `complete \| truncated \| redacted \| failed \| unknown` |
| `model` | object/null | Yes | Per-message model metadata |
| `provider_metadata` | object | Yes | Extensible safe metadata |
| `redactions` | array[string] | Yes | Applicable redaction-record IDs |

**Content Part Record**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `part_id` | string | Yes | Stable message-local identifier |
| `type` | string | Yes | Known or provider-defined type |
| `value` | any | Yes | String, scalar, array, or structured object |
| `mime_type` | string/null | Yes | MIME type when applicable |
| `attachment_id` | string/null | Yes | Related attachment |
| `provider_metadata` | object | Yes | Extensible safe metadata |

Unknown content types must be preserved with their original type label and
structured value whenever policy permits.

### 5.7 Derived Branch Index

The message graph is authoritative. Each derived branch entry includes:

- `branch_id`
- `branch_point_message_id` or `null` for a root branch
- `parent_branch_id` or `null`
- `branch_index` among siblings
- `message_ids` belonging uniquely to that segment
- `leaf_message_id`
- `is_selected`, which may be `true`, `false`, or `null`

Nested branches produce parent/child Branch Index records. `branch_count` means
the number of leaf paths through the message graph and must be computed using a
versioned algorithm. Synthetic roots are preserved in provider metadata or
represented by multiple `root_message_ids`; they must not be converted into a
fabricated user message.

### 5.8 Attachment Record

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `attachment_id` | string | Yes | Stable bundle identifier |
| `message_ids` | array[string] | Yes | Referencing messages |
| `reference` | string/null | Yes | Safe non-secret reference |
| `filename` | string/null | Yes | Original display filename |
| `stored_filename` | string/null | Yes | Sanitized collision-safe filename |
| `mime_type` | string/null | Yes | Detected or declared MIME type |
| `size_bytes` | integer/null | Yes | Stored size when available |
| `local_path` | path/null | Yes | Relative bundle path |
| `sha256` | string/null | Yes | Stored-file integrity hash |
| `status` | enum | Yes | `resolved \| metadata_only \| unresolved \| unauthorized \| quarantined \| unsupported \| skipped` |
| `failure_code` | string/null | Yes | Machine-readable reason |
| `redactions` | array[string] | Yes | Applicable redaction IDs |

### 5.9 Redaction Record and Ledger

Stored as `reports/redactions.yaml` when non-empty.

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `redaction_id` | string | Yes | Stable run-local ID |
| `artifact` | string | Yes | Affected response unit, message, field, or attachment |
| `location` | string | Yes | Non-secret structural locator |
| `category` | enum | Yes | `transport_credential \| ephemeral_access_value \| source_secret \| policy_restricted \| other` |
| `rule_id` | string | Yes | Versioned policy rule |
| `action` | enum | Yes | `removed \| masked \| replaced \| quarantined` |
| `placeholder` | string/null | Yes | Stable placeholder when applicable |
| `created_at` | datetime | Yes | Transformation time |

The removed value, its reversible encoding, and any digest that would enable
credential guessing are prohibited from the ledger.

### 5.10 Version History and Latest Pointer

`version-history.yaml` contains the Source ID and ordered content-version
entries. Each entry records version, capture time, status, canonical content
hash, raw combined hash, bundle path, adapter version, prior version, and change
reason.

`latest.yaml` contains only the Source ID, latest verified content version,
bundle path, canonical content hash, and update time. It is updated atomically.

Unchanged runs are recorded in the run-report store but do not modify immutable
versions. A policy may append an attempt summary to a separate mutable audit
index, but this is not required for content identity.

### 5.11 Capture Report

Every run report includes:

- `schema`, `run_id`, `request_id`, and optional `batch_id`
- Resolved `source_id` when available
- `run_status`: `complete`, `partial`, `failed`, or `unchanged`
- Referenced `capture_version` when available
- Start and completion timestamps
- Adapter and processing-component versions
- Per-stage status: `pending`, `complete`, `skipped`, `partial`, or `failed`
- Coverage counts for messages, roots, leaf paths, content parts, and attachments
- Ordered warnings and structured failures
- Recovery checkpoint information when safe
- Finalized bundle path when available
- Existing bundle reference for unchanged runs

Before a Source ID exists, reports are written under
`<artifact-root>/_runs/<run-id>/capture-report.yaml`. Finalized bundles contain
a copy of or stable reference to the applicable report. Authentication values
must never appear in errors or diagnostics.

### 5.12 Capture Result Handoff

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `run_id` | string | Yes | Capture run identifier |
| `source_id` | string | Yes | Stable Source ID |
| `source_type` | string | Yes | `conversation` for ChatGPT handoff |
| `provider` | string | Yes | Provider name |
| `capture_status` | enum | Yes | `complete \| partial` |
| `capture_version` | integer | Yes | Finalized bundle version |
| `bundle_path` | path | Yes | Artifact bundle path |
| `manifest_path` | path | Yes | Bundle manifest |
| `normalized_path` | path | Yes | Canonical extraction input |
| `transcript_path` | path/null | Yes | Human-readable transcript |
| `capture_report_path` | path | Yes | Coverage and failure report |
| `canonical_content_hash` | string | Yes | Extraction change-detection key |
| `sensitivity` | enum | Yes | Propagated classification |
| `metadata` | object | Yes | Safe provenance, language, model, participant, and coverage summary |

Failed runs do not emit a Capture Result. Partial runs emit one only when
`partial_policy=allow_extraction` and a valid normalized representation exists.

## 6. Artifact Storage Layout

The artifact root is configurable and is not inherently the Mind Garden vault:

```text
<artifact-root>/
├── _runs/
│   └── <run-id>/
│       ├── capture-report.yaml
│       └── checkpoints/
└── conversations/
    └── chatgpt/
        └── chatgpt-<conversation-id>/
            ├── version-history.yaml
            ├── latest.yaml
            ├── v1/
            │   ├── manifest.yaml
            │   ├── raw/
            │   │   ├── index.yaml
            │   │   ├── response-000.json
            │   │   └── response-001.json
            │   ├── normalized/
            │   │   ├── conversation.json
            │   │   └── conversation.md
            │   ├── attachments/
            │   └── reports/
            │       ├── capture-report.yaml
            │       └── redactions.yaml
            └── v2/
                └── ...
```

Empty optional directories or ledgers may be omitted. Finalization shall use a
staging directory outside the immutable version path and publish the complete
directory atomically where supported.

Gardenization later creates a source note such as:

```text
mindgarden/sources/conversations/chatgpt/<stable-source-note>.md
```

That note may reference the private bundle according to local policy. The raw
bundle itself is not a vault-native source note.

## 7. Acceptance Criteria

- **AC-001**: A valid ChatGPT URL or bare identifier resolves to the same Source
  ID and canonical URL.
- **AC-002**: A malformed identifier fails before network retrieval and creates
  only a credential-free run report.
- **AC-003**: Paginated retrieval stores independently hashed response units in
  retrieval order and merges them only during normalization.
- **AC-004**: A completed capture produces a valid manifest, raw index,
  normalized conversation, transcript, report, hashes, and latest pointer.
- **AC-005**: Recomputed raw hashes match every stored raw response unit.
- **AC-006**: Recomputed canonical content hash matches the manifest using the
  declared canonicalization version.
- **AC-007**: Volatile retrieval metadata changes do not create a new content
  version.
- **AC-008**: A new message or changed conversation structure creates a new
  immutable content version without modifying prior versions.
- **AC-009**: An unchanged capture returns the latest bundle and creates no new
  content version.
- **AC-010**: Nested branches and regenerated responses remain reachable through
  the canonical message graph and are visibly represented in the transcript.
- **AC-011**: Unknown roles or content types survive normalization through
  extensible fields.
- **AC-012**: Attachment failures are isolated, recorded, and do not falsely
  mark the conversation capture complete when material coverage is affected.
- **AC-013**: A failed capture never appears under an immutable finalized version
  path as a verified bundle.
- **AC-014**: A partial finalized capture records exact omissions and emits a
  Capture Result only when policy permits.
- **AC-015**: Secret scanning finds no persisted adapter credentials, cookies,
  session tokens, or authorization headers.
- **AC-016**: Every security transformation has a non-secret Redaction Record.
- **AC-017**: A batch failure affects only its source and is reflected in the
  consolidated batch report.
- **AC-018**: Gardenization can create a source note using only the manifest and
  Capture Result without reading authentication state.

## 8. Test Automation Strategy

### Test Levels

- Unit: identifier parsing, path sanitization, canonical serialization, hashing,
  tree validation, branch derivation, redaction, and manifest rendering
- Integration: mocked adapter through finalized bundle and Capture Result
- End-to-end: local export fixtures and opt-in live adapter tests
- Contract: schema compatibility with knowledge extraction and Gardenization
- Regression: stable fixtures for normalization and canonical hashes

### Required Fixtures

- Linear conversation
- Conversation with regenerated assistant responses
- Edited user message with nested branches
- Multiple or synthetic roots
- Unknown role and unknown structured content type
- Tool, developer, image, file, and structured result messages
- Resolved, unresolved, unauthorized, and quarantined attachments
- Paginated retrieval with volatile tokens and timestamps
- Long conversation with interruption and recovery
- Local export containing one conversation
- Export collection requiring conversation selection
- Malformed, inaccessible, and partially corrupted sources
- Synthetic transport credentials and source-authored secret-like text
- Unchanged and materially changed recapture pairs

### CI Validation

CI shall validate schemas, graph integrity, deterministic hashes, idempotency,
version immutability, path safety, redaction accounting, fixture coverage, and
cross-platform latest-pointer behavior. Live provider access must not be
required for ordinary CI.

Performance tests shall define repository-owned time and memory budgets rather
than assuming one universal machine. Processing must be streaming or bounded
where practical and must not require all attachment bytes in memory.

## 9. Examples and Edge Cases

### Standard ChatGPT Capture

```text
Input: https://chatgpt.com/c/<conversation-id>
Result: source ID chatgpt-<conversation-id>
Result: finalized v1 bundle and Capture Result
Result: no knowledge or synapse files created
```

### Paginated Retrieval

```text
The adapter returns four provider pages.
raw/ stores response-000 through response-003 unchanged except declared
security transformations.
raw/index.yaml records their order.
Normalization creates one conversation tree.
```

### Volatile Remote Metadata

```text
The second retrieval contains different request timestamps and signed asset
URLs but identical messages and attachment identities.
Raw hashes differ.
Canonical content hashes match.
No new content version is created.
```

### Material Conversation Change

```text
The conversation gains three messages.
Canonical content hash changes.
v2 is finalized; v1 remains immutable.
latest.yaml points to v2.
```

### Authentication Failure Before Resolution

```text
No bundle version is created.
<artifact-root>/_runs/<run-id>/capture-report.yaml records AUTH_FAILED.
The report contains no credential values.
No Capture Result is emitted.
```

### Partial Long Conversation

```text
Five of eight response pages are captured before interruption.
The report identifies exact successful and omitted page ranges.
If normalization is structurally valid, policy may finalize a partial bundle.
Extraction is blocked unless partial_policy=allow_extraction.
```

### Local Export

```text
A local ChatGPT export is captured through a local-export adapter.
Original export records become response units.
The manifest records local-export provenance without exposing unrelated local
filesystem information in gardenized notes.
```

### Source-Authored Secret-Like Text

```text
A user intentionally discusses an example token in a message.
Policy determines whether it is retained, masked, or replaced.
If transformed, the transcript contains a stable placeholder and the ledger
records the rule and location without storing the removed value.
```

## 10. Validation Criteria

Before finalization, the pipeline shall verify:

- Manifest and report schemas are valid for their declared versions.
- Every raw index entry resolves to one file with matching size and hash.
- Every message parent and child reference resolves and is reciprocal.
- Every root exists and has no canonical parent.
- Every derived branch entry agrees with the message graph.
- Every attachment reference resolves to an Attachment Record.
- Every stored attachment hash matches its file.
- Every redaction reference resolves to a ledger record.
- No prohibited authentication material appears in persisted outputs or logs.
- Canonical serialization and hashing are reproducible.
- Latest and version-history pointers reference finalized bundles only.
- Existing version directories were not modified.
- Partial coverage is never reported as complete.
- Capture Result paths resolve and are permitted by sensitivity policy.
- The handoff conforms to `knowledge-extract.spec.md`.

## 11. Dependencies and Integrations

### External Systems

- ChatGPT or another provider as the remote source
- Configurable durable private artifact storage
- Mind Garden filesystem as a downstream source-note destination, not a required
  raw-archive location

### Infrastructure

- Replaceable provider adapters
- UTF-8 JSON, YAML, and Markdown serialization
- SHA-256 hashing
- Content-type-aware secret and attachment scanning
- Atomic filesystem operations where supported
- Optional OCR or media extraction only for future source-specific adapters

### Downstream Consumers

- `knowledge-extract.spec.md` consumes Capture Results.
- `gardenize.spec.md` renders vault-native source notes from safe capture
  metadata and later derived artifacts.
- `synapse-create.spec.md` consumes extracted knowledge, not raw authentication
  or adapter state.

## 12. Related Specifications and Files

- `.github/specs/knowledge-extract.spec.md`
- `.github/specs/synapse-create.spec.md`
- `.github/specs/gardenize.spec.md`
- `mindgarden/_system/templates/source.md`
- `mindgarden/_system/schemas/metadata-conventions.md`

