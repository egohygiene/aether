# Architecture portability source history

Existing owner: [Aether #38](https://github.com/egohygiene/aether/issues/38).
Pre-change source: `dc3549c8a23bed5fb551a458a22605e7e0777822`.

The [inventory](source-before.json) binds six exact original Git blobs to their
repository-only archives: both skills, their evaluation definitions and the two
authored architecture specifications. Original locators, dates, versions,
requirements and migration wording remain inspectable there and in Git. These
archives are not included in the installed packages or treated as new authority.

## Authored source editions

| Source | Before | Candidate | Bounded change |
| --- | --- | --- | --- |
| `architecture-authoring` | draft1.1.0 | draft1.2.0 | Resolve the existing parent, set contract and structural schema from selected package resources; preserve unresolved migration obligations. |
| `create-architecture-document` | draft1.1.0 | draft1.2.0 | Resolve the same governing resources plus its document-specific contract. |
| `architecture-document` | draft2.1.0 | draft2.1.1 | Clarify stable identity versus source/installed layout, retain related families, and expose existing schema/set resources through valid relative links. |
| `architecture-architecture` | draft1.1.0 | draft1.1.1 | Repair its stale conformance locator with a versioned parent identifier and a relative resource link. |
| `architecture-set` | draft1.0.0 | unchanged exact bytes | Deliver the already-required set selection contract. |
| `architecture-document.schema.json` | existing v1 identity | unchanged exact bytes | Deliver the already-required structural authority. |

The evaluation revision fields follow each skill's1.2.0 version; their existing
cases remain unchanged. Artifact metadata revisions do not create repository
tags/releases or establish stable eligibility, approval or model performance.

## Requirement and placement map

The parent standard already requires stable artifact identifiers, declared
dependencies, canonical ownership, explicit uncertainty and validation. Its
metadata says directory placement cannot replace artifact metadata. The new
source edition applies that existing distinction to installed projections.

| Original source concern | Candidate treatment |
| --- | --- |
| Organization-owned specifications beneath `library/organization/specs/architecture/` | Same canonical sources and owning catalog/architecture; installed projections locate the same governed IDs without cloning that source hierarchy. No source moves or new canonical location. |
| Related skills, agents, prompts, instructions and policies under their original `library/organization/` families | The same five semantic families remain explicit; exact former publisher locators are retained in the original archive. No neighboring ownership transfer. |
| Child conformance to `.github/specs/architecture/document.spec.md` | Stable `architecture-document`2.1.1 and `../document.spec.md`; the latter resolves from both the canonical child hierarchy and its corresponding package hierarchy. |
| Parent structural schema and set-level selection requirements | Same schema and `architecture-set`1.0.0 bytes, now packaged with their referring parent. |

Every tagged `REQ`, `CON`, `GUD` and `AC` paragraph remains byte-identical.
All original specification metadata other than revision/update date remains
unchanged, including IDs, owners, creation dates, lifecycle, dependency graph,
related IDs and supersession. Source `set.spec.md`, schema, `DECISIONS.md` and
the actual staged architecture candidate match the recorded unchanged hashes.
The validator, builder and installed-host adapter are not weakened or rewritten.

This is an authored draft correction, not a generator that strips/encodes
source strings. The existing builder copies each selected governing resource
byte-for-byte. Scoped `.gitattributes` preserve those exact resource bytes and
allow their pre-existing terminal blank lines while keeping other whitespace
checks active. Missing resources still fail strict package checks.

## Historical comparison identity remains unresolved

The original architecture skill names a same-named staged candidate under
`.staging/skills/architecture-authoring/` and says internal “Issue016” should
compare it before retirement. Its exact original wording and locator remain in
[the archived skill](source-before/architecture-authoring.SKILL.md).

That ordinal has no verified current provider mapping in this checkpoint. It
must not be turned into a GitHub issue URL or interpreted as completed review.
The portable summary preserves the candidate identity, possible divergent
content, unique-guidance comparison obligation and prohibition on wholesale
replacement. It explicitly supplies no promotion, retirement or deletion.
Issue38 owns this portability repair; it does not replace the unresolved
comparison identity or ADR-0005's human review/deletion gate.

## Decisions and remaining acceptance

Reference preserved ADR-0001/0002/0004/0005 for canonical/generated ownership,
neighboring owners, artifact-versus-release versions and staging preservation.
No new artifact type, source location, distribution channel, lifecycle or
approval authority is selected. Historical ADR-0002/0006 and proposed ADR-0009
remain unchanged. The [validation record](VALIDATION.md) retains exact executed
source and remaining local/remote/release boundaries.
