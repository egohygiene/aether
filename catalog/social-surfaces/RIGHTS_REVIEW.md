# Media Cheat Sheet rights review

## Decision

- Source candidate: `external/media-cheat-sheet-social-surface-snapshot`
- Snapshot captured: `2026-08-28T17:07:39Z`
- Snapshot SHA-256: `13a44970b5d1fd7a232eabc6a2abe42e7ba5c4a6a68e21484717f2b70509a0ac`
- Terms reviewed: <https://mediacheatsheet.com/terms/>
- Terms last updated by the source: `2026-08-21`
- Review date: `2026-08-29`
- Reviewer: OpenAI Codex, applying Aether's conservative source-governance policy; this is a repository publication decision, not legal advice.
- Decision record: <https://github.com/egohygiene/aether/issues/54>
- Resulting catalog version: `1.0.1`
- Resulting catalog digest (`sha256-utf8-lf`): `cc8186add31b923ceabdd0516c8f959823b36a0397262c2a03a1eef6d380e17e`

| Use | Decision | Evidence and boundary |
| --- | --- | --- |
| Private/internal reference | Permitted for creative work | The terms allow using specifications and guidance for personal or commercial creative work, subject to live verification. |
| Public normalized factual catalog | Not authorized from this snapshot | The terms do not expressly permit republication of the full specification directory; website content remains protected and only limited quotation/linking is identified. Aether therefore treats bulk normalized publication as disallowed. |
| Raw archive or SVG template redistribution | Prohibited | Templates may be used, modified, and shared with same-project collaborators, but may not be republished or redistributed as a competing library or standalone product. Aether does not redistribute them at all. |

## Repository consequences

- The catalog remains experimental and contains zero source-derived records.
- The source candidate is reviewed but restricted and non-publishable.
- The archive and its 302 SVG templates remain absent.
- The catalog and skill remain useful as an offline contract, deterministic
  query implementation, synthetic fixture, provenance record, and consumer
  lock boundary.
- A future independently gathered official-source catalog, or explicit
  permission covering normalized republication, must use a new version and
  digest and pass the normal Aether release gate.

Platform specifications can change. Any production use must verify selected
requirements against the linked official platform source before publishing or
spending money.
