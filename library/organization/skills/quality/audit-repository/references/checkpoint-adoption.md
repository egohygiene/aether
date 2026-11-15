# Checkpoint examples and consumer adoption

The draft checkpoint contract is defined once in repository-audit-data, the
two catalog schemas, the profile registry and the reference helper. The approved
auditor specification retains its existing bytes and independent lifecycle.
The auditor stays read/search-only; a separately authorized writer creates new
reports. Profile selection grants no source, issue or provider mutation.

## Fictional examples

The [examples directory](examples/) contains paired Markdown/JSON fixture inputs.
Every represented repository, commit, observation and finding is synthetic.
The actual Markdown bytes have matching file hashes; example source evidence
digests and prior-audit URLs demonstrate fields without asserting real captures.

| JSON example | Intended behavior |
| --- | --- |
| [repository-complete](examples/repository-complete.json) | One exact repository, observed finding and suggestion-only candidate issue. Complete scope can still contain a defect. |
| [organization-stale-partial](examples/organization-stale-partial.json) | Explicit two-repository roster, old evidence, missing current capture and an unrun check. No current-state or passing claim. |
| [holistic-partial](examples/holistic-partial.json) | Stable leaf composition preserves a blocked profile; experiments remain excluded. |
| [blocked](examples/blocked.json) | Missing input keeps the run blocked with a continuation. |
| [not-applicable](examples/not-applicable.json) | Explicit applicability reason, no findings and no inferred pass. |
| [experimental](examples/experimental.json) | Opt-in informational research remains recommended and low-confidence. |
| [resolved](examples/resolved.json) | Reported delta binds prior artifact identity and distinct current-revision evidence; structural admission cannot prove actual resolution. |

Native tests validate all seven examples with both JSON Schemas and the owner
helper. Mutation controls reject missing provenance, dangling evidence,
malformed findings, profile drift, invented execution success, unsafe/public
references and unsupported resolution. The existing package tests cover profile
cycles, exact selection, overlap, holistic composition and completion rollup.
Deterministic skill evaluations inspect package assertions; they do not test
model decisions or host behavior.

## New consumer

1. Select one reviewed immutable Aether revision. Verify exact hashes of the
   two catalog schemas, profile registry and helper together; do not import a
   caller-supplied implementation or execute report text.
2. Resolve an explicitly authorized roster and exact represented revisions.
   Authenticate every structured repository and URI owner before summarizing
   or hashing public output. Extracting referenced owners is no access proof.
3. Resolve exact profiles. Author one report model with original evidence
   classification and originating leaf for every finding. Generate explanation
   and sidecar from that authored model, retaining missing/uninspected scope.
4. Apply the consumer's explicit freshness, visibility and provenance policy.
   This reference interface preserves clocks and limitations; it neither
   discovers current state nor defines organization applicability policy.
5. Through an authorized output writer, write a new unique Markdown report and
   JSON sidecar. Bind the actual narrative hash. Verify actual cited bytes and
   prior/current evidence separately; schema/helper admission is insufficient.
6. Preserve failed, unavailable and unrun diagnostics. Pin native validation
   integration through EgoLint, execution through Relay, rollout through Pace,
   and portfolio normalization through Observatory at their actual owners.

Holon may present the result and Empathy may compose the generic consumer.
Neither gains policy or publisher authority. Hygiene retains organization
applicability and admission. Aether defines this portable authoring interface;
it installs no scheduler, dashboard or organization mutation workflow.

## Product-source migration after adoption

The completed product audits referenced in egohygiene/egohygiene#315 and #317
remain immutable historical source. No retroactive sidecar is inferred from
their prose. Keep original reports, represented revisions, hashes and issue
history; record unavailable original inputs explicitly.

Once the product has qualified its own exact selection and host, remove or
replace only duplicated reusable audit procedure, copied generic profile
instructions and product-path assumptions in the active harness. Replace them
with the pinned Aether inputs and a thin product-owned roster/evidence/output
adapter. Keep product-specific collection, source facts and policy bindings at
their existing owners. Preview changes and preserve a rollback to the prior
selection; do not delete staged source, archived reports or unresolved findings.

That product conversion and actual host installation/discovery are future
consumer work. These examples do not claim that either happened, that model
quality passed, or that draft artifacts were promoted under Aether #86.
