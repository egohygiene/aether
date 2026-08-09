# Hook Opt-In Guide

> **Status:** Adopted — 2026-08-09
> **Scope:** Requirements for future Aether hook releases
> **Related:** [`hook-threat-model.md`](hook-threat-model.md) · [`DECISIONS.md ADR-007`](../DECISIONS.md#adr-007)

---

## Current status

**No Aether hook packages have been released in this version.**

All staged hook prototypes were reviewed in issue 015 and received reject,
move-out, or needs-human-review dispositions.  See
[`DECISIONS.md ADR-007`](../DECISIONS.md#adr-007) and the disposition records
in `catalog/first-party/staging-dispositions/hooks-*.json`.

The requirements below apply to any future hook release.

---

## Opt-in principle

Aether hook packages are **always opt-in**.  No hook is activated by default
in any repository.  Consumers must explicitly:

1. Copy the hook package into their repository (or reference it via a pinned
   release tag).
2. Create or update a `hooks.json` in their `.github/` or configured hook
   directory that references the hook.
3. Commit the hook configuration to the default branch.

A hook that is not referenced in an active `hooks.json` has no effect.

---

## Installation (template)

```sh
# 1. Copy the hook package from an Aether release into your repository.
#    Replace <hook-name> and <version> with the hook and release tag.
cp -r path/to/aether-release/<hook-name> .github/hooks/<hook-name>/

# 2. Make shell scripts executable.
chmod +x .github/hooks/<hook-name>/*.sh

# 3. Reference the hook in your hooks.json.
#    See the hook README for the correct event and configuration.

# 4. Commit.
git add .github/hooks/<hook-name>/ hooks.json
git commit -m "feat(hooks): opt-in to <hook-name>"
```

---

## Configuration

Each released hook documents its configuration in its own `README.md` under
a **Configuration** heading.  Configuration is supplied via:

- **`hooks.json`** event and `env` block — controls which events trigger the
  hook and supplies non-secret environment variables.
- **Environment variables** set outside `hooks.json` — for secrets and
  sensitive values that must not be committed to version control.

Never commit credentials, tokens, or secret values in `hooks.json`.

---

## Diagnostics

Every released hook must provide a `--diagnose` flag or equivalent dry-run
mode that:

1. Checks for all required external tools (`jq`, `git`, etc.) and reports
   missing tools with installation instructions.
2. Validates the hook configuration without processing live event payloads.
3. Emits its declared platform compatibility (OS, shell version) and whether
   the current environment matches.
4. Exits with a human-readable summary: PASS, WARN, or FAIL.

Run diagnostics before enabling a hook in production:

```sh
.github/hooks/<hook-name>/<hook-name>.sh --diagnose
```

---

## Disabling

To disable a hook temporarily without removing it:

1. Set the hook's skip environment variable (documented per hook, e.g.,
   `SKIP_<HOOK_NAME>=true`) in your shell or CI environment.
2. Or remove the relevant event entry from `hooks.json` and commit.

To disable permanently, remove the hook package directory and its `hooks.json`
entry.

---

## Uninstalling

```sh
# Remove the hook package directory.
rm -rf .github/hooks/<hook-name>/

# Remove the event entries from hooks.json.
# (edit hooks.json manually or with jq)

# Remove any log directories created by the hook.
rm -rf logs/copilot/<hook-name>/

# Commit.
git add -A
git commit -m "chore(hooks): remove <hook-name>"
```

---

## Version compatibility

Each hook release specifies:

- Minimum VS Code version and GitHub Copilot extension version required.
- Supported platforms (macOS, Linux, Windows) and shell versions.
- Required external tools and minimum versions.

Check the hook's `README.md` **Compatibility** table before installing.

VS Code agent hooks are a preview feature and the configuration format may
change between extension releases.  Always pin to a specific Aether release
tag and review the release notes before upgrading.

---

## Catalog registration

Released hook packages are registered in the Aether catalog under a
`hook` artifact type.  Each catalog record includes:

- Artifact ID and version
- Supported events (`sessionStart`, `preToolUse`, `sessionEnd`, `errorOccurred`)
- Declared platform compatibility
- External tool dependencies
- Lifecycle state (`draft` / `experimental` / `stable`)
- Threat model reference
- Failure policy (fail-closed or fail-open-diagnosed)

Catalog records for hooks are stored alongside skill and spec records and
follow the same lifecycle rules: only `stable` artifacts are releasable.
