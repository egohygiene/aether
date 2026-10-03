# Issue-title authoring pilot

This checkpoint connects Aether's existing authoring skill and read-only issue
creator to the organization's candidate contract and Egolint consumer. It
implements [Aether #98](https://github.com/egohygiene/aether/issues/98), a bounded
part of [the default-bundle roadmap](https://github.com/egohygiene/aether/issues/67).

## Discovery and ownership

- Aether's root [AGENTS.md](../AGENTS.md) explicitly selects observe mode and
  points to the [authoring skill](../library/organization/skills/authoring/github-issue-authoring/SKILL.md).
- The skill's [guide](../library/organization/skills/authoring/github-issue-authoring/references/canonical-issue-titles.md)
  resolves one digest-locked source selection. The cache carries unchanged
  upstream bytes, not a separately maintained type or emoji mapping.
- [The managed module](../library/organization/projections/templates/issue-authoring.AGENTS.md)
  is emitted into repository discovery fixtures and the issue-creator agent's
  provider projections. It uses the existing managed-block apply/remove helpers
  to preserve consumer prose and support repeat application and rollback.
- Consumers must explicitly select the policy, install the portable skill, and
  reconcile only the marked block into their local instruction file. Generated
  fixtures are examples, not evidence of installation, adoption, or hooks.
- Egolint owns title formatting and conformance; Aether verifies source/report
  provenance and guides authoring. The issue creator retains `read`, `search`,
  and `web` only. An authorized executor supplies executable validation evidence.

No new architecture decision is introduced: this follows the existing canonical
source, portable skill, managed module, and provider projection boundaries.

## Reproduce the bounded check

With Aether's existing Python dependencies installed, regenerate artifacts:

    python3 aether distribution build --output-directory dist
    python3 aether catalog generate

Build or obtain Egolint from the full consumer revision declared in
[selection.v1.json](../library/organization/skills/authoring/github-issue-authoring/references/issue-title-contract/selection.v1.json),
then use the real executable for the optional integration tests:

    AETHER_EGOLINT_BINARY=/absolute/path/to/egolint python3 -m unittest discover -s tests -p test_issue_title_authoring.py -v

The test stages a fresh temporary consumer with local `AGENTS.md` and the portable
skill, formats a reviewed checkpoint subject, checks report provenance, and
validates the proposed title/label snapshot. It also runs the upstream cases,
rejects incomplete snapshots and changed labels, and verifies that inputs remain
unchanged. Source integrity and managed-block tests run without Egolint; the
three real-consumer tests explicitly skip when the environment variable is
absent. A configured but missing or incompatible executable fails the check.

These are synthetic local results. They do not prove live provider label
availability, a particular host's automatic instruction loading, or a GitHub
write. A proposal passing locally still needs current provider evidence before
an authorized create/update.

## Remaining work

The selected contract and Egolint consumer remain candidates until their owning
reviews complete ([contract PR #45](https://github.com/egohygiene/.github/pull/45),
[Egolint PR #79](https://github.com/egohygiene/egolint/pull/79)). Upgrade pins and
authority through an explicit reviewed change after verifying the accepted
sources. Contract acceptance, local adoption, validation, and enforcement are
separate facts.

Reusable execution/provider mutation, label provisioning, real-repository
adoption, and the fleet title sweep remain separate checkpoints under
[the organization roadmap](https://github.com/egohygiene/.github/issues/24).
This change does not complete the broader default bundle or install it across
repositories.
