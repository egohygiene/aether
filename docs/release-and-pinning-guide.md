# Release and Pinning Guide

## Build and validate before release work

```sh
./aether validate --format "text"
./aether catalog generate --check
python3 catalog/validate_catalog.py
python3 library/organization/skills/build-distributions.py --check
python3 library/organization/agents/build-projections.py --check
```

## Validate publish payload

```sh
gh skill publish "dist" --dry-run
```

## Install pinned releases

```sh
gh skill install "egohygiene/aether" \
  "create-purpose-document" \
  --pin "v1.0.0"
```

Use a repository tag (or commit SHA) for deterministic installs.

## Updating pinned installs

Pinned installs are skipped by default during updates:

```sh
gh skill update --dry-run
gh skill update --unpin
```
