---
description: Load Vibedata strategy, architecture, and GTM context into the conversation (read-only).
allowed-tools:
  - Read
  - Glob
  - Bash
---

Load Vibedata strategy, architecture, and GTM context into this conversation. No analysis — just read and confirm.

## Step 1 — Fetch the Source Graph

Run this command via Bash to fetch `graph.json` from the stable gist URL:

```bash
curl -fsSL "https://gist.githubusercontent.com/admiraldata/47ea7b6d58a3d747b2e5a808360a37f9/raw/graph.json"
```

If curl fails (non-zero exit or empty response), halt immediately with:

> Error: Could not fetch graph.json from the Vibedata source graph gist.
> Run `make publish-graph` in the vd-intelligence repo to republish, then retry this command.

Do not attempt to fall back to local files or sibling repos.

## Step 2 — Parse and Identify Compulsory Nodes

Parse the JSON returned in Step 1.

**Compulsory nodes**: all nodes where `type` is `"strategy"` or `"architecture"`.

For each compulsory node:
- Read `canonical_path`. Format is `owner/repo:path-in-repo`.
- Split on the first `:` to get `<owner/repo>` and `<path-in-repo>`.
- Fetch the file via Bash:

```bash
gh api repos/<owner/repo>/contents/<path-in-repo> --jq '.content' | base64 -d
```

Read the decoded content into the conversation context.

If `canonical_path` is null for a compulsory node, report it as `[ ] MISSING (no canonical_path)` in Step 3 output.

If the `gh api` call fails (auth error, 404, etc.), report it as `[ ] FETCH-FAILED — <node-id>` and continue with remaining nodes. Do not halt the whole command on a single fetch failure.

## Step 3 — Confirm Loaded and List Available Context

After processing all compulsory nodes, output the following. Use checkmarks for successfully loaded files and the failure markers above for anything that didn't load.

### Loaded (compulsory)

```
Context loaded:
- [x] <node-id> — <canonical_path>   (one line per strategy/architecture node)
```

### Available (optional — ask me to load any of these)

For every non-compulsory node that has a `canonical_path` or non-null `summary`, print one line grouped by type:

```
Additional context available (ask me to load any of these):

context:
- <node-id> — <summary if non-null, else canonical_path>

flow:
- <node-id> — <summary if non-null, else canonical_path>

gtm:
- <node-id> — <summary if non-null, else canonical_path>
```

Omit a type section entirely if no nodes of that type have any listable signal (`canonical_path` or `summary`).

## Rules

- Do NOT read optional documents unless the user explicitly asks.
- Do NOT summarize, synthesize, or analyze any content.
- Do NOT modify any files.
- The gist URL is authoritative. Never substitute a different URL or local path.
