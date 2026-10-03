# Canonical issue titles

Use this workflow only when scoped repository instructions explicitly select the
Ego Hygiene title policy. Other repositories retain their own conventions. An
organization's `AGENTS.md` does not automatically govern another repository: a
local pointer, installed instruction module, or explicit read step is required.

## Discover the selected contract

1. Read local `AGENTS.md` and any more specific instructions. Resolve this skill
   from its declared installation; the generated module suggests
   `.agents/skills/github-issue-authoring/SKILL.md` relative to the consumer root.
2. Read [selection.v1.json](issue-title-contract/selection.v1.json). It is the
   single selection of contract ID, version, full commit, authority, and five
   SHA-256 source digests, plus the compatible Egolint candidate revision.
3. Read the selected [contract](issue-title-contract/title-contract.v1.json),
   [catalog](issue-title-contract/label-catalog.v1.json), and
   [semantics snapshot](issue-title-contract/semantics.txt) through the manifest's
   source-to-cache mapping. Do not maintain a second emoji/type table.
4. An authorized executor can run `python3 scripts/verify_title_contract.py`
   from the skill directory. A read-only role instead inspects these sources and
   requests or consumes executor evidence; it must not claim a digest check ran.

The five cached payloads are unchanged upstream bytes. Upstream-relative links
inside them refer to the selected upstream tree, not this flattened cache.
`semantics.txt` retains the Markdown source bytes as a raw snapshot; this guide
provides consumer-local navigation. Refresh all five artifacts and their digests
as one reviewed change when changing the pin.

This selection is **candidate**, with **observe** as its adoption mode. Successful
validation does not accept the contract, enroll a repository, provision labels,
or authorize enforcement. Merging a dependency does not silently change this
selection's authority. The consumer commit identifies source to build; a binary's
reported contract alone does not prove which source produced that binary.

## Author or revise one issue

- Resolve one primary type from repository evidence and the selected contract.
  For an existing issue, read the complete label set before classifying it.
  Missing type labels need classification; multiple recognized types conflict;
  unknown `type:*` labels are unsupported. Do not infer a type from a title emoji.
- Review the exact subject before formatting. Preserve case, wording, checkpoint
  IDs, issue relationships, and unknown legacy prefixes until explicitly reviewed.
  The formatter accepts a reviewed subject; it is not an existing-title parser.
- With execution already authorized and the compatible Egolint available:

      egolint issue-title format --type feature --reviewed-subject '[FLO-OBS-01] Checkpoint 2: Export reports' > proposal.json
      python3 scripts/verify_title_contract.py --report proposal.json

  Read `title` and `required_label` from the proposal. A read-only agent hands
  these commands and inputs to an authorized executor, or prepares an explicitly
  unvalidated proposal from the selected source. Never expand its tool allowlist.
- For a proposed issue, build a local snapshot with `schema_version: 1`,
  `complete: true`, the proposed `title`, and its complete proposed `labels` array.
  For an existing issue, use the actual, freshly fetched title and full labels.
  Keep actual and proposed snapshots separate. Incomplete provider evidence must
  use `complete: false`; do not turn unknown labels into an empty verified set.

      egolint issue-title validate --input issue.json > report.json
      python3 scripts/verify_title_contract.py --report report.json

  Inspect both commands' exit codes and the report's `status`. Source verification
  alone is not title validation. Egolint returns 0 for conformant, 1 for a title or
  classification finding, and 2 for invalid/unavailable input or configuration.
- Separately verify that the required label exists in the target repository and
  that provider evidence is current before any authorized create/update. Proposed
  label conformance does not prove provider label availability. After a delay or
  intervening change, refresh the title/labels and revalidate; never replace the
  current full label set using an older snapshot. Missing labels need a separate
  provisioning task, not automatic creation in this workflow.
- Return title, intended label, selected contract provenance, actual/proposed
  validation status, provider label availability, and unresolved evidence with
  the issue draft. Only claim a provider write after a successful live receipt.

## Unavailable and conflicting evidence

Missing installed skill, source cache, digest mismatch, mutable pin, wrong report
provenance, missing Egolint, or denied execution means validation is unavailable.
Keep a useful draft and report the exact gap; do not substitute a moving `main`
reference, silently repair labels, or call an unvalidated draft conformant.
No script in this package changes GitHub. These instructions do not install a
hook, perform fleet migration, or guarantee future titles without adoption and
the separate provider execution/enforcement work.
