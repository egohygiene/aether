# Local Validation Execution Adapters

Use this guide after repository instructions and canonical commands have been
identified. Adapter availability is observed state, not a permanent property of
a host or repository.

## Selection table

| Adapter | Minimum observations | Default policy | Evidence boundary |
|---|---|---|---|
| Repository-native command | Entrypoint exists; runtime and locked dependencies are usable | Preferred | Proves only the command's declared scope in the current environment |
| Repository hook or task runner | Checked-in configuration and its invoked tools are usable | Preferred when canonical | Hook success does not add remote-runner parity |
| Locked local setup | Lockfile or pinned declaration; isolated writable destination; installation authorized | Allowed for `repository-locked` policy | Setup success is separate from test success |
| Workflow static lint | Compatible linter and workflow files are present | Recommended when available | Checks structure and supported semantics, not job execution |
| Container-backed `act` | Compatible `act`; usable Docker Engine API; sufficient image, disk, network, and action access; trusted graph | Optional | Local runner images and services can differ from GitHub-hosted runners |
| Direct self-hosted `act` | Explicit authorization; trusted graph; compatible host tools; no required container/service isolation | Prohibited by default | Executes action code directly in the agent workspace and lacks container isolation |
| Remote GitHub Actions | User policy and budget allow dispatch or PR-triggered execution | Separate external gate | Only an observed run may be reported as pending, passed, or failed |

## Capability probes

Use the smallest relevant probes and sanitize their output. Examples:

```bash
command -v "python3"
python3 --version
command -v "act"
act --version
command -v "docker"
docker info --format "{{json .ServerVersion}}"
```

Do not treat a successful `command -v "docker"` as proof that the Docker Engine
API is available. Do not enumerate or print environment-variable values to prove
that authentication or proxy configuration exists.

## Native-first translation

When a workflow wraps repository-native commands, plan the native commands
directly. Preserve relevant workflow parameters, versions, matrix dimensions,
and environment assumptions in the report. Mark dimensions that were not
reproduced as limitations.

For example, a workflow that installs locked dependencies and invokes
`./project validate` should normally be represented as two local checks:

1. locked setup;
2. `./project validate`.

This preserves useful validation even when the workflow orchestration layer is
unavailable.

## `act` gates

Container-backed execution is selectable only after the client, engine API,
resources, network, workflow graph, and user policy are all observed as usable.
If any prerequisite is unavailable, record the adapter as `unavailable` or
`blocked` and continue with independent native checks.

Some trusted workflows can be mapped directly to the current machine with a
runner mapping such as:

```bash
act pull_request --platform "ubuntu-latest=-self-hosted"
```

This mode is never an automatic fallback. It may execute third-party action code
directly, and workflow `container`, service-container, hosted image, tool-cache,
permission, and network behavior may not match GitHub. Require explicit
authorization and inspect local, pinned, and marketplace action references
before selection.

Do not change a workflow solely to satisfy `act`. If emulation fails because of
adapter incompatibility, record an emulator limitation rather than a repository
failure. If an underlying native command fails independently, record that check
as failed.

## Setup and retry boundary

Prefer the repository's locked installation command and isolated environment.
One bounded retry is reasonable only for a clearly transient network or registry
failure. Repeated retries, assertion weakening, snapshot replacement, or
unlocked dependency substitution conceal evidence and are prohibited.

## Remote deferral

When remote CI is deferred, do not dispatch it. List the workflows and matrix or
platform dimensions that remain unverified, and keep the remote state
`deferred`. A locally ready candidate can still be `ready-with-limitations` for
handoff when hosted-runner, service, or platform parity matters.

## Upstream references

- [act installation](https://nektosact.com/installation/index.html)
- [act runner images and self-hosted mapping](https://nektosact.com/usage/runners.html)
