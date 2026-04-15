---
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - Agent
---

Generate base pitch decks for all 6 personas in parallel via the Gamma REST API. No company customization for variable personas — produces generic persona-specific decks. Anthropic and Fabric use their fixed company constants.

## Orchestration

Spawn 6 parallel subagents (one per persona). Each runs the full pitch generation pipeline independently. Use Opus for section/assembly/QA agents, Sonnet for Gamma agents.

All 6 personas run simultaneously — do not wait for one to finish before starting another. Gamma generation uses direct curl calls to the REST API (no MCP server needed).

## Persona Configurations

### Fixed-company personas (use company constants)

| Persona Key | COMPANY_NAME | COMPANY_DOMAIN | COMPANY_LOGO_URL | Pitch File | Persona Source |
|-------------|--------------|----------------|-------------------|-----------|---------------|
| `anthropic` | Anthropic | anthropic.com | `https://addataexchange.blob.core.windows.net/adbranding/partners/anthropic-logo.png` | `{VD_GTM_ROOT}/gtm_pitch/decks/anthropic.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/anthropic_partner_persona.md` |
| `fabric` | Microsoft | microsoft.com | `https://addataexchange.blob.core.windows.net/adbranding/partners/microsoft-logo.png` | `{VD_GTM_ROOT}/gtm_pitch/decks/fabric.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/fabric_partner_persona.md` |

For these two personas: run the **full pipeline including research agent** (research the fixed company), then section agents, assembly, QA, auto-approve, Gamma.

### Variable-company personas (generic — no company customization)

| Persona Key | Pitch File | Persona Source |
|-------------|-----------|---------------|
| `customer` | `{VD_GTM_ROOT}/gtm_pitch/decks/customer.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/customer_persona.md` |
| `pe` | `{VD_GTM_ROOT}/gtm_pitch/decks/pe.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/pe_persona.md` |
| `si` | `{VD_GTM_ROOT}/gtm_pitch/decks/si.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/si_persona.md` |
| `investor` | `{VD_GTM_ROOT}/gtm_pitch/decks/investor.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/investor_persona.md` |

For these four personas: **skip the research agent entirely**. Section agents write from persona docs, pitch files, v3 structure, and strategy/architecture docs only. No company name, no company logo on Slide 1, no customization hooks.

## Section Registry

Use the section registries from `/generate-pitch` — same section splits per persona.

### Customer (4 sections)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-4 | Title + hook, The Problem, 5 Failure Categories, Why Now |
| Product | 5-10 | The Shift, What is Vibedata, Four Pillars, Architecture, Builder Agents, Operator Agents |
| Proof | 11-14 | Skills, Flywheel, Demo Placeholder, Results |
| User Experience | 15-21 | FSA, DRE, Data Mesh, Security, Competitive, Journey, CTA |

### Anthropic (3 sections)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-2 | Title + hook, The Consumption Opportunity |
| Product | 3-7 | Why Generic AI Fails, Why Now, Agents, Skills, Architecture |
| Proof & Close | 8-15 | Agent Knowledge, Telemetry, Autonomy, Consumption Growth, Demo, Competitive, Partnership, CTA |

### Fabric (3 sections)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-3 | Title + hook, Problem (Fabric lens), Why Now |
| Product | 4-7 | What is Vibedata, Architecture, Fabric IQ, Agents |
| Proof & Close | 8-16 | Consumption Multiplier, Security, Demo, Success Metrics, Dev Model, Data Mesh, Competitive, Co-Sell, CTA |

### PE (4 sections)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-5 | Title + hook, Problem (portfolio lens), Why Now, 1:10:100 Rule, The Shift |
| Product | 6-10 | What is Vibedata, Architecture, Three Levers, Flywheel, Data Mesh |
| Portfolio Value | 11-15 | Demo, Results, PE Scorecard, Exit Readiness, Security |
| Close | 16-19 | Microsoft Ecosystem, SI Delivery Channel, Typical Playbook, CTA |

### SI (4 sections)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-4 | Title + hook, The Market Shift, Your Gap, The Shift |
| Product | 5-8 | What is Vibedata, Four Pillars, Architecture, Validation as Specification |
| Practice Building | 9-14 | SI Flywheel, Skills Marketplace, Data Mesh, Demo, Deal Economics, Engagement Model |
| Close | 15-19 | Enablement, Agents vs Frameworks, Success Metrics, Partnership Journey, CTA |

### Investor (4 sections)
| Section | Slides | Focus |
|---------|--------|-------|
| Opening | 1-5 | Title + hook, Market Timing, TAM Validation, The Shift, Agent Consumption Tailwind |
| Product | 6-10 | What is Vibedata, Architecture, Four Pillars, Articulation Problem, Demo |
| Investment Thesis | 11-14 | Results, Competitive Moat, Business Model + GTM Efficiency, Traction Signals |
| Close | 15-18 | Exit/Growth Narrative, Due Diligence Summary, Investor-Type CTAs, The Ask |

## Per-Persona Subagent Prompt

Spawn one subagent per persona with this prompt. Replace `{PLACEHOLDERS}` from the tables above.

```
You are generating the base {PERSONA_NAME} pitch deck for Vibedata. This is a generic deck — no company-specific customization.

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

---

## Derive BUILD_DIR

TIMESTAMP = current datetime as YYYYMMDD-HHMM
BUILD_DIR_PREFIX = {PERSONA_KEY}_base

Resume check: look for the most recent folder matching `{VD_GTM_ROOT}/gtm_pitch/_build/{BUILD_DIR_PREFIX}_*/` (sorted descending).
- If one exists AND does not contain `qa_passed` → resume into it (set BUILD_DIR to that folder)
- Otherwise → BUILD_DIR = `{VD_GTM_ROOT}/gtm_pitch/_build/{BUILD_DIR_PREFIX}_{TIMESTAMP}`

Create the BUILD_DIR directory. Mark completed artifacts as `[done]` and only spawn agents for pending tasks.

## Pipeline

You will coordinate a team of agents to produce this deck. Use delegate mode.

### Step 1: Research (fixed-company personas only)

{FOR ANTHROPIC/FABRIC ONLY}:
Spawn a research agent (Opus) to research {COMPANY_NAME} ({COMPANY_DOMAIN}). The research agent must:
1. Read `{PERSONA_SOURCE_PATH}` to understand persona concerns
2. Read `{VD_GTM_ROOT}/gtm_pitch/pitch_structure_v3.md` for v3 framing
3. Research the company via web search through the persona lens
4. Write brief to `{BUILD_DIR}/research.md`

{FOR CUSTOMER/PE/SI/INVESTOR}: Skip this step entirely. No research agent.

### Step 2: Section Agents

Spawn one section agent (Opus) per section from the Section Registry. All run in parallel.

Each section agent reads:
1. `{PITCH_FILE_PATH}` — slide table (only their slide range)
2. `{VD_GTM_ROOT}/gtm_pitch/pitch.md` — shared foundation
3. `{VD_GTM_ROOT}/gtm_pitch/pitch_structure_v3.md` — v3 pitch structure
4. `{PERSONA_SOURCE_PATH}` — persona context
5. Read `.claude/commands/understand-vibedata.md` and load all core context files listed in it.
6. {FOR ANTHROPIC/FABRIC}: `{BUILD_DIR}/research.md`

Content rules:
- 2-4 concise sentences or bullet points per slide
- {FOR ANTHROPIC/FABRIC}: Include company logo on Slide 1 as `![{COMPANY_NAME}]({COMPANY_LOGO_URL})`
- {FOR CUSTOMER/PE/SI/INVESTOR}: No company logo, no company references
- Use v3 framing throughout: "cognitive cowork", "Full Stack Analyst", "validation as specification", "agent composability", "skills as org-specific delta"
- Metrics as capabilities — no caveats
- Brand voice: calm, authoritative, systems-minded
- Hero image slides: keep image as markdown, minimal surrounding text
- Icon-led slides: structured as labelled items (bold label + short description per line)

Write output to: `{BUILD_DIR}/{SECTION_KEY}.md`

### Step 3: Assembly Agent

Spawn one assembly agent (Opus) after all section agents complete. It must:
1. Read all section files for this persona
2. Stitch into one cohesive markdown document
3. Verify narrative flow, v3 framing consistency, and slide count
4. {FOR ANTHROPIC/FABRIC}: Verify company logo on Slide 1 and company customizations
5. Write to: `{BUILD_DIR}/assembled.md`
6. Title format: `# {PERSONA_LABEL}-Base-{Mon}-{DD}`

### Step 4: QA Agent

Spawn one QA agent (Opus) after assembly. Validation checklist:
1. Slide count matches expected total
2. No hype language ("revolutionary", "game-changing", etc.)
3. Metrics as capabilities (no "up to", "targets", "estimated")
4. Persona framing matches cross-persona matrix in pitch.md
5. Narrative coherence (hook → close, claims → proof)
6. Brand voice: calm, authoritative, systems-minded
7. v3 framing compliance (no v2 terminology)
8. No governance language
9. {FOR ANTHROPIC/FABRIC}: Company logo present on Slide 1, customizations accurate
10. {FOR CUSTOMER/PE/SI/INVESTOR}: No stray company references

If ALL pass: write marker file `{BUILD_DIR}/qa_passed`
If ANY fail: message Assembly agent with failures for revision, then re-QA.

### Step 5: Gamma Generation (auto-approve — no manual review)

After QA passes, generate the Gamma presentation directly via curl (no dedicated Gamma agent needed):
1. Read `{BUILD_DIR}/assembled.md`
2. Read `{VD_GTM_ROOT}/gtm_pitch/workflow/gamma.md` — Gamma REST API parameter spec
3. Construct a JSON payload file at `{BUILD_DIR}/gamma_payload.json` with all parameters from `gamma.md`
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
6. Report: "Gamma complete for {PERSONA_NAME}: $GAMMA_URL"
```

## Completion

Collect all 6 Gamma URLs as they come in. Present them to the user in a summary table:

| Persona | Gamma URL |
|---------|-----------|
| Customer | [url] |
| Anthropic | [url] |
| Fabric | [url] |
| PE | [url] |
| SI | [url] |
| Investor | [url] |
