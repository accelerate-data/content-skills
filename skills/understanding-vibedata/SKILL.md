---
name: understanding-vibedata
description: |
  Use when you need to know what Vibedata is, or to find and read where something
  about Vibedata is documented — strategy, architecture, concepts, product
  behaviour, personas, positioning, or published content. Covers work outside your
  own area: a GTM writer asking how the harness works, an engineer asking how we
  position it. Skip it when you are already inside a Vibedata repo working a task
  you already understand.
---

# Understanding Vibedata

## Orientation

**Last verified: 2026-09-08. The mapped docs override this section** — it is hand-written and it goes stale.

Vibedata is a coding agent specialized for data engineering, plus the **harness** around it. The harness is the agentic coordination layer sitting above the data platform. It carries data products from business intent through production operations and gives agents the four things a general coding agent lacks: **isolation**, so being wrong is survivable (code via git worktrees, compute via sandbox containers, data via ephemeral lakehouse workspaces); **guardrails** scoped to the data platform rather than a generic external API; **context** that is data engineering rather than application code; and **cross-platform** reach.

Three agents carry the lifecycle — **build**, **fix**, **detect** — working through the primitives **Domain** (unit of ownership: a GitHub repo plus its lakehouse tables), **Intent** (a unit of work), **Channel** (Slack / Teams / Google Chat wired to an Intent), and **AgentSession**. Four lifecycle functions live in the harness: ingest (dlt into bronze), transform (dbt into silver and gold), deploy (CI gates into production), operate.

The concepts register indexes by mechanism, not by the vocabulary above, so a term from this section rarely has a concept folder of the same name. The three isolation layers are owned by `concepts/semantic-branch/` (the Intent-scoped working world), with runtime policy in `concepts/agent-session-profiles/` and concurrency admission in `concepts/capacity-admission/`.

The strategic stance is **agentic-coding, not vibe-coding**: vibe-coding raises the floor so anyone ships something that runs; agentic-coding holds the ceiling so professionals ship something that survives production. Core belief — models are commodity inputs that improve for everyone equally, so **curation is the product**. Hallucination is handled structurally, not waited out: work is verified by independent execution against real data, never accepted on the agent's own report of it.

ICP: growing data teams, typically 1–5 full-stack practitioners who own the lifecycle from requirements through incidents.

## Steps

### 1. Resolve each repo you need

Repos are identified by `owner/repo`. A checkout's directory name does not have to match its repo name — `accelerate-data/vibedata-strategy-vision` commonly sits in a directory called `docs-product-vision`. Match on the `origin` remote, never on the directory name.

```bash
find_checkout() {  # usage: find_checkout accelerate-data/vibedata-gtm
  local target="$1" top roots=() root g d url slug
  top=$(git rev-parse --show-toplevel 2>/dev/null)
  [ -n "$top" ] && roots+=("$top" "$(dirname "$top")")
  for root in ~/scratch/99_working ~/src ~/code ~/repos ~/projects ~/dev ~/git ~/work ~/Documents; do
    [ -d "$root" ] && roots+=("$root")
  done
  for root in "${roots[@]}"; do
    while IFS= read -r g; do
      d=$(dirname "$g")
      url=$(git -C "$d" remote get-url origin 2>/dev/null) || continue
      slug=$(printf '%s' "$url" | sed -E 's#^git@[^:]+:##; s#^ssh://[^/]+/##; s#^https?://[^/]+/##; s#\.git$##')
      [ "$slug" = "$target" ] && { echo "$d"; return 0; }
    done < <(find "$root" -maxdepth 2 -name '.git' 2>/dev/null)
  done
  return 1
}
```

No match means the repo is not cloned here. Read it from GitHub instead:

```bash
gh api -H "Accept: application/vnd.github.raw" repos/<owner/repo>/contents/<path>
gh api repos/<owner/repo>/contents/<dir> --jq '.[].name'   # list a directory
```

Every repo here is private, so a `gh` auth failure is a hard stop: report it along with the command that fixes it, and read nothing else in its place.

### 2. Check the checkout is current

These repos take many commits a day, so a checkout that has sat untouched is behind.

```bash
git -C <checkout> log -1 --format=%cr
```

Newer than 3 days: use it. Older than 3 days: tell the user the checkout may be behind and read from GitHub instead, unless they say otherwise. Read files from their checkout freely; `git log` is the only *git* command you run in it.

### 3. Read for the stated objective

Read from the map, preferring an index over the tree it indexes. **Stop when every claim you are about to make has a source path behind it.** If five files does not get you there, report the gap rather than reading on.

### 4. Report

State what you read, what you skipped, and the next-best sources you did not open. Where two sources disagree, say so and name both, then resolve by *Which source wins*.

## The map

### `accelerate-data/vibedata-strategy-vision` — intent and direction

Authoritative for strategy, vision, and product architecture.

| Path | Holds |
|---|---|
| `vibedata-strategy.md` | Mission, what Vibedata is, problem and solution, product architecture, differentiation, personas, journey, metrics, assumptions, risks |
| `vibedata-architecture.md` | Architecture overview, tech stack, common misconceptions, core concepts, planning hierarchy, AgentSession, identity, RBAC, deployment modes |
| `concepts/` | Deep-dive explainers for cross-cutting mechanisms. **Start at `concepts/README.md`** — a maintained register naming every concept and what it owns. Within a concept, `engineering-reality.md` is the arbiter when higher-level prose and implementation disagree |
| `assets/diagrams/` | Logical architecture and operating-mode diagrams |

### `accelerate-data/studio` and `accelerate-data/vibedata-data-engineering` — what is built

`studio` is the harness; `vibedata-data-engineering` is the agents shipped as a plugin. Both share one docs vocabulary under `docs/`:

| Directory | Holds |
|---|---|
| `functional/` | What it is supposed to do |
| `design/` | What has been built. Many-to-many with `functional/` |
| `proposals/` | Changes being planned |
| `adr/` | Numbered decisions with their rationale |

`studio/docs/functional/README.md` is a maintained index of the functional areas — open it first for anything about product behaviour.

`studio/docs/design/README.md` is **311 KB**. Read a specific file under `design/` instead of opening that index.

`studio/docs/user-guide/` covers what a user can actually do; `studio/docs/wiki/` covers install, update, and troubleshooting.

### `accelerate-data/vibedata-gtm` — what we have said

Downstream of strategy.

| Path | Holds |
|---|---|
| `docs/vibedata-source-map.md` | GTM's own index of indexes, plus its source-classification rules. **Start here for GTM questions** |
| `gtm_personas/indvidual_personas/` | One persona per file — customer, investor, PE, SI, and the AWS / Fabric / LLM partners. Each is large, so open the file you need rather than the directory |
| `gtm_pitch/master-pitch-deck/` | The master pitch deck |
| `docs/gtm/` | The GTM plan, strategy, and prompts |
| `content/` | Published and drafted content — blog, LinkedIn, Reddit, whitepapers, handouts, video |

## Which source wins

Rank by what is being asked. Use recency only to break a tie *within* one rank.

| The question | The source that wins |
|---|---|
| What does it do today? | `design/` |
| What is it supposed to do? | `functional/` |
| What is coming? | `proposals/` |
| Why was it decided that way? | `adr/` |
| How does this mechanism work? | `concepts/`, then that concept's `engineering-reality.md` |
| Where is it going? How do we position it? | `vibedata-strategy-vision` |
| What have we said publicly? | `vibedata-gtm` — reports what was published; never wins a factual conflict |

GTM material contradicting current strategy is a finding worth reporting, not an error to silently correct.

## Excluded trees

These hold transient process artifacts and superseded copies. They are out of scope: do not open them and do not cite them. Discard any search hit that lands inside one and use the mapped source instead.

| Excluded | Why |
|---|---|
| `studio/docs/review/`, `vibedata-data-engineering/docs/review/` | Dated point-in-time reviews |
| `studio/docs/plans/` | Dated per-ticket implementation plans |
| `studio/docs/superpowers/`, `vibedata-data-engineering/docs/superpowers/` | Dated per-ticket execution plans |
| `studio/docs/engg-planning/`, `studio/docs/memory/`, `studio/docs/reference/`, `studio/docs/runbooks/`, `studio/docs/demo-provisioning/` | Team process and ops detail, not product context |
| `studio/docs/product/vision.md`, `studio/docs/product/strategy.md` | Superseded subset copies. `vibedata-strategy-vision` is authoritative for both. Do not cite them |

## Maintenance

Re-verify and update the `Last verified` date when any of these change: the four repo names, the shared `functional` / `design` / `proposals` / `adr` vocabulary, the indexes this map points at, or the strategic framing in the Orientation. Check the excluded trees at the same time — a directory that starts holding durable content should move into the map.
