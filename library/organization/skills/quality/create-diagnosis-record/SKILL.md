---
name: create-diagnosis-record
description: Creates or updates an evidence-labelled technical diagnosis record from supplied logs, code, commands, and debugging context. Use when an investigation needs a durable, resumable trace without implying that a root cause is confirmed or a fix is authorized.
license: MIT
metadata:
  aether-version: "1.0.0"
  aether-status: "draft"
  aether-spec-id: "diagnosis-record"
  aether-scope: "organization"
  aether-domain: "quality"
  aether-owners: "egohygiene"
  aether-created: "2026-09-04"
  aether-updated: "2026-09-04"
  aether-distribution-resources:
    - source: "catalog/schemas/aether.diagnosis-record.v1.schema.json"
      destination: "references/aether.diagnosis-record.v1.schema.json"
---

# Create Diagnosis Record

Create or append to a durable diagnosis record governed by
`diagnosis-record`. Preserve the difference between evidence and interpretation
and between diagnosis and authorized remediation.

## Inputs

Resolve as much of the following as the supplied evidence supports:

- observed and expected behavior;
- repository, commit or artifact version, component, and environment;
- investigation scope and authorization boundary;
- raw logs, commands, exit codes, screenshots, code locations, and timestamps;
- hypotheses already considered and their current disposition;
- changes applied, if any, and whether they were authorized;
- validation that actually ran and checks that remain unavailable;
- sensitivity, redaction, retention, and publication constraints;
- desired output path or the repository's diagnostics convention.

Use `unknown`, `not-run`, or another contract state when evidence is missing.
Never fill a required field by guessing.

## Workflow

1. Inspect the governing diagnosis-record specification and the repository's
   local instructions.
2. Confirm whether the request authorizes diagnosis only, record authoring, or
   remediation as well. Record authoring does not expand the authority granted;
   use `remediation.status: not-authorized` for diagnosis-only work.
3. Select an existing record by stable ID or create a new
   `diag-YYYYMMDD-<short-slug>` identifier.
4. Inventory supplied evidence and assign stable `E-NNN` identifiers. Preserve
   raw evidence by reference when possible and disclose truncation, copying,
   mutability, or missing timestamps.
5. Redact secrets and unnecessary sensitive values while recording that a
   redaction occurred.
6. Classify material claims as `observed`, `reported`, `inferred`, `unverified`,
   or `disproven`.
7. Record the investigation chronologically. Give hypotheses stable `H-NNN`
   identifiers and explicit lifecycle states; keep competing hypotheses visible.
8. Set reproduction, root-cause, remediation, and validation states
   independently. Do not infer one from another.
9. Create or update the record with
   [DIAGNOSIS_RECORD.template.md](templates/DIAGNOSIS_RECORD.template.md).
10. Validate frontmatter against
    `references/aether.diagnosis-record.v1.schema.json`
    when a schema validator is available, then inspect required heading order,
    ID uniqueness, evidence links, and redaction disclosure.
11. Report the record path, represented artifact, validation performed, and
    remaining unknowns.

## Append-only investigation guidance

When updating an existing record:

- preserve material chronology and stable IDs;
- append new evidence and steps in timestamp order;
- add an amendment when correcting a material statement;
- update hypothesis states without erasing the evidence for earlier states;
- advance `updated` only for substantive changes;
- use `superseded` and link a replacement when a new record takes authority.

## Boundaries

- Do not fabricate a run, command, exit code, metric, timestamp, commit, or
  conclusion.
- Do not treat copied logs as independently observed unless they were verified.
- Do not execute commands, change code, create issues, or publish records unless
  the user separately authorized those actions.
- Do not claim a fix from code inspection alone or claim validation from an
  unexecuted command.
- Do not promote a narrow deterministic compressor or component probe into
  evidence about coding-agent quality or other behavior it did not exercise.
- Do not expose secrets or assume a private record is safe to publish.
- Do not force a confirmed root cause; an honest incomplete record is valid.
- Do not replace ADRs, incident postmortems, or issue trackers with this record.

## Completion criteria

- [ ] The stable record ID and represented context are explicit.
- [ ] The symptom, expected behavior, and scope are evidence-labelled.
- [ ] Evidence and hypotheses have unique stable IDs.
- [ ] Reproduction, root-cause, remediation, and validation states are independent.
- [ ] The chronological trail can be resumed by another human or agent.
- [ ] Raw evidence references and their limitations are visible.
- [ ] Redactions and sensitivity are explicit.
- [ ] Unrun checks and residual uncertainty remain visible.
- [ ] Structural validation ran or its absence is recorded.
