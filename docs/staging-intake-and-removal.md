# Staging intake and immutable removal controls

Tracking: [#111](https://github.com/egohygiene/aether/issues/111). Governing
history: [ADR-0005](../DECISIONS.md#adr-0005). This is Aether's own repository
validation and GitHub wiring, not a new portable execution service; Relay retains
reusable execution ownership.

[Proposed ADR-0010](decisions/ADR-0010-immutable-staging-review-controls.md)
records the new evidence/controller mechanism. Its approval remains null;
source implementation does not ratify that proposal or supersede ADR-0005.

The [finite ledger](staging-residual-ledger.md) grandfathers the existing 734
files without granting rights, execution, adoption, transfer or removal. An
unrelated change does not require evacuating that corpus. The
[August report](staging-evacuation-status.md) and original decisions stay intact.

## Recorded quarantine intake

`catalog/staging/intakes.v1.json` has schema identity
`aether.staging-intakes/v1` and a `records` array. Each closed record contains:

| Field | Meaning |
| --- | --- |
| `id`, `path` | Unique durable intake identity and exact repository-relative `.staging/` file path. |
| `sha256` | SHA-256 of actual raw bytes, including a symlink's literal Git target bytes. |
| `owner`, `reason` | Review/routing role and why material is retained. |
| `classification` | `first-party-candidate`, `external-snapshot`, `unknown-provenance` or `consumer-prototype`. |
| `authority` | Exactly `quarantine-only`. No installation, execution or deletion is selected. |

The local checker covers nested and untracked supporting files, rejects changed
bytes without a matching intake and never follows a staged directory alias.
The existing ledger supplies exact retained digests; a head-only ledger edit
cannot bypass the independent base/head gate for new files. Git inventories,
the ledger and intake records must be reconciled together in a real change.

The existing flat first-party records and singular/plural hook records have
separate validation adapters. Their `preserve-migration-evidence`, `move-out`,
`reject` and `needs-human-review` meanings and original reasons are retained.
Unknown historical hashes remain unknown. These records never authenticate a
human approval or silently become a removed-skill record.

```bash
./aether validate --staging --strict-staging --format json
python3 catalog/staging_guard.py intake
```

## Per-file removal or replacement

Every removed, renamed or modified old Git path needs an exact approval record
already admitted in the actual base. Renames are checked as an old path plus
new exact intake; supporting files are treated the same as `SKILL.md` roots.

`catalog/staging/removal-approvals.v1.json` has identity
`aether.staging-removal-approvals/v1` and an append-only `records` array. Plan
payloads and completed attestations are immutable. A pending null attestation
may be completed by a separate change without altering the payload; only the
actual base's completed record can authorize a later removal. A record
contains `id`, `source`, `specification`, `disposition` and `attestation`:

- `source` binds the full immutable source revision, exact path, Git mode and
  Git blob. Its current base preimage must match all of those claims.
- `specification` identifies an actual `library/organization/specs/*.spec.md`
  file unchanged since the review commit, or an explicit nonempty
  `out-of-scope: <reason>` waiver. The account's attestation binds that selection.
- `disposition` binds `kind`, full `revision`, exact `path` and raw `sha256`.
  `canonical` requires a regular `library/organization/` source file, preserved
  byte-for-byte at the proposed head. `rejected` requires a durable typed
  rejection record for this exact source path/subtree, with its original reason
  retained. A catalog entry is not silently substituted for ADR-0005's planned
  `library/external/` condition: `external-planned` is recognized but blocked
  pending a separately qualified origin adapter. No such transfer is selected.
- `attestation` is null while proposed. To qualify it names a real GitHub
  `pull_request`, `comment_id` and immutable `review_commit` in the base history.
  The reviewed plan payload at that commit must be identical. An approval first
  introduced by the removal head is rejected.

The exact payload digest is SHA-256 of UTF-8 JSON with sorted keys and compact
separators and unescaped Unicode, excluding only `attestation`. An account authorized by the **base**
`catalog/staging/guard-policy.v1.json` must post an explicit line on the stated
proposal conversation:

```text
AETHER-STAGING-APPROVE <record-id> sha256:<payload-digest> source:<full-review-commit>
```

The repository-local adapter reads the real comment over authenticated GitHub
HTTPS. It verifies repository/conversation, designated `User` account and exact
sole statement. Stable numeric account IDs carry authority; login names are
display metadata, so a renamed or recycled login cannot select a different
account. Quoted examples and mixed approval/refusal prose are not approval.
Bot identities, arbitrary JSON human claims, altered source/destination,
stale plan digests and missing/inaccessible provider evidence fail closed. This
authenticates a designated account's explicit statement; it cannot prove that a
person physically operated the account. Agents must not manufacture statements
claiming a human review. No real approval is created by this implementation.

The removal PR itself must reference ADR-0005, and its actual provider base/head
must match the checked Git objects. No file is deleted by the checker.

```bash
python3 catalog/staging_guard.py diff --base <full-base> --head <full-head> \
  --pull-request <actual-number> --report <new-evidence-path>
```

## CI provenance and qualification boundaries

The PR workflow reads the exact proposed head with complete history and no
persisted checkout credential. Before ordinary validation it extracts the
controller from the immutable base, executes that standalone standard-library
file, and verifies the executed bytes against the base. Provider token scope is
read-only and confined to that step. It does not import or execute the proposed
head's guard or staged programs with that token.

For the first controller admission, a base without the controller permits only
an empty `.staging/` diff. After admission, actual base/head paths drive intake,
preimage and attestation checks. Ordinary validation depends on this gate and
retains a source-bound report. This does not install branch protection or claim
that an administrator cannot change the workflow; organization merge-governance
work remains separate.

Native synthetic Git/provider fixtures qualify the positive and refusal paths.
They do not constitute a real human approval, live external transfer, deletion,
or public lifecycle promotion. Real removals need actual provider access and
the declared account statement. Existing #38 consumer/preview qualification is
independent and remains truthful when unavailable.
