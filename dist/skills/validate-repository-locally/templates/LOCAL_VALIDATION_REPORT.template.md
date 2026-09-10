# Local Validation Report

> Human-readable projection of `aether.local-validation-evidence/v1`. The JSON
> companion is authoritative when values differ.

## Candidate

- Repository: `<owner/name>`
- Base revision: `<revision-or-unknown>`
- Candidate revision: `<revision-or-uncommitted>`
- Worktree: `<clean|modified|unknown>`
- Change fingerprint: `<sha256-or-unknown>`
- Generated at: `<UTC timestamp>`
- Execution profile: `<focused|best-effort|exhaustive-local>`

## Delivery policy

- Installation: `<disallowed|repository-locked|allowed>`
- Remote CI: `<disallowed|deferred|allowed|required>`
- Direct action execution: `<disallowed|explicitly-authorized>`
- Commit evidence: `<true|false>`

## Capabilities

| Capability | State | Version | Evidence | Limitations |
|---|---|---|---|---|
| `<id>` | `<available|unavailable|blocked|unknown>` | `<version-or-none>` | `<sanitized probe>` | `<limitations-or-none>` |

## Checks

| Check | Requirement | Applicability | Availability | Selection | Outcome | Exit | Duration | Evidence or reason |
|---|---|---|---|---|---|---:|---:|---|
| `<id>` | `<required|recommended|optional>` | `<state>` | `<state>` | `<state>` | `<state>` | `<code-or-none>` | `<milliseconds-or-none>` | `<bounded evidence>` |

## Remote CI

- State: `<not-requested|deferred|pending|passed|failed|blocked|unknown>`
- Reason: `<reason-or-none>`
- Observed run: `<URL and timestamp, or none>`
- Workflow surfaces still requiring verification:
  - `<repository-relative workflow path or dimension>`

## Local readiness

`<ready|ready-with-limitations|not-ready|unknown>`

Residual risks:

- `<named risk or limitation>`

## Privacy and provenance

- Sensitivity: `<public|internal|restricted>`
- Redactions: `<what was redacted, or none>`
- Excluded from report: `<secret or irrelevant classes, or none>`
- Representation note: `<whether committing this report advances the final revision beyond the tested candidate>`
