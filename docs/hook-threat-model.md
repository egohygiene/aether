# Hook Threat Model

> **Status:** Adopted — 2026-08-09
> **Scope:** All Aether hook packages (current and future)
> **Related:** [`DECISIONS.md ADR-007`](../DECISIONS.md#adr-007) · [`agent-and-hook-safety-guide.md`](agent-and-hook-safety-guide.md)

---

## Purpose

Hooks execute code at an agent trust boundary.  They receive input from the
agent runtime (which may itself process untrusted content) and can influence
agent behavior, modify the repository, or communicate with external systems.
This document defines the threat categories that every Aether hook release must
address before promotion from `draft` to `stable`.

---

## Threat Category Reference

### T1 — Untrusted JSON Input

**Description:** Hook scripts receive event payloads as JSON via stdin or
environment variables.  Payloads originate from the agent runtime and may
reflect user-supplied content, file content read by the agent, or tool results.
All payload fields must be treated as untrusted.

**Required mitigations:**

- Parse JSON exclusively with a validated tool (`jq`, `ConvertFrom-Json`, or
  equivalent).  Do not use `grep`/`sed`/`awk` as primary parsers.
- When the JSON parser is absent, fail closed with a diagnostic message; do not
  silently proceed with empty or partial data.
- Never pass parsed field values as arguments to `eval`, `sh -c`, or equivalent.
- Validate that required fields are present and of the expected type before use.

**Test requirement:** Fixtures for valid payload, missing required fields,
wrong field types, and oversized payload (>1 MB).

---

### T2 — Command Injection

**Description:** Hook scripts may construct shell commands from payload fields
(tool names, file paths, package names, URLs).  Attacker-controlled input in
these fields can break out of quoted contexts and execute arbitrary commands.

**Required mitigations:**

- Never interpolate payload fields directly into shell command strings.
- Pass payload-derived values as arguments, not as part of the command string.
- Use `printf '%s'` for all string formatting that involves external data.
- Avoid `eval`, backtick substitution, and `$()` over untrusted strings.
- In PowerShell, use `-LiteralPath` and parameter arrays; avoid `Invoke-Expression`.

**Test requirement:** Fixture with shell metacharacters in tool name and input
fields (`; rm -rf /`, backtick, `$(...)`, `&`, `|`, newline).

---

### T3 — Path Traversal

**Description:** Hooks that read or write files using payload-derived paths may
be directed outside the intended repository root by a crafted path containing
`../` sequences, absolute paths, or symlinks.

**Required mitigations:**

- Resolve all file paths to canonical form before use (e.g., `realpath` on
  Linux/macOS; `Resolve-Path` on Windows).
- Verify that the resolved path begins with the repository root.
- Never write log files to paths derived directly from payload fields without
  validation.
- Log directory paths derived from environment variables must be validated
  against the repository root before use.

**Test requirement:** Fixture with payload path containing `../../`, absolute
path `/etc/passwd`, and symlink pointing outside the repository.

---

### T4 — Secret, Prompt, and Environment Disclosure

**Description:** Hooks that log event payloads, environment variables, or file
content may inadvertently capture credentials, private prompts, API keys, or
personal information and write them to persistent log files accessible to
unintended readers.

**Required mitigations:**

- Do not log raw prompt text, tool input payloads, environment variable values,
  file content, or credential fields.
- Log only structured metadata: event type, timestamp, tool name, outcome, and
  non-sensitive counts.
- Log files must not be committed to version control; exclude log directories
  via `.gitignore`.
- Provide documented log rotation and retention guidance.
- Fail safely if the log directory cannot be created; do not fall back to
  stdout in a way that captures sensitive data in CI logs.

**Test requirement:** Fixture that confirms no secret-shaped strings appear in
log output when a payload containing a secret-shaped value is processed.

---

### T5 — Denial of Service

**Description:** Hooks run synchronously within the agent session and can block
agent progress if they loop indefinitely, spawn unbounded subprocesses, or
consume excessive memory.

**Required mitigations:**

- Every hook must declare and respect a `timeoutSec` in its `hooks.json`.
- Network requests (if any) must have explicit per-request timeout limits.
- Subprocesses must not be spawned in unbounded loops.
- Pattern matching over large inputs must use bounded iteration.
- Hooks must not write unbounded data to disk without a size or age limit.

**Test requirement:** Fixture demonstrating that a payload exceeding 1 MB is
handled within the declared timeout without unbounded memory growth.

---

### T6 — False Allow / False Deny

**Description:** A hook that incorrectly allows a dangerous operation (false
allow) or incorrectly blocks a safe operation (false deny) degrades agent
utility or creates a false sense of security.

**Required mitigations:**

- Document the expected false-positive and false-negative rate for every
  detection pattern.
- Prefer conservative patterns that produce false denies over patterns that
  produce false allows.
- Provide an opt-in override mechanism (e.g., allowlist, environment variable)
  that is logged when used.
- Test allow and deny cases against the full declared pattern set.

**Test requirement:** Fixtures for at least one expected-allow and one
expected-deny case per detection category; plus one known-ambiguous case with
documented behavior.

---

### T7 — Platform Differences

**Description:** Hooks declared as supporting macOS, Linux, and Windows must
behave equivalently across all declared platforms.  Platform-specific shell
builtins, utilities, and path separators can cause silent behavioral divergence.

**Required mitigations:**

- Do not use GNU-only flags (e.g., `date --date`, `grep -P`) in scripts
  declared as macOS-compatible.
- Use POSIX-compliant shell syntax where portability is required.
- Provide equivalent PowerShell implementations for every Bash hook that
  declares Windows support.
- Verify behavioral parity via test fixtures run on each declared platform (or
  explicitly narrow the declared compatibility).

**Known non-portable constructs to avoid:**

| Construct | Issue | Portable alternative |
|---|---|---|
| `date --date=...` | GNU-only; fails on macOS BSD `date` | Use `python3 -c` or `perl` for date arithmetic |
| `grep -P` | PCRE; absent on macOS default `grep` | Use `grep -E` (ERE) |
| `readlink -f` | GNU-only; absent on macOS | Use `realpath` or `python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))'` |
| `sed -i ''` vs `sed -i` | BSD vs GNU `sed` difference | Use `perl -pi -e` |
| `\\n` in `printf` format | Behavior varies | Use `$'\n'` or explicit newline literal |

**Test requirement:** For each declared platform, a fixture run that exercises
the same code path and produces the same structured output.

---

### T8 — Compromised Dependencies

**Description:** Hooks that invoke external tools (package manager CLIs, network
clients, language runtimes) inherit the trust level of those tools.  A
compromised dependency silently compromises the hook.

**Required mitigations:**

- Minimize external dependencies; prefer POSIX shell built-ins.
- Pin all required external tool versions in documentation.
- When a required tool is absent, fail closed with a clear diagnostic rather
  than falling back to a weaker implementation.
- Do not fetch remote content at hook execution time unless the hook's sole
  purpose is network-based validation, and even then scope and validate all
  fetched content.
- Document all required external tools in the hook's `README.md` under a
  **Dependencies** heading.

**Test requirement:** Fixture demonstrating fail-closed behavior when each
declared required tool is absent from `PATH`.

---

## Failure Policy Requirements

Every Aether hook release must declare one of the following failure policies
for each failure mode:

| Policy | Meaning | When to use |
|---|---|---|
| **fail-closed** | Exit non-zero; block the agent action | Default for safety-critical hooks (pre-tool-use guards) |
| **fail-open-diagnosed** | Exit zero; emit a clear diagnostic message to stderr | Acceptable for advisory hooks (session-end reporting) when blocking would be too disruptive |
| **fail-open-silent** | Exit zero; no output | **Prohibited.** Silent fail-open is never acceptable. |

The declared failure policy must be tested for each failure mode.

---

## Privacy Requirements

| Prohibited log content | Rationale |
|---|---|
| Raw prompt text | May contain personal context or confidential intent |
| Tool input payloads | May contain file content, paths, credentials |
| Environment variable values | May contain secrets, tokens, or private configuration |
| File content captured by the agent | May contain proprietary or personal data |
| Repository paths beyond the basename | May reveal private directory structure |
| User identity beyond what is needed for diagnostics | Personal data minimization |

Permitted log content: event type, timestamp, tool name (not input), outcome
(allow/deny/error), non-sensitive counts, hook version, and repository name.

---

## Platform Compatibility Matrix Template

Every hook release must include a compatibility table in its `README.md`:

| Platform | Shell | Tested | Fixture path |
|---|---|---|---|
| Ubuntu 22.04+ | Bash 5.x | Yes / No | `tests/fixtures/linux/` |
| macOS 13+ | Bash 3.2 / zsh 5.x | Yes / No | `tests/fixtures/macos/` |
| Windows 11 | PowerShell 7.x | Yes / No | `tests/fixtures/windows/` |

If a platform is not tested, its entry must state "No" and the hook's declared
compatibility must exclude that platform.

---

## Hook Release Checklist

Before a hook is promoted from `.staging/` to a first-party release:

- [ ] Ownership classification confirmed as Aether provider adapter
- [ ] Threat model sections T1–T8 addressed in writing
- [ ] Explicit fail-open or fail-closed policy documented for every failure mode
- [ ] Input parsed as data; never evaluated as shell code
- [ ] Platform compatibility matrix completed and fixtures exist
- [ ] Missing dependencies produce fail-closed or fail-open-diagnosed behavior
- [ ] Shell functions use shdoc docstrings and `printf`
- [ ] Underlying lint/license/secret/link checks delegated to Egolint/Relay
- [ ] JSON payload fixtures cover valid, invalid, malicious, missing-tool, platform, allow, deny, and privacy cases
- [ ] Hook package is opt-in and separately identifiable in the catalog
- [ ] Install, disable, diagnostics, and uninstall documentation present
- [ ] No prohibited log content produced by default
- [ ] Human review of threat-pattern list completed
