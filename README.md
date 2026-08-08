# aether specification workflows batch

This archive upgrades four existing specifications and adds one focused
reusable skill for each.

Included specifications:

    library/organization/specs/
        authoring/specfile.spec.md
        quality/auditor.spec.md
        methodology/reflector.spec.md
        publishing/arxiv.spec.md

Included skills:

    library/organization/skills/
        authoring/create-specification-file/
        quality/audit-repository/
        methodology/orchestrate-reflective-development/
        publishing/prepare-arxiv-release/

Conceptual relationship:

    specfile
        defines implementation-contract quality

    auditor
        evaluates repository-observable reality

    reflector
        governs bounded recursive improvement cycles

    arxiv
        applies deterministic release engineering to scholarly publishing

## Canonical validation interface

Use the repository launcher from any working directory:

```sh
./aether validate --format text
./aether validate --format json
./aether catalog generate --check
./aether test
```

### Exit codes

- `0`: validation success
- `1`: validation failure (one or more error diagnostics)
- `2`: invalid invocation or repository resolution error
- `3`: internal/tooling error

### Diagnostic schema

JSON output uses `schema_version: aether.validation-diagnostics/v1` and each
diagnostic emits:

- stable `rule_id`
- `severity`
- optional `artifact_id`
- optional `file` and `line`
- concise `message`
- remediation `guidance`
- machine-readable `context`
