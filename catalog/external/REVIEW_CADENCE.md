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

Run the deterministic check with:

    python3 catalog/external/validate.py
