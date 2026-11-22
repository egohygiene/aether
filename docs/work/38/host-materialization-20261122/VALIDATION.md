# Verified installed-host materialization — 2026-11-22

This checkpoint follows export projection at
`26a8ff90feb4344a7a5836540c55d872da3736a9` under existing
[#38](https://github.com/egohygiene/aether/issues/38). The actual adapter code
selection and file hashes are bound in the [observation](package-and-adapter-observation.json).
The companion remains draft 1.0.0 and excluded from stable payloads.

## Distinct contracts and the repair

Portable validation applies strictly to the pristine exported package. A local
installation is a materialization of that package plus host tracking, rather
than a portable artifact to redistribute verbatim. The global portable validator
and its private/canonical-path rules are unchanged.

The harness now freezes and strictly validates every selected export **before
any installer runs**. Bounded no-follow directory/file reads refuse links,
special inputs, escaping fixture roots and excessive entries/bytes/depth.
After installation it rechecks the source snapshot and compares the actual
installed inventory, all resource bytes, typed semantic frontmatter and body.
The manifest must declare a nonempty, unique, complete installed-file inventory.

Actual gh 2.96.0 adds `metadata.local-path` equal to the exact selected local
package path, reserializes frontmatter and omits one blank LF separator before
the body. Only that verified field and the observed single separator behavior
are admitted. Ordinary field values and remaining body/resource bytes, including
indentation and additional blank lines, must match. Duplicate/non-string keys, aliases and
merge ambiguity fail comparison. Frontmatter delimiters are anchored to whole
lines using the strict validator grammar; a literal `---` in a multiline value
cannot truncate compared fields. Boolean values cannot impersonate numeric
values through Python equality.

No real installed metadata is removed, and no normalized validation copy is
created. The raw installed validator still runs and its `006`/`017` failures
remain recorded as observations. They are never called a raw portable pass.
The required gate instead proves a strict portable export and its exact local
materialization, preserving the installed source tracking used by updates.

Snapshots observe bounded bytes and are not locks against later mutation.
Qualification remains scoped to the existing POSIX harness; no new native OS
or concurrent-adversary guarantee is implied.

## Actual compatible CLI execution

The already installed gh 2.96.0 was selected through command-scoped PATH. Its
exact file hash and all 25 package-file hashes are retained. This is observed
binary identity/self-reported version, not independently verified signature
authenticity. No default CLI, HOME or user/global skill configuration changed.

| Scenario | Direct Identity companion | Existing three pilots |
| --- | --- | --- |
| Actual distribution build | Pass | Pass |
| Actual project-scope local install/list | Pass | Pass |
| Strict pristine export validation | Pass, zero diagnostics | Fail, retained `015`/`016` governing-resource/provenance findings |
| Frozen source / exact installed materialization | Pass | Pass |
| Raw installed portable observation | Fail, `006`/`017` tracking remains visible | Fail, tracking and the original source findings remain visible |
| Manifest/resource/frontmatter/template/eval structure | Pass | Pass |
| Actual publish dry-run / cleanup | Pass / pass | Pass / pass |
| Remote installation/update | Skipped, local scope | Skipped, local scope |
| Selected local readiness | **Ready / complete** | **Not-ready / incomplete** |
| Overall release readiness | **Not-ready** | **Not-ready** |

The standard local CLI returned exit 1 for its retained pilot failures. The
direct companion uses the same harness API with a process-local one-skill
selection; `qualification.complete=true` and `local_status=ready`. No production
pilot list, readiness requirement or failed scenario was removed to produce it.
Both sanitized raw reports are retained:
[companion](consumer-companion.json) and [three pilots](consumer-pilots.json).

Actual commands used the existing local harness and `--from-local` project
installation. Publication was only `gh skill publish ... --dry-run`. Cleanup
preserved the unrelated fixture skill. The private fixture projects were then
removed by the existing harness.

## Executed checks

- `python3 -m unittest discover --start-directory tests --pattern test_consumer_installation_e2e.py --verbose`:
  **32 controls pass**. They cover genuine strict validation, wrong/missing/
  aliased tracking, changed ordinary fields/body/resources, unexpected inventory,
  links/special inputs, ambiguous YAML, bounds, source mutation, missing stages,
  empty selection and empty/duplicate/incomplete manifests.
- `./aether test`: **428 tests; 417 passed, 11 existing optional/native skips**.
- `./aether validate --format text`: pass, retaining only the historical staging
  `AETHER_PROVENANCE_009` warning.
- `./aether distribution build --check --output-directory dist`: pass. This
  checkpoint changes no generated package beyond its projection parent.
- `./aether validate --links --json-files --format text`: pass, zero diagnostics.
  Public receipt JSON/path/secret checks, all 25 package hashes, adapter/unchanged
  validator/observed CLI hashes and pinned continuity schema/headings/budgets pass.
- Actual direct companion local harness: all five required local scenarios pass;
  the standard three-pilot local CLI remains exit 1/not-ready as recorded above.

Independent review reproduced and closed an intermediate substring-parser
false-pass before handoff. The new full-harness negative case fails when the
exact old parser is selected, and the repaired positive/negative multiline
controls pass. The three existing packages lacked this shape, so their earlier
receipts remain historical rather than a claim of broader parser coverage.

A separate independent documentation review confirmed final receipt/status scopes,
all package hashes and retained original pilot failures without material contradictions.

The tests model external command outcomes for deterministic negative controls;
those tests do not substitute for the separate actual CLI observations.

## Remaining acceptance and decisions

The three older pilots still need portable governing-resource/provenance work.
Source paths/history must not be erased or globally whitelisted merely to make
those findings disappear. Actual remote install/update/deprecation/rollback,
eligible stable artifact selection, release/publication and observed agent use
remain under #38 and their existing owners. No tag, release, hosted workflow,
registry action or maturity promotion is performed here.

Decision impact: reference preserved ADR-0001/ADR-0002 for canonical/generated
and neighboring-owner boundaries. The adapter implements the already documented
export versus host-tracking distinction; no broader private-path policy or new
ADR lifecycle is selected. Historical ADR-0002/ADR-0006 conflict and proposed
ADR-0009 remain untouched.

Roadmap impact: **not-affected**, AET-Q01/AET-Q05. Local companion acceptance is
bounded progress within existing release/consumer work, not completion of the
strategic release capability. The [receipt](roadmap-impact.json) retains this
scope and the next source owners.
