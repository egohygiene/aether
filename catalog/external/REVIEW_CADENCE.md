# External Source Review Cadence

The source review register is a governance record, not an installer or a
publication permit. The default disposition for every external artifact is
deny. An allowlisted artifact remains external, restricted, and
agent-assisted-reference-only.

## Routine review

- Review every allowlisted source no later than its register date.
- Review deferred sources before selecting any individual artifact.
- Reconcile source count, artifact count, pin, digest, license, and decision
  against the external catalogs at every review.
- Keep a moved or redirected source frozen to its current immutable pin until
  its successor is independently reviewed.

## Event-driven review

Review immediately when a source reports a security advisory, material license
change, ownership transfer, repository archival, pin change, executable
resource, or proposed external action.

For a known actively exploited or critical vulnerability, remove affected
records from the allowlist within one day. For a high-severity issue, review
within seven days. Run the routine source review at least every 30 days.

## Selection and update rules

1. Validate the source review register and allowlist.
2. Review the exact pinned artifact, including embedded links, tool requests,
   and instructions that could cause external effects.
3. Record a new immutable revision and normalized content digest before
   changing an allowlisted entry.
4. Keep first-party adoption, installation, execution, delivery, and
   publication as separately authorized actions.

Run the offline structural check with:

    python3 catalog/external/validate.py

That command validates real calendar dates, timestamp ordering, source coverage
and the bounded allowlist. A structural pass does not establish freshness or a
live source, license, advisory, or embedded-instruction review.

Select a reproducible calendar assessment explicitly:

    python3 catalog/external/validate.py --as-of 2026-11-14 --format json

The deadline is inclusive through its named UTC calendar day: before/on it is
`current`, after it is `overdue`; missing/unusable evidence or an assessment
before the recorded review is `unknown`. With `--as-of`, any overdue/unknown
source causes exit 1, including deferred/rejected sources. Invalid input exits 2.
Without the flag, no wall clock is substituted and no freshness is claimed.
`complete` applies only to the selected structural/freshness scope, never to a
full live source review or permission to install/use material.

Append-only `followups` preserve blocked/unknown evidence and a concrete next
action. They explicitly set `renews_review: false`: they cannot advance a
deadline, replace the original assessment, allowlist a source, or grant an
installation/execution/publication right. A completed renewed review needs its
own reviewed evidence and explicit date decision rather than relabeling a
follow-up. Preserve the prior record in history.

The [November 14 UTC follow-up](../reports/external-source-followup-2026-11-14.json)
records all three overdue sources. Repository/pin reads were partial evidence;
full license/advisory/instruction qualification remains unknown or blocked.
Their September 30 deadlines are intentionally retained as overdue.
