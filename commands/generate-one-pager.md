---
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Agent
  - AskUserQuestion
  - mcp__read-website-fast__read_website
---

Generate a company-targeted, persona-specific Vibedata one-pager sales document using agent teams.

## Step 1: Determine Persona and Inputs

The persona key is provided as an argument: `$ARGUMENTS`

Valid persona keys: `customer`, `anthropic`, `fabric`, `pe`, `si`, `investor`

If no argument is provided or the argument is not a valid persona key, ask the user which persona to use.

### Persona Registry

| Key | Persona | Persona Source | Tone | Audience |
|-----|---------|---------------|------|----------|
| `customer` | Customer | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/customer_persona.md` | professional, authoritative | data engineering leaders |
| `anthropic` | Anthropic Partner | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/anthropic_partner_persona.md` | professional, strategic | partnership and business development |
| `fabric` | Fabric / Microsoft | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/fabric_partner_persona.md` | professional, technical-commercial | Microsoft SSPs and partner managers |
| `pe` | PE Operating Partner | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/pe_persona.md` | professional, measured | PE operating partners and portfolio managers |
| `si` | SI Partner | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/si_persona.md` | professional, pragmatic | SI practice leaders and consulting partners |
| `investor` | Investor | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/investor_persona.md` | professional, measured | equity investors (PE growth equity, institutional, HNW) |

### Gamma Constants

| Constant | Value |
|----------|-------|
| `AD_PAGERS_FOLDER_ID` | `yl1pixsortcr8dd` |
| `VIBEDATA_THEME_ID` | `jgvzmx3l86ktbs3` |
| `AD_LOGO_URL` | `https://addataexchange.blob.core.windows.net/adbranding/logo/dark/icon.png` |

### Collect Company Inputs

**For variable-company personas** (`customer`, `pe`, `si`, `investor`): Ask the user for:
- `COMPANY_NAME` (required) — Full company name
- `COMPANY_DOMAIN` (required) — Primary web domain

**For fixed-company personas** (`anthropic`, `fabric`): Use these constants — do NOT ask the user:

| Persona | COMPANY_NAME | COMPANY_DOMAIN |
|---------|--------------|----------------|
| `anthropic` | Anthropic | anthropic.com |
| `fabric` | Microsoft | microsoft.com |

### Collect Document Direction (all personas)

Ask the user for guiding input on the direction of the one-pager. This is freeform text that orients the entire workflow — research, drafting, and QA all use it. Store as `{DOC_DIRECTION}`. Optional — if the user has nothing specific, set to empty string.

Examples:
- "Focus on cost reduction — they just had layoffs and are under pressure to do more with less"
- "They're evaluating us against Datafold and Monte Carlo, so lean into the full-lifecycle story"
- "This is for a follow-up after a demo — they saw the product, now need something to circulate internally"

### Persona-Derived Follow-Up Questions (PE, SI, and Investor only)

For `pe`, `si`, and `investor` personas: read the persona source file and derive **up to 3 additional questions** that would improve document customisation. These are not hardcoded — read the persona file's pain points, decision drivers, and success criteria to determine what situational context would most strengthen the one-pager.

For `customer`, `anthropic`, and `fabric`: no additional questions.

Store answers as `{ADDITIONAL_CONTEXT}`.

### Derive COMPANY_KEY

Lowercase `COMPANY_NAME`, replace spaces with hyphens, strip non-alphanumeric characters (except hyphens).

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

### Derive BUILD_DIR

TIMESTAMP = current datetime as YYYYMMDD-HHMM
BUILD_DIR_PREFIX = {PERSONA_KEY}_{COMPANY_KEY}

Resume check: look for the most recent folder matching `{VD_GTM_ROOT}/gtm_onepagers/_build/{BUILD_DIR_PREFIX}_*/` (sorted descending).
- If one exists AND does not contain `review_approved` → resume into it (set BUILD_DIR to that folder)
- Otherwise → BUILD_DIR = `{VD_GTM_ROOT}/gtm_onepagers/_build/{BUILD_DIR_PREFIX}_{TIMESTAMP}`

Create the BUILD_DIR directory. Mark completed artifacts as `[done]` and only spawn agents for pending tasks.

---

## Step 2: Create Team and Task List

### Team Composition

Spawn teammates and create the task list with dependencies:
- **1 research agent** (opus) — runs first, blocks the drafter agent
- **1 drafter agent** (opus) — runs after research, blocks the QA agent
- **1 QA agent** (opus) — runs after drafter

---

## Step 3: Research Agent

Spawn the research agent first. It must complete before the drafter starts.

```
You are the research agent for the {PERSONA_NAME} one-pager targeting {COMPANY_NAME}.

## Resume Check
FIRST check if `{BUILD_DIR}/research.md` already exists and is non-empty. If it does, message the drafter agent with "Company research already complete", and stop.

## Your Assignment
Research {COMPANY_NAME} ({COMPANY_DOMAIN}) and produce a company brief that the drafter agent will use to customise the one-pager.

## Step 1: Understand the Persona
Read the persona source file: `{PERSONA_SOURCE_PATH}`
Identify: audience concerns, pain points, decision drivers, success criteria, competitive emphasis.

## Step 2: Understand v3 Framing
Read `{VD_GTM_ROOT}/gtm_pitch/pitch_structure_v3.md`. Key concepts: cognitive cowork, Full Stack Analyst/Builder, agent consumption tailwind, validation as specification, agent composability, skills as org-specific delta, MCP from Day 1.

## Step 3: Understand Positioning
Read `{VD_GTM_ROOT}/marketing-strategy/02-positioning-messaging.md`. Extract the per-persona messaging variant relevant to {PERSONA_KEY}. Note the primary message, headline, messaging framework elements, and proof points.

## Step 4: Apply Document Direction
User guidance: {DOC_DIRECTION}
If non-empty, this overrides default emphasis. Prioritise research areas that serve the stated direction.

## Step 5: Research the Company
Use web search through the lens of the persona's concerns, filtered through document direction.

Always gather:
- Company snapshot: industry, size, revenue/funding, HQ, core business (3-4 sentences)
- Recent news: last 6 months, 3-5 items

Then research 3-5 additional areas specific to the persona's concerns.

## Step 6: Incorporate Additional Context
Additional context from user: {ADDITIONAL_CONTEXT}

## Output
Write to: `{BUILD_DIR}/research.md`

Include: Company Snapshot, persona-specific research areas (3-5 sections), Recent News, Customisation Hooks (3-5 specific facts mapped to one-pager sections, using v3 concepts), Document Direction notes.

After writing, message the drafter agent: "Company research complete."
```

---

## Step 4: Drafter Agent

After research completes, spawn the drafter agent.

```
You are the drafter agent for the {PERSONA_NAME} one-pager targeting {COMPANY_NAME}.

## Resume Check
FIRST check if `{BUILD_DIR}/one-pager.md` already exists. If so, message the QA agent with "Draft already complete", and stop.

## Your Assignment
Write a complete one-pager sales document — a single markdown file that can be sent directly to a prospect.

## Context Files to Read
1. `{PERSONA_SOURCE_PATH}` — persona context
2. `{VD_GTM_ROOT}/gtm_pitch/pitch_structure_v3.md` — v3 pitch framing and vocabulary
3. `{VD_GTM_ROOT}/marketing-strategy/02-positioning-messaging.md` — per-persona messaging variant and proof points
4. `{BUILD_DIR}/research.md` — company research brief

## Document Direction
User guidance: {DOC_DIRECTION}

## Document Template

Write a markdown document with exactly this structure. The title line and section headers are fixed. Body text across all 6 sections must total 370–490 words.

```markdown
# Vibedata for {COMPANY_NAME}

## The Challenge
[60–80 words]

## The Shift
[50–70 words]

## How Vibedata Works
[90–120 words]

## Why Now
[50–70 words]

## What Makes This Different
[60–80 words]

## Next Step
[40–60 words]
```

## Section Guidance

### The Challenge
Frame the specific problem {COMPANY_NAME} faces through the lens of the persona's pain points. Reference concrete company details from research. Don't describe Vibedata's solution yet — earn the right to propose it.

### The Shift
Introduce the cognitive cowork paradigm — AI as delegation, not automation. Use v3 framing: junior coworker you supervise, not a stateless tool you trigger. Reference the Full Stack Analyst/Builder concept where relevant.

### How Vibedata Works
Describe the four pillars (LLM, Agentic Workflow, Skills, MCP) in terms of outcomes, not architecture. Structure as 3-4 labelled items (bold label + short description). Connect each to a specific {COMPANY_NAME} benefit using research hooks.

### Why Now
Connect to macro forces relevant to the persona: agent consumption tailwind, Full Stack Builder moment, the quality bar rising, competitive urgency. Use 1-2 specific data points (Gartner, Microsoft, Databricks stats from v3 framing).

### What Makes This Different
Draw the contrast with alternatives the persona is considering. Use the positioning doc's competitive framing. Focus on structural advantages (spec-driven, full lifecycle, flywheel, Skills) not feature lists.

### Next Step
Persona-appropriate call to action. Be specific and low-friction. One clear action, not a menu.

## Persona-Specific Emphasis

| Persona | The Challenge | The Shift | How It Works | Why Now | What's Different | Next Step |
|---------|--------------|-----------|-------------|---------|-----------------|-----------|
| `customer` | Backlog, firefighting, knowledge loss in small team | FSA: one person directing agents | Outcomes: pipeline speed, maintenance relief, knowledge capture | Agent consumption of their data; do-more-with-less pressure | vs. status quo, DIY (Claude Code/Cursor), dbt Cloud | CRP with sample data |
| `anthropic` | AI consumption of data creates quality crisis for their customers' customers | Vibedata makes data agent-ready | Consumption multiplier: more agent usage → more data quality needs → more Vibedata | 80% Fortune 500 using agents; quality is the bottleneck | Only full-lifecycle platform for agent-ready data | Partnership exploration meeting |
| `fabric` | Fabric customers need data quality for Fabric IQ and copilots | Vibedata extends Fabric with agentic data engineering | Fabric-native: MCP connectors, ephemeral workspaces, Azure deployment | Fabric adoption accelerating; IQ needs quality data | vs. Fabric Copilot (assistive only), DIY with AI coding tools (build the harness yourself) | Co-sell pilot or joint customer engagement |
| `pe` | Portfolio data teams can't scale; knowledge walks out the door | Platform that compounds across portfolio companies | 3 levers: build speed, operate efficiency, knowledge retention | AI-driven value creation is now PE table-stakes | Skills transfer across portfolio; repeatable playbook | Portfolio assessment call |
| `si` | Practice gap: clients want agentic, SI can't deliver | SI delivery channel for agentic data engineering | Engagement model: assessment → pilot → rollout with Skills IP | Service delivery model is shifting; build practices or lose relevance | Skills marketplace; deal economics; enablement path | SI partnership discussion |
| `investor` | Market timing: agentic data engineering is nascent with clear structural demand | Category creator in $24.5B market | Moat: spec-driven + full lifecycle + Skills flywheel + MCP | 46% CAGR; agent consumption tailwind; Nadella Full Stack Builder | No competitor has build+operate+flywheel | Investment conversation |

## Content Rules
- No hype language: avoid "revolutionary", "game-changing", "cutting-edge", "unprecedented", "best-in-class"
- No governance language: avoid "governance", "compliance", "CDO", "data stewardship"
- Metrics as capabilities: state what the system does, not hedged projections ("pipelines deploy in 2-4 hours" not "up to 80% faster")
- v3 framing: use "cognitive cowork", "delegation", "Full Stack Analyst", "validation as specification", "agent composability", "skills as org-specific delta" where natural
- Pyramid principle: lead each section with the conclusion, then support it
- Brand voice: calm, authoritative, systems-minded — no urgency language, no exclamation marks
- Write for the reader, not about Vibedata: "your team" not "our platform", "{COMPANY_NAME}'s data" not "Vibedata's approach"
- Every claim about {COMPANY_NAME} must trace to the research brief

## Output
Write to: `{BUILD_DIR}/one-pager.md`

After writing, message the QA agent: "Draft complete. Ready for QA."
```

---

## Step 5: QA Agent

```
You are the QA agent for the {PERSONA_NAME} one-pager targeting {COMPANY_NAME}.

## Resume Check
Check if `{BUILD_DIR}/qa_passed` exists. If so, stop.

## Context Files to Read
1. `{BUILD_DIR}/one-pager.md` — the draft to validate
2. `{BUILD_DIR}/research.md` — company research (for accuracy checks)
3. `{PERSONA_SOURCE_PATH}` — persona source (for alignment checks)
4. `{VD_GTM_ROOT}/marketing-strategy/02-positioning-messaging.md` — messaging framework (for positioning checks)

## Document Direction
User guidance: {DOC_DIRECTION}

## Validation Checklist (16 points)

### Structure (4 checks)
1. **Section count**: Exactly 6 sections with correct headers (The Challenge, The Shift, How Vibedata Works, Why Now, What Makes This Different, Next Step)
2. **Word count**: Total body text is 370–490 words (excluding title and headers)
3. **Per-section limits**: Each section falls within its specified word range
4. **Markdown format**: Clean markdown, no broken formatting, no raw HTML

### Content Quality (4 checks)
5. **No hype language**: Zero instances of "revolutionary", "game-changing", "cutting-edge", "unprecedented", "best-in-class", "world-class", "industry-leading", or similar
6. **No governance language**: Zero instances of "governance", "compliance", "CDO", "data stewardship", "regulatory"
7. **Metrics as capabilities**: All metrics stated as facts, not hedged ("pipelines deploy in 2-4 hours" not "up to 80% faster")
8. **v3 framing compliance**: Uses v3 terminology (cognitive cowork, delegation, Full Stack Analyst, validation as specification, skills as org-specific delta); zero v2 terms

### Persona Alignment (4 checks)
9. **Persona tone match**: Document tone matches the persona's specified tone from the registry
10. **Persona emphasis**: Each section reflects the persona-specific emphasis from the drafter's guidance table
11. **Audience-appropriate CTA**: Next Step is appropriate for the persona (not generic)
12. **Pain point accuracy**: The Challenge section addresses pain points documented in the persona source file

### Company Customisation (4 checks)
13. **Company name usage**: {COMPANY_NAME} appears naturally (not forced) in at least 3 sections
14. **Research accuracy**: Every company-specific claim traces to a fact in research.md — no fabricated details
15. **Research utilisation**: At least 3 of the 5 customisation hooks from research.md are incorporated
16. **Document direction alignment**: Content reflects the user's stated direction (if provided)
17. **Suppressed content**: scan one-pager for any topic tagged `[SUPPRESS_FROM_PITCH]` in the persona source file. Flag any instance.

## Scoring and Actions

Count passing checks out of 17.

**If ALL 17 pass**: write marker file `{BUILD_DIR}/qa_passed`, message team lead "QA passed (17/17). Ready for manual review."

**If 15-16 pass**: message the drafter agent with specific failures and ask for targeted fixes. Do not fail the whole document for minor issues.

**If <15 pass**: message the drafter agent with all failures. Request a revision pass.

After the drafter revises, re-validate from scratch.
```

---

## Step 6: Manual Review Gate

After QA passes:
1. Read `{BUILD_DIR}/one-pager.md`
2. Present the full content to the user with QA results summary
3. Ask: **"Approve this one-pager, or provide revision notes?"**

If approved:
- Write marker `{BUILD_DIR}/review_approved`
- Copy `{BUILD_DIR}/one-pager.md` to `{VD_GTM_ROOT}/gtm_onepagers/{PERSONA_KEY}_{COMPANY_KEY}.md`
- Present the final file path to the user
- Proceed to Step 7

If revisions requested:
- Route feedback to the drafter agent
- Re-QA after revisions
- Repeat until approved

---

## Step 7: Gamma A4 Document Generation

After manual review approval, generate a Gamma A4 document from the approved one-pager.

### 1. Build Gamma Payload

Read the approved `{BUILD_DIR}/one-pager.md` and write `{BUILD_DIR}/gamma_payload.json` with the following structure:

```json
{
  "inputText": "<contents of {BUILD_DIR}/one-pager.md>",
  "format": "document",
  "numCards": 2,
  "textMode": "preserve",
  "themeId": "jgvzmx3l86ktbs3",
  "folderIds": ["yl1pixsortcr8dd"],
  "additionalInstructions": "Clean A4 document layout. Use clear section headers with ample white space. No images — text and layout only. Maintain the brand's navy-and-cyan colour scheme. First page: title and opening sections. Second page: remaining sections and call to action. Professional, understated formatting suitable for email attachment or print.",
  "textOptions": {
    "amount": "medium",
    "language": "en-gb",
    "tone": "<tone from Persona Registry for current persona>",
    "audience": "<audience from Persona Registry for current persona>"
  },
  "imageOptions": {
    "source": "noImages",
    "style": "minimalist, professional, clean geometric lines, dark blue and cyan color palette, subtle futuristic technology aesthetic, data visualization, premium corporate style, understated and precise"
  },
  "cardOptions": {
    "dimensions": "a4",
    "headerFooter": {
      "bottomLeft": {
        "type": "image",
        "source": "custom",
        "src": "https://addataexchange.blob.core.windows.net/adbranding/logo/dark/icon.png",
        "size": "sm"
      },
      "hideFromFirstCard": true
    }
  }
}
```

### 2. Create Generation

```bash
GENERATION_ID=$(curl -s -X POST "https://public-api.gamma.app/v1.0/generations" \
  -H "X-API-KEY: $(printenv GAMMA_API_KEY)" \
  -H "Content-Type: application/json" \
  -d @{BUILD_DIR}/gamma_payload.json | jq -r '.id')
echo "Generation ID: $GENERATION_ID"
```

If the POST fails or returns an empty ID: report the error to the user, skip Gamma generation, and jump to Output.

### 3. Poll Until Complete

```bash
while true; do
  RESPONSE=$(curl -s "https://public-api.gamma.app/v1.0/generations/$GENERATION_ID" \
    -H "X-API-KEY: $(printenv GAMMA_API_KEY)")
  STATUS=$(echo "$RESPONSE" | jq -r '.status')
  echo "Status: $STATUS"
  if [ "$STATUS" = "completed" ]; then
    GAMMA_URL=$(echo "$RESPONSE" | jq -r '.gammaUrl')
    echo "Gamma URL: $GAMMA_URL"
    break
  elif [ "$STATUS" = "failed" ]; then
    echo "Gamma generation failed"
    echo "$RESPONSE" | jq .
    break
  fi
  sleep 10
done
```

### 4. Handle Result

- **Success**: Store `GAMMA_URL` for the Output section.
- **Failure**: Inform the user that Gamma generation failed but the markdown one-pager was delivered successfully. Do not fail the overall workflow.

---

## Output

Present both deliverables to the user:

1. **Markdown one-pager**: `{VD_GTM_ROOT}/gtm_onepagers/{PERSONA_KEY}_{COMPANY_KEY}.md`
2. **Gamma A4 document**: `{GAMMA_URL}` (if generation succeeded; omit this line if Gamma was skipped or failed)
