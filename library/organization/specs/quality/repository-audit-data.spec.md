---
schema: aether.specification/v1
id: repository-audit-data
title: Composable Audit Profiles and Checkpoint Data
kind: specification
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-11-09
updated: 2026-11-09
domain: quality
tags:
  - audit
  - profiles
  - evidence
  - provenance
  - read-only
applies_to:
  - repository-audits
  - organization-audits
  - checkpoint-sidecars
depends_on:
  - specfile
  - auditor
related:
  - audit-repository
  - reflector
supersedes: []
source_files:
  - repository-audit-data.spec.md
---

# Composable Audit Profiles and Checkpoint Data

## Authority and maturity

This draft extends the approved `auditor` specification 2.0.0 with a portable
machine projection and intent profiles. The approved specification retains its
exact source and human lifecycle; this draft neither amends its approval nor
promotes the `audit-repository` skill or auditor agent. Normative machine
contracts are `aether.audit-profile-registry/v1` and
`aether.repository-audit-report/v1`, each contract version `1.0.0`.

The canonical Markdown report remains the explanation and evidence narrative.
The JSON sidecar projects that same authored finding model; it cannot rewrite
history, supply missing evidence or authorize any action. Machine validity is
structural admission, not proof that observations, execution, severity, policy
interpretation, reported resolution or human acceptance are true.

## Canonical sources

- `catalog/schemas/aether.audit-profile-registry.v1.schema.json`
- `catalog/schemas/aether.repository-audit-report.v1.schema.json`
- `library/organization/skills/quality/audit-repository/references/audit-profiles.v1.json`
- `library/organization/skills/quality/audit-repository/scripts/audit_contract.py`

The schemas own closed data structure. The standalone standard-library helper
owns exact profile resolution and cross-field reference semantics. Consumers
pin these public resources together to one immutable Aether revision and
verify exact source bytes before importing the helper. The helper performs no
provider discovery, repository scan, command execution, issue mutation or
artifact publication.

## Profiles and composition

Each registry entry records ID/version, leaf/composite kind, stable/experimental
intent, focus, applicability evidence, required evidence classes, exclusions,
composed profile references and permitted finding natures. These are small
selectors over one generic audit procedure, not duplicated auditor prompts.
Actual organization applicability and conformance policy remain Hygiene's.

Initial leaf profiles:

| ID | Focus | Distinction |
| --- | --- | --- |
| `feature-opportunity` | Useful capabilities, integrations, workflows and ergonomics | An opportunity is not an existing requirement or a defect. |
| `experimental-opportunity` | Speculation, research and prototype ideas | Explicit opt-in; informational recommendations remain unverified/recommended. |
| `implementation-quality` | Bugs, reliability, tests, automation, security/privacy, performance, maintainability and documentation | Use observed evidence and explicit execution limits. |
| `contract-drift` | Required artifacts, generated drift, ownership, declared integrations and lost capabilities | A policy failure requires explicit observed policy evidence. |

`holistic` composes all stable leaf profiles in the selected registry. It does
not copy their instructions or silently include experiments. Several explicit
requests, including `holistic` plus `experimental-opportunity`, resolve to one
sorted unique leaf set. Every finding keeps its original exact leaf profile;
overlapping findings are not silently merged or reclassified. A future stable
leaf must be added to the reviewed holistic composition. New domains do not
require a new core finding schema.

`stable` describes profile intent, independently of the registry's **draft**
authoring lifecycle. It does not claim a release, approved profile policy,
deterministic qualification or installed host capability.

## Scope and completion

A report declares one repository or an explicit organization repository roster,
with each exact represented commit and visibility. Included, excluded,
inspected and uninspected scope are distinct. Missing or private repositories
are not inferred from a public count. Consumers authenticate target membership
and visibility before reading identities, counts, findings, hashes or links;
Aether's declared visibility alone cannot establish provider identity.
Structured evidence and URI owners also require admission before any full
report digest. The helper's `referenced_repositories` extraction does not
authenticate membership or make arbitrary narrative text public.

Profile completion states are `complete`, `partial`, `blocked`, `failed`,
`unsupported`, `not_applicable` and `unknown`. Every resolved leaf has a state
and non-complete reason. The overall state is a deterministic scope rollup:
any failed profile makes it failed; all not-applicable profiles make it
not-applicable; excluding not-applicable entries, one shared state is preserved
and mixed states are partial. Complete means the declared applicable scope was
inspected, with no uninspected scope; it never means passed, conformant,
ratified, free of findings, deployed or installed. Unknown completion can omit
its completion timestamp; other completed sidecars retain an actual timestamp.
A not-applicable leaf cannot be the originating profile of a finding.

## Findings and evidence

Every nontrivial finding retains `AUDIT-NNN`, visibility, represented repository,
title, approved observation classification, nature, severity, confidence,
status, area, effort, impact, observation, significance, recommendation,
suggested validation, dependencies, evidence references, exact source profile,
missing evidence and explicit history metadata. Classification slugs are the
approved observation names with spaces replaced by hyphens; lifecycle/status
vocabularies otherwise remain independent of severity or impact.

Finding nature separates defects, opportunities, experimental opportunities,
policy/conformance observations, risks, clarifications and strengths. Positive
observations are indexed by their finding IDs; absence requires a stated reason.
Low-confidence and unverified/recommended findings state missing evidence.
Confirmed findings require observed evidence. Experimental findings stay
informational, recommended/unverified, and never confirmed defects. An absent
feature is not promoted to a policy failure or a blocking production gap.

Evidence records have stable IDs, observed/inferred/recommended/unverified
labels, source kind, optional repository/revision, credential-free HTTPS URI or
repository-relative path, optional SHA-256, actual observation time and bounded
summary. Source evidence carries its exact repository and revision. No command
output, file position, exploitability or human intent is invented. Provenance
lists tool versions, executed/failed/not-run/unavailable/unsupported commands,
actual exit codes when known, evidence references, limitations and redactions.
Unknown or unrun checks are never counted as successful execution.

## Canonical report, sidecar and immutable history

Write a new `audits/{audit-name}-{utc-timestamp}.md` narrative and matching JSON
sidecar only through an explicitly authorized output writer. The read-only
agent otherwise returns candidates to that writer; it gains no edit or execute
tool by selecting a profile. Never replace an existing report or sidecar.
The sidecar's canonical report reference binds the Markdown path and actual
file SHA-256, plus an immutable URI when available. It does not contain its own
future Git commit or pretend a pre-commit URI exists. Raw file hashes, canonical
JSON digests, upload ZIP digests and represented source revisions are distinct.
Consumers separately verify actual report bytes and immutable source identity.

Known prior audits retain their IDs, exact artifact hashes and predecessor or
related relationship. Finding history explicitly labels new, unchanged,
improved, regressed, resolved, unverified or not-compared state, prior audit and
finding identity when known, evidence classification and supporting references.
No disappearance, missing capture, changed title or later timestamp implies
resolution. Reported resolution requires an observed prior relationship and
prior-audit evidence bound to its selected hash and URI/local path, together
with distinct observed comparison evidence at the current represented revision;
structural validation cannot verify the resolution claim. Historical source
reports remain untouched.

Candidate issues are suggestions only, with source finding IDs, priority,
outcome, acceptance criteria and dependencies. Their sole status is
`suggested`. No issue URL or created/closed lifecycle is manufactured. Actual
issue creation or remediation needs a separately authorized owning workflow.

## Owners and downstream boundaries

Aether owns this portable data/specification/procedure. Hygiene owns
organization applicability, public admission and conformance policy. EgoLint
owns production validation integration; this reference helper is no substitute
for released EgoLint qualification. Relay owns immutable execution/delivery,
Reflector owns campaign orchestration, Observatory owns normalization and
portfolio queries, Holon owns presentation primitives, Empathy composes generic
consumer scaffolding and Pace observes rollout. A report or campaign manifest
cannot claim organization-wide adoption, human ratification or automatic merge.

Legacy Markdown is not silently scraped or upgraded. New sidecars need the
actual original report bytes and explicit authored scope/profile/evidence
metadata. Consumers preserve old reports and reference their limitations while
adopting this separately pinned interface. Product-specific agents, tools and
paths are not imported into the portable contract.

## Qualification remaining

The staged/canonical source reconciliation is recorded in the skill's
`references/staged-reconciliation.md`; historical staged files are retained.
Single/multi-profile, holistic, experimental, partial, blocked, unsupported,
not-applicable, stale evidence and malformed-input fixtures, dependency-graph
validation, consumer host/discovery execution and deterministic qualification
remain deferred. Source/schema inspection and generated catalog/distribution
bytes do not promote any draft artifact or prove those behaviors.
