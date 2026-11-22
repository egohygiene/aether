# Canonical Skill Frontmatter Contract

This document defines the required and optional frontmatter fields for every
`SKILL.md` in `library/organization/skills/`.  It is the authoritative
reference for contributors and validators.

---

## Specification source

Aether skills conform to the **Agent Skills** specification.  The current
published reference is <https://agentskills.io/specification>.  Hosts that
load skills include GitHub Copilot, GitHub CLI (`gh skill`), VS Code, and
Codex-compatible runtimes.

---

## Fields

### `name` (required)

- Type: string
- Constraints:
  - lowercase kebab-case (`[a-z][a-z0-9-]*[a-z0-9]` or single letter)
  - at most 64 characters
  - **must match the parent directory name exactly**

### `description` (required)

- Type: string
- Constraints: non-empty, at most 1,024 characters
- Must state **what the skill does** and **when it should be loaded**.
  Skill hosts use this field for routing and discovery.

### `license` (optional)

- Type: string
- Canonical value for first-party Aether skills: `MIT`

### `compatibility` (optional)

- Type: string
- Include only when the skill has genuine runtime constraints
  (e.g. requires a specific tool, API, or repository structure).

### `metadata` (optional)

- Type: YAML mapping
- All Aether-specific lifecycle and relationship data belongs here,
  using the `aether-` prefix.

#### Supported `metadata` keys

| Key | Type | Description |
|---|---|---|
| `aether-version` | string (semver) | Skill version in Aether catalog |
| `aether-status` | string | Lifecycle state: `draft`, `experimental`, `stable`, `deprecated`, `retired` |
| `aether-spec-id` | string | ID of the Aether specification this skill implements |
| `aether-scope` | string | `organization`, `repository`, or `personal` |
| `aether-domain` | string | Primary domain: `architecture`, `authoring`, etc. |
| `aether-owners` | string | Owning team or user handle |
| `aether-created` | string (date) | ISO 8601 creation date |
| `aether-updated` | string (date) | ISO 8601 last-updated date |
| `aether-distribution-resources` | list of source/destination mappings | Build-only repository resources to bundle at package-local destinations; consumed during generation and omitted from exported frontmatter |

#### Build-only resource projection

Canonical source may declare `metadata.aether-distribution-resources`. The
distribution builder validates and copies every declared resource before
omitting only this build instruction from generated `SKILL.md`; it is not a
runtime dependency on the canonical repository. Update runtime instructions
to use the bundled destination rather than the declaration's source path.

For these opted-in skills the generated YAML header is deterministically
serialized with all other field values retained, and the complete normalized
Markdown body is unchanged. Skills without this key remain verbatim UTF-8/LF
copies. Companion resources retain their original bytes. This is the sole
build-only frontmatter projection; it does not remove genuine runtime paths,
installer tracking, unknown metadata or historical prose to satisfy validation.

The existing distribution manifest's `source_digest` still hashes canonical
`SKILL.md` with UTF-8/LF normalization. It does not claim to hash the projected
export. Generated inventory and release payload hashes retain their separate
roles; no manifest schema fields, canonical authoring bytes or artifact maturity
are changed by this projection.

### `allowed-tools` (experimental, optional)

- Type: list of strings
- Restrict the tools available to the skill when a host supports it.

---

## Prohibited top-level keys

The following keys are **not** supported by Agent Skills hosts and must not
appear at the top level:

`schema`, `id`, `title`, `kind`, `version`, `status`, `owners`, `created`,
`updated`, `domain`, `tags`, `depends_on`, `related`, `supersedes`,
`implements`, `recommended_agents`, `specs`

Move any Aether-specific values to `metadata`.

---

## Do not pre-populate install-tracking keys

GitHub CLI injects installation metadata (`metadata.github-*`) into installed
copies.  Canonical source files must **not** contain these keys.

---

## Repository continuity composition

Repository-scoped skills are classified in the canonical disposition inventory:

[`../instructions/repository-continuity/continuity-dispositions.v1.json`](../instructions/repository-continuity/continuity-dispositions.v1.json)

Each applicable skill composes the single canonical
`maintain-repository-continuity` procedure instead of copying that procedure.
The visible composition block in a consuming skill must:

- carry exactly one `aether-continuity-disposition` marker;
- describe its domain-specific evidence contribution and prohibited claims;
- require **Resume** before work selection when `startup_read` is true;
- require **Refresh** and **Verify** after domain validation and before pull-request
  presentation when `pre_pr_write` is true;
- preserve an explicit read-only or reader boundary without gaining edit
  authority; and
- leave a reasoned `not-applicable` skill unchanged.

The inventory, not a copied workflow, is the reviewable source for every
reader, writer, reader-writer, read-only, or not-applicable disposition.
Static skill text does not install or guarantee an automatic pre-pull-request
hook.

---

## Valid example

```yaml
---
name: create-purpose-document
description: Creates or updates PURPOSE.md from repository evidence. Use when a project needs to define, repair, or review why it exists and whom it serves.
license: MIT
metadata:
  aether-version: "1.0.0"
  aether-status: "draft"
  aether-spec-id: "architecture-purpose"
  aether-scope: "organization"
  aether-domain: "architecture"
  aether-owners: "egohygiene"
  aether-created: "2026-08-01"
  aether-updated: "2026-08-01"
---
```

---

## Validation

Run the deterministic validator to check the current canonical skill corpus:

```sh
python3 library/organization/skills/validate-skills.py
```

Exit code `0` means all skills are valid.

---

## Naming convention

Skill directories follow the pattern:

```
library/organization/skills/<domain>/<name>/SKILL.md
```

where `<name>` is the kebab-case skill identifier that appears in `name`.
