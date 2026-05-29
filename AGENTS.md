# Content Skills Plugin

Shared plugin repository for customer-facing content and GTM strategy commands used by Claude Code and Codex.

**Maintenance rule:** This file contains durable repository guidance, not volatile inventory.

## Instruction Hierarchy

1. `AGENTS.md` - canonical, cross-agent source of truth
2. `CLAUDE.md` - Claude-specific adapter and routing

## Repository Purpose

Single plugin-source repo for GTM content and strategy commands plus shared writing and video-creation skills.

- Root manifests: `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`
- Commands: `commands/`
- Skills: `skills/`

## Commands

Slash commands for creating customer-facing content (pitch decks, blog posts, sales one-pagers) and maintaining GTM strategy artifacts (positioning, personas, marketing strategy).

## Skills

Auto-activating agent skills under `skills/`. Each skill is a `SKILL.md` file with frontmatter (`name`, `description`); Claude Code and Codex auto-discover them from the plugin's `skills/` directory.

| Skill | Activates on | Source |
|---|---|---|
| `humanizer` | "sounds like AI", "de-AI this", cleaning AI-generated drafts | [blader/humanizer](https://github.com/blader/humanizer) (MIT) |
| `human-writing` | Drafting blog posts, vision docs, technical posts in a peer/human voice | [pr-pm/prpm](https://github.com/pr-pm/prpm) `human-writing` |
| `remotion` | Any Remotion / video-in-React code task | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) `@remotion/skills` (Remotion License — see `skills/remotion/NOTICE`) |
| `vibedata-docs-router` | "where is X documented in Vibedata", "load context for X", routing across the Vibedata source graph | Internal — first-party skill for this org's `vd-intelligence` graph |

`humanizer` and `human-writing` are complementary: `humanizer` cleans existing AI-generated text; `human-writing` guides drafting fresh content.

`vibedata-docs-router` (skill) and `/vibedata-docs-router` (command) share the same routing algorithm — the skill auto-fires on routing questions; the command is the explicit user-typed entry. Both fetch `accelerate-data/vd-intelligence:reports/graph.json` directly via `gh api` (no intermediate gist; the scanner repo is the single source of truth). The `/understand-vibedata` command also reads the same graph artifact for bulk-loading strategy + architecture.

## Conventions

- Commands live under `commands/`; skills live under `skills/<skill-name>/SKILL.md`.
- Both are auto-discovered. Commands are user-invoked (`/foo`); skills auto-activate on semantic match to their `description`.
- Vendored skills must include a `NOTICE` file when the upstream license requires attribution. See `skills/remotion/NOTICE` for the format.
- Keep `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` on the same plugin `name`, `description`, and `version`.
- Both manifests must expose this repo's command surface with `commands` set to `./commands` and the skills surface with `skills` set to `./skills/`.
- When plugin package metadata changes, bump both manifest versions together and run the manifest and version-bump validators.
