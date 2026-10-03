<!-- BEGIN AETHER ISSUE-AUTHORING -->
<!-- aether-instruction {"id":"issue-authoring","selection":"library/organization/skills/authoring/github-issue-authoring/references/issue-title-contract/selection.v1.json","selection_sha256":"435d9310e49ee10cafa3f477c2080a88e666a247e9496dc40dbb17356d319582","skill":"github-issue-authoring","status":"draft","version":"0.1.0"} -->
## Issue authoring discovery

When scoped repository instructions explicitly select the Ego Hygiene issue-title
policy, read `.agents/skills/github-issue-authoring/SKILL.md` from the consumer
root and its `references/canonical-issue-titles.md`. If installed elsewhere,
resolve the declared local skill path. If absent, report discovery unavailable;
this block alone does not install the skill or adopt the policy.

Follow `references/issue-title-contract/selection.v1.json` inside that skill for
the immutable contract, source digests, and candidate authority. Preserve the
reviewed subject and IDs; obtain title and intended label from that selection.
An already authorized executor may use Egolint and the skill's source verifier.
Read-only roles prepare drafts or consume executor evidence without gaining
execution permission. Missing sources/tools, stale pins, ambiguous type labels,
and unavailable current provider labels remain explicit gaps.

This is static discovery guidance, not a hook or fleet migration. Organization
instructions do not automatically inherit into consumer repositories. Preserve
consumer-owned prose, nested instruction precedence, and role permissions.
<!-- END AETHER ISSUE-AUTHORING -->
