# Report-to-findings adapter

The stdlib-only script consumes one completed Realm `realm.local-ci/v1`
repository report. Iterate the repository rows in a sweep's aggregate report;
do not present an aggregate file as a single executed repository report.

```sh
python3 scripts/triage-local-ci.py \
  --report /path/to/local-run/report.json --repository owner/repository \
  --expected-revision FULL_CURRENT_SHA \
  --diagnoses /path/to/diagnoses.json --issues /path/to/issues.json \
  --output /path/to/new-private-packet
```

`--diagnoses` is an explicitly reviewed input, not model inference hidden inside
the executable. Example:

```json
{"checks":{"tests":{"category":"repository-defect","confirmed":true,"root_cause":"missing-fixture","subject":"Restore the referenced fixture","summary":"The executed test references a missing checked-in fixture."}}}
```

Categories are `repository-defect`, `environment`, `coverage` and `unknown`.
Only confirmed actionable diagnoses for failed/blocked checks produce finding
actions. Reuse the same stable root-cause ID when several checks fail from one
cause. Unconfirmed, skipped and unsupported checks stay visible in coverage.

`--issues` is a fresh provider snapshot array with `number`, `body` and `state`
(`open` or `closed`). Before producing it, search existing issues semantically;
legacy issues lack generated fingerprints. An empty array is valid only after
the authorized executor actually searched. Omitted snapshots produce draft
actions. Duplicate matching markers produce conflicts. Closed matches produce
regression-review proposals; no automatic reopen is performed.

Outputs are `evidence.json` (existing Aether schema), `intake.json` (local triage
packet) and `report.md`. The packet includes stable finding markers and separate
evidence markers. A repeated same-revision, same-outcome packet matches noop;
new evidence updates the same finding. The script writes only a new local
directory; it never runs checks or accesses GitHub.

A nonempty coverage-only inventory is retained with unknown readiness and no
issue actions. An empty check array rejects. Deadline expiry retains its observed
exit code and explicit reason: zero exit from a termination handler maps to
blocked, while a nonzero timeout remains failed. Neither establishes a pass.

Freshness is conservative: `--expected-revision` must match the report's full
revision and its worktree must be clean. Otherwise findings remain drafts.
Actual live verification is the executor's responsibility; supplying a string
does not prove its truth. Recheck immediately before provider writes.

Review output before public sharing. Pattern redaction removes common credential
forms and private paths but cannot prove arbitrary log text is non-sensitive.
Logs must be bounded regular files adjacent to the report; traversal and symlink
references reject. Existing issue text is only matched, never copied into new
reports. An updater should append/replace its own managed evidence block while
preserving the rest of a human-authored issue.
