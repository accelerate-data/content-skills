from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.check_plugin_version_bump import parse_semver, validate_version_bump


def write_manifest(root: Path, relative_path: str, version: str) -> None:
    manifest = {
        "name": "content-skills",
        "description": "Customer-facing content and GTM strategy artifacts.",
        "version": version,
        "author": {"name": "Accelerate Data"},
        "repository": "https://github.com/accelerate-data/content-skills",
        "license": "MIT",
        "commands": "./commands",
    }
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest), encoding="utf-8")


def write_manifest_pair(root: Path, claude_version: str, codex_version: str | None = None) -> None:
    write_manifest(root, ".claude-plugin/plugin.json", claude_version)
    write_manifest(root, ".codex-plugin/plugin.json", codex_version or claude_version)


class VersionBumpTests(unittest.TestCase):
    def test_parse_semver(self) -> None:
        self.assertEqual(parse_semver("1.2.3"), (1, 2, 3))

    def test_parse_semver_rejects_non_semver(self) -> None:
        with self.assertRaises(ValueError):
            parse_semver("1.2")

    def test_validate_version_bump_accepts_higher_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_manifest_pair(root, "1.0.1")

            with patch(
                "scripts.check_plugin_version_bump.git_show_json",
                return_value={"version": "1.0.0"},
            ):
                self.assertEqual(validate_version_bump("origin/main", root), [])

    def test_validate_version_bump_rejects_equal_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_manifest_pair(root, "1.0.0")

            with patch(
                "scripts.check_plugin_version_bump.git_show_json",
                return_value={"version": "1.0.0"},
            ):
                errors = validate_version_bump("origin/main", root)

        self.assertIn("plugin version was not bumped or was downgraded (base 1.0.0, current 1.0.0)", errors)

    def test_validate_version_bump_rejects_lower_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_manifest_pair(root, "0.9.9")

            with patch(
                "scripts.check_plugin_version_bump.git_show_json",
                return_value={"version": "1.0.0"},
            ):
                errors = validate_version_bump("origin/main", root)

        self.assertIn("plugin version was not bumped or was downgraded (base 1.0.0, current 0.9.9)", errors)

    def test_validate_version_bump_rejects_manifest_version_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_manifest_pair(root, "1.0.1", "1.0.2")

            errors = validate_version_bump("origin/main", root)

        self.assertIn("Claude and Codex plugin versions must match: '1.0.1' != '1.0.2'", errors)

    def test_validate_version_bump_rejects_missing_base_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_manifest_pair(root, "1.0.1")

            with patch("scripts.check_plugin_version_bump.git_show_json", return_value=None):
                errors = validate_version_bump("origin/main", root)

        self.assertIn("origin/main:.claude-plugin/plugin.json: manifest could not be read", errors)


if __name__ == "__main__":
    unittest.main()
