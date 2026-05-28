---
description: Find the Vibedata documentation source(s) most relevant to a topic.
allowed-tools:
  - Bash
  - Read
  - WebFetch
---

Find the Vibedata documentation sources most relevant to a given topic. Takes the topic as the slash-command argument (e.g., `/vibedata-docs-router auth flows`).

This command runs the same routing algorithm documented canonically in `skills/vibedata-docs-router/SKILL.md`. The algorithm is restated inline below per Claude Code conventions — commands are stand-alone documents.

---

## Step 1 — Fetch the Source Graph

Run via Bash:

```bash
curl -fsSL "https://gist.githubusercontent.com/admiraldata/47ea7b6d58a3d747b2e5a808360a37f9/raw/graph.json"
```

If curl fails (non-zero exit or empty response), halt with:

> Error: Could not fetch graph.json. Run `make publish-graph` in the vd-intelligence repo and retry.

## Step 2 — Tokenize the Topic

The topic is the argument provided with this slash command. If no argument is given, ask the user for a topic before proceeding.

1. Lowercase the entire topic string.
2. Split on whitespace and punctuation (`[ \t\r\n.,;:!?/()\[\]{}"'` + backtick]).
3. Drop tokens matching the stop-word list:

   ```
   the, a, an, of, in, on, for, with, and, or, is, are, where, how, what,
   when, why, vibedata, docs, doc, documentation, source, sources
   ```

4. The remaining tokens are the **topic tokens** (treat as a set — duplicates don't add signal).

## Step 3 — Score Each Node

Iterate over every node in `graph.json["nodes"]`. For each node:

**Skip rules (apply before scoring):**
- SKIP if `type == "code"` — code repo nodes are not documentation.
- SKIP if `summary` is null AND `tags` is an empty list — no rankable signal.

**Score computation** (additive):

| Signal | Points |
|---|---|
| Each topic token that appears verbatim in `tags` | +3 per match |
| Each topic token that appears in lowercased, whitespace-split `summary` tokens | +1 per match |
| Any topic token appearing verbatim as a substring in the node id | +2 (once total, not per token) |
| Any topic token appearing verbatim as a substring in `canonical_path` | +1 (once total, not per token) |

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

## Rules

- Do NOT read any of the matched files. Return node IDs, paths, and scores only. The calling agent decides what to fetch next.
- Do NOT modify graph.json or any local files.
- Do NOT call the gist URL more than once per invocation.
- The gist URL is authoritative. Never substitute a different URL or local path.
