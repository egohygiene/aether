# Aether completeness, usability, and work-ledger audit

- **Assessment ID:** `aether-completeness-20261020T011246Z`
- **Assessment date:** 2026-10-20 UTC. The identifier is not a cutoff for later validation receipts recorded during this assessment.
- **Repository:** [egohygiene/aether](https://github.com/egohygiene/aether)
- **Frozen source:** [`dc8a16851f452763ef4f7fbe4bf057d4500b1921`](https://github.com/egohygiene/aether/tree/dc8a16851f452763ef4f7fbe4bf057d4500b1921)
- **Git tree:** `26b3ffdf1f6d2758631157d9c8cf5b991c4ad258`
- **Governing specification:** [auditor 2.0.0, approved][auditor]
- **Procedure:** [audit-repository 1.1.0, draft][audit-skill], composed with repository-continuity **Resume** behavior.
- **Report status:** **partial**. Local Linux source, deterministic validation, bounded counterexamples, hosted-run evidence, staging inventory, and the complete original issue ledger were inspected. Published delivery, real host adoption, platform coverage, and a comprehensive security assessment remain unverified.
- **Validation receipt:** [data/aether-completeness-20261020T011246Z.validation.json](data/aether-completeness-20261020T011246Z.validation.json), intended repository path `audits/data/aether-completeness-20261020T011246Z.validation.json`.
- **Tactical ledger at assessment:** [roadmap #105](https://github.com/egohygiene/aether/issues/105), with 30 original work issues. Eight new issue keys below are **uncreated candidates in this dated assessment**. Subsequent tracker changes belong in the live roadmap, not as retroactive edits to this assessment.

## Executive summary

Aether has a substantial working foundation: canonical source roots, 68 skill/specification catalog records, deterministic distributions, a unified CLI, provenance records, provider projections, repository-continuity composition, and a large passing local test suite. The immediate problem is making existing evidence and delivery claims agree, then bringing the original backlog and deferred migration work into one navigable ledger. Finishing every speculative integration is not necessary to make that foundation usable.

Eighteen findings are recorded here: fourteen medium and four low. No high or critical finding was confirmed. Four bounded implementation repairs concern catalog metadata, build exit/inventory behavior, evaluation evidence, and filesystem containment. Seven release/consumer findings belong to existing #38. Three migration/governance findings address intake/removal controls, overdue external reviews, and deferred migration coverage. Four documentation/handoff findings address contradictory current-state descriptions, an obsolete next action, a dated staging view, and a stale audit-skill issue pointer.

The healthy local path passes: two independent 335-file distribution builds are byte-identical; CLI validation, shell checks, strict staging validation, catalog/schema/provenance checks, deterministic eval execution, and the official checksum-verified GitHub CLI publication dry run succeed. The complete prepared local suite runs **199 tests with zero skips**. These successes coexist with concrete negative-case defects. The deterministic eval output reports 205 cases, of which 195 execute zero machine checks; many are intentionally structural/prose cases and are not, by that count alone, defects or behavioral-model proof.

There are no releases or tags and no open PRs at the assessment snapshot. The exact-main release workflow failed before scheduling any jobs. The successful PR validation run and publication dry run therefore do not establish a working published release, consumer update path, or stable default bundle. Consumer-installation readiness is also not established; the final receipt and the separate consumer-qualification note below distinguish successful CLI operations from failing semantic package checks.

## Scope, context, and evidence rules

The request covers a comprehensive repository audit, reconciliation against every open issue, and a roadmap that preserves existing scope. This report is the read-only audit artifact; tracker reconciliation and roadmap edits are separately authorized follow-on work. This procedure does not grant permission to publish artifacts, ratify decisions, promote draft content, run staged hooks, transfer ownership, or delete staged source.

The source snapshot contains **1,543 tracked Git entries** and **13,619,985 bytes of blob payload**. Counts describe tracked content, not a checkout's disk allocation or an installed product.

| Inventory | Observed count |
| --- | ---: |
| Canonical specifications | 32 |
| Canonical skills | 36 |
| Canonical agents | 9 |
| Canonical instruction modules | 1 |
| First-party catalog records | 68: 36 skills and 32 specifications |
| Catalog lifecycle | 59 draft, 8 experimental, 1 stable |
| Release-included stable catalog records | 1: `specification/auditor` |
| Tracked distribution files | 335 |
| Tracked staging files | 734 |
| Staging blob payload bytes | 6,791,350 |
| Current staged skill directories containing `SKILL.md` | 186 |
| Approved external skill-text records checked against current staged text | 56 of 56 digests match |
| Unresolved-provenance staged skill entries | 130 |
| Historical removed first-party skill entries | 6 |
| First-party disposition documents | 14: 6 removed skills and 8 hook/integration decisions |
| Open work issues / existing roadmap issues | 30 / 1 |
| Open PRs / releases / tags | 0 / 0 / 0 |

The staging buckets contain agents 13, hooks 26, instructions 2, integrations 42, manifests 2, scripts 2, skills 641, and specs 6 files. Nine generic agents have canonical destination paths; four domain agents retain move-out ownership. Destination acceptance receipts were not independently verified. The only repeated staged Git-blob group found is two empty files; the audit does not recommend blanket deduplication.

Evidence labels used throughout:

- **Observed:** source, inventory, fetched tracker/run state, or executed bounded result directly inspected.
- **Inferred:** a conclusion from the observed contract or control flow, with its scope stated.
- **Recommended:** proposed repair, acceptance criteria, or sequencing, not delivered work.
- **Unverified:** unavailable or unexecuted evidence; not treated as success or failure.

Severity, confidence, status, effort, and impact use the governing auditor's normalized vocabulary. A medium severity boundary defect does not assert a demonstrated exploit. Finding history uses `new`, `recurring`, `changed`, `apparently resolved`, or `unable to verify`; “new” means newly established in this assessment, not proof of when a defect was introduced.

## Method and history reconciliation

The audit read [AGENTS][agents] first, then the canonical auditor and audit procedure, continuity Resume guidance and the current handoff, navigation/architecture documents, catalog and provenance contracts, source/build/eval/release helpers, workflows and focused tests. It inventoried the immutable Git tree and all staged files, inspected all 30 work issues plus #105 and their empty comment collections, checked the native roadmap hierarchy, and read referenced upstream issue/policy evidence where relevant to sequencing. It compared the public entry path a fresh human or bot follows with actual source and generated output.

The exact approved Hygiene ADR policy selection was checked against upstream evidence: policy **1.2.0** at `a05b14f8b9e2772124f879f818e09a911e996ad8`, approved in [Hygiene PR #72](https://github.com/egohygiene/hygiene/pull/72). The existing human ratification and four-digit naming amendment are already recorded. This audit does not manufacture another ratification prerequisite or promote Aether's draft authoring artifacts.

No canonical `audits/` directory exists at the frozen source. The animation-plugin audit inside staging is not a previous Aether repository audit. Relevant historical evidence includes the dated [staging evacuation status][staging-status], closed #18, accepted ADRs, the older ROADMAP audit summary, and recently merged foundation work. Historical documents and accepted decisions must remain historically legible.

| Historical observation | Classification in this assessment |
| --- | --- |
| Canonical catalog/build/projection/continuity foundations described as future work | **Apparently resolved** for their bounded delivered portions; current-state prose still conflicts with them (AUDIT-014). |
| Closed #18 intake/removal-control intent and explicitly deferred migration corpus | **Recurring** unmet control/coverage scope (AUDIT-011, AUDIT-013). Closed issue history is preserved. |
| August external reviews with September deadlines | **Changed**: deadlines are now overdue as of the explicit October assessment date (AUDIT-012). |
| Active pre-merge continuity action | **Changed** by merged PR #104; the stated next merge action is superseded (AUDIT-015). |
| Dated staging counts/decisions and old issue pointer | **Recurring** navigation drift (AUDIT-016, AUDIT-017). |
| First artifact release | **Unable to verify** as delivered: no release/tag exists, and the exact-main workflow schedules zero jobs. Local build/dry-run foundations are observed. |

Root validation used prepared development dependencies and explicit owner/native inputs. Negative-case reproductions ran in temporary fixtures/copies, not by changing the audited source or executing staged instructions. An observed repro success below often means the defect was reproduced; it is not a product-readiness pass. No real secret, provider write, tag creation, release, deployment, or destructive migration was needed.

## Overall assessment

The current source is a credible base for a focused repair and qualification cycle. Keep canonical sources under `library/organization/` and `catalog/`, preserve generated output provenance, repair the current trust/evidence boundaries, and refresh live navigation before extending scope. The original 30 work items remain visible; the roadmap should distinguish a usable authoring/distribution spine from the full opt-in backlog.

The report is **partial**, because local source/tests and tracker evidence cannot substitute for released consumer adoption. Required continuation evidence includes an explicitly authorized release proof, actual immutable install/update/rollback acceptance, relevant host/platform canaries, source-rights/destination review where migration needs it, and any separately scoped security assessment. None of those limitations blocks the bounded local repairs proposed here.

## Findings summary

| ID | Finding | Severity | Confidence | Status | History | Coverage at assessment |
| --- | --- | --- | --- | --- | --- | --- |
| AUDIT-001 | Catalog regeneration retains stale source-owned metadata | medium | high | confirmed | new | Uncreated `CATALOG` candidate |
| AUDIT-002 | Normal builds return success on errors and checks ignore extra owned output | medium | high | confirmed | new | Uncreated `BUILD` candidate |
| AUDIT-003 | Eval run can pass invalid, empty, or unexecuted requested checks | medium | high | confirmed | new | Uncreated `EVAL` candidate |
| AUDIT-004 | Spec output and skill companions can cross declared filesystem boundaries | medium | high | confirmed | new | Uncreated `BOUNDARY` candidate |
| AUDIT-005 | Release job env uses an unavailable steps context | medium | high | confirmed | new | Existing #38 |
| AUDIT-006 | Release identity uses dispatch SHA and a mutable tag between jobs | medium | high | confirmed | new | Existing #38 |
| AUDIT-007 | Privileged GitHub CLI release steps lack token mapping | medium | high | confirmed | new | Existing #38 |
| AUDIT-008 | Selected stable manifest and actual archive are not closed over the same payload | medium | high | confirmed | new | Existing #38 |
| AUDIT-009 | Rebuilding release metadata includes stale/self-referential digests | medium | high | confirmed | new | Existing #38 |
| AUDIT-010 | Changelog parser misses the required bracketed Unreleased section | low | high | confirmed | new | Existing #38 |
| AUDIT-011 | Strict staging validation does not enforce intake or base/head removal approval | medium | high | confirmed | recurring | Uncreated `STAGING` candidate |
| AUDIT-012 | External reviews are overdue and impossible calendar dates validate | medium | high | confirmed | changed | Uncreated `EXTERNAL` candidate |
| AUDIT-013 | Deferred migration residuals lack a live, bounded work-issue home | medium | high | confirmed | recurring | Uncreated `MIGRATION` candidate |
| AUDIT-014 | Architecture, instructions, and accepted decisions conflict with current source | medium | high | confirmed | recurring | Uncreated `DOCS` candidate |
| AUDIT-015 | Active continuity still proposes merging already-merged work | low | high | confirmed | changed | Uncreated `DOCS` candidate |
| AUDIT-016 | Dated evacuation snapshot contradicts completed removal/classification evidence | low | high | confirmed | recurring | Uncreated `MIGRATION` candidate |
| AUDIT-017 | Audit procedure routes staged reconciliation to old Issue 016 | low | high | confirmed | recurring | Existing #86 |
| AUDIT-018 | Consumer readiness fails while its report-generator test remains green | medium | high | confirmed | new | Existing #38; related #63/#67 |

### Critical and high severity

None confirmed within the inspected scope. This is not a clean bill of health from a full security assessment.

### Medium severity

#### AUDIT-001 — Catalog regeneration retains stale source-owned metadata

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** catalog/provenance. **Effort:** medium. **Impact:** high. **History:** new.
- **Observation — observed:** seven current catalog versions differ from their canonical source. Regeneration copies an existing record and refreshes its digest without rederiving overlapping source-owned metadata. The catalog can therefore contain a current source digest and an old version/lifecycle while drift validation succeeds.
- **Evidence:** [aether_validator.py:794–816,876–888][validator]; [catalog/README.md:38–50][catalog-guide]; [first-party catalog:3457–3458][catalog]. The bounded reproduction changed a temporary complete corpus's audit skill to `9.9.9`/`stable`; regeneration retained `1.1.0`/`draft`, and catalog validation reported zero errors before and after.
- **Why it matters — inferred:** consumer discovery, provenance, and eventual release eligibility can disagree with the source while the generated catalog appears verified. No invalid artifact was shown to have been published.
- **Recommendation — recommended:** derive shared fields from parsed current source metadata, retain catalog-owned fields deliberately, and validate semantic disagreement independently of source-digest freshness. Preserve documented legacy lifecycle normalization.
- **Suggested validation:** version, description, license, dependency and lifecycle mutations update the generated fields; invalid source metadata and stale source-owned fields fail. Preserve intentional auditor `approved` → catalog `stable` mapping plus `source_state`; that mapping is not a defect.
- **Dependencies or risks:** no external predecessor is needed for this repair. Avoid overwriting hand-authored catalog-only policy or promoting draft artifacts. **Coverage:** uncreated `CATALOG` candidate; #38 is related release acceptance, not an explicit owner of this independent current catalog defect.

| Artifact | Source version | Catalog version |
| --- | --- | --- |
| skill/create-decisions-document | 2.1.0 | 1.1.0 |
| skill/create-epistemology-document | 1.1.0 | 1.0.0 |
| skill/github-issue-authoring | 1.2.0 | 1.1.0 |
| skill/social-surface-specs | 1.0.1 | 1.0.0 |
| skill/validate-repository-locally | 1.1.0 | 1.0.0 |
| specification/architecture-decisions | 3.1.0 | 2.0.0 |
| specification/architecture-document | 2.1.0 | 2.0.0 |

#### AUDIT-002 — Normal builds return success on errors and checks ignore extra owned output

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** CLI/build. **Effort:** medium. **Impact:** medium. **History:** new.
- **Observation — observed:** normal skill/spec generation logs exceptions and counts drift but returns zero unless check mode is selected. Expected-file comparison does not reject additional stale packages/files in the generator's owned output.
- **Evidence:** [skill builder:265–271,291–303][skill-builder] and [spec builder:79–94][spec-builder]. A synthetic declared-but-missing distribution resource produces `ERROR`, zero packages, and normal exit 0; check mode exits 1. An extra `dist/skills/removed-skill/SKILL.md` beside correct output survives and check mode still exits 0.
- **Why it matters — inferred:** a documented build can claim success without creating the requested artifact, and regeneration can retain a removed package. Clean CI's later check mitigates ordinary generation errors but does not repair standalone exit semantics or full-inventory comparison.
- **Recommendation — recommended:** propagate generation errors in every mode; distinguish generation failure from content drift; compare complete owned output inventories and diagnose unexpected paths.
- **Suggested validation:** missing/malformed input, partial multi-artifact failure, removed package, extra companion, and clean build/check have explicit nonambiguous outcomes.
- **Dependencies or risks:** no new build platform or upstream gate is required. Fail safely on extra user output rather than silently deleting it. **Coverage:** uncreated `BUILD` candidate, linked to #38's qualification work.

#### AUDIT-003 — Eval run can pass invalid, empty, or unexecuted requested checks

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** evaluation/evidence. **Effort:** medium. **Impact:** high. **History:** new.
- **Observation — observed:** `run_evals()` bypasses the schema/duplicate preflight used elsewhere, attaches category failure only when a case exists, and executes declared assertions only inside the existing-golden branch. Overall success is based on a zero failure count.
- **Evidence:** [aether_validator.py:1470–1517,1528–1585,1605–1627][validator]. Three bounded counterexamples pass: an empty v2 cases array despite separate `AETHER_EVAL_001` validation; an unmatched explicit skill filter with zero skills/cases; and a declared `contains` assertion without a golden, yielding empty checks and no validation error.
- **Why it matters — inferred:** typoed selections or incomplete evidence can look like successful requested evaluation. This is distinct from intentional prose/trigger-routing structural cases, which do not claim to execute an LLM. The 195 current cases with zero machine checks are not all classified as defects.
- **Recommendation — recommended:** share preflight, reject invalid suites and unmatched explicit selections, and require the evidence declared assertions need. Report nonexecuted assertions as nonexecuted/partial, not passed; filesystem assertions should not accidentally depend on a text golden.
- **Suggested validation:** invalid schema, duplicate IDs, zero-case suites, unmatched filters, missing golden with an assertion, and positive real assertions. Retain explicit structural-only semantics and avoid implying model-behavior coverage.
- **Dependencies or risks:** no paid model or provider is needed to fix deterministic evidence correctness. **Coverage:** uncreated `EVAL` candidate; #73 owns future task/model evaluations, not this runner bug.

#### AUDIT-004 — Spec output and skill companions can cross declared filesystem boundaries

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** filesystem/package boundaries. **Effort:** medium. **Impact:** high. **History:** new.
- **Observation — observed:** spec IDs are used as output paths without adequate syntax/containment validation. Automatic skill-companion discovery follows symlinks with `is_file()`/`read_bytes()` without enforcing resolved source containment.
- **Evidence:** specification collection in [aether_validator.py][validator]; [spec builder:36–48,60–76][spec-builder]; [skill builder:210–217,232–238][skill-builder]. Synthetic ID `../../escaped` validates and builds with exit 0, writing outside the chosen distribution directory. A companion symlink to a harmless sentinel outside the temporary repository is copied into output as an ordinary file; a later output-symlink check cannot recover that lost origin.
- **Why it matters — inferred:** malformed authoring can write beyond the selected output boundary or package bytes outside canonical source. The reproduction used only synthetic data. No real secret, external disclosure, code execution, or privilege escalation was established.
- **Recommendation — recommended:** parse metadata once, validate spec IDs, enforce resolved destination containment, and reject or explicitly govern companion symlinks/source escapes. Reuse the stricter explicit-resource guards where applicable.
- **Suggested validation:** traversal/absolute/invalid IDs, symlinked file and directory companions, legitimate contained resources, and harmless outside sentinels. Assert no write/read escapes and no leakage into the generated package.
- **Dependencies or risks:** local repair can start now; portability and intended within-tree symlink behavior need explicit decisions. **Coverage:** uncreated `BOUNDARY` candidate; do not inflate it into an unsupported exploit claim.

#### AUDIT-005 — Release job env uses an unavailable steps context

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** CI/release scheduling. **Effort:** small. **Impact:** high. **History:** new.
- **Observation — observed:** job-level env sets `AETHER_E2E_REMOTE_TAG` from `steps.release-context.outputs.release_tag`. GitHub's context matrix does not allow `steps` in `jobs.<job_id>.env`; it is allowed in a later step's env and in appropriate outputs.
- **Evidence:** [release workflow:27–31][release-workflow]; [GitHub context availability reference](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts). Exact-main [run 39167340837](https://github.com/egohygiene/aether/actions/runs/39167340837), attempt 1 at the audited SHA, failed immediately with **zero jobs**. The provider's detailed validation annotation was unavailable through the inspected connector resources; the invalid context is established by exact source and the official matrix.
- **Why it matters — inferred:** the current release/consumer qualification workflow cannot schedule its jobs. Local unit success and a prior PR workflow green badge cannot establish this path works.
- **Recommendation — recommended:** resolve the output only at a supported later step/job boundary; add a narrowly scoped provider-valid workflow check.
- **Suggested validation:** provider syntax/context acceptance and an actual nonpublishing validation run with scheduled jobs, followed by the already-owned release checks. Do not dispatch or publish merely as part of this read-only audit.
- **Dependencies or risks:** this is local configuration repair; a release write still requires separate authority under AGENTS. **Coverage:** existing [#38](https://github.com/egohygiene/aether/issues/38), not a new release umbrella.

#### AUDIT-006 — Release identity uses dispatch SHA and a mutable tag between jobs

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** release identity/provenance. **Effort:** medium. **Impact:** high. **History:** new.
- **Observation — observed:** validation checks out the user-selected existing tag but passes event `GITHUB_SHA` to the provenance builder. Publication checks out the tag again rather than a validated commit and again records event SHA. For a dispatch from main targeting an older tag, event SHA and payload HEAD identify different objects.
- **Evidence:** [release workflow:53–57,95–98,147–151,177–180][release-workflow]; [release builder:226–245][release-builder]; [GitHub workflow_dispatch reference](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#workflow_dispatch). A bounded execution of the actual provenance helper with one synthetic file preserves an arbitrary supplied 40-character SHA without checking payload HEAD. The inspected rulesets response was empty, and the publication dry run warns there is no active tag protection. No retag attempt or published mislabeling occurred.
- **Why it matters — inferred:** provenance may name the workflow trigger rather than the packaged source; a mutable tag can select different source across validation and publication. Declared immutable-tag intent is not a digest-bound job handoff.
- **Recommendation — recommended:** resolve tag-to-full-commit once, use that exact checked-out commit in metadata and both jobs, and bind accepted payload digests across the handoff. Preserve event SHA separately if useful.
- **Suggested validation:** older-tag/default-branch dispatch, mismatch rejection, moved-tag-between-jobs rejection, and exact commit/digest agreement in approved metadata and bytes. Use synthetic fixtures before any authorized publication.
- **Dependencies or risks:** related release-design issues can inform the successor contract, but the known local identity wiring can be corrected now. **Coverage:** existing #38; related #63/#94/#95 are not prerequisites invented by this finding.

#### AUDIT-007 — Privileged GitHub CLI release steps lack token mapping

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** release authentication. **Effort:** small. **Impact:** medium. **History:** new.
- **Observation — observed:** the publication job grants contents-write but does not map `GH_TOKEN` or `GITHUB_TOKEN` for GitHub CLI release-view, live skill-publish, and release-upload commands. Checkout's Git credential configuration does not establish CLI authentication.
- **Evidence:** [release workflow:142–145,198–216][release-workflow]; GitHub's [workflow CLI guidance](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-github-cli) and [CLI environment contract](https://cli.github.com/manual/gh_help_environment). No credential was accessed, displayed, or used for a publication attempt. A successful CLI dry run is not proof of live authenticated execution.
- **Why it matters — inferred:** after the scheduling defect is repaired, a clean runner's privileged CLI commands still lack their documented authentication input.
- **Recommendation — recommended:** map the existing job token only where required, with appropriate existing least-privilege permissions; add a bounded authentication/preflight checkpoint before an independently authorized write.
- **Suggested validation:** documented CLI token availability in required steps without printing it, correct behavior when absent, and controlled authentication/read preflight. Live publication remains a separately authorized acceptance step.
- **Dependencies or risks:** avoid broadening role permissions or introducing a new credential platform. **Coverage:** existing #38.

#### AUDIT-008 — Selected stable manifest and actual archive are not closed over the same payload

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** artifact selection/distribution closure. **Effort:** medium. **Impact:** high. **History:** new.
- **Observation — observed:** release metadata selects stable/included records, while the workflow rebuilds all distributions and passes `dist` to the publisher. The tar archive includes entire `skills`, `github`, and `release` trees, rather than the selected manifest closure. Catalog bytes and other provider/specification resources are outside those archive roots.
- **Evidence:** [release builder:39–50,96–137][release-builder]; [release workflow:165–180,187–205][release-workflow]. An exact-tar-options synthetic fixture with one selected stable skill, one draft skill, a selected governed catalog, and provider/spec resources exits 0: the archive contains both skills and omits selected catalog/provider/spec resources. GNU tar correctly excludes its output archive; tar self-inclusion is not a separate finding. The actual `gh skill publish` payload was not published and its byte selection must be inspected before acceptance.
- **Why it matters — inferred:** manifest eligibility alone does not keep draft extras out of the delivered archive or ensure selected resources arrive. No draft artifact was shown to have been released; no release exists, and current stable skill selection is not yet qualified.
- **Recommendation — recommended:** assemble one manifest-selected payload and validate every archived/published path/digest against its allowed closure. Reject extra drafts and missing selected resources; do not promote draft artifacts just to make release selection pass.
- **Suggested validation:** selected stable plus unselected draft fixtures, governed catalogs/companions, actual archive inventory, adapter payload preview, missing-resource and extra-resource failures, and immutable install acceptance.
- **Dependencies or risks:** keep present v1 repair bounded; coordinate broader channels with #63 without making all adapters mandatory. **Coverage:** existing #38.

#### AUDIT-009 — Rebuilding release metadata includes stale/self-referential digests

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** release reproducibility/provenance. **Effort:** medium. **Impact:** high. **History:** new.
- **Observation — observed:** rebuilding release metadata into the same output includes files produced by the previous run, including old release provenance, in subsequent checksum/provenance inputs. The current provenance can list its own old digest.
- **Evidence:** [release builder:148–156,227–247,250–281][release-builder]. Two consecutive runs with identical synthetic input and the same output directory change `checksums.txt` and `release-provenance.v1.json`. The second provenance lists itself, but its recorded digest differs from the final file bytes.
- **Why it matters — inferred:** the resulting checksum inventory is not a reproducible description of final release bytes. The workflow's two-build distribution comparison runs before this metadata stage and does not prove metadata repeatability.
- **Recommendation — recommended:** define an explicit non-self-referential payload inventory and generation order; make output independent of stale prior generated metadata.
- **Suggested validation:** same-output repeat, clean-directory independent repeat, preseeded old metadata, and validation of every declared digest against final files. State which metadata files are intentionally outside their own inventories.
- **Dependencies or risks:** preserve digest semantics and avoid circular self-hash promises. **Coverage:** existing #38.

#### AUDIT-011 — Strict staging validation does not enforce intake or base/head removal approval

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** CI/provenance/migration controls. **Effort:** medium. **Impact:** medium. **History:** recurring, newly reproduced from closed #18 item 10 and ADR-0005 scope.
- **Observation — observed:** staging validation checks the eight immediate bucket names, not nested intake records or actual removals. The PR workflow validates the present tree without a base/head removal approval gate. The dated status claims a stronger intake requirement than the check supplies.
- **Evidence:** [aether_validator.py:1247–1263][validator]; [PR workflow:23–51][pr-workflow]; [DECISIONS.md:234–245][decisions]; [staging status:158–165][staging-status]; [staging inventory tests:40–77][staging-tests]. In a temporary root, an unrecorded nested `SKILL.md` produces zero strict diagnostics; deleting it without approval also produces zero diagnostics. This does not claim the complete CI suite accepted a real unapproved deletion.
- **Why it matters — inferred:** a strict-stage pass establishes neither recorded intake nor per-file reviewed removal. Skill inventory tests cover some root/count expectations, not immutable authorization for all 734 files.
- **Recommendation — recommended:** explicitly distinguish grandfathered legacy retention from new intake; validate typed current records; compare actual base/head removals against exact preimage digests and required durable dispositions/destination receipts.
- **Suggested validation:** unrecorded intake rejected; documented legacy retention allowed; missing, stale, fabricated, or changed-source approval rejected; exact approved removal accepted; unrelated changes need no staging cleanup. Test all relevant file classes, not only root skills.
- **Dependencies or risks:** reconcile ADR-0005's literal outcomes with newer catalog/reference practice through the appropriate human-governed decision. Eight older hook records do not claim the six removed-skill records' schema; their schema mismatch shows a typed-enforcement gap, not invalid decisions. Do not require adopting or resolving all old unknown sources to introduce a gate. **Coverage:** uncreated `STAGING` candidate; preserve closed #18.

#### AUDIT-012 — External reviews are overdue and impossible calendar dates validate

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** external-source provenance/freshness. **Effort:** medium. **Impact:** medium. **History:** changed since the recorded August review.
- **Observation — observed:** three of four source records have a `next_review.not_after` date of 2026-09-30, twenty calendar days before the assessment date. This includes the source of all seven allowlisted references. Structural governance validation accepts these records and also accepts `2026-99-99` in a temporary copy.
- **Evidence:** [source-review register:34–35,65–66,124–125][external-register]; [review cadence:10–15,23–25][external-cadence]; [external validator:45–51,66–69,124–126][external-validator]; [external review guide:35–46][external-guide]. The overdue records are `coreyhaines31-marketingskills` (deferred), `emilkowalski-skill` (allowlisted), and `vercel-labs-skills` (deferred). Their current structural validator returns no errors.
- **Why it matters — inferred:** validity does not communicate that time-sensitive review has lapsed. Reference-only restrictions reduce exposure but do not refresh an assessment. No new upstream vulnerability or license violation was established.
- **Recommendation — recommended:** conduct and record a bounded current review, retain pins/evidence until independently reviewed, parse actual calendar dates, and provide reproducible explicit-`as_of` current/overdue/unknown assessment.
- **Suggested validation:** frozen-time current/overdue cases, impossible dates, future/retrograde records, before/at/after deadlines, and allowlisted versus deferred dispositions. Review must not grant new external effects or silently slide deadlines.
- **Dependencies or risks:** fresh upstream assessment may need external evidence; offline deterministic checks are not live advisory scans. **Coverage:** uncreated `EXTERNAL` candidate, not #38's first-party release or specialized #71/#72 scope.

#### AUDIT-013 — Deferred migration residuals lack a live, bounded work-issue home

- **Classification:** maintainability risk. **Severity:** medium. **Confidence:** high for local inventory/coverage. **Status:** confirmed. **Area:** ownership/backlog completeness. **Effort:** medium for reconciliation; eventual adoption is unknown. **Impact:** medium. **History:** recurring, explicitly deferred in the dated #18 report.
- **Observation — observed:** closed #18 and its status document enumerate 130 unresolved skill entries, four move-out agents, hook residuals, integrations, instructions/scripts/specs, and old task-note mapping. None of the original 30 work issues provides one current bounded home for this residual corpus. No later issue-home comment is recorded on #18.
- **Evidence:** [closed #18](https://github.com/egohygiene/aether/issues/18), the complete original issue inventory below, [staging status:145–181][staging-status], and [staged agent ledger:61–83][agent-ledger]. All 734 staged files were inventoried; destination receipts remain unverified rather than presumed absent or completed.
- **Why it matters — inferred:** the original roadmap can accurately cover every open issue while omitting deferred migration work the maintainer wants to resume. Unknown receipts are not permission to remove source.
- **Recommendation — recommended:** create one finite reconciliation stream mapping each semantic unit and its supporting files to owner, source digest, disposition, and a bounded next job or honest retained/deferred state. Separate inventory, owner adoption, transfer proof, and source removal checkpoints. Preserve #18 history.
- **Suggested validation:** every tracked staging file accounted for without duplicate/dangling ledger entries; nine canonical agent deltas reviewed; durable receipts or explicit unknowns for four move-outs/integrations; each unresolved class has a next job; reruns do not create duplicate issues.
- **Dependencies or risks:** inventory can start now; adoption and deletion require relevant owners/review. Mindgarden/capture/animation routing hints are not verified destination decisions. Do not make adopting all 130 skills a minimum-v1 requirement. **Coverage:** uncreated `MIGRATION` candidate, also owning AUDIT-016; #51/#69 cover only parts of future capability work.

#### AUDIT-014 — Architecture, instructions, and accepted decisions conflict with current source

- **Classification:** documentation gap. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** human/agent entry points and decision coherence. **Effort:** medium. **Impact:** medium. **History:** recurring current-state drift.
- **Observation — observed:** README correctly describes existing source, validators, schema/catalog roots, builds, agents, and instruction modules. Other primary entry points say those capabilities do not exist. Copilot instructions prohibit local CI/release workflows while current AGENTS, release declaration, and workflow guide select repository-owned workflows. Accepted ADR-0006 prohibits committed `dist/`, despite 335 tracked output files.
- **Evidence:** [README][readme]; [ARCHITECTURE.md:76–83,137–140,169–175,193–199][architecture]; [SYSTEM.md:95–105][system]; [ROADMAP.md:43,65–69,195–215,235–260][strategic-roadmap]; [Copilot instructions:36–37][copilot]; [DECISIONS.md:270–275][decisions]. ADR-0002 also excludes local CI. The [ADR adoption guide:4–5,58–60][adr-guide] still describes earlier skill/spec/runtime versions than merged PR #104 supplies. Strategic ROADMAP counts and its AET-Q07 status/pins are stale.
- **Why it matters — inferred:** a fresh human/bot receives contradictory source ownership, tooling availability, and next-work guidance. A factual README does not neutralize conflicting governing navigation.
- **Recommendation — recommended:** reconcile active factual/navigation claims against current evidence and link #105 as the tactical ledger. Preserve strategic intent and accepted history; propose or record the appropriate clarification/successor decision instead of silently rewriting accepted ADR outcomes.
- **Suggested validation:** follow README → AGENTS → META/architecture → ROADMAP and obtain consistent roots, commands, delivery/lifecycle state, current policy pins, and issue ledger. Compare assertions with the tracked inventory and actual validation receipts.
- **Dependencies or risks:** ordinary factual refresh need not wait for an organization-wide document move or broad historical ADR backfill. Human-governed policy changes remain human-governed. **Coverage:** uncreated `DOCS` candidate, also owning AUDIT-015. Existing #87/#88 create reusable review/completion behavior; they do not themselves repair Aether's current prose.

#### AUDIT-018 — Consumer readiness fails while its report-generator test remains green

- **Classification:** confirmed defect. **Severity:** medium. **Confidence:** high. **Status:** confirmed. **Area:** consumer installation/readiness evidence. **Effort:** medium. **Impact:** high. **History:** new.
- **Observation — observed:** the final readiness receipt is `not-ready`: local install, publish dry run, and removal pass, but all three pilot portable-package validations fail. Remote pinned install/update skip pending an approved release. The unit test explicitly accepts either ready or not-ready and verifies report generation, so 199 passing zero-skip tests do not establish consumer readiness.
- **Evidence:** final consumer readiness receipt; [consumer harness test:133–136,541–552][consumer-tests]; [portable validator:213–224,338–355][validator]; [generated architecture-authoring:77–83][architecture-skill-dist]; [generated create-architecture-document:78–80][create-architecture-skill-dist]. Both architecture workflows name governing source specifications absent from their individual installed packages. Manifest-resource, routing, frontmatter and template checks pass; no secret-pattern or broken/escaping local Markdown-link diagnostics were reported for these pilots.
- **Why it matters — inferred:** a working installer operation and successful report-generator tests can coexist with unresolved required governing resources. Missing-evidence behavior remains available, so this is not proof every use crashes or is impossible. Broad `.staging/` diagnostics in these packages concern historical migration prose, not an active staged lookup. Absolute/local-path diagnostics appear only after local installation, consistent with installer origin metadata; the cleaned harness does not retain exact installed bytes to independently establish their value or implementation. No builder leakage, disclosure, or transmission was proved.
- **Recommendation — recommended:** make governing dependencies actionable through an explicit package layout, bundle/resolver, or immutable resource reference. Separate export-package policy from intentional installed-host origin metadata, and interpret historical provenance text deliberately. Add a distinct readiness gate for the scenarios required by each declared distribution profile while preserving negative report-generator tests.
- **Suggested validation:** fresh consumers resolve every required governing resource without canonical-source checkout assumptions; historical staged prose is classified appropriately; pre-install export and installed-host policies are tested separately without broadly allowing private paths; required local failures block local-ready; skipped remote acceptance cannot be presented as full released-consumer acceptance.
- **Dependencies or risks:** local dependency/policy fixes need no publication. Remote install/update proof needs a separately approved immutable release; do not delete provenance or update metadata merely to silence broad substring rules. **Coverage:** existing #38; #63/#67 are related distribution/default-bundle scope, not duplicate initiatives.

### Low severity

#### AUDIT-010 — Changelog parser misses the required bracketed Unreleased section

- **Classification:** confirmed defect. **Severity:** low. **Confidence:** high. **Status:** confirmed. **Area:** release metadata. **Effort:** small. **Impact:** medium. **History:** new.
- **Observation — observed:** the release parser matches `## Unreleased`, while AGENTS and the current changelog require/use exact `## [Unreleased]`. Extracting the actual populated section yields an empty excerpt. Existing tests seed the legacy unbracketed form.
- **Evidence:** [release builder:184–197][release-builder]; [AGENTS release convention][agents]; [CHANGELOG.md][changelog]; bounded current-changelog extraction recorded an empty result.
- **Why it matters — inferred:** release notes omit intended unreleased context despite a valid canonical changelog.
- **Recommendation — recommended:** recognize the declared canonical bracketed heading and define any deliberate legacy compatibility.
- **Suggested validation:** actual canonical heading and populated bullets, next release boundary, empty section, and accepted legacy syntax if retained.
- **Dependencies or risks:** no upstream dependency; avoid broad changelog rewriting. **Coverage:** existing #38.

#### AUDIT-015 — Active continuity still proposes merging already-merged work

- **Classification:** documentation gap. **Severity:** low. **Confidence:** high. **Status:** confirmed. **Area:** continuity/current-work handoff. **Effort:** small. **Impact:** medium. **History:** changed by merged PR #104.
- **Observation — observed:** CONTINUITY remains active and ready-for-review, with next action to merge the four-digit authoring package. Audited HEAD is already the merge of that package; there are no open PRs.
- **Evidence:** [CONTINUITY.md:9–13,47–48,55–68,138][continuity]; [PR #104](https://github.com/egohygiene/aether/pull/104), merged head `237880404528f5556e114d789a0dfd4e2c61fc21` into the audited SHA. Null candidate values, recorded older base/date, and transition-safe semantics are not themselves defects.
- **Why it matters — inferred:** a resumed worker can select a superseded merge action instead of current roadmap work.
- **Recommendation — recommended:** have the separately authorized repository-changing workflow perform continuity Refresh/Verify against live state and current issue ledger. Preserve prior evidence in history.
- **Suggested validation:** Resume accurately distinguishes historical base/candidate from live merged state and identifies a viable current next action without inventing completed work.
- **Dependencies or risks:** the read-only Auditor must not assume continuity-write permission. **Coverage:** uncreated `DOCS` candidate; #92/#102 are related process improvements.

#### AUDIT-016 — Dated evacuation snapshot contradicts completed removal/classification evidence

- **Classification:** documentation gap. **Severity:** low. **Confidence:** high. **Status:** confirmed. **Area:** migration navigation/history. **Effort:** small. **Impact:** medium. **History:** recurring dated-snapshot drift.
- **Observation — observed:** the dated status correctly counts six historical removals but later says the same six candidates remain; their paths are absent and records explicitly say removed. It calls all hook classification pending even though ADR-0007/eight records classify three move-outs, four rejects, and one human-review residual. It describes a deletion outcome differently from ADR-0005's literal accepted wording.
- **Evidence:** [staging status:34–58,90–102,145–165][staging-status]; [disposition records][dispositions]; [DECISIONS.md:234–243,336–345][decisions]. The mismatch concerns current navigation, not permission to invalidate or rewrite historical decisions.
- **Why it matters — inferred:** a new reader can repeat completed classification or mistake catalog registration for reviewed removal authority.
- **Recommendation — recommended:** preserve the dated snapshot and provide an explicitly current reconciled ledger/status view with immutable source references. Route policy-intent changes through the human decision process.
- **Suggested validation:** Git/current counts reconcile; removed entries are historical; existing decisions stay linked; each pending action has an owner/issue; each removal outcome cites the actual governing policy.
- **Dependencies or risks:** factual reconciliation can begin now; changed authority cannot be silently inferred. **Coverage:** uncreated `MIGRATION` candidate with AUDIT-013, not another prose-only issue.

#### AUDIT-017 — Audit procedure routes staged reconciliation to old Issue 016

- **Classification:** documentation gap. **Severity:** low. **Confidence:** high. **Status:** confirmed. **Area:** audit procedure/navigation. **Effort:** small. **Impact:** low. **History:** recurring unresolved staged/canonical reconciliation pointer.
- **Observation — observed:** canonical audit-repository still says “Issue 016 should compare” the staged repository-audit variant and extract unique workflow/format/taxonomy. #16 is closed; live #86 explicitly owns the composable audit profile and staged/canonical delta work.
- **Evidence:** [audit-repository Staged Variant section][audit-skill]; [closed #16](https://github.com/egohygiene/aether/issues/16); [open #86](https://github.com/egohygiene/aether/issues/86).
- **Why it matters — inferred:** a reusable instruction sends future workers to an obsolete coordination home, obscuring which required delta is outstanding.
- **Recommendation — recommended:** reconcile the staged delta under #86 and correct the canonical pointer as part of that bounded work. Preserve provenance; do not activate or copy the staged file wholesale.
- **Suggested validation:** current link resolves to the live owner; delta disposition is explicit; source/generated output references agree after regeneration.
- **Dependencies or risks:** audit profile composition and maturity qualification remain #86 scope; this finding is not evidence that a second auditor or automatic issue creator should be installed. **Coverage:** existing #86; no duplicate issue recommended.

## Positive observations

- **Observed:** README's 32/36/9/1 canonical artifact counts match the immutable inventory. Source, generated distributions, and staging have named ownership boundaries rather than one untyped content tree.
- **Observed:** clean local distribution generation and check succeed, and two independent complete 335-file output trees match byte for byte. The local full suite passes 199 tests with zero skips when exact native ADR and issue-title/EgoLint inputs are supplied.
- **Observed:** artifact provenance, explicit lifecycle, schema fixtures, pinned owner policy evidence, distribution manifests, and resource guards already exist. Repairs can extend that foundation instead of inventing a second framework.
- **Observed:** all 56 governed external staged skill-text hashes match captured records; the four-source review register covers all 57 cataloged external artifacts. Default selection is deny, and seven selected references retain human review/external-effect restrictions. This does not establish rights/security for all companions or the 130 unresolved entries.
- **Observed:** rejected/move-out/deferred hook prototypes retain safety rationale. Unknown provenance and unaccepted destinations are preserved instead of being erased for a clean tree.
- **Observed:** audit and continuity contracts separate read-only assessment from fixes, history rewriting, issue creation, and handoff mutation. Release task handoffs preserve separately authorized publication boundaries.
- **Observed:** provider projections disclose fixture/manual-import limits, retain bounded tool mappings, and reuse managed modules. Generated files are not represented as automatically scheduled host installations.
- **Observed:** every original open work issue is a native child of #105 exactly once. Existing work should be retained, with additive reconciliation instead of silent deletion or duplicate umbrellas.

## Opportunities and already-covered gaps

These are scope/qualification observations, not additional confirmed runtime failures:

| Area | Observed boundary or open question | Existing work home / bounded next proof |
| --- | --- | --- |
| Provider consumption | Projection contract describes fixtures, not host materialization. Generated skill/spec paths and actual host installation roots need consumer closure proof. | #38 first delivery; #63/#67 distribution/default bundle and consumer owners. Install a synthetic real consumer and follow every declared dependency; do not infer host success from generated text. |
| Audit skill dependencies | A single skill package does not itself bundle the governing auditor spec/continuity dependency. Required-input resolution is explicit; no offline self-contained guarantee was found. | #67/#86: define pinned resolution/closure and report missing inputs honestly. |
| Auditor artifact output | Read/search projections coexist with a mission to write/validate a report. A writer handoff or narrowly declared capability remains a design concern. | #64/#65/#86. Do not silently grant edit/execute to a read-only role. |
| Agent/instruction catalog scope | Nine agent sources and one instruction exist but are not skill/spec catalog records. | #41 and #40, respectively; not duplicate audit issues. |
| Checkpoint reports and profiles | Auditor2.0 and audit skill1.1 provide a real base, while machine-readable delta/profile composition remain future work. | #68/#86, preserving one auditor and explicit authority. |
| Native/live coverage | Prepared local native suites now execute; hosted PR tests previously skipped optional native inputs. | Preserve exact environment receipts; actual hosted release and host adoption remain separate proof. |
| Release successor design | Existing v1 path and future engine/units/channels are distinct scopes. | #38 can repair/qualify present delivery; #94/#95/#93/#63 handle the successor without blocking every local correction. |
| Repository documentation layout | Current factual drift is confirmed; a universal document relocation is not decided here. | Bounded `DOCS` reconciliation now; broader ownership/layout proposals retain their own review. |

## Original 30-issue coverage and recommended journey

At assessment there are 31 open issues: #105 plus the 30 work issues below. Every comment collection was fetched and empty, so issue-body requirements remain the primary work contract. The original child order is preserved. `*` marks a dependency/readiness gate for the **full requested outcome**, not a claim that no bounded preparation can begin; an unstarred issue is not a claim of merge readiness or small effort.

| Existing order | Issue | Current implementation/coverage | * | Next bounded outcome / preserved boundary |
| --- | --- | --- | --- | --- |
| 1 | #103 Exploration notes | Existing architecture/document authoring, ADR, journal and continuity foundations; no dedicated exploration-note artifact in canonical catalog. | No | Define one small optional note contract/template, synthetic proof, then reviewed canary. Mindgarden indexing and Holon scaffold are downstream, not prerequisites for initial note semantics. |
| 2 | #102 Conversation checkpoints | Draft repository-continuity spec/skill/instruction and managed hooks already delivered in closed #79/#80; no discussion-ledger/onboarding extension in catalog. | No | Compose bounded snapshot plus optional meaningful discussion ledger. Do not dump transcripts or make Mindgarden archives a prerequisite. |
| 3 | #92 Bounded execution | Draft worker-strategy 0.1.0 landed via PR #96 and composes continuity/local-validation evidence. | No | Reconcile existing WRK rules into the requested sizing/skill/instruction/eval outcome. Do not duplicate the worker strategy or claim it fulfills every #92 acceptance criterion. |
| 4 | #40 Prompt/instruction libraries | One canonical repository-continuity instruction exists; main catalog currently has only skill/spec kinds. | No | Add the distinct prompt/instruction lifecycle/schema/catalog/projected behavior and reconcile approved source material. AET-01 = closed #36; AET-04 = closed #39. |
| 5 | #68 Checkpoint audits | Approved auditor spec 2.0.0 and draft audit-repository 1.1.0 exist; repository/organization report, machine-readable finding/delta/fixture and migration work remains. | No | One shared checkpoint-report schema/delta contract consuming existing auditor semantics, scoped organization behavior, fixtures. Distinguish this from profile selection in #86. |
| 6 | #86 Composable audit profiles | Existing auditor/spec/agent/skill; canonical skill still says “Issue 016” must reconcile staged variant. | No | Profile registry/composition, source-profile finding metadata, staged/canonical delta reconciliation, corrected references and maturity proof. No second auditor or automatic issue creation. |
| 7 | #87 Architecture coherence review | Existing reflector/Human Alignment Anchor and auditor foundations. | No | Thin read-only review workflow and versioned assessment/ratification record; explicit human outcome remains necessary. |
| 8 | #88 Roadmap impact | Decision-impact and continuity managed modules exist; they do not establish the requested universal roadmap-impact hook/disposition. | No | Compose one completion hook with bounded updated/proposed/not-affected/blocked evidence. Organization roadmap mutation remains separate authority. |
| 9 | #94 Release-engine decision | Existing draft release v1, egohygiene/relay#47 foundation and current owner workflows provide inspection inputs. | No | One compact proposed decision/probe. Entry explicitly says no new implementation prerequisite; do not turn this into an adapter implementation or publication. |
| 10 | #38 First artifact release | Deterministic build/validator/projection/workflow/consumer fixture foundations exist in closed #8/#12/#13/#17/#36/#39. Only auditor spec stable; no tags/releases. Current release workflow failure remains. | No | Repair/qualify the actual existing release path, choose/qualify a small releasable skill payload, prove immutable package/install/upgrade/rollback when separately authorized. Keep source versus dry-run versus release truth distinct. |
| 11 | #95 Release units/channels | Draft repository-release/v1 already exists; successor contract is not accepted. | Yes | Wait for reviewed #94 decision; extend/migrate one authority model with explicit fixtures. No engine or adapter implementation. |
| 12 | #93 Release-model umbrella | Existing foundation #61 closed; #94/#95 are the bounded design checkpoints and egohygiene/hygiene#65 is the policy review. | Yes | Reconcile design outcomes and evidence; not one giant implementation and not a prerequisite for proving the existing v1 release in #38. |
| 13 | #63 Distribution declarations | Existing repository-release/v1 foundation; channel/build/authority/evidence extensions not yet present. | Yes | Coordinate accepted #95 successor and egohygiene/hygiene#29. Schema/fixtures do not require all delivery adapters to be finished first. |
| 14 | #64 Capability manifest | Existing artifact provenance and Realm manifest foundation; no agent-facing capability/evidence contract delivered. | Yes | Versioned capability/evidence vocabulary plus one real pilot. egohygiene/hygiene#30 remains open; #41 broader policy remains separate. |
| 15 | #41 Agent/catalog/cost rules | Nine canonical agent sources/projections already delivered; current artifact catalog omits agent records and no task/risk/cost policy outcome is established. | Yes | Consume #64, catalog current agents, add explainable synthetic model/tool-selection cases. Do not re-create the delivered provider-projection engine. |
| 16 | #65 Operational-agent workflows | Existing canonical agent/projection/lifecycle substrate; event-driven workflow/state/schema and runtime-owner decision remain future work. | Yes | Compose #64/#41 as available, compare egohygiene/realm#9, egohygiene/realm#13, prove one fake-data provider-neutral workflow. Do not build a hosted autonomous company. |
| 17 | #73 Task-specific model evaluations | Existing deterministic skill eval framework; no task/model qualification profile delivered. | Yes | Consume #64/#65 and exact environment capabilities, prove role-specific results with public/synthetic fixtures or record unavailable candidates. egohygiene/realm#27 is open. |
| 18 | #67 Small default bundle | Closed #10/#11/#39/#49/#79/#80/#98 deliver important parts. Issue #98 is already completed despite unchecked link-based checkpoint in #67. Full stable bundle/host/class/install proof not delivered. | Yes | Qualify a small pinned selection, compose #92, demonstrate three classes/two hosts and local preservation. Related egohygiene/hygiene#64 documentation layout is proposed, not silently mandatory. |
| 19 | #66 Future-First Design | No dedicated catalog spec/skill. Upstream rights review/adapt matrix and pilots are scope in this issue. | **No recommended** | Existing roadmap marks it `*`, but body names no explicit outstanding predecessor. Start a bounded source/right/fit review now; do not fabricate an external gate from related owners. Landing policy/consumer changes still requires normal review. |
| 20 | #56 People-first content | Hygiene owns policy; Aether skill is not in canonical catalog. | Yes | egohygiene/hygiene#23 remains open; consume a pinned released profile, preserve high-stakes reviewer and uncertainty boundaries. |
| 21 | #90 Intelligence ownership | Current body contains explicit ownership-reconciliation warning; broad proposed “Aether owns contracts” language conflicts with existing Hygiene contract boundary. | Yes | A bounded read-only reconciliation can begin now; full contract outcome requires ownership resolution against egohygiene/hygiene#19, egohygiene/hygiene#60, egohygiene/.github#42 and existing read models. Do not block already-supported Relay roadmap wiring on this proposal. |
| 22 | #97 Composed planning | Existing architecture-roadmap/create-roadmap-document/worker-strategy; tactical planning composition not delivered. Explicitly later work. | Yes | Compose #88/#92/#78 and egohygiene/hygiene#60 when ready. Preserve Now/Next/Later; do not turn strategic ROADMAP.md into a backlog. |
| 23 | #51 Garden curator | Existing quality/authoring skill substrate; no curator skill; Mindgarden schemas are the correct contract owner. | Yes | egohygiene/mindgarden#13, egohygiene/mindgarden#14, egohygiene/mindgarden#15 remain open. Preserve deterministic planning when AI is disabled; bookmark/Akashic reference journey is a consumer, not publication authority. |
| 24 | #78 Brain-dump triage | Issue-authoring and continuity sources exist; candidate/triage/gardenization composition missing. | Yes | Compose #51 and Mindgarden plan/routing/ingestion; preserve raw capture/private context and deduplicate approved issue batches. egohygiene/mindgarden#39 is superseded, not an implementation dependency to resurrect. |
| 25 | #89 Project incubation | Existing foundational document skills; cohesive reviewed bootstrap-pack contract missing. | Yes | Compose #78 and current Mindgarden plan/routing; choose bounded layer inventory rather than empty decorative files. Reconcile legacy Sanctuary/Mindgarden references before downstream materialization. |
| 26 | #69 Scoped sessions | No scoped session-capability contract delivered; current provider outputs are not enforcement proof. | Yes | Consume #64/#65, egohygiene/hygiene#39, egohygiene/mindgarden#29 and egohygiene/realm#25. Fail closed; no credentials or authority escalation. |
| 27 | #77 Consumer organization profile | Existing provider-neutral projection engine; explicit external-organization/overlay contract and private canary remain. | Yes | egohygiene/hygiene#42, egohygiene/holon#41 and #67 remain open. Public synthetic external-org proof first; private Incompris evidence stays private. |
| 28 | #71 Confidential research bundle | No such opt-in bundle in canonical catalog. | Yes | Compose #69/#51/#64/#67 plus egohygiene/mindgarden#30, egohygiene/mindgarden#31, egohygiene/mindgarden#35 and egohygiene/realm#25. No universal-default inclusion or hosted fallback. |
| 29 | #72 Legal-document review | No such canonical skill/schema/eval corpus. Cross-agent evidence foundation #70 is closed. | Yes | Depends on #71 and imported provenance-bound source packets/Realm; synthetic examples only, professional-review boundary stays explicit. |
| 30 | #85 Historical ADR backfill | Authoring spec3.1.0, skill2.1.0 and managed module0.3.0 already select accepted Hygiene1.2.0 and four-digit IDs via merged PR104. Local corpus backfill/publication not performed. | Yes | Preserve explicit shared-system scheduling gate. egohygiene/hygiene#15 and egohygiene/holon#6 are closed and current pins exist; egohygiene/relay#5, egohygiene/relay#27, egohygiene/relay#33 and egohygiene/pace#5 remain open. Update stale three-digit issue examples additively; do not request duplicate policy ratification. |

With the proposed #66 readiness correction, **11 original work issues have no identified outstanding entry prerequisite and 19 have gated full outcomes**. The prior roadmap starred #66, but its body names no explicit outstanding predecessor for a bounded source/rights/fit review. Do not invent a dependency from related owners; retain normal review for changes that affect policy or consumers.

Important reconciliation rules:

- **Preserve all original issues.** Completed checkpoints can receive dated additive notes. Do not delete issues, silently replace their requirements, or close them merely because a foundation exists. Proper future closure needs specific evidence and rationale.
- **Keep identifier namespaces distinct.** #38's portfolio `REL-04` is closed egohygiene/relay#4; the newer program's Roadmap-Key `REL-04` is open egohygiene/relay#122. The newer successor's open state does not create a new prerequisite for present v1 delivery.
- **Consume current Mindgarden ownership.** egohygiene/mindgarden#39 is closed `not_planned` and explicitly superseded; old `garden/`, parallel `schemas/`, and local skill-tree assumptions conflict with current `.garden/`, `contracts/v1`, extracted package, and Aether skill ownership. Route useful scope through current egohygiene/mindgarden#5, egohygiene/mindgarden#40, egohygiene/mindgarden#42, egohygiene/mindgarden#48 and egohygiene/hygiene#61 instead of resurrecting the old tree.
- **Do not duplicate approved policy decisions.** Current authoring already selects accepted Hygiene1.2.0/four-digit naming. #85's broad historical publication/backfill and scheduling gate remain; older three-digit examples can receive additive reconciliation.
- **Respect owner boundaries.** Hygiene owns applicability policy; Relay reusable execution; Egolint conformance; Pace observes adoption; consumer repositories own credentials/adapters. #90's explicit ownership warning calls for reconciliation, not a silent transfer of every contract to Aether.

### Suggested finite sequencing

1. **Repair evidence and navigation:** candidate `CATALOG`, `BUILD`, `EVAL`, `BOUNDARY`, `DOCS`; introduce bounded `STAGING`/`EXTERNAL` controls and a `MIGRATION` ledger. Inventory and factual reconciliation can begin without completing every destination adoption.
2. **Qualify present delivery:** use existing #38 for AUDIT-005 through AUDIT-010 and consumer acceptance. Prove selected payload, immutable identity, reproducible metadata, and installation/update boundaries before claiming release readiness. Publication still requires its separate explicit authorization.
3. **Finish the authoring/audit workflow queue:** #103/#102/#92/#40/#68/#86/#87/#88. Compose delivered foundations rather than creating parallel systems.
4. **Resolve successor release and capability/consumer design in order:** #94/#95/#93/#63/#64/#41/#65/#73/#67, preserving each issue's bounded owner/outcome.
5. **Keep extended work opt-in and visible:** #66/#56/#90/#97/#51/#78/#89/#69/#77/#71/#72/#85 with their declared gates. Their visibility is useful; making them all prerequisites for the basic authoring/distribution spine is not established by this audit.

This ordering is a recommendation for a live roadmap, not implementation, merge, ratification, publication, or a new product scope. A proposed minimum-v1 milestone can be explicit and finite while all original work remains in the ledger.

## Suggested issue backlog and no-duplicate decisions

The keys below are **proposals, not issue numbers**. No issue creation is claimed by this immutable dated assessment. A later authorized reconciliation should map created numbers in #105 and maintain a trace from every finding to exactly one bounded primary home.

| Candidate / existing home | Findings | Candidate acceptance / scope boundary |
| --- | --- | --- |
| `CATALOG` — uncreated | AUDIT-001 | Source-owned metadata refreshes; semantic drift fails; catalog-owned fields and documented lifecycle normalization survive. |
| `BUILD` — uncreated | AUDIT-002 | Generation errors fail in both modes; complete owned inventory detects stale extras without silent destructive cleanup. |
| `EVAL` — uncreated | AUDIT-003 | Shared preflight, explicit nonempty selection, and honest assertion execution status; preserve intentional structural-only cases. |
| `BOUNDARY` — uncreated | AUDIT-004 | Validated IDs and resolved read/write containment; synthetic traversal/symlink cases fail without exposing outside bytes. |
| `STAGING` — uncreated | AUDIT-011 | Typed intake plus actual base/head removal/preimage approval evidence; grandfathered retention remains explicit. |
| `EXTERNAL` — uncreated | AUDIT-012 | Current bounded review plus actual calendar parsing and explicit-as-of freshness results; no fabricated review or authority. |
| `MIGRATION` — uncreated | AUDIT-013, AUDIT-016 | Complete 734-file reconciliation, current/historical navigation, ownership/next-job/retention evidence; preserve dated #18 history and human transfer/removal checkpoints. |
| `DOCS` — uncreated | AUDIT-014, AUDIT-015 | Consistent current entry points, honest source/delivery status and policy pins, appropriate ADR clarification, separately authorized continuity refresh. |
| Existing #38 | AUDIT-005–AUDIT-010, AUDIT-018 | Repair and qualify current release path, selected bytes, immutable handoff, authentication, metadata repeatability, canonical changelog and explicit consumer readiness; no duplicate release umbrella or premature publication. |
| Existing #86 | AUDIT-017 | Reconcile staged/canonical audit delta and point canonical/generated instructions at the live owner; no wholesale staged promotion. |

Existing #40/#41 own instruction/agent catalog expansion, #68 machine-readable checkpoint semantics, #73 task-specific model evaluation, #67 default bundle/adoption, and #85 historical ADR work. These are not automatically defects because they are unfinished; preserve their issue contracts and do not create duplicate issues from the same observation.

## Validation notes

| Check | Observed outcome | Practical limit |
| --- | --- | --- |
| Full prepared local unit suite | 199 tests, zero skips, exit 0 | Local Linux with exact optional native inputs; not live provider/host adoption. |
| Baseline local suite | 199 tests, 11 skips, exit 0 | Optional native owner/consumer inputs absent in that baseline; superseded locally by complete prepared run, not erased historically. |
| Exact native ADR suite | 11 tests, zero skips | Bounded owner/runtime fixture proof. |
| Exact issue-title suite | 11 tests, zero skips | Bounded selected contract/EgoLint inputs. |
| Distribution build/check | Pass | Happy-path success does not cover counterexamples in AUDIT-002/004. |
| Independent distribution rebuilds | 335 files in each; byte-identical inventories | Does not include same-output release-metadata repeatability; AUDIT-009 reproduced separately. |
| General/shell/strict-stage CLI validation | Pass | Strict staging currently has the limited behavior in AUDIT-011. |
| Catalog generation/schema/provenance checks | Pass | Does not diagnose AUDIT-001's retained source-owned metadata. |
| Deterministic eval run | 205 cases reported; 195 with zero executed checks | Structural-only cases are intentional; model behavior is unverified. AUDIT-003 covers separate invalid/missing-assertion counterexamples. |
| Official GitHub CLI 2.102.0, checksum-verified | Version check and `gh skill publish dist --dry-run` pass | Warns no active tag protection; no authenticated publication or released artifact proof. |
| Generated-source drift | No unexpected generated drift after tested happy path | Audited source remains the frozen baseline; repair is not claimed. |
| Consumer installation harness | Clean install, dry run and removal operations observed; readiness **NOT-READY** in the final local receipt | Portable pilot semantic validations fail; remote install/update skip because no release exists. Final classification needs the injected-metadata versus package-closure distinction below. |
| Hosted PR validation | [run 39167262844](https://github.com/egohygiene/aether/actions/runs/39167262844), attempt1, success, PR104 head `237880404528f5556e114d789a0dfd4e2c61fc21` | Logs show 199 tests/11 skips, not zero-skip native execution; this is PR head evidence, not an exact-main release success. |
| Exact-main release workflow | [run 39167340837](https://github.com/egohygiene/aether/actions/runs/39167340837), attempt1, failed, zero jobs | No release or publish steps executed. Detailed provider annotation unavailable; source/context cause is separately grounded. |

### Consumer qualification note

The final local consumer readiness receipt reports **NOT-READY**. All three portable pilot semantic validations fail after local GitHub CLI installation; clean install, publication dry run, and removal pass, and the two remote install/update scenarios skip because no release exists. This is the existing #38 acceptance gap in AUDIT-018. Before installation, architecture-authoring has diagnostics 015/016, create-architecture-document 015, and audit-repository 016; after installation, each also has 006/017. All identifiers use prefix `AETHER_PORTABLE_`. Diagnostic 015 reveals the two unresolved governing source-specification dependencies; 016 flags historical staging prose; 006/017 arise only after installation and are consistent with local-origin metadata. No secret-pattern (018) or broken/escaping local Markdown-link (019–021) diagnostic appears in these pilot results. The report does not equate these broad diagnostics with a product leak. No publication, credential access, or exfiltration is inferred.

## Deferred scope, uncertainties, and continuation requirements

- **Unverified:** released payload bytes, authenticated publication, hosted install/update/rollback against an immutable release, actual end-user host adoption, and Mac/Windows execution. No tags/releases existed to prove those paths.
- **Unverified:** the named release environment's required-reviewer settings. YAML environment naming is observed; absent verification is not proof of missing protection.
- **Unverified:** all unresolved-source licensing/security, every staged companion's rights, destination acceptance for retained move-outs, or new upstream vulnerabilities. Matching 56 skill-text hashes establishes those text pins only.
- **Unverified:** a comprehensive security scan, fuzz campaign, model/provider evaluation, operational reliability, or broad organization conformance. None was substituted with a green unit-test count.
- **Observed access limits:** the connector rejected some tags/workflow-specific collection resources. Tags were checked with local Git, and general run/release collections succeeded. No state was inferred from an access error.
- **Recommended continuation:** attach exact source/command/artifact receipts to repairs; refresh current navigation and continuity through the authorized owner workflow; map findings and all original issues into #105; qualify the smallest useful published selection only when its publication is separately authorized.

## Evidence index

The accompanying [validation receipt](data/aether-completeness-20261020T011246Z.validation.json) is the machine-readable audit record for source identity, command outcomes/log digests, distribution inventories, bounded code/staging counterexamples, native suite receipts, hosted observations, and consumer readiness. Temporary execution locations are intentionally omitted from this report. Reproduction logic uses temporary fixtures and the frozen source rather than changing live repository inputs.

| Evidence group | Immutable source or inspected record | What it supports |
| --- | --- | --- |
| Governing procedure | [AGENTS][agents], [auditor2.0][auditor], [audit-repository1.1][audit-skill] | Authority, evidence model, report contract, continuity read-only composition. |
| Source inventory | [frozen Git tree](https://github.com/egohygiene/aether/tree/dc8a16851f452763ef4f7fbe4bf057d4500b1921) and receipt inventory | Exact tracked counts, modes/digests, canonical/staged/dist separation. |
| CLI/catalog/evals | [aether_validator.py][validator], [catalog][catalog], [catalog guide][catalog-guide] | AUDIT-001/003/011 and healthy validation outcomes. |
| Distribution helpers | [skill builder][skill-builder], [spec builder][spec-builder] | AUDIT-002/004 and bounded negative fixtures. |
| Release | [workflow][release-workflow], [artifact builder][release-builder], [CHANGELOG][changelog], hosted runs above | AUDIT-005–010 and source/dry-run/release distinctions. |
| Staging controls/history | [status][staging-status], [DECISIONS][decisions], [dispositions][dispositions], [agent ledger][agent-ledger], [tests][staging-tests] | AUDIT-011/013/016, retained unknowns, historical decisions. |
| External governance | [register][external-register], [cadence][external-cadence], [validator][external-validator], [guide][external-guide] | AUDIT-012; pin/freshness/rights distinction. |
| Human/agent navigation | [README][readme], [ARCHITECTURE][architecture], [SYSTEM][system], [ROADMAP][strategic-roadmap], [Copilot instructions][copilot], [ADR adoption guide][adr-guide], [CONTINUITY][continuity] | AUDIT-014/015 and current-vs-historical discovery. |
| Tracker/history | All original issue bodies and #105 native child list; [#18](https://github.com/egohygiene/aether/issues/18), [#104](https://github.com/egohygiene/aether/pull/104), approved upstream policy evidence | Coverage, no duplicate scope, previous work/current handoff reconciliation. Tracker URLs are live; the receipt preserves the assessed observations. |
| Provider platform contracts | Official GitHub context/workflow_dispatch/CLI references linked within findings | Allowed context and event-SHA/authentication semantics; source configuration conclusions, not fabricated platform annotations. |

[agents]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/AGENTS.md
[auditor]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/specs/quality/auditor.spec.md
[audit-skill]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/skills/quality/audit-repository/SKILL.md
[validator]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/aether_validator.py
[catalog-guide]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/catalog/README.md
[catalog]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/catalog/first-party/catalog.v1.json
[skill-builder]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/skills/build-distributions.py
[spec-builder]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/specs/build-distributions.py
[release-builder]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/library/organization/skills/build-release-artifacts.py
[release-workflow]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/.github/workflows/release-first-party-skills.yml
[pr-workflow]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/.github/workflows/pr-validation.yml
[staging-status]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/docs/staging-evacuation-status.md
[decisions]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/DECISIONS.md
[dispositions]: https://github.com/egohygiene/aether/tree/dc8a16851f452763ef4f7fbe4bf057d4500b1921/catalog/first-party/staging-dispositions
[staging-tests]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/tests/test_staging_supply_chain_inventory.py
[agent-ledger]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/.staging/manifests/agents-ledger.json
[external-register]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/catalog/external/source-review-register.v1.json
[external-cadence]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/catalog/external/REVIEW_CADENCE.md
[external-validator]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/catalog/external/validate.py
[external-guide]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/docs/external-source-review-guide.md
[readme]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/README.md
[architecture]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/ARCHITECTURE.md
[system]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/SYSTEM.md
[strategic-roadmap]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/ROADMAP.md
[copilot]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/.github/copilot-instructions.md
[adr-guide]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/docs/adr-authoring-adoption.md
[continuity]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/CONTINUITY.md
[changelog]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/CHANGELOG.md
[consumer-tests]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/tests/test_consumer_installation_e2e.py
[architecture-skill-dist]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/dist/skills/architecture-authoring/SKILL.md
[create-architecture-skill-dist]: https://github.com/egohygiene/aether/blob/dc8a16851f452763ef4f7fbe4bf057d4500b1921/dist/skills/create-architecture-document/SKILL.md
