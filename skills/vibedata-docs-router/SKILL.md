---
name: vibedata-docs-router
description: |
  Use when an agent needs to find which Vibedata documentation source(s) cover a topic,
  including questions like "where is X documented in Vibedata", "load context for X",
  "find docs about Y in vd-intelligence/strategy/architecture/flows", or any question
  that requires routing across the Vibedata source graph before reading content.
  Auto-activates on Vibedata-specific routing questions; does not activate for generic
  web/library docs.
---

# Vibedata Docs Router

Routes a topic string to the most relevant Vibedata documentation source nodes in `graph.json`. The skill's job ends at "here are the N best sources" — it does NOT read the matched files. The calling agent's next step is to read the returned sources.

## Why this skill exists

The Vibedata source graph can have dozens of nodes across strategy, architecture, context, flow, and GTM types. Without routing, an agent either reads everything (expensive) or guesses wrong. This skill runs a lightweight keyword-overlap scoring pass so the caller loads only the most relevant nodes.

## Step 1 — Fetch the Source Graph

Run via Bash:

```bash
curl -fsSL "https://gist.githubusercontent.com/admiraldata/47ea7b6d58a3d747b2e5a808360a37f9/raw/graph.json"
```

If curl fails (non-zero exit or empty response), halt with:

> Error: Could not fetch graph.json. Run `make publish-graph` in the vd-intelligence repo and retry.

## Step 2 — Tokenize the Topic

The input topic comes from the user's question or the slash-command argument.

1. Lowercase the entire topic string.
2. Split on whitespace and punctuation (`[ \t\r\n.,;:!?/()\[\]{}"'` + backtick]).
3. Drop tokens that match the stop-word list:

   ```
   the, a, an, of, in, on, for, with, and, or, is, are, where, how, what,
   when, why, vibedata, docs, doc, documentation, source, sources
   ```

4. The remaining tokens are the **topic tokens** (a set — duplicates don't add signal).

**Why**: Stop words are too common to distinguish nodes. Vibedata-specific terms like "vibedata" and "docs" appear in almost every node and would flood scores.

## Step 3 — Score Each Node

Iterate over every node in `graph.json["nodes"]`. For each node:

**Skip rules (apply before scoring):**
- SKIP if `type == "code"` — code repo nodes are not documentation.
- SKIP if `summary` is null AND `tags` is an empty list — no signal to rank against.

**Score computation** (additive):

| Signal | Points |
|---|---|
| Each topic token that appears verbatim in `tags` | +3 per match |
| Each topic token that appears in lowercased, whitespace-split `summary` tokens | +1 per match |
| Any topic token appearing verbatim as a substring in the node id | +2 (applied once, not per token) |
| Any topic token appearing verbatim as a substring in `canonical_path` | +1 (applied once, not per token) |

**Why these weights**: Tags are curated keywords — a direct match is high-confidence. Summary matches are weaker (longer text, more incidental words). Node-id and canonical-path substring matches are structural signals, worth less than curated tags.

## Step 4 — Return Top Results

Collect all nodes with score > 0. Sort descending by score. Take the top 5.

For each result, output:

```
**<node-id>**
<summary>   (if summary is non-null)
(no summary — only canonical_path: <canonical_path>)   (if summary is null)
(score=<n>, matched: <comma-separated matched tokens>)
```

Separate results with a blank line.

## Step 5 — Zero-Match Fallback

If no nodes score above 0, output:

```
No matches in the graph for `<original topic>`. Try broader terms, or load the
full baseline context: strategy, architecture, and context:product.

Fallback sources:
- strategy — <canonical_path of strategy node, or "(see graph.json)">
- architecture — <canonical_path of architecture node, or "(see graph.json)">
- context:product — <canonical_path of context:product node, or "(see graph.json)">
```

**Why**: Strategy, architecture, and context:product are the broadest Vibedata docs. If topic-specific routing fails, these three give the widest coverage without loading everything.

## What NOT to do

- Do NOT read any of the matched files. Return paths and scores only. The calling agent decides what to fetch.
- Do NOT modify graph.json or any local files.
- Do NOT call the gist URL more than once per invocation.
