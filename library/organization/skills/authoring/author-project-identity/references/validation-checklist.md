# Identity companion validation checklist

## Inputs and authority

- Resolve repository instructions, authorized operations and the current handoff.
- Identify absent, legacy-v0 or actual v1 source and existing generated roots.
- Resolve the immutable Identity implementation, required Python/runtime,
  script/artifact digests and selected schema/profile versions.
- If using the optional source helper, retain its limited selected-file result;
  do not claim it authenticated a binary, Git commit or complete checkout.
- Retain exact master bytes, provenance, permissions, reviewer and same-subject
  approvals. Unknown facts stay unknown; templates are not real evidence.
- Keep local candidate defaults distinct from organization-wide approved policy.

## Execution and evidence

- Preserve existing canonical/generated/unrelated files and prior source pins.
- Prepare a separate candidate using the actually supported interface or manual
  route. Missing facts may produce an incomplete candidate without adoption.
- Run actual source checks with the matching authoritative validator, retaining
  diagnostics, command, exit, represented source and limitations.
- Establish producer support separately. Never force a pass by renaming an
  unsupported format, deleting provenance or borrowing another approval subject.
- Checking stays read-only. Generation, adoption and recovery are explicit
  operations; an unavailable check does not authorize repair or installation.
- Verify selected output roots/profiles with their actual interfaces. Preserve
  incomplete/unsupported/runtime-error/stale distinctions rather than guessing
  from human stderr.
- Review visual/copy changes and exact output inventories before publication.
- For upgrades, review source/schema/profile changes and restore previous
  source, evidence, pins and outputs together when rehearsing rollback.

## Handoff and package qualification

- Report prepared, validated, generated and verified results separately; a
  complete public kit is a larger claim than a source or core-output pass.
- Refresh/verify continuity only for authorized repository changes; check-only
  use gains no write authority from this skill.
- Validate metadata, local references, immutable lock shape, package copying and
  its governing spec. Exercise the helper from a copied package outside Aether.
- Retain deterministic evaluation scope. Authored routing/golden cases are not
  proof of agent reasoning, execution or creative quality.
- Actual `gh skill` install/update/dry-run and release-scope qualification are
  separate gates; draft/source readiness does not imply publication readiness.
- The Identity Rust release and Aether skill release have independent artifact
  versions, pins, runtimes and publication evidence.
