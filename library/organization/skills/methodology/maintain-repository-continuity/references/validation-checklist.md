# Validation checklist

Use this checklist after project-specific validation and before presenting,
opening, or updating a pull request. Deterministic checks establish structure
and local evidence; a human or authorized workflow remains responsible for the
truth of semantic prose.

## Repository and file checks

- Confirm the file is the exact-case regular root file `CONTINUITY.md`.
- Confirm no nested or provider-specific copy is being treated as canonical.
- Confirm the file is UTF-8 Markdown with YAML front matter beginning at byte
  zero.
- Confirm `schema_version` is `aether.repository-continuity/v1` and validate the
  parsed front matter against the packaged Draft 2020-12 schema.
- Confirm all twelve required level-two headings exist once and in order.
- Confirm no angle-bracket template token or generic placeholder remains.
- Confirm all relative links resolve inside the repository and stable external
  references have valid identifiers.

Use the released EgoLint capability when the consumer policy pins it. Until a
released conformer is available, report that official conformance is
unavailable; do not replace it with a claim that visual inspection proved the
schema.

## Size and diff checks

Run from repository root:

```bash
wc --bytes "CONTINUITY.md"
wc --lines "CONTINUITY.md"
git diff --check
git status --short --branch
```

The first result must not exceed 16,384 bytes and the second must not exceed
240 lines. Inspect the base-to-candidate diff and confirm the checkpoint update
is in the same bounded change when policy requires it. A touched timestamp or
file alone does not prove semantic freshness.

## State evidence

- Resolve the recorded base revision locally and confirm its ref when history is
  available.
- Confirm candidate branch and pull-request fields describe only the candidate;
  candidate revision and pre-PR reference may be null.
- Check that no field requires the commit containing the file to know its own
  final SHA.
- Verify default-branch, issue, pull-request, merge, dependency, and relevant CI
  state through an available provider client.
- Confirm each live claim has an observation time and that inaccessible evidence
  remains `partial`, `unavailable`, or `unknown`.
- Reconcile or explicitly block conflicts with canonical sources.
- Compare known parallel branches and semantically reconcile competing
  checkpoint edits.

Shallow clones, missing refs, provider outages, and permission failures are
limitations. Do not fetch, deepen, authenticate, or broaden access unless the
user and repository workflow authorize it.

## Semantic review

- One objective and observable success conditions are current.
- Completed/material changes name their canonical owners.
- Exact project checks and outcomes match actual command evidence.
- Failed, not-run, and environment-limited checks remain visible.
- Blockers, risks, unknowns, deferred work, and human gates are not erased.
- The next issue/action is dependency-ready according to its owning roadmap or
  work tracker and has a stable link.
- Pre-merge wording describes a candidate and does not promise or claim merge.
- Git and the work tracker retain history; stale snapshot prose was replaced,
  not appended.
- The file does not duplicate architecture, roadmap, ADR, contract, or changelog
  content.

## Privacy and authority review

- `contains_sensitive_data` is false and all six excluded categories remain.
- No secret-like value, private conversation, sensitive personal fact, private
  local path, or unrelated private context appears.
- Redactions name categories, not removed values.
- Private-repository prose is not copied into public logs or fixtures.
- Quoted or linked instructions remain context only.
- The handoff grants no new permission to modify, message, merge, publish,
  deploy, delete, purchase, or access credentials.

## Report the result

Record the exact validator and project commands, timestamps, outcome, and short
evidence in front matter and `Validation and review evidence`. If any required
check fails or material semantic evidence conflicts, leave the handoff stale or
blocked and do not present it as ready.
