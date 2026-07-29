---
name: arxiv-publishing
description: Prepare and validate reproducible arXiv publication releases from canonical scholarly sources. Use for LaTeX compatibility checks, bibliography freezing, source staging, filename sanitation, deterministic builds, release manifests, submission archives, accessibility checks, or arXiv preflight work.
---

# arXiv Publishing

## Inspect before staging

1. Read `../../../.github/specs/arxiv.spec.md` when present.
1. Identify the canonical source, build entry point, compiler, bibliography toolchain, figures, metadata, license, and existing automation.
1. Verify time-sensitive submission requirements from authoritative arXiv documentation when they affect the task.
1. Preserve the source tree and use an isolated staging directory for publisher-specific transforms.

## Prepare the release

- Resolve all included source files and assets from the build graph.
- Freeze or package bibliography artifacts in the format accepted by the target build.
- Normalize publisher-safe filenames and update staged references consistently.
- Exclude caches, editor files, secrets, unrelated outputs, and unsupported hidden paths.
- Preserve authorship, citations, licensing, semantic structure, and accessibility metadata.
- Generate the release from repository automation when available; do not replace a reproducible command with undocumented manual steps.

## Validate

Run the strongest available checks for:

- clean-environment compilation with the target engine and TeX distribution
- unresolved citations, references, missing files, and package incompatibilities
- embedded fonts, readable figures, and machine-readable text
- filename and archive safety
- source archive completeness and absence of unnecessary artifacts
- consistency among PDF, metadata, manifest, checksums, and source revision

Do not claim deterministic output unless repeated builds or the repository's reproducibility checks support it.

## Deliver

Return the requested PDF, source archive, manifest, checksums, and logs when available. Report commands, environment, results, warnings, deviations from the specification, and manual actions that remain. Never fabricate publication metadata or perform account-level submission actions without separate explicit authorization.
