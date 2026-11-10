# Issue #107 implementation handoff

Issue: https://github.com/egohygiene/aether/issues/107
Roadmap: https://github.com/egohygiene/aether/issues/105
Role: implementation; stop after draft PR delivery and maintainer sync.
Base: `dc8a16851f452763ef4f7fbe4bf057d4500b1921` (`main`).
Branch: `fix/107-authoritative-catalog-metadata`.
Strategy: repository-owned Bounded Worker Strategy 0.1.0 at the base revision above.

## Implemented

- Existing catalog records refresh source-owned metadata instead of updating only their digest.
- Catalog-owned summaries/annotations and explicit release exclusions are retained. Non-stable source cannot remain release-included.
- Approved specification lifecycle normalizes to stable while retaining `source_state: approved`, including normalized provenance.
- Invalid source metadata prevents catalog replacement; field-level drift diagnostics remain independent of digest freshness.
- First-party catalog and contribution guidance are updated; focused regression cases are authored.

No canonical skill/specification lifecycle or version is promoted. No release, tag, package publication, workflow dispatch, or work on #108–110 is included.

## Checks actually performed

- `./aether catalog generate`: completed successfully; artifact generation only.
- Python `ast.parse` on changed Python files: completed successfully; syntax only.
- `git diff --check`: completed successfully; whitespace only.
- Source/diff review: the regenerated catalog reconciles seven stale artifact versions and current source relationships.

Regression tests have **not** run. No behavioral, integration, merge-readiness or publication claim is made. Commits use `[skip ci]` to suppress existing GitHub push/PR workflows without changing workflow configuration.

## Deferred completion pass

Test execution, full deterministic validation, distribution qualification and hosted CI are deferred at the maintainer's request. Run these against the exact final PR head during the later sweep:

```sh
python3 -m unittest discover --start-directory tests --pattern test_aether_validator.py --verbose
python3 -m unittest discover --start-directory tests --pattern test_provenance_model.py --verbose
./aether catalog generate --check
./aether validate --catalog --provenance --format json
python3 catalog/validate_catalog.py
python3 catalog/provenance_model.py check --scope all
./aether distribution build --output-directory dist
./aether distribution build --output-directory dist --check
```

Confirm source version/lifecycle/description/license/dependency mutations update metadata, current-digest stale metadata fails validation, invalid source does not replace the catalog, approved source provenance survives normalization, catalog-owned settings survive, and repeated generation produces identical bytes. The three authored catalog regressions and one provenance regression are unexecuted starting points for that sweep; they do not replace full acceptance review.

## Original next action and boundaries (historical)

Review the draft against issue #107, then run and record the deferred checks before accepting it. Audit PR #106 and its historical artifacts are independent; reconcile handoff conflicts without rewriting dated evidence. Tracker #105 selects #108 next, but this session stops for maintainer sync after #107.

## Current reconciliation for Audits/Sanity source work

The current authorized continuation reconciles original source
`4d22c53148e7775ebbf3049768c1c2a89152efc2` with main
`5077797448d32a59b06eabe4b38f091137d58052`. Evaluator/distribution containment
source and both sets of authored regression imports/cases are retained. The
updated root continuity records PR #115, static source/JSON/AST and merge
inspection, and the deferred qualification scope. The original stop-after-draft
note describes that earlier checkpoint; it does not override the maintainer's
subsequent implementation/merge authorization. Audit PR #106 remains independent.

This correction is a metadata prerequisite for the new Aether #86/#87 contracts.
Their canonical source, generated catalog and distribution projections are
separate slices. No canonical lifecycle or human approval is promoted, and no
regression, native, CI, distribution or publication acceptance is claimed here.
