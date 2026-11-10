# Audit profile and sidecar interface

The approved `auditor` 2.0.0 specification owns audit behavior. The separately
**draft** `repository-audit-data` 1.0.0 extension owns composable profile and
checkpoint data semantics. The skill and read-only auditor remain draft.

## Exact portable resources

The package contains `scripts/audit_contract.py` and
`references/audit-profiles.v1.json`. Distribution resources mirror the canonical
`catalog/schemas/aether.audit-profile-registry.v1.schema.json` and
`catalog/schemas/aether.repository-audit-report.v1.schema.json` into references.
All four resources must be selected from the same reviewed immutable Aether
revision with exact file SHA-256 checks. Never import a consumer-selected module
or execute arbitrary report text.

The standard-library API is:

- `parse(content)` returns a bounded object, rejecting duplicate keys and NaN.
- `validate_registry(registry)` checks closed profile structure, exact versions,
  composition cycles and holistic stable-leaf closure.
- `resolve_profiles(requested, registry)` accepts profile IDs or explicit
  `{id, version}` references and returns registry version/canonical digest plus
  sorted requested/resolved leaf references.
- `completion_state(profile_states)` rolls up **scope completion**, never pass,
  conformance, deployment or human acceptance.
- `validate_report(report, registry)` returns the structurally admitted report
  or raises a closed `AuditContractError`; it performs no collection.
- `referenced_repositories(report)` extracts declared public scope/finding/
  evidence owners and structured GitHub URL owners without reading audit IDs,
  publishing counts or computing report hashes. A consumer must authenticate
  **every** returned owner through its exact public roster before summary or
  digest use; this extraction is not admission. Narrative namespace/privacy
  checks remain a separate consumer gate.
- `canonical_bytes(value)` and `digest(value)` provide deterministic semantic
  JSON bytes/digest, distinct from actual original file or upload ZIP hashes.
- `report_summary(report, registry)` returns typed metadata for a campaign index:
  scope kind and represented repositories, exact profile selection, timestamps,
  completion states, finding IDs/classification/nature/severity/confidence/status/
  effort/impact/origin/evidence labels/history references, canonical report
  reference and sidecar semantic digest. It excludes observations, evidence
  summaries, recommendations, candidate issue prose and scope/completion prose.

The closed report schema documents the exact field names. Do not substitute a
legacy Reflector action/invariant report, parse narrative headings or make a
second finding taxonomy. `profiles` must equal the exact resolution output.
`source_profile` always identifies a resolved leaf, even when holistic was
requested. Per-profile completion must cover that same leaf set once.

## Writing and review

Resolve scope and public admission before reading private or excluded findings,
IDs, counts or hashes. Keep canonical Markdown and the sidecar synchronized
through the same authored finding model, then hash the actual Markdown bytes.
No helper fabricates narrative content, verifies stakeholder intent or proves
that a cited command ran. An immutable source/transport adapter must verify
actual file identities separately.

Use `not-compared` and unverified history when prior evidence is absent. An
explicit reported delta is not automatic lifecycle promotion. Keep experiments
informational and opt-in; issue candidates remain suggestions. Record unrun
validation and missing evidence rather than inventing passing fixtures.

Evidence URIs use a deliberately bounded canonical HTTPS profile: no credentials,
query, percent escapes, traversal, machine paths or ambiguous fragments. A local
canonical path can preserve a source that has no supported public URI. A leaf
marked not-applicable cannot originate a finding. Reported resolved history
requires an observed prior relationship, observed prior-audit evidence bound to
that selected prior artifact's hash and URI/local path, plus distinct observed
current-revision comparison evidence. These are structural bindings, not proof
that remediation actually succeeded.
Successful and failed command claims also require observed command/artifact/
provider/manual evidence. A recommended or unverified reference cannot become
execution metadata merely by supplying an exit code.

The pure helper is an authoring/reference contract. Its presence does not
establish deterministic scenario qualification, consumer installation, a host
execution capability or organization rollout.
