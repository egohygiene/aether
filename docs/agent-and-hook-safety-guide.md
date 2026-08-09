# Agent and Hook Safety Guide

## Scope

Aether includes canonical agent source in `library/organization/agents/` and staged hook material in `.staging/hooks/`.

Hooks execute code at an agent trust boundary and are held to **stricter** requirements than passive skill instructions.  No staged hook prototype has been promoted to a first-party Aether release artifact; see [`DECISIONS.md ADR-007`](../DECISIONS.md#adr-007) for the disposition of each staged prototype.

## Staged hook dispositions (first release)

| Prototype | Disposition | Owner |
|---|---|---|
| `dependency-license-checker` | move-out | Egolint |
| `fix-broken-links` | move-out | Egolint |
| `governance-audit` | reject | — |
| `secrets-scanner` | move-out | Egolint |
| `session-auto-commit` | reject | — |
| `session-logger` | reject | — |
| `tool-guardian` | needs-human-review | — |
| `integrations/github-copilot/hooks/` + `scripts/` | reject | — |

Disposition records: `catalog/first-party/staging-dispositions/hooks-*.json`

## Threat model

Every Aether hook release must address all eight threat categories defined in
[`docs/hook-threat-model.md`](hook-threat-model.md):

- **T1** Untrusted JSON input
- **T2** Command injection
- **T3** Path traversal
- **T4** Secret, prompt, and environment disclosure
- **T5** Denial of service
- **T6** False allow / false deny
- **T7** Platform differences
- **T8** Compromised dependencies

## Failure policy

Every hook must declare one of the following for each failure mode:

| Policy | Meaning |
|---|---|
| **fail-closed** | Exit non-zero; block the agent action |
| **fail-open-diagnosed** | Exit zero; emit a clear diagnostic to stderr |
| **fail-open-silent** | **Prohibited.** |

## Privacy requirements

No released hook may log any of the following by default:

- Raw prompt text
- Tool input payloads
- Environment variable values
- File content captured by the agent
- Repository paths beyond the basename
- User identity beyond what diagnostics require

## Safety rules

- Treat all staged hooks and agents as untrusted prototypes until promoted through governed review.
- Use least-privilege tool declarations in agent frontmatter.
- Never add secrets, tokens, or private endpoints to agent or hook artifacts.
- Input received from the agent runtime must be parsed as data, never evaluated as shell code.
- Keep `.staging/` as non-canonical evidence unless promoted through governed review (ADR-005).

## Validation checks

```sh
python3 library/organization/agents/validate-agents.py
python3 library/organization/agents/build-projections.py --check
./aether validate --links --format "text"
```

