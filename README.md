# Aether

Aether is Ego Hygiene’s canonical first-party library of reusable AI specifications, skills, and agent source with deterministic validation and build tooling.

Architecture navigation: [META.md](META.md) inventories Aether's complete
18-document architecture graph. The reusable materialization contract, schema,
and consumer validator live under
[library/organization/specs/architecture/](library/organization/specs/architecture/README.md).

## 1) Lifecycle and status

- Repository status: active, with canonical source in `library/organization/`.
- Publishing/install surfaces (`gh skill`, release tags) are preview-dependent and may change CLI behavior.
- Artifact lifecycle policy: `draft -> stable -> deprecated -> retired` (see `ARCHITECTURE.md`).
- Catalog records may also include `experimental` state where explicitly defined by catalog contracts.
- Only `stable` artifacts are releasable per catalog policy.

## 2) What Aether owns (and does not own)

Aether owns:
- First-party canonical specs, skills, and agents.
- Catalog/provenance schemas and deterministic validators.
- Distribution/projection build scripts.

Aether does **not** own:
- Org-wide deployment automation, CI baseline, templates, environment provisioning, shell command runtime tooling, lint implementation, release orchestration, or conformance enforcement in consumer repos.

See `PURPOSE.md#4-what-aether-is-not`.

## 3) Architecture: canonical vs generated

Canonical source:
- `library/organization/specs/`
- `library/organization/skills/`
- `library/organization/agents/`

Generated artifacts:
- `catalog/first-party/catalog.v1.json`
- `dist/skills/`
- `dist/github/`

`.staging/` is non-canonical migration/provenance holding space and cannot be emptied without ADR-005 deletion-gate requirements (`DECISIONS.md#adr-005`).

## 4) First-party catalog summary

Current canonical inventory snapshot (recompute with the commands shown):
- 28 specifications (`find library/organization/specs -name "*.spec.md"`)
- 34 skills (`find library/organization/skills -name "SKILL.md"`)
- 9 canonical agent profiles (`find library/organization/agents -name "AGENT.md"`)

Machine-readable catalog and provenance:
- `catalog/first-party/catalog.v1.json`
- `catalog/external/approved-skills.v1.json`

## 5) Prerequisites

- Python 3.12+
- Git
- GitHub CLI (`gh`) 2.96+ for skill publish/install flows
- Task 3 (optional) for convenience wrappers in `Taskfile.yml`

Install dev dependencies:

```sh
pip install -r requirements-dev.lock
```

## 6) Quickstart

From repository root:

```sh
./aether distribution build --output-directory "dist"
./aether validate --format "text"
./aether catalog generate --check
./aether test
```

Prepare a deterministic, human-reviewable social campaign packet from an exact
Identity package, pinned Aether catalog, and user brief:

```sh
python3 \
  "dist/skills/prepare-social-campaign-handoff/scripts/campaign-handoff.py" \
  prepare \
  --identity-package "identity-social-surfaces.json" \
  --catalog "catalog.v1.json" \
  --brief "campaign-brief.json" \
  --output "campaign-handoff.json"
```

The skill never posts, schedules, buys ads, or accepts platform credentials.
It authorizes immutable export only after freshness evidence, every required
check, human review, and a digest-bound approval record are present.

## 7) Validation and tests

Primary validator:

```sh
./aether distribution build --output-directory "dist"
./aether validate --format "text"
./aether validate --format "json"
```

Targeted validation scopes:

```sh
./aether validate --skills --format "text"
./aether validate --specifications --format "text"
./aether validate --catalog --format "text"
./aether validate --distribution --format "text"
./aether validate --provenance --format "text"
./aether validate --staging --format "text"
./aether validate --links --format "text"
./aether validate --evals --format "text"
```

Catalog check:

```sh
python3 catalog/validate_catalog.py
```

Test suite:

```sh
./aether test
```

## 8) Build and inspect distributions

Build deterministic first-party skill distributions:

```sh
./aether distribution build --output-directory "dist"
./aether distribution build --output-directory "dist" --check
```

Underlying generators remain available when a narrower check is needed:

```sh
python3 library/organization/skills/build-distributions.py
python3 library/organization/skills/build-distributions.py --check
python3 library/organization/agents/build-projections.py
python3 library/organization/agents/build-projections.py --check
```

Inspect generated output:

```sh
find dist/skills -maxdepth 2 -type f | sort
find dist/github -maxdepth 4 -type f | sort
```

Validate publishability (no release write):

```sh
gh skill publish "dist" --dry-run
```

Optional Taskfile convenience wrappers build first and delegate to the same canonical command surface:

```sh
task skills:build
task skills:publish:dry-run
task skills:publish RELEASE_TAG="v1.0.0"
```

The live Taskfile publish path requires an explicit release tag and runs the dry-run task before publishing. See `docs/taskfile-workflows.md` for direct-command equivalents and ownership boundaries.

## 9) Install locally with GitHub CLI

Install from local build output:

```sh
gh skill install "./dist" "create-purpose-document" --from-local
```

Install from repository default ref:

```sh
gh skill install "egohygiene/aether" "create-purpose-document"
```

## 10) Install a pinned release with GitHub CLI

Pin by release tag (or commit SHA):

```sh
gh skill install "egohygiene/aether" \
  "create-purpose-document" \
  --pin "v1.0.0"
```

## 11) Update and remove installed skills

Update skills:

```sh
gh skill update --dry-run
gh skill update --all
gh skill update --unpin
```

Inspect installed paths (for manual removal when needed):

```sh
gh skill list --json skillName,path,scope,pinned
```

At present, GitHub CLI exposes `update` but no dedicated `remove` subcommand; remove by deleting the listed installed skill directory at the reported path.

## 12) Release and version model

- Repository release tags pin installable snapshots.
- Artifact versions are per-record metadata in the first-party catalog.
- Breaking changes require major version increments in artifact metadata and release documentation.
- Only stable artifacts are eligible for release manifests.
- Release publication is explicit through `.github/workflows/release-first-party-skills.yml`; PR validation stays read-only in `.github/workflows/pr-validation.yml`.

See `CHANGELOG.md` and `docs/release-and-pinning-guide.md`.

Every active Ego Hygiene repository also declares its repository-level release
profile, version authorities, changelog, evidence, and manual handoff in
`.egohygiene/release.json`. The canonical convention and migration guide are
[`repository-release`](library/organization/specs/release/repository-release.spec.md)
and [repository release convention](docs/repository-release-convention.md).

## 13) External-skill provenance policy

External skill records must be reconstructable from staged provenance evidence and validated against schema:

- `catalog/external/approved-skills.v1.json`
- `catalog/schemas/aether.external-source-record.v1.schema.json`
- `.staging/manifests/skills-lock.json`

Policy and review workflow: `docs/external-source-review-guide.md`.

## 14) Security, privacy, and executable-resource warning

- Treat all generated or imported agent/skill artifacts as executable instruction surfaces.
- Review tools, links, scripts, and external references before promotion or installation.
- Never commit credentials/secrets in frontmatter, templates, eval fixtures, or hooks.

See `SECURITY.md` and `docs/agent-and-hook-safety-guide.md`.

## 15) Contribution workflow

1. Edit canonical source only (`library/organization/`, `catalog/` schemas/contracts).
2. Run deterministic validation/build checks.
3. Regenerate derived artifacts when required.
4. Submit focused PRs with clear scope and evidence.

Detailed process: `CONTRIBUTING.md`.

## 16) Ecosystem boundaries

Aether interfaces with neighboring repos/systems but does not replace them:

- `egohygiene/.github`: org agent deployment surfaces
- Empathy: repository baselines
- Holon: repository templates
- Realm: dev environment provisioning
- Mantle: shell command runtime
- Egolint: lint implementation
- Relay: GitHub Actions/workflow automation
- PACE: conformance enforcement
- Consumer repositories: local policy/overrides and runtime adoption

Consumer-local instructions override Aether defaults in consumer context.

## 17) License and support

- License: `LICENSE`
- Support: `SUPPORT.md`

## 18) External source selection

The external review register evaluates every captured source. The initial
allowlist is intentionally deny-by-default and contains only immutable,
external, agent-assisted reference records. It does not authorize automatic
installation, execution, first-party promotion, or external delivery.

Use the external source review guide and review cadence document before
selecting or updating an external artifact.
