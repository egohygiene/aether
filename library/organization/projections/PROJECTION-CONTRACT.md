# Aether provider projection contract

Status: `aether.projection-interface/v1`  
Interface version: `1.2.0`
Owner: `egohygiene/aether`  
Registry: [`provider-registry.v1.json`](provider-registry.v1.json)

## Purpose

Aether keeps reusable agent intent provider-neutral and projects that intent into provider-specific formats only at distribution time.

```text
canonical Aether agent
        ↓
provider projection interface
        ├── GitHub Copilot / VS Code
        ├── Claude Code
        ├── OpenCode
        ├── Zencoder manual-import packet
        └── MCP configuration templates
        ↓
consumer-owned installation / deployment
```

No provider file is canonical. A provider adapter may omit or translate a canonical capability, but it must never silently grant additional authority.

## Canonical input

Canonical agent source remains:

```text
library/organization/agents/<agent-id>/AGENT.md
```

The source owns:

- stable Aether ID;
- human-readable name and description;
- canonical tool intent;
- reusable instructions;
- Aether lifecycle metadata;
- skill/spec relationships.

Provider adapters may transform syntax and paths, but they do not rewrite canonical intent.

Canonical repository-continuity instruction source is:

```text
library/organization/instructions/repository-continuity/INSTRUCTION.md
```

Its complete skill and agent disposition inventory is:

```text
library/organization/instructions/repository-continuity/continuity-dispositions.v1.json
```

Every projected agent also receives the shared, canonical decision-impact
module from
[`templates/decision-impact.AGENTS.md`](templates/decision-impact.AGENTS.md).
The module is injected through managed markers instead of being copied into
each role source. It currently pins the proposed Hygiene ADR policy at version
`1.0.0` and Repository Intelligence contract at `1.0.0-alpha.1`, both at
immutable Hygiene revision `5e0602265b6ac5e5165b89f418e55a3fd12f8a64`.
Its draft projection does not promote either upstream proposal or grant
implementation authority.

Every projected agent also receives the repository-continuity module through
its own managed marker pair. The module points to the consumer repository's
root `CONTINUITY.md`, composes `maintain-repository-continuity`, and preserves
the reviewed role disposition. It does not copy the full continuity procedure.

## Projection states

Every provider entry declares one of these states:

- `native` — Aether has a verified repository- or organization-native format and generates it directly.
- `native-shared` — the provider consumes the exact same native artifact as another adapter; Aether does not emit a duplicate file.
- `manual-import` — Aether can generate a reviewed import packet, but no repository-native provider file format has been verified.
- `unsupported` — Aether has no safe projection path; generation must surface that state instead of guessing.

Unsupported capabilities remain explicit in the provider registry and generated manifest.

## Provenance

Every generated Markdown agent includes an `aether-projection` HTML comment immediately after YAML frontmatter. The header records:

- projection-interface version;
- provider adapter;
- canonical source path;
- normalized SHA-256 source digest;
- the decision-impact module version, upstream pins, source, and normalized
  digest;
- the repository-continuity module version, contract, source, and normalized
  digest;
- the canonical agent's reviewed continuity disposition;
- generator path.

JSON/manual outputs carry equivalent provenance fields, and `dist/projections/manifest.v1.json` records hashes for every generated output.

The build is intentionally timestamp-free so identical canonical inputs produce byte-identical output.

## Tool authority

Canonical Aether tools express intent rather than provider implementation details:

```text
read
search
edit
execute
web
```

Adapters translate that intent through explicit allowlists.

Rules:

1. A projection may lose unsupported capability, but must never gain capability silently.
2. Claude Code receives an explicit `tools` allowlist.
3. OpenCode starts from wildcard deny and allows only translated canonical tools; declared Aether skills are separately allowlisted.
4. GitHub Copilot/VS Code retain the existing Aether-to-Copilot tool aliases for compatibility.
5. Zencoder preserves canonical tool intent in its manual-import packet; a human selects provider tools during import.

## Provider outputs

### GitHub Copilot and VS Code

Repository agents:

```text
dist/github/repository/.github/agents/<agent-id>.agent.md
```

Repository instruction surface:

```text
dist/github/repository/.github/copilot-instructions.md
```

Organization agents:

```text
dist/github/organization/agents/<agent-id>.agent.md
```

VS Code consumes the repository-level `.github/agents` contract, so it is registered as `native-shared` with GitHub Copilot rather than receiving duplicate files.

### Claude Code

```text
dist/claude/repository/.claude/agents/<agent-id>.md
```

Repository instruction surface:

```text
dist/claude/repository/CLAUDE.md
```

Canonical tools are translated into Claude Code built-in tool names. Repository-local skill/spec references remain ordinary repository paths rather than provider-owned copies.

### Codex-compatible runtimes

```text
dist/codex/repository/AGENTS.md
```

The fixture models repository-root `AGENTS.md` precedence. It preserves local
repository prose around the managed block and does not imply that every
compatible runtime can run a pre-pull-request hook.

### OpenCode

```text
dist/opencode/repository/.opencode/agents/<agent-id>.md
```

Agents are projected as subagents with deny-by-default permissions and explicit canonical-tool mappings.

### Zencoder

```text
dist/zencoder/manual-import/agents.json
```

As of the registry's `last_verified` date, Aether has not verified a repository-native custom-agent file format for Zencoder. The generated JSON is therefore deliberately labeled `manual-import` and is input to the provider UI/catalog rather than a file that claims automatic discovery.

### Legacy repository-instruction fixture

```text
dist/fixtures/repository-instructions/AGENTS.md
```

This generated file is an integration fixture for repository-root guidance,
not a consumer-owned instruction file to overwrite wholesale. Holon or another
authorized installer must preserve repository commands, boundaries, and nested
instruction precedence while reconciling the marked module. Reapplying the
module replaces the existing marked block and never adds a second copy.

All four repository instruction fixtures exercise the same lifecycle:

- install into local prose with exactly one marked block;
- upgrade by replacing that block in place;
- remove only that block while preserving surrounding prose;
- reject malformed, nested, or duplicate marker sets; and
- report unsupported automatic-hook behavior honestly.

The generated files are not instructions for Aether itself and are not
consumer installations. Holon owns materialization into downstream
repositories; Relay, Hygiene, EgoLint, and Pace retain their respective
execution, policy, validation, and rollout boundaries.

## GitHub MCP template

Aether publishes a secret-free local Docker template at:

```text
dist/mcp/github/.mcp.json
```

The template passes `GITHUB_PERSONAL_ACCESS_TOKEN` into the official GitHub MCP Server by environment-variable name. It contains no credential value and must not be modified to embed one.

GitHub Copilot CLI already provides GitHub integration capabilities of its own; consumers should avoid configuring a duplicate MCP server unless their selected host/runtime needs the explicit server.

## Ownership boundary

Aether owns:

- canonical reusable agent intent;
- projection interface/schema;
- provider adapters;
- generated release artifacts;
- provider compatibility evidence.

Consumers own:

- whether a projection is installed;
- provider account/workspace settings;
- credentials and local secrets;
- organization deployment policy;
- repository-specific overrides.

The organization-level fallback tracked by
[`egohygiene/.github#1`](https://github.com/egohygiene/.github/issues/1) may
remind compatible agents to look for repository continuity. It is not a
substitute for repository-local instructions, cannot supply repository state,
and must yield to the repository's normal instruction precedence.

The dependency direction is:

```text
Aether projection contract/release
        ↓
Empathy editor/AI integration profile
        ↓
Holon materialization / consumer repository
```

`egohygiene/empathy#63` therefore consumes released Aether projections. It is a downstream integration/golden-consumer concern, not a prerequisite for defining the Aether projection interface.

## Validation

The compatibility entrypoint remains:

```bash
python3 library/organization/agents/build-projections.py \
  --output-directory "dist"
```

The provider-neutral implementation is also directly invokable:

```bash
python3 library/organization/projections/build-projections.py \
  --output-directory "dist"

python3 library/organization/projections/build-projections.py \
  --output-directory "dist" \
  --check
```

Aether's existing `distribution build` command continues calling the compatibility entrypoint, so provider projections participate automatically in release builds, drift checks, and two-build reproducibility validation.

## Provider maintenance

Provider formats change independently of Aether. When a provider contract changes:

1. verify current authoritative documentation;
2. update the registry's `last_verified` date;
3. update only that adapter and its tests;
4. preserve the canonical Aether agent contract unless the underlying intent changed;
5. represent unavailable or unsupported semantics explicitly;
6. run two-build reproducibility checks before release.
