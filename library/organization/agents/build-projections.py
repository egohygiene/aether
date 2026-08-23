#!/usr/bin/env python3
"""Compatibility entrypoint for Aether provider projections.

The canonical implementation moved to
``library/organization/projections/build-projections.py``. Keep this path so
existing release automation and local commands continue to work while the
provider-neutral interface becomes authoritative.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
AGENTS_DIR = REPO_ROOT / "library" / "organization" / "agents"
IMPLEMENTATION = (
    REPO_ROOT / "library" / "organization" / "projections" / "build-projections.py"
)
SPEC = importlib.util.spec_from_file_location("aether_provider_projections", IMPLEMENTATION)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load provider projection builder: {IMPLEMENTATION}")
provider_projections = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(provider_projections)

load_registry = provider_projections.load_registry


def _sync_legacy_overrides() -> None:
    """Apply legacy monkey-patchable source paths to the new implementation."""
    provider_projections.AGENTS_DIR = AGENTS_DIR


def find_agents():
    """Return canonical agents while preserving the legacy AGENTS_DIR override."""
    _sync_legacy_overrides()
    return provider_projections.find_agents()


def build(*, check: bool = False, output_directory: Path | None = None) -> int:
    """Build projections through the provider-neutral implementation."""
    _sync_legacy_overrides()
    return provider_projections.build(
        check=check,
        output_directory=output_directory,
    )


def main() -> int:
    """Run the provider-neutral CLI through the compatibility entrypoint."""
    _sync_legacy_overrides()
    return provider_projections.main()


if __name__ == "__main__":
    raise SystemExit(main())
