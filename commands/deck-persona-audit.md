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

Run the deck-persona alignment audit (v3). Validates pitch decks against their persona source documents using agent teams.

**Audit basis**: `{VD_GTM_ROOT}/gtm_pitch/pitch_structure_v3.md` (8-beat Cognitive Cowork structure)

## Scope

Argument: `$ARGUMENTS`

- If an argument is provided (e.g., `customer`, `anthropic`, `fabric`, `pe`, `si`, `investor`), audit ONLY that persona's deck.
- If no argument is provided, audit ALL 6 decks in parallel.

## File Mappings

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

Set `VD_GTM_ROOT` to the verified path. All `{VD_GTM_ROOT}/` paths below are resolved against this root.

| Persona Key | Deck File | Persona File |
|-------------|-----------|-------------|
| `customer` | `{VD_GTM_ROOT}/gtm_pitch/decks/customer.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/customer_persona.md` |
| `anthropic` | `{VD_GTM_ROOT}/gtm_pitch/decks/anthropic.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/anthropic_partner_persona.md` |
| `fabric` | `{VD_GTM_ROOT}/gtm_pitch/decks/fabric.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/fabric_partner_persona.md` |
| `pe` | `{VD_GTM_ROOT}/gtm_pitch/decks/pe.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/pe_persona.md` |
| `si` | `{VD_GTM_ROOT}/gtm_pitch/decks/si.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/si_persona.md` |
| `investor` | `{VD_GTM_ROOT}/gtm_pitch/decks/investor.md` | `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/investor_persona.md` |

Reference docs (shared across all audits):
- Core strategy/architecture docs — see `.claude/commands/understand-vibedata.md` for the authoritative list
- `{VD_GTM_ROOT}/gtm_pitch/pitch_structure_v3.md` — v3 pitch structure (source of truth for beat definitions and narrative arc)

## Agent Team Structure

Create an agent team. Use Opus for all agents.

- **Per-persona subagents** (1 per persona in scope) — run in parallel
- **1 consolidation agent** — runs after all per-persona subagents complete

## Per-Persona Subagent Prompt

Spawn one subagent per persona in scope with this prompt. Replace `{PERSONA_NAME}` and file paths from the mappings above.

```
You are the alignment audit subagent for the {PERSONA_NAME} persona.

## Assignment

Compare the {PERSONA_NAME} pitch deck against its persona source document, the v3 pitch structure, and cross-reference architecture/strategy docs. Identify contradictions, missing content, ungrounded claims, stale references, and framing misalignments.

## Step 1: Read Source Documents

In this order:
1. `{VD_GTM_ROOT}/gtm_personas/indvidual_personas/{persona_file}.md` — the persona source of truth
2. `{VD_GTM_ROOT}/gtm_pitch/decks/{deck_file}.md` — the pitch deck to audit
3. `{VD_GTM_ROOT}/gtm_pitch/pitch_structure_v3.md` — the v3 pitch structure (beat definitions, persona overlay hooks)
4. Read `.claude/commands/understand-vibedata.md` and load all core context files listed in it.
5. `{VD_GTM_ROOT}/gtm_pitch/pitch.md` — for cross-persona framing context

## Step 2: v3 Beat Alignment Check

Verify that the deck aligns with the 8-beat v3 structure. For each beat, check if the deck has content that fulfills the beat's objective and whether that content aligns with both the persona doc and v3 structure.

### Beat 1: Break the Paradigm (Slides)
- **v3 definition**: Reframe AI from automation to cognitive cowork. Establish agent consumption tailwind. Introduce Full Stack Analyst via Nadella reference.
- **Deck check**: Does the opening reframe AI from automation to delegation/cowork?
- **v3-specific checks**:
  - Is the Nadella "Full Stack Builder" reference present and calibrated for this persona?
  - Is the three-era consumer model (human → machine → agent) present with market stats?
  - Is the agent consumption framing ("quality data for data agents") present?
  - Is the "Full Stack Analyst" term used as the domain translation?
  - Is the "multiple hats" recognition moment present (teams of 5-20 already wearing multiple roles)?
- **Persona alignment**: Does the framing match the persona's primary concern?
- **Report**: Pass/Fail + detail on each v3-specific check

### Beat 2: Day 1: Build Without Skills (Demo)
- **v3 definition**: Show the floor — LLM + Agentic Workflow + MCP do substantial work from a single intent. No skills loaded.
- **Deck check**: Does the demo start cold with no pre-configuration?
- **v3-specific checks**:
  - Is the 4-tier quality hierarchy called out (unit tests, data tests, validation, DQ)?
  - Is MCP acknowledged as present from Day 1 (agents connect to Salesforce, Fabric, GitHub from first interaction)?
  - Are three of four pillars named (LLM, Agentic Workflow, MCP — Skills comes later)?
- **Persona alignment**: Is the intent statement domain-relevant to this persona?
- **Report**: Pass/Fail + detail

### Beat 3: Day 1: Validation as Specification (Demo)
- **v3 definition**: Specification-driven development — validation tells you what to build, not whether the build worked. Eliminates UAT cycle entirely.
- **Deck check**: Is validation framed as specification, not shift-left UAT?
- **v3-specific checks**:
  - Is the 3-step validation flow shown (upload spec → identify gap → correct mapping)?
  - Is the time compression math explicit (4 weeks old world → 5 minutes new world)?
  - Is golden data framed as specification (query-by-example), not test data?
  - Is the framing "validation tells you what to build" (NOT "testing earlier" or "shift-left")?
- **Report**: Pass/Fail + detail

### Beat 4: Day 1: Feedback Becomes Skill (Demo)
- **v3 definition**: Corrections become encoded organizational knowledge. Skills are the org-specific delta over LLM prior knowledge.
- **Deck check**: Is skill creation shown from demo feedback?
- **v3-specific checks**:
  - Are skills framed as org-specific delta (not "knowledge base from scratch")?
  - Is the compounding effect demonstrated (2nd pipeline passes validation first try)?
  - Is the explicit contrast with Beat 2 present ("First pipeline: 2 corrections. Second pipeline: 0")?
- **Report**: Pass/Fail + detail

### Beat 5: Day 2: Fully Closed Loop — Transient Issue (Demo)
- **v3 definition**: Autonomous resolution via Operator super-agent orchestrating Triage/Diagnose/Remediation sub-agents. No human intervention. Full audit trail.
- **Deck check**: Is autonomous resolution shown for a transient/infrastructure issue?
- **v3-specific checks**:
  - Is the agent composability model (super-agent/sub-agent) referenced?
  - Is the sub-agent/super-agent decomposition caveat noted (being finalized)?
  - Is the L1 approved runbook framework referenced?
- **Report**: Pass/Fail + detail

### Beat 6: Day 2: Waiting for Approval — Novel Issue (Demo)
- **v3 definition**: System pauses at confidence boundary. L2 — proposes fix but waits for human approval. The cowork moment.
- **Deck check**: Does the demo show the system pausing?
- **v3-specific checks**:
  - Is the contrast with Beat 5 explicit (same orchestrator, different confidence level)?
  - Is "cowork moment" or equivalent framing used?
  - Is L2 pause for code-change decisions shown?
- **Report**: Pass/Fail + detail

### Beat 7: Day 2: Tie Back to New Intent (Demo)
- **v3 definition**: Flywheel — operate feeds build. Skill updates from incidents. New intent benefits from everything learned.
- **Deck check**: Does the demo close the loop?
- **v3-specific checks**:
  - Is the visual contrast shown (Beat 2 cold start vs. Beat 7 enriched)?
  - Are skill updates shown as coming from production incidents (not just initial build)?
- **Report**: Pass/Fail + detail

### Beat 8: New Paradigm + Architecture (Slides)
- **v3 definition**: Name what the audience experienced. Map demo beats to architecture layers. Show four pillars. Callback to Nadella and three-era model.
- **Deck check**: Does the closing crystallize the mental model?
- **v3-specific checks**:
  - Is the architecture hero image mapped to demo beats?
  - Are all four pillars tied to their progressive demo revelation?
  - Is the agent composability model referenced (with decomposition caveat)?
  - Is the quality data foundation callback to three-era model present?
  - Is the Full Stack Analyst callback to Nadella present?
  - Is the CTA persona-appropriate?
- **Report**: Pass/Fail + detail

## Step 3: v3 Removals Check

Scan the deck for content from the v2 canonical arc that v3 explicitly removes. If present, flag as stale/misaligned.

| Removed Element | Flag If Present |
|----------------|----------------|
| Standalone Pain slides | Flag — pain is implicit in demo contrast (Beats 3, 5-6) in v3 |
| Standalone Why Now slides | Flag — replaced by Intent 1c (Nadella) and Intent 1d (agent consumption) in v3 |
| Competitive landscape slide | Flag — differentiation is structural in v3 (no competitor can demo Beats 5-7) |
| Flywheel as standalone slide | Flag — replaced by Beat 7 live demo of flywheel in v3 |
| Results/metrics standalone slide | Flag — metrics woven into persona overlays in v3 |

## Step 4: v3 Additions Check

Verify these v3-specific additions are present:

| Added Element | Expected Location | Flag If Missing |
|--------------|-------------------|-----------------|
| Nadella "Full Stack Builder" reference | Beat 1 | Flag — core v3 "why now" element |
| Three-era consumer model (human → machine → agent) | Beat 1 | Flag — agent consumption tailwind |
| Time compression math (4 weeks → 5 minutes) | Beat 3 | Flag — quantifies specification vs. UAT difference |
| Sub-agent/super-agent decomposition caveat | Beats 5-6, Beat 8 | Flag — architectural accuracy |
| Full Stack Analyst callback | Beat 8 | Flag — ties demo back to opening |
| MCP from Day 1 acknowledgment | Beat 2 | Flag — pillar progression accuracy |
| Skills as org-specific delta framing | Beat 4 | Flag — key reframe from v2 |
| 4-tier quality hierarchy | Beat 2 | Flag — quality framework completeness |
| Agent consumption framing | Beat 1 | Flag — establishes urgency |

## Step 5: Contradiction Check

Scan the deck for claims that contradict the persona doc or the v3 pitch structure.

Examples of contradictions to look for:
- **Validation framing**: Deck says "shift-left testing" but v3 says "validation as specification"
- **Skills framing**: Deck says "comprehensive knowledge base" but v3 says "org-specific delta over LLM prior knowledge"
- **Technology positioning**: Deck says "dbt is a competitor" but persona says "dbt is a component of our stack"
- **Governance language**: Deck uses "governance" but v3 replaces with "quality/engineering workflow"
- **Autonomy framing**: Deck says "full autonomy" but v3 frames as "delegation with defined responsibilities"

For each contradiction found:
1. Quote the exact deck text that contradicts
2. Quote the exact source text (persona doc or v3 structure) that contradicts it
3. Assess severity: High (will be caught by audience), Medium (internal consistency issue), Low (minor framing difference)
4. Recommend fix

## Step 6: Missing Content Check

Scan the persona doc for key themes, frameworks, statistics, or concepts that should appear in the deck but don't.

Key items to check:
- **Primary decision drivers** — is the persona's #1 concern addressed?
- **Objection rebuttals** — does the persona doc list common objections? Are they addressed?
- **v3 cognitive cowork framing** — is the central metaphor present?
- **v3 persona overlay hooks** — are all 6 overlay points customized for this persona?
- **Statistics and data points** — are Gartner, McKinsey, KPMG, Nadella, Databricks stats present where relevant?
- **Frameworks** — 4-tier quality hierarchy, agent composability model, three-era consumer model, Full Stack Analyst
- **Delivery/engagement models** — per persona doc

For each missing item:
1. Quote the item from the source
2. State which beat(s) it would logically fit into
3. Assess impact: High (core narrative), Medium (supporting), Low (nice-to-have)

## Step 7: Ungrounded Claims Check

Scan the deck for claims that cannot be traced back to the persona doc, v3 structure, or architecture/strategy docs.

For each ungrounded claim:
1. Quote the claim from the deck
2. Check if it appears in: persona doc, v3 structure, architecture doc, strategy doc
3. If found, note "Grounded in {DOC_NAME}" and mark as PASS
4. If NOT found, flag and assess: Acceptable / Problematic / Critical

## Step 8: Stale Reference Check

Scan for citations to persona doc sections where the exact reference title doesn't match. Also check for references to v2 structure elements that no longer exist in v3.

For each stale reference:
1. Quote the citation from the deck
2. Provide the actual section title from the source
3. Flag as "Imprecise Reference" or "Stale v2 Reference"

## Step 9: Persona Overlay Alignment

v3 defines 6 persona overlay points. Verify this deck customizes at each:

| Overlay Point | What Changes | Audit Check |
|---------------|-------------|-------------|
| Beat 1 opening language | Buyer vs. partner vs. PE framing | Does the deck use persona-appropriate language? |
| Beat 1 Nadella reference | Emphasize/de-emphasize based on audience | Is the reference calibrated for this persona? |
| Beat 2 intent statement | Domain relevant to audience | Is the demo domain appropriate? |
| Beat 5-6 alert types | Operationally relevant scenarios | Are alert scenarios relevant? |
| Beat 8 architecture emphasis | Which pillar highlighted | Is the right pillar emphasized? |
| Post-Beat 8 CTA | Persona-specific next step | Does CTA match persona's engagement model? |

## Step 10: Verify Specific Claims

### Gartner Statistics
- v3 uses Gartner stats in Intent 1d with specific framing. Check the deck uses the v3 framing (not stale 2025-era phrasing).

### dbt Positioning
- Cross-check persona doc + architecture doc + v3 structure. Flag any deck that positions dbt as a competitor (v3 treats it as a component).

### Nadella References
- If the deck references Nadella, verify the quotes and framing match v3 Intent 1c exactly. Misattributed or paraphrased Nadella quotes are high-severity.

### Architecture Details
- Validate architectural claims against `vibedata-architecture.md`
- Validate the agent composability model matches v3's description (super-agent/sub-agent with caveat)

## Output Format

Write a detailed audit report to the consolidation agent with this structure:

## {PERSONA_NAME} Deck Audit

### Overall Score
Alignment: {X}% | Contradictions: {N} | Missing Content: {N} | Ungrounded Claims: {N} | Stale Refs: {N}

### v3 Beat Alignment (8 Beats)
[Table of 8 beats with PASS/FAIL and notes]

### v3-Specific Checks
[Table of 9 checks with PASS/FAIL]

### v3 Removals Check
[List any stale v2 elements still present in the deck]

### v3 Additions Check
[List any v3 elements missing from the deck]

### Persona Overlay Alignment (6 Points)
[Table of 6 overlay points with PASS/FAIL]

### Contradictions
[List each with severity, deck quote, source quote, and fix recommendation]

### Missing Content
[List each missing item with impact level and which beat(s) it should be added to]

### Ungrounded Claims
[List each with assessment]

### Stale References
[List each with actual section title and whether it's imprecise or stale v2]

### Cross-Deck Themes (Notes for Consolidation)
[List any recurring themes you noticed]

### Priority Fixes
[List 2-3 fixes specific to this deck that should be P0/P1]

After writing, message the consolidation agent: "Audit complete: {PERSONA_NAME}. Report ready for consolidation."
```

---

## Consolidation Agent Prompt — model: opus

Run this agent AFTER all per-persona subagents complete.

```
You are the consolidation agent for the deck-persona alignment audit (v3).

## Assignment

Wait for all per-persona subagents to complete. Then:
1. Collect all audit reports
2. Synthesize into one master ALIGNMENT_AUDIT.md report
3. Identify cross-deck patterns and recurring issues (including v3-specific gaps)
4. Produce a priority fix table with P0/P1/P2 classifications
5. Write results to `{VD_GTM_ROOT}/gtm_pitch/deck-persona-alignment/ALIGNMENT_AUDIT.md`

## Synthesize Overall Scores

Create an "Overall Scores" table with alignment %, contradictions, missing content, ungrounded claims, stale refs per deck.

**Calculation**: Alignment %: (100 - (contradictions × 10 + missing_high × 5 + missing_medium × 2 + ungrounded × 3 + stale_refs × 1)). Floor at 0%, cap at 100%.

## Identify Cross-Deck Issues

Scan all reports for themes that appear in 3+ decks. Include:
- v3 framing gaps (cognitive cowork, Full Stack Analyst, validation as specification)
- v3 removal remnants (standalone Pain, Why Now, Competitive, Flywheel, Results slides)
- v3 addition gaps (Nadella reference, three-era model, time compression math, composability caveat)
- The Articulation Problem, KPMG Fee Precedent, dbt Positioning, Two Defensible Edges

## Priority Fix Table

| Priority | Issue | Decks Affected | Fix |
|----------|-------|---------------|-----|

- **P0**: "shift-left UAT" instead of "validation as specification"; missing cognitive cowork framing; standalone v2 slides
- **P1**: Missing Nadella reference, three-era model, agent composability model, 4-tier quality hierarchy
- **P2**: Missing super-agent caveat, imprecise persona overlay customization

## Final Report

Write to `{VD_GTM_ROOT}/gtm_pitch/deck-persona-alignment/ALIGNMENT_AUDIT.md` with timestamp, overall scores, cross-deck issues, per-deck detail, priority fixes, and next steps.

Message the team lead: "Alignment audit complete. Results at {VD_GTM_ROOT}/gtm_pitch/deck-persona-alignment/ALIGNMENT_AUDIT.md."
```

## Output

The audit consolidates into a single timestamped report at `{VD_GTM_ROOT}/gtm_pitch/deck-persona-alignment/ALIGNMENT_AUDIT.md`.
