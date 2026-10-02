# Trying the bounded worker strategy

The [worker strategy](../library/organization/specs/methodology/worker-strategy.spec.md)
is a draft, opt-in contract for short work sessions with durable handoffs.
Use it directly from a branch or immutable commit while it is under review.
Its [portable copy](../dist/specs/worker-strategy.spec.md) is generated from
canonical source. No skill installation or organization-wide rollout is required.

## Flow suite bootstrap

Copy the prompt below into a new chat and supply the canonical specification URL
from the desired branch or commit. Prefer a full commit SHA for reproducibility.
The URL must be accessible to the new session; access failure is a reported gap,
not permission to invent the specification.

```text
Read this Aether worker-strategy spec: <paste the canonical specification URL>.
Use that version for this session, together with its continuity and validation
dependencies at the same Aether ref and the applicable consumer instructions.

I want to push forward on the Flow suite tools roadmap: egohygiene/flow,
egohygiene/renderflow, egohygiene/optiflow, and egohygiene/aniflow.

The consumer goal is to generate a complete, inspectable artifact tree for my
comic work. Use synthetic fixtures while developing and validating the tools;
real comic assets remain outside scope unless I explicitly authorize them.

Start with bootstrap and reporting only. Check live default branches, relevant
issues and sub-issues, open PRs, repository instructions, and continuity files.
Reconcile the existing roadmap and avoid duplicate issues. Separate observed
implementation from validation still owed, and disclose anything inaccessible.
Keep the scan bounded; inspect detailed code only for the next candidate.

Report a short dependency-aware roadmap, which toolchain gap is closest to
blocking the comic artifact tree, and one small checkpoint to do next. Propose
any useful issue/checklist changes, then come back to me before implementation.

For later execution, use the implementation-first profile: roughly 5–10-minute
checkpoints, one role per session, a committed handoff, and a draft PR. Defer
broad tests, documentation polish, local CI mirroring, and audits to explicit
completion checkpoints. Do not dispatch or rerun remote CI. Preserve existing
workflow settings and disclose automatic push/PR triggers. Do not merge unless
I authorize it. Record a finite loop-back boundary so validation stays visible.
```

This prompt deliberately requests a startup report. To execute a checkpoint
afterward, name it and its role:

```text
Execute the recommended implementation checkpoint under the same strategy.
Create or update its issue/checklist structure as needed, reusing existing work.
Keep the scope small; commit and push a draft PR with the repository handoff.
Report what changed, which checks ran, what remains deferred, and the next job.
Stop after this checkpoint. Leave the parent issue open while required
validation remains outstanding.
```

## Completion pass

Select one role per job, combining only work that fits the same small scope:
test authoring, test execution, documentation, local validation / CI preparation,
audit, or a named repair/refactor. Follow the handoff's finite loop-back trigger.
Run the repository's commands instead of inventing a second CI interface.

Keep three distinctions visible in every report:

- Implemented behavior versus verified behavior.
- Local evidence versus observed remote CI.
- Required acceptance fixes versus optional improvement issues.

The source contracts are
[repository continuity](../library/organization/specs/methodology/repository-continuity.spec.md)
and [local validation evidence](../library/organization/specs/quality/local-validation-evidence.spec.md).
Reuse existing consumer handoff paths. If none exists, the strategy suggests a
small `docs/work/<parent-issue-number>/HANDOFF.md` record and a pointer from root
`CONTINUITY.md` when present. Keep older unresolved obligations reachable from
their parent issues after the active repository checkpoint moves on.

No Flow issue ordering is frozen into this guide. Each bootstrap verifies the
live roadmap and bases its recommendation on the current artifact-tree goal.
