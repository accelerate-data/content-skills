---
allowed-tools:
  - Read
  - Glob
  - Bash
---

Load Vibedata strategy, architecture, and GTM context into this conversation. No analysis — just read and confirm.

## Step 1 — Discover Repo Locations

Use `git rev-parse --show-toplevel` to get the GTM repo root. From its parent directory, locate the sibling repos:

- **vd-specs-product-vision** — contains strategy docs and user flows
- **vd-specs-product-architecture** — contains architecture docs

If either sibling repo is not found, warn the user but continue with whatever is available.

## Step 2 — Read Compulsory Documents

Read both of these files in parallel (these are required context):

1. `vd-specs-product-vision` → `vibedata-strategy.md`
2. `vd-specs-product-architecture` → `vibedata-architecture.md`

If a file is missing, report it as `[ ] NOT FOUND` in the confirmation output.

## Step 3 — Confirm and List Available Context

After reading the compulsory files, output a checklist showing what was loaded and what additional context is available (without reading it). Format:

```
Context loaded:
- [x] vibedata-strategy.md (product vision repo)
- [x] vibedata-architecture.md (architecture repo)

Additional context available (ask me to load any of these):
- User flows — vd-specs-product-vision → user-flows/ (workflow inventory, persona views, component views, category inventories)
- GTM personas — gtm_personas/individual_personas/*.md (6 persona files)
- Marketing strategy — marketing-strategy/*.md (11 workstream docs)
- Position changes — position-changes/ (historical positioning analysis)
- Branding — branding/
- Case studies — case-studies/
- Content — content/
- Pitch decks — pitch-decks/
- One-pagers — one-pagers/

Ready for follow-up instructions.
```

Do not read optional documents unless the user explicitly asks. Do not summarize, synthesize, or analyze any content.
