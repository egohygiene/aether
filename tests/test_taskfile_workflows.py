"""Contract tests for Aether's optional Taskfile workflow wrappers."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]


class TaskfileWorkflowTests(unittest.TestCase):
    def test_root_taskfile_composes_skill_tasks(self) -> None:
        root = yaml.safe_load((ROOT / "Taskfile.yml").read_text(encoding="utf-8"))
        self.assertEqual(str(root["version"]), "3")
        self.assertEqual(root["includes"]["release"]["taskfile"], "./.tasks/release.yml")
        self.assertTrue(root["includes"]["release"]["flatten"])
        self.assertEqual(root["includes"]["skills"]["taskfile"], "./.tasks/skills.yml")
        self.assertTrue(root["includes"]["skills"]["flatten"])

    def test_publish_tasks_delegate_to_canonical_commands(self) -> None:
        workflow = yaml.safe_load(
            (ROOT / ".tasks" / "skills.yml").read_text(encoding="utf-8")
        )
        tasks = workflow["tasks"]
        self.assertEqual(
            tasks["skills:build"]["cmds"],
            ['./aether distribution build --output-directory "{{.DIST_DIR}}"'],
        )
        dry_run = tasks["skills:publish:dry-run"]["cmds"]
        self.assertEqual(dry_run[0]["task"], "skills:build")
        self.assertEqual(dry_run[1], 'gh skill publish "{{.DIST_DIR}}" --dry-run')
        publish = tasks["skills:publish"]
        self.assertEqual(publish["requires"]["vars"], ["RELEASE_TAG"])
        self.assertEqual(publish["cmds"][0]["task"], "skills:publish:dry-run")
        self.assertEqual(
            publish["cmds"][1],
            'gh skill publish "{{.DIST_DIR}}" --tag "{{.RELEASE_TAG}}"',
        )

    def test_taskfiles_do_not_embed_credentials(self) -> None:
        content = "\n".join(
            path.read_text(encoding="utf-8")
            for path in (
                ROOT / "Taskfile.yml",
                ROOT / ".tasks" / "skills.yml",
                ROOT / ".tasks" / "release.yml",
            )
        ).lower()
        for forbidden in ("github_token:", "gh_token:", "personal_access_token:", "bearer "):
            self.assertNotIn(forbidden, content)

    def test_release_handoffs_are_explicit_and_non_publishing(self) -> None:
        workflow = yaml.safe_load((ROOT / ".tasks" / "release.yml").read_text(encoding="utf-8"))
        tasks = workflow["tasks"]
        for name in ("release:plan", "release:prepare", "release:verify", "release:publish"):
            self.assertIn(name, tasks)
        self.assertEqual(tasks["release:publish"]["requires"]["vars"], ["RELEASE_VERSION"])
        serialized = json.dumps(workflow, sort_keys=True).lower()
        self.assertNotIn("gh release", serialized)
        self.assertNotIn("git tag", serialized)


if __name__ == "__main__":
    unittest.main()
