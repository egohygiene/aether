# DECISIONS.md — Architectural Decision Records

> **Document owner:** This file  
> **Related:** [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`PURPOSE.md`](PURPOSE.md) · [`SYSTEM.md`](SYSTEM.md) · [`ROADMAP.md`](ROADMAP.md)

---

## How to Use This Document

Each ADR answers one focused question.  Read the decision and consequences
before implementing anything it covers.  Propose amendments by opening a pull
request; do not edit past decisions in place—append a superseding ADR instead.

---

## ADR Index

| ID | Question | Status |
|---|---|---|
| [ADR-001](#adr-001) | Canonical source vs. generated distribution | Accepted |
| [ADR-002](#adr-002) | Aether vs. neighboring repositories | Accepted |
| [ADR-003](#adr-003) | First-party vs. external artifact ownership | Accepted |
| [ADR-004](#adr-004) | Repository-release vs. per-artifact versioning | Accepted |
| [ADR-005](#adr-005) | Staged-material lifecycle and deletion gate | Accepted |
| [ADR-006](#adr-006) | Whether generated `dist/` content is committed or release-only | Accepted |
| [ADR-007](#adr-007) | Staged hook prototype disposition for first release | Accepted |

---

## ADR-001

**Question:** Where does canonical source live, and how is it distinguished from generated distribution?

**Date:** 2026-08-08  
**Status:** Accepted

### Context

The repository contains hand-authored specifications and skills under
`library/organization/`.  Future consumers will need installable artifacts
without cloning the entire tree.  There is a risk that generated indexes or
distribution bundles could be confused with authoritative source.

### Decision

`library/organization/` is the **sole canonical source**.  Generated artifacts
(catalogs, distribution bundles) are placed in `dist/` and are **never
hand-edited**.  Every generated file carries a machine-readable header or
filename convention indicating it is generated.

### Alternatives Considered

- **Single-directory model:** Merge canonical and generated content in one
  location.  Rejected because it makes it impossible to distinguish
  authoritative files from assembled ones.
- **Generated content only in releases:** Consistent with ADR-006; not mutually
  exclusive with this decision.

### Consequences

- Contributors editing `dist/` files will be correcting the wrong source.
- CI (when built) must regenerate `dist/` rather than accept manual edits.
- Any file not in `library/organization/` or explicit root governance documents
  is presumed non-authoritative.

---

## ADR-002

**Question:** Which responsibilities belong to Aether and which to neighboring repositories?

**Date:** 2026-08-08  
**Status:** Accepted

### Context

The Ego Hygiene organization has multiple repositories with overlapping scope
potential.  Without an explicit split, contributors will place artifacts in the
wrong repository or duplicate effort.

### Decision

Aether owns **reusable specifications, skills, agent source, schemas, catalogs,
and distributions**.  The following table is binding:

| Concern | Owner |
|---|---|
| Reusable specifications, skills, agent source, schemas, catalogs, distributions | **Aether** |
| Organization custom-agent deployment and Copilot policy | `egohygiene/.github` and GitHub organization settings |
| Universal repository baseline | Empathy |
| Repository creation/customization | Holon |
| Development environment and installed toolchain | Realm |
| Portable shell commands | Mantle |
| Lint/static-check implementation | Egolint |
| Reusable GitHub Actions | Relay |
| Conformance and drift | PACE |
| Mind Garden domain contracts | Mindgarden |
| Flutter application contracts | `egohygiene` application repositories |
| Video/animation compiler contracts | Aniflow or Flow |

### Alternatives Considered

- **Monorepo for all concerns:** Would eliminate cross-repository references but
  create an unmanageable single repository.  Rejected.

### Consequences

- Pull requests that add CI workflows, organization deployment config, or
  toolchain setup to Aether are out of scope and should be redirected.
- Neighboring repositories listed above do not yet exist or are not yet
  operational.  Their absence does not transfer their responsibilities to Aether.

---

## ADR-003

**Question:** How are first-party and external artifacts distinguished?

**Date:** 2026-08-08  
**Status:** Accepted

### Context

`.staging/` contains material from multiple owners and lifecycle states.
Some files originate outside the organization.  Without a classification rule,
it is impossible to determine which files are governed by Aether quality
standards.

### Decision

| Classification | Definition | Location |
|---|---|---|
| First-party | Authored or explicitly adopted by Ego Hygiene contributors | `library/organization/` |
| External | Imported from outside the organization; origin documented | Planned `library/external/` subtree (not yet created) |
| Staged | Unreviewed; provenance not yet confirmed | `.staging/` |
| Generated | Assembled from canonical source by build tooling | `dist/` (not yet created) |

No file in `.staging/` is first-party until it passes review and is promoted
into `library/organization/`.

### Consequences

- External skills or specifications added without review are staged, not
  first-party.
- A planned `library/external/` directory will hold reviewed external material
  alongside its origin record.

---

## ADR-004

**Question:** Should Aether use repository-level releases or per-artifact versioning?

**Date:** 2026-08-08  
**Status:** Accepted

### Context

Individual skills and specifications carry their own `version` field in front-
matter.  Distributions could be versioned at the repository level (one release
tag covers all artifacts at that point in time) or per artifact (each skill has
independent release tags).

### Decision

Aether uses **repository-level releases** as the primary distribution versioning
mechanism.  The repository tag (e.g., `v0.1.0`) identifies a snapshot of all
canonical artifacts.

Individual artifact `version` fields in front-matter are **informational** and
record the artifact's own revision history, but do not drive distribution
tagging.

### Rationale

Repository-level releases are simpler to implement, easier for consumers to
reason about ("install Aether v0.2.0"), and consistent with how most library
repositories operate.  Per-artifact versioning adds complexity without a
demonstrated consumer need at this scale.

### Alternatives Considered

- **Per-artifact versioning:** Allows fine-grained consumer dependencies.
  Deferred until a consumer requires it; may be revisited in a future ADR.

### Consequences

- Bumping any artifact's front-matter version does not trigger a release.
- Releases are tagged at the repository level by a maintainer.

---

## ADR-005

**Question:** What must happen before `.staging/` may be emptied?

**Date:** 2026-08-08  
**Status:** Accepted

### Context

`.staging/` holds 936+ files from multiple owners and lifecycle states.
Deleting them without review would destroy potentially valuable work.

### Decision

**Deletion gate:** No file may be removed from `.staging/` until all of the
following conditions are satisfied for that file:

1. Its content has been reviewed by a human contributor against the relevant
   Aether specification (or explicitly waived as out of scope).
2. It has been either:
   - Promoted into `library/organization/` (first-party adoption), or
   - Placed in a planned `library/external/` path with origin documented, or
   - Explicitly rejected with a recorded reason in a pull request or issue.
3. The pull request that removes the file references this ADR.

Mass deletion without individual review is not permitted.

### Consequences

- `.staging/` will not be empty until a dedicated review phase is complete.
- This issue (issue 002 and later) must not move or delete `.staging/` content.

---

## ADR-006

**Question:** Should generated `dist/` content be committed to version control or published as release-only artifacts?

**Date:** 2026-08-08  
**Status:** Accepted

### Context

Some repositories commit generated output (e.g., `dist/`) to allow consumers to
reference it without running a build.  Others exclude generated content from
version control and publish it only as release artifacts.  Committing generated
content risks stale diffs and confusion with canonical source.

### Decision

Generated `dist/` content is **release-only** and is **not committed** to
version control.

`dist/` is excluded from version control via `.gitignore` once the build
process exists.  Consumers obtain distribution artifacts exclusively from
GitHub Releases.

### Rationale

- Committed generated content creates stale-diff noise and tempts hand-edits.
- Excluding `dist/` from version control enforces the canonical source boundary
  established in ADR-001.
- GitHub Releases provide an appropriate versioned distribution channel.

### Alternatives Considered

- **Commit `dist/` to a dedicated branch:** Avoids noise on the default branch
  but adds complexity.  Not justified at current scale.

### Consequences

- The `dist/` directory does not yet exist.  When build tooling is introduced,
  it will add `dist/` to `.gitignore` at that time.
- Consumers cannot reference `dist/` via raw GitHub URLs on the default branch.

---

## ADR-007

**Question:** What disposition applies to each staged hook prototype for the first Aether release?

**Date:** 2026-08-09
**Status:** Accepted

### Context

Issue 015 required an audit of all staged hook prototypes against security,
privacy, portability, testability, and ownership criteria.  Hooks execute code
at an agent trust boundary and are held to stricter requirements than passive
skill instructions.

The staged hooks are:

| Prototype path | Candidate use |
|---|---|
| `.staging/hooks/dependency-license-checker/` | License compliance gate at session end |
| `.staging/hooks/fix-broken-links/` | Link validation and repair |
| `.staging/hooks/governance-audit/` | Repository governance logging |
| `.staging/hooks/secrets-scanner/` | Secret detection at session end |
| `.staging/hooks/session-auto-commit/` | Automatic commit at session end |
| `.staging/hooks/session-logger/` | Prompt and session content logging |
| `.staging/hooks/tool-guardian/` | Pre-tool-use threat screening |
| `.staging/integrations/github-copilot/hooks/` + `scripts/` | GitHub Copilot-specific wiring |

Observed concerns included: obsolete monolith paths; non-portable `date --date`
(GNU-only); non-executable `.sh` files; unsafe universal auto-commit; raw
prompt logging; overlap with Egolint/Relay responsibilities; and absent tests,
threat models, and PowerShell parity.

### Decision

**No staged hook prototype is promoted to a first-party Aether release artifact
in this issue.**

Each prototype receives the following disposition:

| Prototype | Disposition | Owner | Rationale |
|---|---|---|---|
| `dependency-license-checker` | **move-out** | Egolint | License scanning is a lint concern; duplicating it in a hook creates two conflicting authorities. |
| `fix-broken-links` | **move-out** | Egolint | Link checking is a lint concern owned by Egolint; hook delivery channel is Relay. |
| `governance-audit` | **reject** | — | References obsolete monolith paths (`mindgarden`, `tools/mindcap`); silently fails open when `jq` is absent; logs working-directory path at session start, which may reveal private information. |
| `secrets-scanner` | **move-out** | Egolint | Secret scanning is a security-lint concern owned by Egolint; duplicating scanners in hooks creates false confidence. |
| `session-auto-commit` | **reject** | — | Auto-commit is unsafe as a universal default; violates the explicit non-goal in the issue. Must not be distributed as a default. If retained as research it stays in `.staging/` and is excluded from distributions. |
| `session-logger` | **reject** | — | Logs raw prompts, environment content, and working-directory paths by default, which captures private material without consent. |
| `tool-guardian` | **needs-human-review** | — | Closest to a justified Aether provider adapter (pre-tool-use safety screening), but contains regex-injection risk in the pattern-matching loop and has no tests or PowerShell parity. Deferred to a subsequent issue after human review. |
| `integrations/github-copilot/hooks/` + `scripts/` | **reject** | — | `session-start.sh` hard-codes a `Taskfile.yml` dependency absent from the repository; uses GNU `date --date` (non-portable to macOS BSD `date`); `.sh` files are not executable in the snapshot; `pre-tool-use.sh` lacks validation fixtures; no PowerShell equivalence is verified. |

### Rationale

- Rejecting or deferring all prototypes is preferable to releasing unsafe hooks
  under time pressure.
- Move-out dispositions correctly attribute ownership without deleting staging
  evidence prematurely (ADR-005 deletion gate).
- `tool-guardian` is the only prototype with a plausible Aether-first-party
  justification, but it requires human review before adoption can be accepted.

### Constraints on future hook releases

Any hook promoted from `.staging/` to a first-party Aether release must satisfy
all of the following before merging:

1. Ownership classification: Aether provider adapter confirmed (not Egolint/Relay).
2. Threat model: covering untrusted JSON input, command injection, path
   traversal, secret/prompt/environment disclosure, denial of service, false
   allow/false deny, platform differences, and compromised dependencies.
3. Explicit fail-open or fail-closed policy documented and tested.
4. Input parsed as structured data; never evaluated as shell code.
5. Declared macOS/Linux/Windows compatibility tested via fixtures or narrowed.
6. Missing dependencies produce safe, diagnosed behavior (not silent fail-open).
7. Shell functions use shdoc docstrings and `printf`; strict mode enabled.
8. Underlying lint/license/secret/link checks delegated to Egolint/Relay.
9. JSON payload fixtures for every supported event; tests for valid, invalid,
   malicious, missing-tool, platform, allow, deny, and privacy cases.
10. Packaged separately from skill distributions; registered in the catalog.
11. Install, disable, diagnostics, and uninstall documentation present.
12. No raw prompt, environment variable, tool payload, credential, private path,
    or captured source content logged by default.

### Consequences

- No hook artifacts are released in the first Aether release.
- `.staging/hooks/` files are **not removed** (ADR-005 deletion gate; human
  review not yet complete).
- Move-out items remain in `.staging/` until Alan reviews and transfers them.
- `tool-guardian` is deferred to a subsequent issue for human review.
- Disposition records for each prototype are added to
  `catalog/first-party/staging-dispositions/`.
- The safety guide at `docs/agent-and-hook-safety-guide.md` is updated to
  reflect the threat model and failure-policy requirements.

---

## Unresolved Questions Captured Here

| ID | Question | Linked ADR |
|---|---|---|
| OQ-D1 | Whether ArXiv is a first-class distribution channel | Deferred; see [`PURPOSE.md §7`](PURPOSE.md#7-open-questions) |
| OQ-D2 | Whether per-artifact versioning will be needed at larger scale | Deferred; may supersede ADR-004 |
| OQ-D3 | Whether hooks belong in Mantle or Relay | Deferred; see [`SYSTEM.md §10`](SYSTEM.md#10-open-questions) |
| OQ-D4 | Whether `tool-guardian` qualifies as an Aether provider adapter | Deferred; see ADR-007; requires human review |
