"""Integration tests for the materialized architecture-document contract."""

from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = (
    REPOSITORY_ROOT
    / "library"
    / "organization"
    / "specs"
    / "architecture"
    / "validate.py"
)


class ArchitectureMaterializationTests(unittest.TestCase):
    """Prove Aether's own architecture corpus satisfies its reusable contract."""

    def test_aether_complete_reference_set(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(VALIDATOR),
                "--repository",
                str(REPOSITORY_ROOT),
                "--require-complete-reference",
            ],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

