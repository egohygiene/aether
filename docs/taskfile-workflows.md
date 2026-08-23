# Aether Taskfile workflows

Taskfile is an optional developer-experience layer over Aether's canonical command surfaces. The repository does not require Taskfile for CI, release automation, or direct use of `./aether` and GitHub CLI.

## Build distributions

Convenience command:

```sh
task skills:build
```

Direct equivalent:

```sh
./aether distribution build --output-directory "dist"
```

Override the output directory when needed:

```sh
task skills:build DIST_DIR="/tmp/aether-dist"
```

## Validate a skill publication

Preferred local convenience command:

```sh
task skills:publish:dry-run
```

This performs the deterministic distribution build first and then runs:

```sh
gh skill publish "dist" --dry-run
```

No release is created by the dry-run task.

## Publish an explicit tagged release

Publication is intentionally gated on an explicit `RELEASE_TAG` value:

```sh
task skills:publish RELEASE_TAG="v1.2.3"
```

The task runs the complete `skills:publish:dry-run` path before invoking:

```sh
gh skill publish "dist" --tag "v1.2.3"
```

The GitHub Actions release workflow remains the protected production publication path. This local task is an explicit convenience wrapper, not a replacement for repository release policy or environment review gates.

## Authority boundary

- `./aether distribution build` owns deterministic distribution generation.
- `gh skill publish` owns GitHub CLI validation/publication behavior.
- `Taskfile.yml` only sequences those commands for developer ergonomics.
- Credentials remain in the developer or CI environment; Taskfiles must never contain token values.
