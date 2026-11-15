---
name: author-exploration-note
description: Creates, revises, links or parks a repository-owned tentative exploration note. Use when an opted-in repository needs durable brainstorming before an issue, RFC, ADR or specification; do not promote ideas automatically.
license: MIT
compatibility:
  required_tools: [python3, PyYAML]
metadata:
  aether-version: "1.0.0"
  aether-status: "draft"
  aether-spec-id: "exploration-note-authoring"
  aether-scope: "organization"
  aether-domain: "authoring"
  aether-owners: "egohygiene"
  aether-created: "2026-11-15"
  aether-updated: "2026-11-15"
  aether-executable-resources: ["scripts/note.py"]
---

# Author Exploration Note

<!-- aether-continuity-disposition: reader-writer -->

## Repository continuity composition

Compose `maintain-repository-continuity` Resume before selection; after domain
validation, use **Refresh** and **Verify** before an authorized PR handoff.
Conversation checkpoints and current execution state remain in their own owners.

- **Contribute:** Tentative idea identity, provenance, alternatives, uncertainty, parked or linked next step and validation limits
- **Never claim:** That an exploration, template, link, review or passing check accepts architecture, authorizes a task or publishes knowledge

## Author within scope

Read `exploration-note-authoring`0.1.0 and applicable repository guidance. Confirm
local opt-in, current write authority, selected authored path, existing related
notes and canonical decisions before creating a file. Use the
[small template](templates/EXPLORATION.template.md); adapt the consumer's layout
and omit irrelevant sections. A parked idea needs no issue or invented deadline.

Distinguish observations, user direction, agent suggestions, independently
approved decisions and actionable tasks. Link actual source revisions, competing
approaches, assumptions and uncertainty. Preserve conflicting accepted decisions;
the note is exploratory and cannot supersede them. Missing sources stay partial.

For an explicitly authorized new file in an existing approved directory:

```sh
python3 scripts/note.py --create "<new-note.md>" --template "<filled-reviewed-template.md>"
```

An identical repeat is unchanged; different existing content, symlinks and special
files are refused. The helper never updates existing notes or promotes work.
Revise authored content through normal authorized edits, recording corrections,
Git provenance and split/merge/supersession links. Inspect duplicate stable IDs
and source/topic overlap; propose reconciliation without deleting contributions.

## Review and park/link

Use `--check <note.md> --repository <consumer-root>` for bounded structural/local
source checks. A null next_step is parked; linking an issue/ADR/specification
leaves the note draft. Only a separately authorized owning workflow can promote
work or dispose of architecture. External references are not fetched or verified.
Keep privately derived notes private and review free-form prose before sharing.

Read [examples and owner handoff](references/examples.md). Compose Aether78
brain-dump triage,102 conversation continuity and44 journals without duplicating
them. Holon scaffold, Hygiene applicability, Pace rollout and Mindgarden garden
projection remain separate; no new issue, ingestion engine or fleet install is
needed for this bounded authoring output. No required directory is created in an
unselected repository.
