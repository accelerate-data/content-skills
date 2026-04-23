# Content Skills

Customer-facing content and GTM strategy artifacts.

## Commands

Slash commands in `commands/` for:
- Creating customer-facing content (pitch decks, blog posts, sales one-pagers)
- Maintaining GTM strategy artifacts (positioning, personas, marketing strategy)

## Install

```bash
claude plugin add accelerate-data/content-skills
```

## Local development

```bash
claude --plugin-dir .      # Load without installing
claude plugin validate .   # Validate structure
python3 scripts/validate_plugin_manifests.py
python3 scripts/check_plugin_version_bump.py --base-ref origin/main
python3 -m unittest discover -s tests
```

`claude plugin validate .` validates Claude plugin structure. `scripts/validate_plugin_manifests.py` validates both Claude and Codex manifests, including the shared `commands` content surface. `scripts/check_plugin_version_bump.py` verifies that Claude and Codex versions match and that the shared version has been bumped above `origin/main`.

Codex CLI marketplace registration is performed against a marketplace repository/root, not directly against this plugin source repository. Keep this repository as the source plugin package and verify marketplace install/discovery from the marketplace root after merge.

## Updating the plugin

1. Make your changes to commands, manifests, or documentation
2. Bump `version` in both `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
3. Keep both manifests on the `content-skills` name and `./commands` content surface
4. Validate: `claude plugin validate .`
5. Validate manifests: `python3 scripts/validate_plugin_manifests.py`
6. Validate version bump: `python3 scripts/check_plugin_version_bump.py --base-ref origin/main`
7. Test locally: `claude --plugin-dir .`
8. Commit and push — the marketplace picks up the latest default branch automatically (no version field in marketplace entries)
