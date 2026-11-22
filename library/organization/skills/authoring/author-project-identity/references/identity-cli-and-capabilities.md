# Identity implementation and command guidance

This package accompanies the separately installed Rust `identity` tool. It
does not install a binary, provide branding approvals or duplicate Identity's
field/schema semantics. Aether owns this agent workflow; Identity owns its
contracts, validator, producers and release artifacts.

## Resolve one compatible implementation

The [source lock](identity-source-lock.json) records observed upstream Identity
revision `afc368003bfc6a2101051229efd237c8d6fadf71` and selected file hashes.
It is a source reference, not a claim that a released binary exists at that
revision or that later revisions are compatible. Review source/contract/profile
changes before updating the pin. Never download and execute mutable `main`.

When an already prepared matching checkout is available, the optional packaged
helper checks its selected file bytes without network, writes or execution:

```sh
python3 scripts/verify_identity_source.py --source-root "/trusted/identity"
```

Run from this installed skill directory, or supply its absolute script path.
It emits JSON and exits 0 for matching declared resources, 1 for missing,
changed, unreadable or symlinked resources, and 2 for invalid inputs/lock.
The result does not authenticate Git HEAD, the binary, an installation, the
whole checkout, approvals, or a release. Retain the separately verified binary
artifact digest and runtime/profile pins. Checking a few files cannot replace
those controls. The helper does not execute Identity or classify project drift.

## Commands observed at the pinned source

| Operation | Existing interface and limits |
| --- | --- |
| Legacy initialization/validation | `identity init` and `identity validate` operate on v0 `.identity/identity.toml`. They are not v1 migration commands. |
| Explicit v1 candidate | `identity v1-init --repository-root ROOT --request FILE --output-directory DIR` prepares a separate candidate from actual supplied facts. Request/output paths are repository-relative, output must be new/disjoint, and missing facts remain incomplete. |
| V1 source-only diagnostics | `python3 scripts/validate_identity.py --repository-root ROOT --format json`, using the standalone validator from the matching reviewed Identity implementation. It is not this skill's resource-lock helper. |
| Selected core generation | `identity v1-generate --repository-root ROOT` performs source preflight and explicit transactional generation. It requires generation authority and actual supported producer inputs. |
| Selected core verification | `identity v1-verify --repository-root ROOT` performs source preflight and read-only selected-output drift checks. Use the actual selected `--output-root` when nondefault. |
| Inspection/recovery | `v1-inspect` is read-only transaction inspection; `v1-recover` is explicit generated-state rollback, not a lint-time fix or source validator. |

There is no `identity v1-validate` command or universal `--format json` flag for
the native v1 verification command at this pin. Do not invent either. Standalone
source diagnostics use `identity.diagnostics/v1`; native runtime failure text
does not provide the complete structured source/producer/output classification.

The newer CLI embeds its trusted scripts but requires Python 3.11+ to execute
the v1 bridge. It does not require a Rust compiler when using a qualified
prebuilt binary. A `gh skill` installation provides agent instructions, not the
Rust binary, Python runtime or a consumer's brand assets.

Observed stable `v1.0.0` predates the explicit initializer and executable nullable
guidance. Matching package version/schema IDs alone do not establish those
capabilities. The source lock is deliberately explicit rather than pretending
the old stable release includes later work. Native producer support is also
narrower than all valid source formats; preserve unsupported PNG/font source
facts instead of renaming files or removing governance.

## Preparation and result boundaries

Read the lock's immutable upstream sources for actual field and request
contracts. If they or the required implementation/runtime are unavailable,
record the limitation; author only the review material the available evidence
supports. The skill does not silently install tools or acquire network inputs.

Keep source validation, producer support, selected-output verification and
complete public-kit readiness as separate results. Core verification does not
verify every optional package. An incomplete candidate, arbitrary exit 1,
missing Python, unsupported producer and stale output are not interchangeable.

For a changed asset or public claim, retain its exact subject/hash, actual
rights and reviewer evidence. A named permission, passing check, generation or
merge does not invent approval. Choose profiles for real surfaces; a small
repository does not need every website, social or PWA projection.

## Skill distribution

The source package remains draft. Aether builds a self-contained
`dist/skills/author-project-identity` package containing this guide, source lock,
helper, evaluation definitions and governing workflow specification. Structural
checks and synthetic helper tests are not an agent/model evaluation or actual
host installation.

Use a compatible, actually qualified `gh skill` adapter for local installation
and publish dry runs. The observed CLI in this workspace is 2.46.0 and lacks
the `skill` subcommand. Publication follows Aether's selected stable payload,
immutable release tag, consumer qualification and authorized publication gate.
No command here claims this draft is already released or installed.
