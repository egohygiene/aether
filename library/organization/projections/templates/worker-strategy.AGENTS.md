<!-- BEGIN AETHER WORKER-STRATEGY -->
<!-- aether-instruction {"id":"worker-strategy","version":"1.0.0","status":"draft","skill":"execute-issue-checkpoint","spec":"worker-strategy","spec_version":"0.2.0"} -->
## Bounded issue execution

For authorized repository issue work, compose `execute-issue-checkpoint` with
the selected `worker-strategy`, continuity, local-validation and roadmap-impact
contracts. Keep small issues unsplit; preserve a larger parent with the smallest
useful checkpoints; reuse existing stable checkpoint/PR identities. Parent links
group scope and do not create false blockers. Preserve all original acceptance.

Execute one bounded checkpoint at a time within the caller's authorized batch.
Save meaningful progress and the exact resume action before planned handoffs;
commit/push/update the existing draft PR only when current authority permits.
Reverify actual branch, working tree, issue/PR and checks on fresh-session resume.
Prepared, validated, review-ready, merged and delivered remain separate; retain
failed/unrun/unavailable checks and parent obligations. Read-only roles gain no
writes. Missing access, unpushed work and abrupt-loss limits stay explicit.

This draft module supplies guidance, not a scheduler, installed recovery hook,
guaranteed context warning, zero-loss promise or fleet-adoption evidence.
<!-- END AETHER WORKER-STRATEGY -->
