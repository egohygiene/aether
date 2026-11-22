# Identity companion local host qualification — 2026-11-22

Base: Aether `625aa5389473e05d5317fa7181db48117ef0cc42`, containing merged
companion PR #139. Release/consumer acceptance remains owned by [#38](https://github.com/egohygiene/aether/issues/38).

## Actual selection and scope

An already installed Linux x86_64 `gh` **2.96.0 (2026-07-02)** exposes the preview
skill commands. Its observed SHA-256 is
`56b8bbbb27b066ecb33dbef9a256dc9d1314adaeff0908a752feba6c34053b40`.
This identifies the tested file and its self-reported version; no independent
binary signature/authenticity qualification is supplied. Python 3.12.14 and
Git 2.52.0 were used. The prior default/PATH observation of gh 2.46.0 was valid
for that earlier invocation; no global CLI or user configuration was changed.

The actual generated `author-project-identity` package remains **draft 1.0.0**.
Its manifest pins canonical source digest
`756e88cf9292429a8bc4a169b17fc90fe57547b4dc9abb4eb9e1ad235378a09b`.
[The package observation](package-observation.json) records all tested package
file hashes, the exact CLI hash and pristine validation diagnostics. The
companion still references Identity `afc368003bfc6a2101051229efd237c8d6fadf71`;
this checkpoint changes no Identity source/runtime authority or resource pin.

## Executed local scenarios

| Scenario | Historical three pilots | Direct companion |
| --- | --- | --- |
| Distribution build | pass | pass |
| Actual local install and JSON listing | pass across the existing three host placements | pass, Codex/project `.agents/skills/author-project-identity` |
| Strict raw installed-package validation | fail | fail: `006`, `015`, `017` |
| `gh skill publish <generated-dist> --dry-run` | pass | pass; validates generated distribution, not a remote release |
| Manual removal preserving unrelated skill | pass | pass |
| Remote install and update | skipped: local scope | skipped: local scope |
| Local/overall readiness | not-ready / not-ready | not-ready / not-ready |

Full sanitized receipts: [three pilots](consumer-pilot-observation.json) and
[direct companion](consumer-companion-observation.json). The companion run
selected only that skill through the harness's process-local pilot input;
production harness code and readiness rules were unchanged. Its
manifest/resource, declared positive/negative evaluation-category, frontmatter
and intake-template checks ran; these structural checks do not observe an
agent authoring a real identity.

The standard local CLI gate returned exit **1**. The direct harness API returned
`qualification.complete=false`; its invocation does not provide a CLI exit gate.
No failed scenario is relabeled passed because other commands succeeded.

## Distinct portability failures and next repair

Pristine `dist/skills/author-project-identity` independently fails
`AETHER_PORTABLE_015`: the builder's declared verbatim-copy behavior retains
`metadata.aether-distribution-resources[].source` naming the canonical
`library/organization/` resource. That compile-time packaging directive is
distinct from a missing packaged resource: the destination spec is present and
manifest/resource checks pass. This record does not waive the strict rule.

Actual local installation additionally injects an absolute
`metadata.local-path` source-tracking field, producing `006`/`017`. The installer
help explicitly describes this tracking. Do not confuse that installed-host
metadata with the pristine export artifact or blanket-whitelist private paths.
The original three pilots also retain their canonical/staging-provenance prose
findings; this companion run does not close their acceptance.

The next bounded #38 repair should align **package-build metadata projection
with the existing verbatim-copy contract** and verify pristine portability,
without deleting provenance or weakening the global validator. Then handle
only verified CLI-injected tracking as a separately evidenced installed-host
materialization, with exact source/destination constraints if a copied
validation input is used. Preserve genuine runtime paths and historical pilot
findings; rerun the strict gate and retain not-ready until required scenarios
actually pass. No production adapter/builder/validator repair is made here.

## Replay

Select a reviewed compatible binary for these invocations only; replace the
placeholder below with its containing directory. Use new report paths, because
the harness refuses to overwrite existing evidence:

```sh
env PATH="<compatible-gh-directory>:$PATH" \
  python3 -m catalog.consumer_installation --scope local --timeout 60 \
  --output <new-pilot-report-directory>
```

For the targeted companion observation, run the same selected PATH with:

```python
from pathlib import Path
from catalog import consumer_installation

consumer_installation.PILOT_SKILLS = [
    ("author-project-identity", "codex", ".agents/skills/author-project-identity"),
]
harness = consumer_installation.ConsumerInstallationHarness(
    Path.cwd(), scope="local", timeout=60,
    report_root=Path("<new-companion-report-directory>"),
)
report = harness.run()
assert report["qualification"]["complete"] is False  # observed current failure
```

The harness creates and removes disposable consumer Git projects. Installation
uses `gh skill install <generated-dist> author-project-identity --from-local
--agent codex`; JSON listing confirms project scope and placement. Publication
is only `--dry-run`; no remote install, update or publication is selected.
Pristine diagnostics use the existing
`aether_validator.validate_portable_skill_package` on the generated companion.

## Handoff and limits

Documentation/evidence and root continuity only changed. Existing artifact
maturity, catalog/generated payloads, strict validator, release workflows,
versions, tags and release exclusion are unchanged. Local skill commands are
not observed model behavior, automatic discovery or supported OS-matrix proof.
No user-scope install, registry action, hosted CI, stable promotion, tag or
release creation occurred. #38 remains open/not-ready; do not create a duplicate
issue for these already-owned export/consumer gates.

Decision impact: **reference ADR-0001/ADR-0002** for canonical/generated and
neighboring-owner boundaries; no new consequential design or ADR disposition.
Loaded local source skills at the immutable base: execute-issue-checkpoint,
maintain-repository-continuity, create-decisions-document,
reconcile-roadmap-impact, architecture-roadmap and create-roadmap-document.
Roadmap impact: **not-affected**, AET-Q01/AET-Q05; the local observations refine
existing #38 evidence without completing release acceptance or changing intent.

## Checkpoint checks

- `./aether validate --links --json-files --format text`: passed, zero diagnostics.
- `./aether distribution build --check --output-directory dist`: all distribution
  drift checks passed; generated artifacts remain unchanged.
- Existing roadmap-impact receipt checker: passed structure-only validation.
- Root continuity: Draft 2020-12 schema, exact twelve headings and byte/line
  budgets passed. Official released EgoLint conformance is not claimed.
- All 25 recorded package file hashes/sizes match; receipt failure/skipped
  statuses and local-path redaction checks pass.
- Independent read-only review: no blockers in scoped claims, evidence or
  privacy. Staged whitespace passed.

No production code changed, so the historical full suite was not rerun or
reported as fresh evidence. The failed consumer/pristine portability outcomes
above are retained separately from these documentation/checkpoint checks.
