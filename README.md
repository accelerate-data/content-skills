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
```

## Updating the plugin

1. Make your changes to skills, commands, or rules
2. Bump `version` in `.claude-plugin/plugin.json`
3. Validate: `claude plugin validate .`
4. Test locally: `claude --plugin-dir .`
5. Commit and push — the marketplace picks up the latest default branch automatically (no version field in marketplace entries)
