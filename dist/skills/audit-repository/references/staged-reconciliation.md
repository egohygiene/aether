# Staged repository-audit reconciliation

This is the source disposition for Aether #86 and #68, replacing the stale
internal “Issue 016” pointer. Source baseline:
`5077797448d32a59b06eabe4b38f091137d58052`. The inspected files below are retained
as historical migration evidence and are not canonical executables.

| Inspected source | SHA-256 |
| --- | --- |
| `.staging/skills/repository-audit/SKILL.md` | `af9f21603e9f99f9e732083fd3a1f673234162155f9fc37cef212f9bb047a7ef` |
| `.staging/agents/auditor.agent.md` | `0ae0ca6b156c6dc1a5764a2d7d53f45075ba4b0849e5cdcdbb1f4e351b214928` |
| Approved `library/organization/specs/quality/auditor.spec.md` 2.0.0 | `f9f4d56673cefac4233fad4d53c78d1ba0726201b7e097bb78f67a721b81e62f` |

| Staged behavior | Canonical disposition |
| --- | --- |
| Resolve strategy, focus, depth, constraints and inferred defaults | Preserve through one generic procedure plus explicit profile resolution; defaults remain recorded. |
| Systematic discovery, prior audits and material unavailable sources | Already governed by approved auditor2; make missing/uninspected scope and continuation explicit in sidecar completion. |
| Read-only diagnostics when useful | Preserve as an explicitly authorized host capability or supplied capture. The thin agent retains only read/search; no execute permission is imported. |
| Separate observation, significance, recommendation and uncertainty | Preserve in canonical finding/evidence dimensions and low-confidence missing evidence. |
| Recheck recurring findings rather than repeating them | Preserve explicit prior-audit identity and reported deltas; missing evidence never resolves a finding. |
| Unique Markdown filename, strengths, backlog, blocked checks | Retain approved behavior, add a separately authorized immutable JSON sidecar and suggestion-only issue metadata. |
| Staged agent tools `edit` and `execute` | Not adopted. Profile selection cannot grant mutation, issue creation, source edits or tool permission. |
| Monolith `.agents` / `.github/specs` paths and alternate skill name | Not adopted. Use Aether's canonical auditor, audit-repository skill and draft data extension. |

No staged source is deleted or promoted. No duplicate auditor agent is created.
The existing approved specification bytes and lifecycle remain unchanged.
The skill's source version can change while `aether-status` remains `draft`;
reconciliation alone cannot satisfy the deterministic fixtures, dependency
closure, host/discovery or evaluation maturity gates. Those remain explicit
acceptance under #86/#68 and the parent qualification tracker.
