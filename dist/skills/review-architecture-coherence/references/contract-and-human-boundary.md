# Portable record and human boundary

The closed schema is `aether.architecture-coherence-review.v1.schema.json` in
this directory after distribution. Canonical source lives in Aether's
`catalog/schemas/`. The specification is `architecture-coherence-review`.

## APIs

`scripts/architecture_coherence.py` is standalone, stdlib-only and performs no
network requests, clock reads, source execution or writes.

- `loads_review(bytes_or_text, *, public_repositories=None)` rejects duplicate
  members and returns a validated record, with a 2 MiB transport bound.
- `load_review(path, *, public_repositories=None)` reads at most that bound.
- `validate_review(value, *, public_repositories=None)` validates closed shape,
  bounded text/arrays, all references and revision/governance bindings.
- `review_subject(value)` returns `{id, assessment_sha256, scope,
  represented_revisions, completed_at}`. It validates the assessment, but its
  digest deliberately excludes governance and does not authenticate that field.
- `evaluate_review(value, *, as_of, public_repositories,
  trusted_human_evidence=(), material_changes=(), change_inventory='unknown',
  current_revisions=None)` retains execution and reviewer recommendation
  separately from the exact Hygiene governance evaluation.
- `human_statement(value, *, public_repositories, kind='decision')` constructs
  the bound public statement that an external trusted verifier must inspect.
  It is not proof of authentic human approval.
- `import_human_decision(value, governance, *, as_of, public_repositories,
  trusted_human_evidence)` returns a new artifact only if exact separately
  trusted human evidence verifies the bound human decision. It does not mutate
  the input or change the immutable assessment digest.
- `governance_contract()` exposes the verified adjacent Hygiene owner module,
  including its exact `TrustedHumanEvidence` class and material-change APIs.
  Use this module instance for typed context; raw dictionaries and a type from
  a separately loaded module are not interchangeable proof.

The adjacent `governance.lock.json` binds exact Hygiene source commit
`d11580e9a9c5d78b9a5d21474deaa612712a0fb9`, helper, governance/material-change
schemas and proposed policy digest. The helper and two schemas are unchanged
byte mirrors of that owner source, not locally maintained governance rules.
The full review schema embeds the governance schema with only local `$defs`
namespacing, so standalone JSON Schema validation needs no network resolver.
Consumers should reuse `governance_contract()`; its process cache is
`sys.modules['egohygiene_hygiene_architecture_coherence_' + full_owner_sha]`
with checked `__owner_revision__` and `__owner_helper_sha256__` attributes.
This preserves the same typed evidence class across standalone owner imports.

The helper raises bounded `ContractError` codes and never includes rejected
payload text in diagnostics. A valid record establishes shape/bindings, not
source authenticity, judgment quality, public membership, or human authority.

## Record shape and bounds

All top-level members are required and unknown members rejected: schema,
contract_version, id, visibility, scope, represented_revisions, generated_at,
reviewer, execution, sources, explanation, components, relationships,
dimensions, assumptions, strengths, concerns, questions, alternatives,
recommendation, governance. Empty lists/unknown outcomes preserve absence of
evidence honestly; complete execution requires one target source at its exact
revision and all seventeen dimensions. A complete review can still contain
unknown dimensions.

Stable row IDs identify sources, components, relationships, assumptions,
strengths, concerns, questions and alternatives. Evidence lists reference
source IDs; relationships reference components and consequential concerns
reference alternatives. Sources separate canonical/implementation/human-record/
prior-ai-review/external origins. Claims requiring evidence cannot rely only
on earlier AI reviews.

Scope repositories and represented revision rows are sorted and unique. A
repository/subsystem scope contains one repository; its key is the repository
or `<repository>:<subsystem-slug>`. An organization key is its organization and
all repositories belong to it. Sources may also refer to separately versioned
canonical owners outside the represented target scope.

Source URLs reject credentials, queries, percent encoding, ambiguous path
traversal, unsafe fragments, local hostnames and non-global/ambiguous numeric
addresses. HTTPS alone does not authenticate a source or establish that a DNS
name is public; public admission remains a separate trusted-caller obligation.

The assessment supports general/private local authoring with governance null.
The initial pinned Hygiene evaluator is a public Ego Hygiene profile. A
non-null governance record requires an independently authenticated
`public_repositories` set; the helper never derives it from the record itself.
The list is trusted caller context, not an artifact's self-assertion. Public
projections must authenticate every scope and source owner before reading
review identities, text, counts or hashes. Do not pass an untrusted list from
the review as this context. Private/mixed reviews cannot be relabelled as a
public subset of the same review.

## Exact immutable digest

Remove only the top-level `governance` member, then encode the remaining JSON
with Python's `json.dumps(sort_keys=True, separators=(',', ':'),
ensure_ascii=False, allow_nan=False).encode('utf-8')`, without a trailing
newline. SHA256 of those bytes is `assessment_sha256`. Arrays and text are not
trimmed, case-folded or sorted. The digest includes execution, completion time,
sources, findings and recommendation. Governance review_ref and human_decision
bind this digest and the exact ID/scope/revisions; they do not hash themselves.

## Trusted human import

The only trusted context is an instance of the pinned Hygiene module's
immutable `TrustedHumanEvidence(statement_sha256, capture_sha256)`. A privileged
source adapter/operator constructs it only **after** independently verifying
authentic human provenance, authority and the exact statement. The type checks
binding and makes the trust boundary explicit; it performs no authentication
and is not a cryptographic boundary against code with constructor access.

No JSON decoder, actor kind, provider boolean, URL, merge, silence, ongoing
implementation, AI recommendation or self-asserted digest can create this
context. The capture digest is operational/private and is not emitted by
evaluation. Callers must retain actual immutable human evidence under their
own privacy/retention policy. This source change creates none.

Material-change inventories are separate evaluation inputs. Unknown/partial
inventory does not prove current freshness. Ordinary Git revision differences
remain distinct from scoped architecture materiality. Explicit human
invalidation also requires separately trusted human evidence. Historical human
disposition is retained independently from current/stale/unknown freshness.

## Qualification and ownership

Hygiene owns applicability/governance policy; Aether owns the complete
assessment/procedure; Observatory owns normalized queries; Relay owns
delivery/rendering; Reflector owns orchestrated campaign/continuation.
The policy remains proposed until explicit owner selection. No default blocker,
exception, architecture approval, or fictional ratification is introduced.

For this implementation batch the user deferred behavioral tests, skill evals,
native runs, builds and CI. Static syntax/schema/source review does not qualify
those paths. Root integration owns generated catalog/dist metadata, continuity
and the shared proposed decision record. Refs Aether #87, not issue closure.
