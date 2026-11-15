"""Release source controls using actual disposable Git origins; no publication."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from catalog.release_source import resolve_release_source


class ReleaseSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="aether-release-source-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.origin = self.root / "origin.git"
        self.repository = self.root / "source"
        self.repository.mkdir()
        subprocess.run(["git", "init", "--bare", "--initial-branch=main", str(self.origin)],
                       check=True, capture_output=True)
        self.git("init", "--initial-branch=main")
        self.git("remote", "add", "origin", str(self.origin))
        self.git("commit", "--allow-empty", "-m", "selected release source")
        self.selected = self.git("rev-parse", "HEAD")
        self.git("tag", "v1.2.3")
        self.git("tag", "-a", "v1.2.4", "-m", "annotated release fixture")
        self.git("commit", "--allow-empty", "-m", "later workflow dispatch source")
        self.dispatch = self.git("rev-parse", "HEAD")
        self.git("push", "--tags", "origin", "main")
        self.git("checkout", "--detach", self.selected)

    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=Release fixture",
                               "-c", "user.email=release-fixture@example.invalid", *args],
                              cwd=self.repository, text=True, capture_output=True,
                              check=True).stdout.strip()

    def test_lightweight_and_annotated_tags_use_selected_source_not_dispatch_head(self):
        self.assertNotEqual(self.dispatch, self.selected)
        for tag in ("v1.2.3", "v1.2.4"):
            result = resolve_release_source(self.repository, tag, "main")
            self.assertEqual(self.selected, result["commit_sha"])
            self.assertEqual(result, resolve_release_source(self.repository, tag, "main", self.selected))

    def test_moved_remote_tag_refuses_previously_validated_commit(self):
        resolve_release_source(self.repository, "v1.2.3", "main")
        self.git("tag", "--force", "v1.2.3", self.dispatch)
        self.git("push", "--force", "origin", "refs/tags/v1.2.3")
        with self.assertRaisesRegex(ValueError, "moved after validation"):
            resolve_release_source(self.repository, "v1.2.3", "main", self.selected)

    def test_wrong_checkout_missing_tag_and_nonancestor_refuse(self):
        self.git("checkout", "--detach", self.dispatch)
        with self.assertRaisesRegex(ValueError, "checked out source differs"):
            resolve_release_source(self.repository, "v1.2.3", "main")
        with self.assertRaises(ValueError):
            resolve_release_source(self.repository, "v9.9.9", "main")
        self.git("checkout", "--orphan", "unrelated")
        self.git("commit", "--allow-empty", "-m", "not default-branch history")
        self.git("tag", "v2.0.0")
        self.git("push", "origin", "refs/tags/v2.0.0")
        with self.assertRaisesRegex(ValueError, "merge-base"):
            resolve_release_source(self.repository, "v2.0.0", "main")

    def test_invalid_selection_cannot_become_git_options(self):
        for tag, branch, expected in (("--help", "main", None), ("v01.2.3", "main", None),
                                      ("v1.2.3", "--help", None), ("v1.2.3", "main", "short")):
            with self.subTest(tag=tag, branch=branch), self.assertRaises(ValueError):
                resolve_release_source(self.repository, tag, branch, expected)


class ReleaseWorkflowTests(unittest.TestCase):
    def test_workflow_keeps_pr_canary_read_only_and_publication_dispatch_only(self):
        root = Path(__file__).resolve().parents[1]
        path = root / ".github/workflows/release-first-party-skills.yml"
        workflow = yaml.load(path.read_text(), Loader=yaml.BaseLoader)
        self.assertIn(str(path.relative_to(root)), workflow["on"]["pull_request"]["paths"])
        self.assertEqual({"contents": "read"}, workflow["permissions"])
        jobs = workflow["jobs"]
        self.assertNotIn("environment", jobs["qualify-source"])
        for job_id in ("validate-release", "publish-release"):
            self.assertEqual("github.event_name == 'workflow_dispatch'", jobs[job_id]["if"])
        self.assertEqual("qualify-source", jobs["validate-release"]["needs"])
        publish = jobs["publish-release"]
        self.assertEqual("first-party-skill-release", publish["environment"]["name"])
        self.assertEqual("${{ env.RELEASE_COMMIT }}", publish["steps"][0]["with"]["ref"])
        for job in jobs.values():
            self.assertFalse(any("steps." in str(value) for value in job.get("env", {}).values()))
            for step in job["steps"]:
                if "run" not in step:
                    continue
                checked = subprocess.run(["bash", "-n"], input=step["run"], text=True, capture_output=True)
                self.assertEqual(0, checked.returncode, f"{step['name']}: {checked.stderr}")
                if "gh skill publish" in step["run"] or "gh release " in step["run"]:
                    self.assertEqual("${{ github.token }}", step["env"]["GH_TOKEN"])
                    self.assertNotIn('gh skill publish "dist"', step["run"])
        source = path.read_text()
        self.assertNotIn("${GITHUB_SHA}", source)
        self.assertEqual(2, source.count('--expected-commit "${RELEASE_COMMIT}"'))
        self.assertIn('--commit-sha "${RELEASE_COMMIT}"', source)


if __name__ == "__main__":
    unittest.main()
