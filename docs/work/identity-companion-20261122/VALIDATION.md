# Identity companion checkpoint — 2026-11-22

Base: Aether `3c836942bc2af10baaaf8936b114d4c9f4f59be8`.
Identity reference: `afc368003bfc6a2101051229efd237c8d6fadf71`.

## Delivered source and scope

`project-identity-authoring` and `author-project-identity` add one draft workflow
specification and companion skill. Identity remains authoritative for schemas,
semantic validation, CLI and producer behavior. The package includes pinned
resource hashes, command/capability guidance, a small-batch intake worksheet,
validation checklist, authored cases and an optional read-only source-hash
checker. The checker authenticates neither a binary nor Git HEAD; its scope is
only the declared resource bytes.

The first copied-package test reproduced a real builder failure: standard
Agent Skills compatibility prose was expanded as a mapping. The bounded repair
preserves that prose in the existing distribution manifest's `notes` field,
retains legacy mapping behavior and rejects invalid types. Three regression
cases cover those paths; no distribution schema change is introduced.

## Executed checks

| Check | Actual result |
| --- | --- |
| `./aether catalog generate` | Regenerated first-party/agent catalogs from source. Only the new specification/skill records are added; draft release exclusion remains. |
| `./aether distribution build --output-directory dist` and `--check` | Build and drift verification pass, including the bundled governing spec, helper and focused resources. |
| `./aether validate --format text` | Pass; existing staging `computedHash` provenance warning remains unchanged. |
| `./aether test` | 405 tests: 394 passed, 11 existing optional/native skips, no failures after the continuity-block formatting correction. |
| New copied-package tests | Eleven controls pass under Python `-I` outside Aether: matching/tampered/missing/oversized resources, malformed locks, unsafe paths, links, limited scope and no source/package mutation. |
| Actual pinned source helper | Nine actual upstream Git resource byte/hash checks pass from the generated package outside Aether. [Receipt](source-lock-check.json) binds checker/lock bytes and limited scope. |
| `./aether eval run --skill author-project-identity --mode deterministic --format json` | Eight authored scenario/golden cases pass structural and declared assertions. This is not observed routing, model reasoning or an actual brand-authoring run. |
| Roadmap-impact receipt | Existing schema/checker passes; [not-affected](roadmap-impact.json) within AET-Q01, with strategic step IDs and release gates unchanged. |

The initial full-suite continuity failure was a wrapped domain-evidence line
that did not match the declared compact handoff. The corrected source was
regenerated and the complete suite rerun successfully; no assertion was weakened.

## Actual consumer gate and publication status

`python3 -m catalog.consumer_installation --scope local` was actually executed.
Its distribution build passed. The installed `gh` 2.46.0 lacks the preview
`skill` commands, so actual local install/list, package validation, publish
dry-run and cleanup qualification are blocked. Exit 1 and not-ready are retained
in the [sanitized observation](consumer-observation.json); no required host
scenario is relabeled passed. The harness's existing pilot set is not a direct
install of this new skill.

The specification and skill remain **draft 1.0.0**, excluded from stable payloads.
No tool was installed, no remote install/update was selected, no hosted workflow
was dispatched, and no tag, skill/Rust binary release or site was published.
Actual compatible-host evaluation, observed agent use, stable promotion and
release-scope consumer/payload proof remain with their existing owners.

## Decisions, roadmap and next action

Reference the preserved canonical/generated and neighboring-owner boundaries
in Aether ADR-0001/ADR-0002. No new ownership, Identity field semantics,
consumer enforcement or publication authority is selected. The local builder
repair implements the existing compatibility shapes; no duplicate ADR is needed.

Roadmap impact: **not-affected**, AET-Q01. The new source is a bounded addition
within the existing authoring corpus and does not complete release milestones.

Review the companion, qualify a genuinely compatible `gh skill` adapter and
observe actual authoring/installation behavior before promotion/publication.
Upgrade the Identity pin only after reviewing source/CLI/schema differences
and binary/runtime evidence. Identity's broader release preparation remains
under its #98/#116 owners and separate version/tag history.

## Later local host observation

The [separate 2026-11-22 host checkpoint](../identity-companion-host-20261122/VALIDATION.md)
actually exercised a preinstalled gh 2.96.0 without changing the default CLI.
It supersedes the adapter-unavailable limitation for that selected binary only;
the earlier 2.46.0 run above remains historical evidence. Actual local commands
run, while strict pristine/installed portability and complete release readiness
remain failed or unqualified in the new receipts.
