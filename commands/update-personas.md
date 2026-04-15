---
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Agent
  - AskUserQuestion
---

Refresh all GTM persona documents to align with the latest Vibedata strategy and architecture using agent teams.

## Step 0 — Discover Repo Locations

Use `git rev-parse --show-toplevel` to get this repo's root. From its parent directory, locate sibling repos:
- **vd-specs-product-vision** (VISION_ROOT)
- **vd-specs-product-architecture** (ARCH_ROOT)

If a required sibling repo is not found, warn the user and halt.

## Step 1: Load Core Context

Execute `/understand-vibedata` and wait for its confirmation checklist. This loads `vibedata-strategy.md`, `vibedata-architecture.md`, and all 6 current personas into context.

## Step 2: Create Agent Team

Create an agent team with 6 teammates. Use Opus for all agents. Run in delegate mode — coordinate only, do not edit persona files directly.

### Persona Teammates (5 agents)

Each persona teammate owns exactly one persona file:

| Teammate Name | Persona File | Focus |
|---|---|---|
| `customer-persona` | `gtm_personas/indvidual_personas/customer_persona.md` | Buyer + User alignment with strategy |
| `fabric-partner` | `gtm_personas/indvidual_personas/fabric_partner_persona.md` | Microsoft partnership + consumption model |
| `anthropic-partner` | `gtm_personas/indvidual_personas/anthropic_partner_persona.md` | Technology partnership + API consumption |
| `si-partner` | `gtm_personas/indvidual_personas/si_persona.md` | Regional SI enablement + practice building |
| `pe-investor` | `gtm_personas/indvidual_personas/pe_persona.md` | PE operating partner + portfolio value |

### Spawn Prompt for Each Persona Teammate

```
You are refreshing the {PERSONA_NAME} GTM persona to align with the latest Vibedata strategy and architecture.

Read these source documents first:
- Strategy: {VISION_ROOT}/vibedata-strategy.md
- Architecture: {ARCH_ROOT}/vibedata-architecture.md

Then read your assigned persona file:
- gtm_personas/indvidual_personas/{PERSONA_FILE}

Optional references (consult as needed):
- User personas: {VISION_ROOT}/context/personas/
- Competitors: {VISION_ROOT}/context/competition/
- Decision log: {VISION_ROOT}/context/decision-log.md
- Utility strategy: ./marketing-strategy/07a-utility-inventory.md (persona-utility mapping for channel tables)

Update the persona file to reflect the latest strategy and architecture. Preserve the existing document structure. Focus on:
- New capabilities, modules, or agents mentioned in strategy/architecture
- Updated positioning, messaging, or value propositions
- Changed pricing, packaging, or commercial terms
- New competitive dynamics or market positioning
- Revised success metrics or KPIs

### ICP Quality Checklist

After making strategy-alignment updates, audit the persona against these dimensions.
If a dimension is missing or thin, add a new section at the END of the document.
Do NOT restructure existing sections.

1. **Pain Point Severity** — Every pain point must have severity (1-10) and
   frequency (daily/weekly/monthly). Add inline to existing pain points if missing.

2. **JTBD Statements** — At least 2 Jobs-To-Be-Done statements:
   "When I [situation], I want to [action], so I can [outcome]."
   Add "## Jobs To Be Done" section at end if none exists.

3. **Objection Handling** — Top 3 objections this persona would raise, categorized
   (Price/Timing/Trust/Inertia/Authority/Technical) with response frameworks.
   For partner personas, "objections" = reasons they hesitate to integrate/invest.
   Add "## Objection Handling" section at end if none exists.

4. **Qualifying Criteria** — Must-have signals (this persona is a fit),
   nice-to-have, and disqualifying signals. Add "## Qualifying Criteria" section
   at end if none exists.

5. **Buying Behavior** — Research style (self-serve/peer/sales-assisted),
   decision speed (fast/slow), budget authority (yes/needs approval/influences).
   Add to Profile table or "## Buying Behavior" section if not present.

6. **Channel Mapping** — Top 3-5 channels where this persona looks for information,
   with relevance score (1-5). Include free downloadable utilities as a channel if
   the persona appears in 07a-utility-inventory.md. Add "## Channel Mapping" section
   at end if none exists.

If a dimension already exists with adequate depth, do not duplicate it.

After updating, message other persona teammates to check cross-persona consistency:
- Do partner value props reference the same customer pain points?
- Are pricing/packaging references consistent?
- Is terminology uniform across all personas?

Send the lead a summary of: changes made, content added, content removed, open questions. Flag which ICP dimensions were added vs. already present.
```

### Review Teammate (1 agent)

Spawn the review teammate (`persona-reviewer`) with a dependency on all 5 persona tasks completing first.

The review teammate must:

1. Wait for all persona teammates to finish (task dependency)
2. Read all 5 updated persona files
3. Read the existing `gtm_personas/decisions.md` to understand current decision numbering
4. Read the existing `gtm_personas/clarification.md`
5. Read the existing `gtm_personas/changelog.md` (create if it doesn't exist)
6. Perform these updates:

**decisions.md** — Append new entries if any persona teammate made decisions that should be logged. Follow the existing format:

```markdown
## {Persona Name} Decisions

| ID | Decision | Rationale |
|----|----------|-----------|
| XX-NN | Decision text | Why this decision was made |
```

Continue the existing ID numbering sequence (e.g., if CP-15 exists, next is CP-16).

**clarification.md** — Append any open questions that arose during the refresh:

```markdown
## Open Questions from {Date} Refresh

| Persona | Question | Context | Answer |
|---------|----------|---------|--------|
| {name} | Question text | Why this needs clarification | (blank until resolved) |
```

**changelog.md** — Append a dated entry summarizing all changes:

```markdown
## {YYYY-MM-DD} — Strategy Refresh

### Summary
One-paragraph overview of what changed and why.

### Changes by Persona

#### Customer Persona
- List of specific changes

#### Fabric Partner Persona
- List of specific changes

#### Anthropic Partner Persona
- List of specific changes

#### SI Persona
- List of specific changes

#### PE Persona
- List of specific changes

### New Decisions Logged
- Count and summary of new decisions added to decisions.md

### Open Questions
- Count and summary of questions added to clarification.md
```

## Step 3: Create Task List

```
1. [persona] Refresh customer persona — assigned to customer-persona
2. [persona] Refresh Fabric partner persona — assigned to fabric-partner
3. [persona] Refresh Anthropic partner persona — assigned to anthropic-partner
4. [persona] Refresh SI persona — assigned to si-partner
5. [persona] Refresh PE persona — assigned to pe-investor
6. [review] Cross-persona review and docs update — assigned to persona-reviewer (depends on tasks 1-5)
```

Tasks 1-5 run in parallel. Task 6 starts after all 5 complete.

## Completion Criteria

The refresh is complete when:

1. All 5 persona files are updated and aligned with current strategy/architecture
2. Cross-persona consistency has been verified via inter-agent messaging
3. `decisions.md` has new entries (if any decisions were made)
4. `clarification.md` has new entries (if any questions arose)
5. `changelog.md` has a dated summary of all changes
6. The lead has reviewed teammate summaries and confirmed no conflicts
