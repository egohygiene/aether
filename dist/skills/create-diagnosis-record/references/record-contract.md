# Diagnosis Record Authoring Contract

Use the canonical `diagnosis-record` specification as the governing authority.
This reference is a compact authoring checklist for skill consumers.

## Core state

Keep these concerns independent in frontmatter:

- reproduction;
- root cause;
- remediation;
- validation;
- record lifecycle;
- sensitivity and redaction.

A successful remediation does not prove a suspected root cause. A committed
change is not necessarily published, deployed, or validated. A structurally
valid record does not prove that its claims are true.

## Evidence

Assign every material evidence item a stable `E-NNN` identifier. Record its
timestamp or `unknown`, source, claim classification, statement, and integrity
limitations. Preserve exact commands and exit codes when known, but reference
large raw output rather than copying it without bounds.

Use only the contract classifications:

- `observed`
- `reported`
- `inferred`
- `unverified`
- `disproven`

## Hypotheses

Assign each hypothesis a stable `H-NNN` identifier and one lifecycle state:

- `proposed`
- `testing`
- `supported`
- `eliminated`
- `confirmed`
- `superseded`

Every state transition should cite supporting or contradicting evidence. Keep
competing hypotheses until evidence disposes of them.

## Safe updates

- Append material investigation history.
- Add amendments instead of silently erasing incorrect earlier claims.
- Preserve stable IDs.
- Advance `updated` for substantive changes.
- Mark a replacement record through `superseded_by`.
- Redact secrets and mark `redactions: present`.

## Validation limits

Schema and heading checks validate structure only. A narrow functional check
supports only the behavior and artifact it exercised. Missing, blocked,
skipped, stale, or unrun checks must remain visible.
