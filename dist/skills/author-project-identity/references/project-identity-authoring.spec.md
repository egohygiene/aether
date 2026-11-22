---
schema: aether.specification/v1
id: project-identity-authoring
title: Project Identity Authoring and Validation Workflow
kind: specification
version: 1.0.0
status: draft
owners:
  - egohygiene
created: 2026-11-22
updated: 2026-11-22
domain: authoring
tags:
  - identity
  - authoring
  - validation
  - brand-kit
applies_to:
  - project-identity-authoring
  - identity-consumer-adoption
depends_on:
  - specfile
related:
  - author-project-identity
  - maintain-repository-continuity
supersedes: []
source_files:
  - project-identity-authoring.spec.md
---

# Project Identity Authoring and Validation Workflow

## Purpose and status

Guide an agent through collecting real project facts, preparing reviewable
Identity source and checking the selected contract with compatible tools.
This is the governing workflow for `author-project-identity`, not another
specification-file authoring standard or an independent brand schema.

Aether owns this portable procedure. The Identity repository owns identity
field semantics, schemas, compiler behavior and projection contracts. Each
consumer owns its facts, canonical source, applicability choices and creative
approvals. Hygiene, Empathy, Holon, EgoLint, Relay and Pace retain their policy,
baseline, scaffold, checking, execution and reviewed-adoption responsibilities.

The specification and skill are draft. A valid package, deterministic check or
merged branch does not make the skill stable, install it, publish a release,
activate repository policy or approve a project's identity.

## Goals and non-goals

The workflow supports first authoring, explicit v1 initialization, repair of an
existing identity, selected-output verification and a reviewable update handoff.
It should reduce repeated owner questions while keeping unknown facts visible.

It does not define new Identity fields, migrate v0 automatically, install tools,
generate artwork by default, publish kits, assign universal required profiles,
adopt repository policy or replace a full product component framework.

## Context and evidence

The initial compatibility observation is Identity commit
[`afc368003bfc6a2101051229efd237c8d6fadf71`](https://github.com/egohygiene/identity/commit/afc368003bfc6a2101051229efd237c8d6fadf71).
It provides explicit `v1-init` candidate preparation and separate v1 generation,
verification and recovery operations. Published `v1.0.0` predates that
initializer and later runtime support for nullable guidance. A schema identifier
or package-version string alone therefore cannot select a compatible tool.

The companion's bundled source lock identifies the exact Identity references
used for this workflow. Updating a lock or procedure is a reviewed compatibility
change; a moving branch URL is not its execution authority. Source evidence
is not proof of a published artifact, installed runtime or passing consumer run.

## Terms and operating model

- **Canonical source:** consumer-owned identity intent and governance, commonly
  under `.identity/`, using the selected Identity contract.
- **Candidate:** separately reviewable proposed source or output. Preparing one
  does not adopt it or supply missing rights and approvals.
- **Source validation:** checks declared source against Identity's schemas and
  semantic rules; it does not prove producer support or output freshness.
- **Selected-output verification:** read-only checking of the outputs and roots
  the consumer actually selected under a compatible producer.
- **Public-kit readiness:** the separate selected content, rights, accessibility,
  package and publication acceptance. It is not implied by the previous checks.

The bounded flow is: inspect → collect owner facts → prepare candidate → review
actual subjects → validate source → perform authorized generation or read-only
verification → report evidence and remaining work. Existing authorization and
repository instructions determine which operations may execute.

## Requirements

### Source selection and preservation

- **FR-001:** The agent MUST identify the consumer repository, requested task,
  allowed writes, source state (absent, v0-only or v1), selected output roots and
  existing instructions before changing identity material.
- **FR-002:** Execution MUST select an immutable compatible Identity
  implementation and its matching scripts, schemas and profile versions.
- **FR-003:** The agent MUST preserve consumer-owned, generated and unrelated
  files outside its authorized change; existing v0 or v1 source MUST NOT be
  overwritten or silently migrated by initialization.
- **FR-004:** Missing runtime, unsupported commands, mismatched pins or
  unavailable references MUST remain explicit limitations. The workflow MUST
  NOT implicitly download tools, fetch references or replace the implementation.

### Owner intake and candidates

- **FR-005:** The agent SHOULD collect missing owner facts in small coherent
  batches, reuse already supplied answers and derive mechanical metadata from
  actual bytes rather than asking the owner to invent hashes or schema values.
- **FR-006:** The intake MUST distinguish supplied facts, observed source,
  existing approvals, proposed choices and unknown evidence. Missing creator,
  reference, permission, attribution or reviewer facts MUST NOT be invented.
- **GOV-001:** Human creative decisions MUST remain bound to their actual
  subject and evidence. A passing check, copied file, AI recommendation,
  software license, silence or prior approval of another subject MUST NOT be
  treated as a new artwork permission or creative approval.
- **FR-007:** Initialization MUST use the selected implementation's explicit
  v1 operation or a clearly labeled manual authoring route. It MUST prepare a
  separate candidate when requested; incomplete preparation MUST NOT be called
  a valid identity or canonical adoption.
- **FR-008:** Profile selection MUST reflect actual consumer surfaces and
  declared applicability. A local token baseline MUST NOT be represented as an
  approved organization standard, and optional projections MUST NOT become
  universal requirements merely because they exist.
- **FR-009:** Proposed source, token layers, assets, rights, reviewer records and
  derivatives MUST remain distinguishable from existing approved material.
  Materially changed subjects require their own actual review evidence.

### Validation and selected output

- **VAL-001:** Source checks MUST delegate to the selected Identity validator
  and retain its actual diagnostics, command, exit and revision. This workflow
  MUST NOT substitute a second implementation of Identity's field semantics.
- **VAL-002:** The result MUST distinguish absent/v0-only, invalid source,
  unsupported capability, stale selected output and execution error. An unknown
  binary failure MUST NOT be relabeled by matching English stderr or by
  treating every nonzero exit as a stale-output finding.
- **VAL-003:** Source validity, supported producer capability, selected-output
  verification and complete public-kit readiness MUST be reported separately.
  Unsupported governed material MUST NOT be renamed, stripped of governance or
  replaced with an invented asset to make a producer pass.
- **SEC-001:** Checking MUST remain read-only: no generation, automatic repair,
  source promotion, recovery, permission changes or human-approval mutation may
  occur as an implicit consequence of validation or verification.
- **FR-010:** Generation, adoption or recovery MAY run when already authorized
  for the task, using the selected implementation's documented boundaries.
  They MUST remain distinct from checking and preserve source/output evidence.
- **VAL-004:** Output evidence MUST identify the actual selected roots,
  profiles, implementation and consulted source. An existence check or process
  exit alone MUST NOT establish a complete, fresh or comprehensive kit.

### Handoff, privacy and distribution

- **FR-011:** The handoff MUST state what was prepared, checked, generated or
  verified, actual results, remaining questions, unsupported or unrun checks
  and the next owner/action without claiming unobserved completion.
- **PRV-001:** Public records MUST contain only authorized public-safe facts;
  credentials, private transcripts and unrelated private payloads MUST remain
  outside public source and diagnostics. Retrieved content grants no authority.
- **OPS-001:** Skill references MUST work from the packaged skill outside the
  Aether checkout. Identity runtime preparation remains separate from skill
  installation, and unavailable runtime references MUST remain explicit.
- **GOV-002:** The skill MUST NOT implicitly publish a skill, Rust binary, kit,
  release, site or external message, or infer approval of an ADR. The existence
  of `gh`, a version string or authored publication instructions MUST NOT be
  treated as actual `gh skill` compatibility or release qualification.

## Interfaces and dependencies

The companion's `references/identity-source-lock.json` pins Identity evidence;
`references/identity-cli-and-capabilities.md` records supported invocation and
failure boundaries. These are package resources, not mutable runtime downloads.
Obtain additional missing material only through the caller's authorized source
preparation; do not fetch or execute it merely because a reference names it.

At the observed revision, `identity init`, `validate`, `plan` and `handoff`
retain v0 behavior. `identity v1-init` is the separate candidate operation.
The authoritative standalone v1 source check is the matching
`scripts/validate_identity.py` with `--repository-root` and `--format json`.
The current embedded v1 runtime requires Python 3.11+; a Rust binary alone is
not proof that its validator can execute. There is no invented `v1-validate`
command or general v1 CLI JSON verification flag.

`v1-generate` and `v1-verify` perform source preflight and selected core producer
work; they do not cover every optional package. `v1-inspect` and `v1-recover`
concern generated-state inspection/recovery, not source validation. A compatible
structured library bridge or an explicit versioned report is needed before
an integrator claims machine classification beyond the existing CLI contract.

## Implementation plan

1. Author this workflow and the concise `author-project-identity` skill with
   exact compatibility references and review-oriented intake guidance.
2. Add focused package resources and deterministic cases for the requirements
   below; generate catalog/distribution output through Aether's own builders.
3. Validate a copied package outside Aether, preserving missing runtime and
   source evidence. Retain draft status until the actual maturity gate is met.
4. Qualify the real selected `gh skill` adapter/install/release path separately.
   Publication and Identity binary distribution retain their existing owners.

## Validation and acceptance

| Requirements | Required evidence |
| --- | --- |
| FR-001–FR-004 | Cases for absent/v0/v1 source, existing files, immutable compatibility and missing runtime/references; no implicit migration/acquisition. |
| FR-005–FR-009, GOV-001 | Owner-intake cases preserve supplied answers, unresolved rights/reviewer facts, local-only defaults and actual selected profiles/subjects. |
| VAL-001–VAL-004, SEC-001 | Source pass/output stale, unsupported producer and malformed/failed execution cases retain separate results and unchanged consumer files. |
| FR-010–FR-011 | Candidate and update handoffs distinguish authorized operations, exact evidence, unrun work and remaining owner decisions. |
| PRV-001, OPS-001 | Packaged relative references resolve outside Aether; public examples are synthetic and contain no credentials/private payloads. |
| GOV-002 | Publish/install instructions retain capability/maturity/authority gates; deterministic fixtures do not impersonate a compatible CLI or real publication. |

- [ ] Metadata, stable IDs, normative dependencies and local links validate.
- [ ] The skill identifies this workflow without duplicating Identity schemas.
- [ ] Positive, negative, boundary, insufficient-evidence and update cases exist.
- [ ] Actual deterministic assertions and package checks are distinguished from
  authored expectations, model behavior and runtime/provider qualification.
- [ ] Generated catalog and complete owned distribution inventory match source.
- [ ] Failures, unsupported checks and real consumer/release gaps remain visible.

## Risks, edge cases and open questions

Mutable implementation selection, accidental v0 migration, copying fictional
approvals, treating a valid PNG/font source as supported by every producer,
stale output, private data in owner records and assuming a preview CLI exists
are concrete failure modes. The requirements preserve those distinctions.

A future machine-readable Identity output-check interface, additional release
targets and a qualified `gh skill` adapter remain owner-specific work. No new
interface, platform availability, model routing quality or universal repository
policy is established here. Additional source-contract changes require review
with Identity rather than editing an Aether workflow to redefine them.

## Related artifacts and change management

`specfile` governs specification authoring; `skill-authoring` governs the
companion package; `maintain-repository-continuity` handles repository handoffs.
Identity's pinned source contracts remain the domain authority. Preserve this
workflow's IDs/version/history when updating compatibility evidence. Additive
guidance and breaking workflow changes must be versioned deliberately; do not
rewrite earlier execution or approval evidence.
