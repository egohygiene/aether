# Deterministic evaluation evidence

`aether eval run` validates suite/case structure and executes the declared
deterministic assertions. It does not execute a model, skill routing, subjective
behavior, or the `expected`/`prohibited` prose. A case with no assertions can
pass its recorded structural preflight only; the result and text output state
that scope explicitly.

The validator and runner share the v2 schema, case-ID uniqueness, category,
identity and required-fixture preflight. Invalid, unreadable or duplicate-key
JSON and malformed schemas fail closed. A rejected suite executes zero cases
and records its diagnostics. An unmatched explicit `--skill`, unsupported mode,
or run with no executable cases returns failure rather than an empty success.
Legacy v1 or absent suites are explicitly skipped; a skip establishes no pass.

Text assertions require a readable golden. Missing evidence records a failed
requirement with an unexecuted-assertion reason. Filesystem assertions execute
independently of text-golden presence. An invalid regular expression or failed
assertion is recorded at its actual case/check; no model or provider is added.

In `aether.eval-run-result/v1`, `total_cases`, `total_passed` and `total_failed`
describe admitted case results. `total_suite_errors` counts rejected suites,
and `errors` records run-level failures such as unmatched selection. Neither
is fabricated as an executed case. `total_skipped` retains its existing meaning
of skipped skill suites. Per-skill diagnostics and case checks retain the
attributable evidence; text output reports the same counts and reasons.

```sh
./aether validate --evals --format json
./aether eval run --skill create-decisions-document --mode deterministic --format json
```

These commands run checks when invoked. Authored regression cases and a source
merge alone do not establish that those checks executed or that a skill behaves
correctly in a real task. Evaluation remains independent of release or provider
publication authority.
