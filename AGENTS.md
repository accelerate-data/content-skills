# Content Skills Plugin

Shared plugin repository for customer-facing content and GTM strategy commands used by Claude Code and Codex.

**Maintenance rule:** This file contains durable repository guidance, not volatile inventory.

## Instruction Hierarchy

1. `AGENTS.md` - canonical, cross-agent source of truth
2. `CLAUDE.md` - Claude-specific adapter and routing

## Repository Purpose

Single plugin-source repo for GTM content and strategy commands.

- Root manifests: `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
- Commands: `commands/`

## Commands

Slash commands for creating customer-facing content (pitch decks, blog posts, sales one-pagers) and maintaining GTM strategy artifacts (positioning, personas, marketing strategy).

## Conventions

- Keep all command files under `commands/`.
- Commands are auto-discovered from the `commands/` directory.
