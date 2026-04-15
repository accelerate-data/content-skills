---
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Agent
  - Skill
  - AskUserQuestion
---

You are building a comprehensive marketing strategy for Vibedata, an analytics product by Accelerate Data. You will use sub-agents (the Task tool) to run workstreams in parallel wherever dependencies allow. Save all outputs to `{VD_GTM_ROOT}/marketing-strategy/`.

All output paths below use `{VD_GTM_ROOT}` which is resolved in the Preamble. Every deliverable goes into `{VD_GTM_ROOT}/marketing-strategy/`.

## Preamble — Discover Repo Locations

### Locate vd-gtm Repository

Use Bash to locate the local clone of `accelerate-data/vd-gtm`:

```bash
find ~ -maxdepth 4 -type d -name "vd-gtm" 2>/dev/null | head -5
```

For each candidate directory, verify it is the correct repo:

```bash
git -C {candidate_path} remote -v 2>/dev/null | grep "accelerate-data/vd-gtm"
```

If no match is found or the result is ambiguous, use AskUserQuestion to ask the user for the local path to their `accelerate-data/vd-gtm` clone.

Set `VD_GTM_ROOT` to the verified path.

### Locate Sibling Repos

From `{VD_GTM_ROOT}`'s parent directory, locate sibling repos:
- **vd-specs-product-vision** (VISION_ROOT)
- **vd-specs-product-architecture** (ARCH_ROOT)

If a required sibling repo is not found, warn the user and halt.

---

## Step 0: Context Ingestion

**Core context (strategy, architecture, all 6 personas):**

Execute `/understand-vibedata` and wait for its confirmation checklist. This loads `vibedata-strategy.md`, `vibedata-architecture.md`, and all 6 current persona files into context.

Then read these additional files. Do not proceed until every file is read.

**Supporting vision context:**
- All files in `{VISION_ROOT}/context/`

**Existing competitor research (authoritative — do NOT do new competitor research, use this as ground truth):**
- All files in `{VISION_ROOT}/context/competition/`

**Supporting architecture context:**
- All files in `{ARCH_ROOT}/context/`

**Engineering-as-marketing reference docs (authoritative — preserve these, do not regenerate):**
- `{VD_GTM_ROOT}/marketing-strategy/07a-utility-inventory.md` — ranked utility inventory with competitive whitespace
- `{VD_GTM_ROOT}/marketing-strategy/07b-external-validation.md` — competitions, benchmarks, and recognition opportunities

After reading everything, produce and save an internal context brief to `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md` containing:
- Core value prop and differentiation
- Target segments and persona summary (pain points, JTBD, channel preferences)
- Technical capabilities relevant to marketing claims
- Competitive landscape summary (from the competition files)
- Key constraints or open questions from the source material
- Engineering-as-marketing strategy: utility trust loop, downloadable-first distribution model, Wave 1 utilities, external validation opportunities (from 07a and 07b)

This file is the shared context artifact. Every sub-agent must read it before starting its work.

---

## Step 1: Parallel Foundation Layer

Launch **three sub-agents simultaneously** using the Task tool. Each agent reads `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md` plus the specific source files it needs.

### Agent 1A: ICP Refinement & Persona Validation

Read and follow `{VD_GTM_ROOT}/.claude/openclaudia-skills/icp-builder/SKILL.md`.

Read: `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md`, all files in `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/`, `{VISION_ROOT}/vibedata-strategy.md`, `{VD_GTM_ROOT}/marketing-strategy/07a-utility-inventory.md`

Task:
1. Validate or challenge whether the current personas are the right targets given the product's actual capabilities and positioning.
2. For each validated persona, produce a B2B ICP card: firmographics, technographics, situational triggers, Jobs to Be Done, top 3 objections with response frameworks, channel mapping (where they consume content, where buying decisions happen).
3. Identify persona gaps — segments the product clearly serves but no persona exists for.
4. Rank personas by estimated revenue impact and acquisition feasibility.
5. Integrate utility channel mapping: for each persona where free downloadable utilities are relevant (per 07a-utility-inventory.md), add utility channel to the channel mapping table with relevance score.

Output: `{VD_GTM_ROOT}/marketing-strategy/01-icp-personas.md`

### Agent 1B: Competitive Landscape Analysis

Read and follow `{VD_GTM_ROOT}/.claude/openclaudia-skills/competitor-analysis/SKILL.md`.

Read: `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md`, all files in `{VISION_ROOT}/context/competition/`, `{VD_GTM_ROOT}/marketing-strategy/07a-utility-inventory.md`

Task — use ONLY the existing competitor research files as source material, do not invent competitors or do web research:
1. Categorize competitors into: direct (same category), indirect (alternative approaches), and aspirational comparisons.
2. For each direct competitor, synthesize from the existing research: positioning, pricing model, product strengths/weaknesses, and gaps relative to Vibedata.
3. Map competitors on a 2x2 matrix using the two differentiation dimensions most relevant to Vibedata (derive these from the competition files).
4. Produce a SWOT for Vibedata relative to the competitive set.
5. List 5 concrete positioning opportunities — gaps competitors leave open that Vibedata can own.
6. Include a sixth positioning opportunity on free utilities as a trust-building competitive advantage. Reference the competitive whitespace analysis from 07a-utility-inventory.md — note which utilities have zero alternatives.

Output: `{VD_GTM_ROOT}/marketing-strategy/03-competitive-analysis.md`

### Agent 1C: Growth Model Foundation

Read and follow `{VD_GTM_ROOT}/.claude/openclaudia-skills/growth-strategy/SKILL.md`.

Read: `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md`, `{VISION_ROOT}/vibedata-strategy.md`, `{ARCH_ROOT}/vibedata-architecture.md`

Task:
1. Define a North Star Metric for Vibedata and justify it against the product strategy.
2. Map the AARRR funnel with Vibedata-specific definitions, target benchmarks, and measurement approach for each stage.
3. Identify 2-3 viable growth loops (viral, content, paid, sales-led expansion) given the product type. For each loop: mechanism, expected compounding effect, and dependencies. Include the Utility Trust Sub-Loop (engineering-as-marketing) as a sub-loop of the Content Authority Loop: free downloadable utilities → repeated-use trust → community mentions → AI search discoverability → CRP path. Key properties: downloadable-first (zero inference cost), email-gated, each utility extracted from production skills/agents.
4. Recommend an attribution model and justify the choice.

Output: `{VD_GTM_ROOT}/marketing-strategy/04a-growth-model.md`

---

## Step 2: Positioning (depends on Step 1A + 1B)

Wait for Agents 1A and 1B to complete. Then launch **one agent**:

### Agent 2: Positioning & Messaging

Read and follow `{VD_GTM_ROOT}/.claude/openclaudia-skills/product-marketing/SKILL.md`.

Read: `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md`, `{VD_GTM_ROOT}/marketing-strategy/01-icp-personas.md`, `{VD_GTM_ROOT}/marketing-strategy/03-competitive-analysis.md`

Task:
1. Apply the April Dunford positioning framework: competitive alternatives → unique attributes → customer value → target segment → market category. Use the competitive analysis output (not new research) for competitive alternatives.
2. Build a messaging hierarchy: internal positioning statement → value proposition → external headlines → feature-level messaging.
3. Create audience-specific messaging variants for each validated persona from the ICP output.
4. Draft battlecards for the top 2 competitor categories identified in the competitive analysis.

Output: `{VD_GTM_ROOT}/marketing-strategy/02-positioning-messaging.md`

---

## Step 3: Parallel Execution Layer (depends on Step 1 + Step 2)

Wait for Steps 1 and 2 to complete. Then launch **three sub-agents simultaneously**:

### Agent 3A: Demand Generation Plan

Read and follow `{VD_GTM_ROOT}/.claude/openclaudia-skills/demand-gen/SKILL.md`.

Read: `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md`, `{VD_GTM_ROOT}/marketing-strategy/01-icp-personas.md`, `{VD_GTM_ROOT}/marketing-strategy/02-positioning-messaging.md`, `{VD_GTM_ROOT}/marketing-strategy/04a-growth-model.md`

Task:
1. Design a full-funnel demand gen plan built on the growth loops from 04a:
   - TOFU: awareness channels and content types per persona, budget allocation rationale. Include free downloadable utilities as a TOFU trust-building channel: Wave 1 utilities, email-gated download, 4-email post-download nurture sequence (Day 1 confirmation, Day 7 feedback, Day 14 bridge to platform, Day 30 CRP invitation), success criteria before building more.
   - MOFU: nurture sequences, lead scoring model (demographic fit + behavioral intent signals specific to Vibedata's personas)
   - BOFU: conversion campaigns, trial/demo strategy, sales enablement hooks
   - ABM component for enterprise persona if applicable
2. Define MQL/SQL criteria specific to Vibedata's buyer journey.

Output: `{VD_GTM_ROOT}/marketing-strategy/04b-demand-gen.md`

### Agent 3B: Content Strategy & Channel Plan

Read and follow `{VD_GTM_ROOT}/.claude/openclaudia-skills/content-strategy/SKILL.md`.

Read: `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md`, `{VD_GTM_ROOT}/marketing-strategy/01-icp-personas.md`, `{VD_GTM_ROOT}/marketing-strategy/02-positioning-messaging.md`, `{VD_GTM_ROOT}/marketing-strategy/03-competitive-analysis.md`

Task:
1. Design 2-3 topic clusters (pillar + supporting articles) aligned to the highest-value personas and their search intent.
2. Map content types to buyer journey stages (awareness → consideration → decision → retention) with specific Vibedata content ideas.
3. Propose a publishing cadence realistic for an early/growth-stage company.
4. Build a 90-day content calendar: blog, LinkedIn, email, and community channels relevant to the personas.
5. Define a repurposing workflow: how each pillar piece becomes 8+ derivative assets.
6. KPIs per content type and channel.
7. Include utility-related content types: utility landing pages (SEO surface, email-gated download, 500-800 words), utility launch posts (LinkedIn, 300-500 words, problem-first), GitHub repos as community engagement channel.

Output: `{VD_GTM_ROOT}/marketing-strategy/05-content-channel-plan.md`

### Agent 3C: Launch Strategy

Read and follow `{VD_GTM_ROOT}/.claude/openclaudia-skills/launch-strategy/SKILL.md`.

Read: `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md`, `{VD_GTM_ROOT}/marketing-strategy/01-icp-personas.md`, `{VD_GTM_ROOT}/marketing-strategy/02-positioning-messaging.md`, `{VD_GTM_ROOT}/marketing-strategy/04a-growth-model.md`, `{VD_GTM_ROOT}/marketing-strategy/07b-external-validation.md`

Task:
1. Classify the appropriate launch type (stealth, beta, public, Product Hunt, etc.) based on product maturity from the strategy docs.
2. Build an 8-week pre-launch → launch week → 8-week post-launch timeline with specific activities per week.
3. Include platform-specific playbooks if Product Hunt or Hacker News launches are recommended.
4. Define launch success metrics with specific numeric targets.
5. Propose budget allocation across content, paid, PR/outreach, and tools.
6. Prioritized list of the top 10 marketing actions to execute first, ordered by expected impact and effort.
7. Integrate utility shipment into the launch timeline: Wave 1 utilities ship Week 1-2 of Phase 1 (before first CRP conversions measured). Include competition/benchmark submissions from 07b-external-validation.md with their deadlines. Add utility download metrics to the Phase 1→Phase 2 gate criteria.

Output: `{VD_GTM_ROOT}/marketing-strategy/06-launch-execution.md`

---

## Step 4: Synthesis (depends on ALL prior steps)

Wait for all agents to complete. Then produce the final deliverable yourself (no sub-agent):

### Executive Summary

Read every file in `{VD_GTM_ROOT}/marketing-strategy/`.

Produce:
1. 1-page strategy overview connecting all workstreams into a coherent narrative.
2. Key bets and assumptions that need validation (with suggested validation methods).
3. Critical dependencies and risks.
4. Sequenced execution roadmap — what to do in weeks 1-4, 5-8, 9-12.
5. Metrics dashboard: what to track weekly, monthly, quarterly.
6. Budget summary rolled up from all workstreams.

Output: `{VD_GTM_ROOT}/marketing-strategy/00-executive-summary.md`

---

## Execution Architecture (Dependency Graph)

```
Step 0: Context Ingestion → {VD_GTM_ROOT}/marketing-strategy/_context-brief.md
  │
  ├──→ Agent 1A: ICP/Personas ──┐
  ├──→ Agent 1B: Competitive ───┤──→ Agent 2: Positioning ──┐
  └──→ Agent 1C: Growth Model ──┘                           │
                                                             ├──→ Agent 3A: Demand Gen ──┐
                                                             ├──→ Agent 3B: Content ─────┤──→ Step 4: Synthesis
                                                             └──→ Agent 3C: Launch ──────┘
```

## Output Manifest

All deliverables land in `{VD_GTM_ROOT}/marketing-strategy/`:

| File | Agent | Step |
|------|-------|------|
| `_context-brief.md` | Orchestrator | 0 |
| `01-icp-personas.md` | 1A | 1 |
| `03-competitive-analysis.md` | 1B | 1 |
| `04a-growth-model.md` | 1C | 1 |
| `02-positioning-messaging.md` | 2 | 2 |
| `04b-demand-gen.md` | 3A | 3 |
| `05-content-channel-plan.md` | 3B | 3 |
| `06-launch-execution.md` | 3C | 3 |
| `00-executive-summary.md` | Orchestrator | 4 |
| `07a-utility-inventory.md` | — (reference input) | — |
| `07b-external-validation.md` | — (reference input) | — |
| `09-linear-hierarchy.md` | — (not regenerated) | — |

## Rules for ALL agents:

- Every agent MUST read `{VD_GTM_ROOT}/marketing-strategy/_context-brief.md` as its first action.
- Every agent MUST read its declared input files from prior steps before producing output.
- All outputs go to `{VD_GTM_ROOT}/marketing-strategy/`. No exceptions.
- Use ONLY the existing competitor research in `{VISION_ROOT}/context/competition/`. Do not do web searches for competitor information. Do not invent competitors not present in the source files.
- Be specific to Vibedata. Every recommendation must trace to something in the source material. Generic marketing advice is unacceptable.
- When a skill prompts for information already available in the context files, use that data — do not ask the user.
- Flag genuine ambiguities or gaps in source material explicitly in the output rather than guessing.
- No filler. Every sentence must be actionable or inform a decision.
- Do NOT regenerate `07a-utility-inventory.md`, `07b-external-validation.md`, or `09-linear-hierarchy.md`. These are reference/operating documents maintained separately. Read them as inputs; integrate their content into the strategy docs you produce.
