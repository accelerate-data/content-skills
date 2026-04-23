from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from scripts.validate_plugin_manifests import validate


def write_manifest(root: Path, relative_path: str, **overrides: object) -> None:
    manifest = {
        "name": "content-skills",
        "description": "Customer-facing content and GTM strategy artifacts.",
        "version": "1.0.1",
        "author": {"name": "Accelerate Data"},
        "repository": "https://github.com/accelerate-data/content-skills",
        "license": "MIT",
        "commands": "./commands",
    }
    manifest.update(overrides)
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest), encoding="utf-8")


def write_valid_pair(root: Path) -> None:
    write_manifest(root, ".claude-plugin/plugin.json")
    write_manifest(root, ".codex-plugin/plugin.json")
    write_command(root)


def write_command(root: Path) -> None:
    commands_dir = root / "commands"
    commands_dir.mkdir(parents=True, exist_ok=True)
    (commands_dir / "sample.md").write_text("# Sample\n", encoding="utf-8")


class ManifestValidationTests(unittest.TestCase):
    def test_valid_manifest_pair_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_valid_pair(root)

            self.assertEqual(validate(root), [])

    def test_codex_name_must_match_plugin_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_valid_pair(root)
            write_manifest(root, ".codex-plugin/plugin.json", name="ad-content")

            errors = validate(root)

        self.assertIn(".codex-plugin/plugin.json: expected name 'content-skills', found 'ad-content'", errors)
        self.assertIn("manifest mismatch: 'name' differs between Claude and Codex", errors)

    def test_codex_version_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_valid_pair(root)
            codex_path = root / ".codex-plugin/plugin.json"
            codex = json.loads(codex_path.read_text(encoding="utf-8"))
            del codex["version"]
            codex_path.write_text(json.dumps(codex), encoding="utf-8")

            errors = validate(root)

        self.assertIn(".codex-plugin/plugin.json: missing required field 'version'", errors)
        self.assertIn(".codex-plugin/plugin.json: version must be a semver string like 1.2.3", errors)

    def test_commands_path_must_be_commands_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_valid_pair(root)
            write_manifest(root, ".codex-plugin/plugin.json", commands="./skills")

            errors = validate(root)

        self.assertIn(".codex-plugin/plugin.json: commands must point to './commands'", errors)

    def test_commands_path_accepts_trailing_slash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_manifest(root, ".claude-plugin/plugin.json", commands="./commands/")
            write_manifest(root, ".codex-plugin/plugin.json", commands="./commands/")
            write_command(root)

            self.assertEqual(validate(root), [])

    def test_commands_path_rejects_double_trailing_slash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_valid_pair(root)
            write_manifest(root, ".codex-plugin/plugin.json", commands="./commands//")

            errors = validate(root)

        self.assertIn(".codex-plugin/plugin.json: commands must point to './commands'", errors)

    def test_commands_directory_must_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_manifest(root, ".claude-plugin/plugin.json")
            write_manifest(root, ".codex-plugin/plugin.json")

            errors = validate(root)

        self.assertIn("commands/: directory is missing", errors)

    def test_commands_directory_must_contain_markdown_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_manifest(root, ".claude-plugin/plugin.json")
            write_manifest(root, ".codex-plugin/plugin.json")
            (root / "commands").mkdir()

            errors = validate(root)

        self.assertIn("commands/: no command markdown files found", errors)

    def test_manifest_version_must_be_semver(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            write_valid_pair(root)
            write_manifest(root, ".codex-plugin/plugin.json", version="1.0")

            errors = validate(root)

        self.assertIn(".codex-plugin/plugin.json: version must be a semver string like 1.2.3", errors)
        self.assertIn("manifest mismatch: 'version' differs between Claude and Codex", errors)

    def test_required_manifest_fields_are_enforced(self) -> None:
        for field in ("name", "description", "version", "author", "repository", "license", "commands"):
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    root = Path(tmp_dir)
                    write_valid_pair(root)
                    codex_path = root / ".codex-plugin/plugin.json"
                    codex = json.loads(codex_path.read_text(encoding="utf-8"))
                    del codex[field]
                    codex_path.write_text(json.dumps(codex), encoding="utf-8")

                    errors = validate(root)

                self.assertIn(f".codex-plugin/plugin.json: missing required field '{field}'", errors)

    def test_manifest_parity_fields_are_enforced(self) -> None:
        for field in ("description", "repository", "license"):
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp_dir:
                    root = Path(tmp_dir)
                    write_valid_pair(root)
                    write_manifest(root, ".codex-plugin/plugin.json", **{field: f"different-{field}"})

                    errors = validate(root)

                self.assertIn(f"manifest mismatch: '{field}' differs between Claude and Codex", errors)


if __name__ == "__main__":
    unittest.main()
