---
description: Load Vibedata strategy, architecture, and GTM context into the conversation (read-only).
allowed-tools:
  - Read
  - Glob
  - Bash
---

Load Vibedata strategy, architecture, and GTM context into this conversation. No analysis — just read and confirm.

## Step 1 — Discover Repo Location

Use `git rev-parse --show-toplevel` to get the GTM repo root. From its parent directory, locate the sibling repo:

- **docs-product-vision** (a.k.a. `vibedata-strategy-vision` on GitHub) — contains both strategy and architecture docs as peer documents at the repo root. The repo absorbed the former `vibedata-architecture` repo on 2026-05-28.

If the sibling repo is not found, warn the user but continue with whatever is available.

## Step 2 — Read Compulsory Documents

Read both of these files in parallel (these are required context); both live in `docs-product-vision/`:

1. `docs-product-vision` → `vibedata-strategy.md`
2. `docs-product-vision` → `vibedata-architecture.md`

If a file is missing, report it as `[ ] NOT FOUND` in the confirmation output.

## Step 3 — Confirm and List Available Context

After reading the compulsory files, output a checklist showing what was loaded and what additional context is available (without reading it). Format:

```
Context loaded:
- [x] vibedata-strategy.md (docs-product-vision)
- [x] vibedata-architecture.md (docs-product-vision)

Additional context available (ask me to load any of these):
- Architecture appendices — docs-product-vision → appendices/ (A: engineering sidebar, B: data mesh, C: release lifecycle, D: implementation gap log, E: agent architecture, F: harness, G: coordination patterns)
- Architecture changelog — docs-product-vision → CHANGELOG-architecture.md
- Compliance + war review — docs-product-vision → context/{compliance.md, war-review.md, testing-strategy-policy.md}
- User flows — docs-product-vision → user-flows/ (workflow inventory, persona views, component views, category inventories)
- GTM personas — gtm_personas/individual_personas/*.md (6 persona files)
- Marketing strategy — marketing-strategy/*.md (11 workstream docs)
- Position changes — position-changes/ (historical positioning analysis)
- Branding — branding/
- Case studies — case-studies/
- Content — content/
- Pitch decks — pitch-decks/
- One-pagers — one-pagers/
```

Do not read optional documents unless the user explicitly asks. Do not summarize, synthesize, or analyze any content.
