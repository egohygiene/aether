# Identity companion skill

Status: **draft; local host installation and publish dry-run observed, strict
portability and complete release qualification still fail/remain pending**.

The [`author-project-identity` skill](../library/organization/skills/authoring/author-project-identity/SKILL.md)
helps an agent collect project facts in small batches, preserve actual rights
and reviewer decisions, prepare explicit v1 candidates, and use Identity's
existing source/generation/verification interfaces. Its
[workflow specification](../library/organization/specs/authoring/project-identity-authoring.spec.md)
constrains the procedure; Identity remains the owner of field/schema semantics
and runtime behavior.

This is the tool-specific companion. Aether's existing
`create-specification-file` handles general specification writing. It is not a
second Identity validator, a component framework or a global repository policy.

## Package and preparation

Canonical source lives under `library/organization/`. Build the package with:

```sh
./aether distribution build --output-directory dist
./aether validate --format text
```

The generated `dist/skills/author-project-identity/` includes the skill, governing
workflow spec, reference lock/capability/checklist guides, owner-intake template,
authored evaluation cases and optional read-only file-hash helper. Do not edit
the generated copy directly.

The source lock pins Identity
`afc368003bfc6a2101051229efd237c8d6fadf71` and nine selected upstream resource
hashes. The helper can check those resources in an already prepared local tree;
it neither executes them nor authenticates a binary or the whole checkout.
The [packaged capability guide](../library/organization/skills/authoring/author-project-identity/references/identity-cli-and-capabilities.md)
records the v0/v1 distinction, Python prerequisite and source/output limits.

## Separate installations and releases

Installing a skill provides instructions/resources for an agent. Installing a
prebuilt Identity CLI provides the Rust executable. Its current v1 bridge also
needs Python 3.11+; a Rust compiler is required only for a source build.

The inspected published Identity v1.0.0 predates its explicit v1 initializer.
Select a reviewed compatible implementation rather than assuming a package or
schema version means every later command is present. Preserve canonical source,
candidates and generated output separately.

Actual `gh skill` qualification requires a CLI that exposes the compatible
preview commands. The earlier PATH-selected CLI was 2.46.0 and had no `skill`
subcommand. A later local checkpoint selected an already installed **2.96.0**
through command-scoped PATH and actually ran companion project installation,
listing, publish `--dry-run` and cleanup. This is an additional available CLI,
not a claim that the default CLI or user configuration was upgraded.

The [dated qualification record](work/identity-companion-host-20261122/VALIDATION.md)
retains **not-ready**. The pristine generated package fails strict portability
because its verbatim `SKILL.md` contains a canonical build-resource source
directive. The installed instance additionally contains CLI-injected absolute
`metadata.local-path` tracking. No validator rule or release gate was weakened.
The historical three-pilot run retains its own portable/provenance failures.
Remote installation/update, publication, stable promotion and observed agent
authoring remain unqualified. Local package copying, helper tests and authored
evaluation assertions do not prove those outcomes.

Follow [Aether's release and pinning guide](release-and-pinning-guide.md) for
stable artifact selection, immutable repository tags, actual consumer gates,
payload checksums and the selected publication action. This draft is excluded
from stable release payloads until its own maturity and release gates pass.
Identity's Rust binary release and Aether's skill release keep separate pins,
versions and evidence.
