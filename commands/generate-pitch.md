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

Generate a company-targeted, persona-specific Vibedata pitch deck via the Gamma REST API using agent teams.

## Step 1: Determine Persona and Inputs

The persona key is provided as an argument: `$ARGUMENTS`

Valid persona keys: `customer`, `anthropic`, `fabric`, `pe`, `si`, `investor`

If no argument is provided or the argument is not a valid persona key, ask the user which persona to use.

### Persona Registry

| Key | Persona | Pitch File | Persona Source | Tone | Audience | Bookend Slides | All Slides |
|-----|---------|-----------|---------------|------|----------|----------------|------------|
| `customer` | Customer | `{VD_GTM_ROOT}/gtm_pitch/decks/customer.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/customer_persona.md` | professional, authoritative | data engineering leaders | 1-10, 13 (Buyer Section) | 1-21 |
| `anthropic` | Anthropic Partner | `{VD_GTM_ROOT}/gtm_pitch/decks/anthropic.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/anthropic_partner_persona.md` | professional, strategic | partnership and business development | 1, 2, 5, 6, 7, 12, 13, 15 | 1-15 |
| `fabric` | Fabric / Microsoft | `{VD_GTM_ROOT}/gtm_pitch/decks/fabric.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/fabric_partner_persona.md` | professional, technical-commercial | Microsoft SSPs and partner managers | 1, 2, 5, 6, 8, 9, 10, 15, 16 | 1-16 |
| `pe` | PE Operating Partner | `{VD_GTM_ROOT}/gtm_pitch/decks/pe.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/pe_persona.md` | professional, measured | PE operating partners and portfolio managers | 1, 2, 3, 4, 5, 7, 8, 11, 14, 19 | 1-19 |
| `si` | SI Partner | `{VD_GTM_ROOT}/gtm_pitch/decks/si.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/si_persona.md` | professional, pragmatic | SI practice leaders and consulting partners | 1, 2, 3, 4, 7, 9, 12, 13, 19 | 1-19 |
| `investor` | Investor | `{VD_GTM_ROOT}/gtm_pitch/decks/investor.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/investor_persona.md` | professional, measured | equity investors (PE growth equity, institutional, HNW) | 1, 2, 3, 4, 5, 7, 8, 11, 14, 18 | 1-18 |

### Collect Company Inputs

**For variable-company personas** (`customer`, `pe`, `si`, `investor`): Ask the user for:
- `COMPANY_NAME` (required) — Full company name
- `COMPANY_DOMAIN` (required) — Primary web domain
- `COMPANY_LOGO_URL` (required) — Direct URL to the company's logo image (PNG/SVG)

**For fixed-company personas** (`anthropic`, `fabric`): Use these constants — do NOT ask the user:

| Persona | COMPANY_NAME | COMPANY_DOMAIN | COMPANY_LOGO_URL |
|---------|--------------|----------------|-------------------|
| `anthropic` | Anthropic | anthropic.com | `https://addataexchange.blob.core.windows.net/adbranding/partners/anthropic-logo.png` |
| `fabric` | Microsoft | microsoft.com | `https://addataexchange.blob.core.windows.net/adbranding/partners/microsoft-logo.png` |

### Collect Deck Direction (all personas)

Ask the user for guiding input on the direction of the deck. This is freeform text that orients the entire workflow — research, section writing, assembly, and QA all use it. Store as `{DECK_DIRECTION}`. Optional — if the user has nothing specific, set to empty string.

Examples:
- "Focus on cost reduction — they just had layoffs and are under pressure to do more with less"
- "They're evaluating us against Datafold and Monte Carlo, so lean into the full-lifecycle story"
- "This is a second meeting — skip the problem framing, go deeper on architecture and the flywheel"

### Persona-Derived Follow-Up Questions (PE, SI, and Investor only)

For `pe`, `si`, and `investor` personas: read the persona source file and derive **up to 3 additional questions** that would improve deck customisation. These are not hardcoded — read the persona file's pain points, decision drivers, and success criteria to determine what situational context would most strengthen the pitch.

For `customer`, `anthropic`, and `fabric`: no additional questions.

Store answers as `{ADDITIONAL_CONTEXT}`.

### Derive COMPANY_KEY

Lowercase `COMPANY_NAME`, replace spaces with hyphens, strip non-alphanumeric characters.

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

Resume check: look for the most recent folder matching `{VD_GTM_ROOT}/gtm_pitch/_build/{BUILD_DIR_PREFIX}_*/` (sorted descending).
- If one exists AND does not contain `review_approved` → resume into it (set BUILD_DIR to that folder)
- Otherwise → BUILD_DIR = `{VD_GTM_ROOT}/gtm_pitch/_build/{BUILD_DIR_PREFIX}_{TIMESTAMP}`

Create the BUILD_DIR directory. Mark completed artifacts as `[done]` and only spawn agents for pending tasks.

---

## Step 2: Create Team and Task List

### v3 Beat Structure Reference

| # | Beat | Type | Duration | Purpose |
|---|------|------|----------|---------|
| 1 | Break the paradigm | Slide(s) | 5 min | Reframe AI from automation to cowork; Full Stack Analyst/Builder; agent consumption tailwind |
| 2 | Day 1: Build without skills | Demo | 5 min | LLM + Agentic Workflow floor; 4-tier quality framework |
| 3 | Day 1: Validation as specification | Demo | 5 min | Specification-driven development; time compression |
| 4 | Day 1: Feedback becomes skill | Demo | 5 min | Org-specific knowledge capture; compounding begins |
| 5 | Day 2: Fully closed loop (transient) | Demo | 5 min | Autonomous resolution; agent composability |
| 6 | Day 2: Waiting for approval (novel) | Demo | 5 min | Cowork moment; agent knows confidence boundary |
| 7 | Day 2: Tie back to new intent | Demo | 5 min | Flywheel; operate feeds build |
| 8 | New paradigm + architecture | Slide(s) | 5 min | Name the paradigm; architecture; four pillars; quality foundation |

### Section Registry

#### Customer (4 section agents)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-4 | Title + hook, The Problem, 5 Failure Categories, Why Now |
| Product | 5-10 | The Shift: Full Stack Analyst, What is Vibedata, Four Pillars, Architecture, Builder Agents, Operator Agents |
| Proof | 11-14 | Skills, Flywheel, Demo Placeholder, Results |
| User Experience | 15-21 | FSA, DRE, Data Mesh, Security, Competitive, Journey, CTA |

#### Anthropic (3 section agents)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-2 | Title + hook, The Consumption Opportunity |
| Product | 3-7 | Why Generic AI Fails, Why Now, Agents, Skills, Architecture |
| Proof & Close | 8-15 | Agent Knowledge, Telemetry, Autonomy, Consumption Growth, Demo, Competitive, Partnership, CTA |

#### Fabric (3 section agents)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-3 | Title + hook, Problem (Fabric lens), Why Now |
| Product | 4-7 | What is Vibedata, Architecture, Fabric IQ, Agents |
| Proof & Close | 8-16 | Consumption Multiplier, Security, Demo, Success Metrics, Dev Model, Data Mesh, Competitive, Co-Sell, CTA |

#### PE (4 section agents)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-5 | Title + hook, Problem (portfolio lens), Why Now, 1:10:100 Rule, The Shift |
| Product | 6-10 | What is Vibedata, Architecture, Three Levers, Flywheel, Data Mesh |
| Portfolio Value | 11-15 | Demo, Results, PE Scorecard, Exit Readiness, Security |
| Close | 16-19 | Microsoft Ecosystem, SI Delivery Channel, Typical Playbook, CTA |

#### SI (4 section agents)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-4 | Title + hook, The Market Shift, Your Gap, The Shift |
| Product | 5-8 | What is Vibedata, Four Pillars, Architecture, Validation as Specification |
| Practice Building | 9-14 | SI Flywheel, Skills Marketplace, Data Mesh, Demo, Deal Economics, Engagement Model |
| Close | 15-19 | Enablement, Agents vs Frameworks, Success Metrics, Partnership Journey, CTA |

#### Investor (4 section agents)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-5 | Title + hook, Market Timing, TAM Validation, The Shift, Agent Consumption Tailwind |
| Product | 6-10 | What is Vibedata, Architecture, Four Pillars, Articulation Problem, Demo |
| Investment Thesis | 11-14 | Results, Competitive Moat, Business Model + GTM Efficiency, Traction Signals |
| Close | 15-18 | Exit/Growth Narrative, Due Diligence Summary, Investor-Type CTAs, The Ask |

### Team Composition

Spawn teammates and create the task list with dependencies:
- **1 research agent** (opus) — runs first, blocks all section agents
- **N section agents** (opus) — one per section, run in parallel after research
- **1 assembly agent** (opus) — runs after all sections complete
- **1 QA agent** (opus) — runs after assembly
- (No dedicated Gamma agent — team lead runs curl directly after manual review approval)

---

## Step 3: Research Agent

Spawn the research agent first. It must complete before section agents start.

```
You are the research agent for the {PERSONA_NAME} pitch deck targeting {COMPANY_NAME}.

## Resume Check
FIRST check if `{BUILD_DIR}/research.md` already exists and is non-empty. If it does, message all section agents with "Company research already complete", and stop.

## Your Assignment
Research {COMPANY_NAME} ({COMPANY_DOMAIN}) and produce a company brief that section agents will use to customise the pitch deck.

## Step 1: Understand the Persona
Read the persona source file: `{PERSONA_SOURCE_PATH}`
Identify: audience concerns, pain points, decision drivers, success criteria, competitive emphasis.

## Step 2: Understand v3 Pitch Framing
Read `{VD_GTM_ROOT}/gtm_pitch/pitch_structure_v3.md`. Key concepts: cognitive cowork, Full Stack Analyst/Builder, agent consumption tailwind, validation as specification, agent composability, skills as org-specific delta, MCP from Day 1.

## Step 3: Apply Deck Direction
User guidance: {DECK_DIRECTION}
If non-empty, this overrides default emphasis. Prioritise research areas that serve the stated direction.

## Step 4: Research the Company
Use web search through the lens of the persona's concerns, filtered through deck direction.

Always gather:
- Company snapshot: industry, size, revenue/funding, HQ, core business (3-4 sentences)
- Recent news: last 6 months, 3-5 items

Then research 3-5 additional areas specific to the persona's concerns.

## Step 5: Incorporate Additional Context
Additional context from user: {ADDITIONAL_CONTEXT}

## Output
Write to: `{BUILD_DIR}/research.md`

Include: Company Snapshot, persona-specific research areas (3-5 sections), Recent News, Customisation Hooks (3-5 specific facts mapped to slides/sections, using v3 concepts), Deck Direction notes, Target Company Logo URL.

After writing, message all section agents: "Company research complete."
```

---

## Step 4: Section Agents

After research completes, spawn section agents in parallel (one per section). Each uses this prompt:

```
You are the {SECTION_NAME} section agent for the {PERSONA_NAME} pitch deck targeting {COMPANY_NAME}.

## Resume Check
FIRST check if `{BUILD_DIR}/{SECTION_KEY}.md` already exists. If so, stop.

## Your Assignment
Write presentation-ready content for slides {SLIDE_RANGE}.

## Deck Direction
User guidance: {DECK_DIRECTION}

## Context Files to Read
1. `{PITCH_FILE_PATH}` — slide table (only slides {SLIDE_RANGE})
2. `{VD_GTM_ROOT}/gtm_pitch/pitch.md` — shared foundation
3. `{VD_GTM_ROOT}/gtm_pitch/pitch_structure_v3.md` — v3 pitch structure
4. `{PERSONA_SOURCE_PATH}` — persona context
5. Read `.claude/commands/understand-vibedata.md` and load all core context files listed in it.
6. `{BUILD_DIR}/research.md` — company research brief

## Content Rules
- For each slide: 2-4 concise sentences or bullet points
- Opening section Slide 1: include company logo as `![{COMPANY_NAME}]({COMPANY_LOGO_URL})`
- Hero image slides: keep image as markdown, minimal surrounding text
- Icon-led slides: structured as labelled items (bold label + short description per line)
- [COMMON] slides: use as written, reference company context where it strengthens the message
- [PERSONA-SPECIFIC] slides: tune language and incorporate customisation hooks from research brief
- Use v3 framing: "cognitive cowork", "delegation", "Full Stack Analyst", "validation as specification", "agent composability", "skills as org-specific delta"
- Metrics as capabilities — no caveats
- Brand voice: calm, authoritative, systems-minded

## Messaging Protocol
Coordinate with other section agents before writing. After writing, message the Assembly agent with section complete summary.

## Output
Write to: `{BUILD_DIR}/{SECTION_KEY}.md`
```

---

## Step 5: Assembly Agent

```
You are the assembly agent for the {PERSONA_NAME} pitch deck targeting {COMPANY_NAME}.

## Resume Check
Check if `{BUILD_DIR}/assembled.md` exists. If so, stop.

## Task
Wait for all section agents. Then:
1. Read all section files and research brief
2. Stitch into one cohesive markdown document
3. Verify narrative flow, v3 framing consistency, company customisations, slide count, and company logo on Slide 1
4. Write to: `{BUILD_DIR}/assembled.md`

Title format: `# {PERSONA_LABEL}-{COMPANY_NAME}-{Mon}-{DD}`

Message QA agent when complete.
```

---

## Step 6: QA Agent

```
You are the QA agent for the {PERSONA_NAME} pitch deck targeting {COMPANY_NAME}.

## Resume Check
Check if `{BUILD_DIR}/qa_passed` exists. If so, stop.

## Validation Checklist
1. Slide count matches expected total
2. No hype language ("revolutionary", "game-changing", etc.)
3. Metrics as capabilities (no "up to", "targets", "estimated")
4. Persona framing matches cross-persona matrix in pitch.md
5. Narrative coherence (hook → close, claims → proof)
6. Naming convention follows format
7. Brand voice: calm, authoritative, systems-minded
8. Company logo on Slide 1
9. Company customisation accuracy (cross-reference against research brief)
10. Deck direction alignment
11. v3 framing compliance (no v2 terminology)
12. No governance language ("governance", "compliance", "CDO")

If ALL pass: write marker file `{BUILD_DIR}/qa_passed`, message team lead "QA passed. Ready for manual review."
If ANY fail: message Assembly agent with specific failures.
```

---

## Step 7: Manual Review Gate

After QA passes:
1. Read the assembled markdown
2. Present the full content to the user with QA results summary
3. Ask: **"Approve for Gamma generation, or provide revision notes?"**

If approved: write marker `{BUILD_DIR}/review_approved`, message Gamma agent to proceed.
If revisions requested: route feedback to Assembly/section agents, re-QA, repeat until approved.

---

## Step 8: Gamma Generation (team lead runs directly)

After manual review approval, the team lead generates the Gamma presentation via the REST API:

1. Read `{BUILD_DIR}/assembled.md` — the final, user-approved slide content
2. Read `{VD_GTM_ROOT}/gtm_pitch/workflow/gamma.md` — Gamma REST API parameter spec
3. Construct a JSON payload file at `{BUILD_DIR}/gamma_payload.json` with all parameters from `gamma.md` (fixed + variable for this persona)
4. Create the generation:
   ```bash
   GENERATION_ID=$(curl -s -X POST "https://public-api.gamma.app/v1.0/generations" \
     -H "X-API-KEY: $(printenv GAMMA_API_KEY)" \
     -H "Content-Type: application/json" \
     -d @{BUILD_DIR}/gamma_payload.json | jq -r '.id')
   ```
5. Poll until complete:
   ```bash
   while true; do
     RESPONSE=$(curl -s "https://public-api.gamma.app/v1.0/generations/$GENERATION_ID" \
       -H "X-API-KEY: $(printenv GAMMA_API_KEY)")
     STATUS=$(echo "$RESPONSE" | jq -r '.status')
     if [ "$STATUS" = "completed" ]; then
       GAMMA_URL=$(echo "$RESPONSE" | jq -r '.gammaUrl')
       break
     elif [ "$STATUS" = "failed" ]; then
       echo "Generation failed"; echo "$RESPONSE" | jq .; break
     fi
     sleep 10
   done
   ```

---

## Output

Present the Gamma presentation URL to the user when complete.
