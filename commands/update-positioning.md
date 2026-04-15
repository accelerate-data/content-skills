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

Update Vibedata positioning by propagating new strategic input through the strategy and architecture docs, with adversarial debate analysis, product-marketing validation, and human review gates at each phase.

Input: `$ARGUMENTS` — either inline text or a file path to read.

---

## Step 0: Parse Input

1. Examine `$ARGUMENTS`:
   - If it starts with `/`, `../`, `./`, `~`, or ends with `.md` or `.txt`, treat it as a **file path** and read the file contents. That content is the "new input."
   - Otherwise, treat `$ARGUMENTS` directly as the "new input" text.
2. Derive `{SHORT_SLUG}`: take the first ~4 meaningful words from the new input, lowercase, hyphenated (e.g., `shift-to-consumption-pricing`). This is used for branch names and filenames.
3. Set `{TODAY}` to today's date in `YYYY-MM-DD` format.

---

## Step 0b — Discover Repo Locations

Use `git rev-parse --show-toplevel` to get this repo's root. From its parent directory, locate sibling repos:
- **vd-specs-product-vision** (VISION_ROOT)
- **vd-specs-product-architecture** (ARCH_ROOT)

If a required sibling repo is not found, warn the user and halt.

---

## Step 1: Phase 1 — Strategy Update (with Debate)

### Step 1.1: Read

- The new input (resolved from Step 0)
- `{VISION_ROOT}/vibedata-strategy.md`
- All files in `{VISION_ROOT}/context/`
- All files in `{VISION_ROOT}/context/competition/`
- All files in `{VISION_ROOT}/context/personas/`

### Step 1.2: Debate Intake + Research Ingestion

Main agent performs inline (debate Phases 0–1):

1. **Auto-derive framing question** from the new input:
   "How should Vibedata's positioning evolve given {new input summary}?"

2. **Research docs**: `vibedata-strategy.md`, all `context/` files, and the new input.

3. **Reference cases**: Auto-derive 2+ from the `competition/` and `personas/` directories.
   Each reference case needs: Name, Context (1-2 sentences), Specifics.
   If fewer than 2 usable cases are found, ask user to provide additional cases via AskUserQuestion before proceeding.

4. **Build tension map** internally (do not output). Key disagreements, value tensions, evidence gaps, open questions.

### Step 1.3: Mandate Generation → HUMAN GATE 1

Read `.claude/skills/debating-it-out/references/position-discovery.md` for mandate generation guidance.

Generate 4 mandates (one per agent role) per debate Phase 2:

| Agent | Role |
|-------|------|
| **Maximalist** | Go all in on the positioning shift |
| **Purist** | Reject the shift / defend status quo |
| **Hybrid** | Adopt structurally, not substantively |
| **Economist** | ROI/resource arbiter |

Each mandate: 3-5 sentences specifying what position the agent defends, sub-questions to address, how to use reference cases, and what research arguments to engage.

Present all 4 mandates via AskUserQuestion:
- "Here are 4 debate angles. Approve / Edit / Flag overlaps?"

If the tension map doesn't support 4 genuinely distinct positions, say so and offer to reframe or drop to 3.

### Step 1.4: Round 1 — Position Papers

Read `.claude/skills/debating-it-out/references/position-paper-template.md` to construct agent prompts.

Create workspace: `./position-changes/{TODAY}-debate-workspace/round1/`

**Spawn 4 Task subagents in a single message** (parallel). Each gets:
- Research document file paths (agent reads them itself)
- Its mandate from Step 1.3
- All reference cases with full details
- Word limit: 2000
- Output path: `./position-changes/{TODAY}-debate-workspace/round1/position_{role}.md`
  where role is: maximalist, purist, hybrid, economist

After all 4 complete, verify all position papers exist and are non-empty.
If a subagent fails, retry once. If still fails, continue with remaining agents.

### Step 1.5: Thread Extraction → HUMAN GATE 2

Main agent reads all 4 position papers.

Extract 5-8 specific debate threads per debate Phase 4. A thread is a concrete disagreement, not a vague topic. Format:

```
Thread N: "[Short label]"
  - Maximalist says: [specific claim]
  - Purist says: [specific counterclaim]
  - Evidence status: [what would resolve this]
```

Present threads to user via AskUserQuestion (multi-select to deselect threads).
This gate prunes the debate to what the user actually cares about.

### Step 1.6: Round 2 — Rebuttals

Read `.claude/skills/debating-it-out/references/rebuttal-template.md` to construct agent prompts.

**Spawn 4 Task subagents in a single message** (parallel). Each gets:
- All 4 Round 1 position paper file paths
- Approved debate threads only (the ones user kept)
- Its original mandate
- Reference cases
- Word limit: 1500
- Output path: `./position-changes/{TODAY}-debate-workspace/round2/rebuttal_{role}.md`

After all 4 complete, verify all rebuttals exist.

### Step 1.7: Synthesis

Read `.claude/skills/debating-it-out/references/synthesis-template.md` for structure and rules.

Main agent performs debate Phase 6 inline. Read all 8 documents (4 positions + 4 rebuttals). Produce:

1. **Debate arc** — Where each agent started vs. ended
2. **Convergence map** — What all agents agreed on
3. **Residual disagreements** — What's unresolved, why
4. **Decision framework** — Economist's revised rubric + evidence from debate
5. **Reference case application** — Framework applied to each case
6. **Recommendations** — What to do fully, partially, avoid, or investigate further
7. **Prioritized action list**

**Anti-flattening rule**: For each recommendation, state which agents agree, which disagree, and what evidence would resolve the disagreement.

Write to `./position-changes/{TODAY}-debate-workspace/synthesis.md`.

### Step 1.8: Product-Marketing Validation

Spawn 1 Task subagent with this mandate:

> Read the synthesis at `./position-changes/{TODAY}-debate-workspace/synthesis.md` and the current strategy at `{VISION_ROOT}/vibedata-strategy.md`.
>
> Validate the proposed positioning changes against Dunford's 5 positioning elements:
> 1. **Competitive alternatives** — still correctly identified?
> 2. **Unique attributes** — strengthened or diluted?
> 3. **Value mapping** — "so what?" still clear for each attribute?
> 4. **Target customer** — still coherent or shifted?
> 5. **Market category** — framing still holds?
>
> For each element: state whether the proposed changes strengthen, weaken, or break coherence, with specific fixes where needed.
>
> Write your report to `./position-changes/{TODAY}-positioning-coherence-report.md`.
> Final response under 2000 characters. List outcomes, not process.

### Step 1.9: Strategy Recommendation

Main agent writes `./position-changes/{TODAY}-strategy-recommendations.md` combining:

- **Debate synthesis executive summary** — key findings from the 4-agent debate
- **Specific recommended changes** — each as add / modify / remove with rationale
- **Positioning coherence report findings** — which Dunford elements strengthen, weaken, or break
- **Downstream impact assessment** — what this means for architecture, personas, and marketing

### Step 1.10: HUMAN GATE 3 — Approve Strategy Changes

Present the strategy recommendation + coherence report findings via AskUserQuestion:
- Option 1: "Approve as-is" — proceed with all recommended changes
- Option 2: "Modify" — user provides feedback; revise recommendation only (do NOT re-run debate) and re-present
- Option 3: "Reject" — abort Phase 1 (and skip Phase 2); print a message and stop

### Step 1.11: Apply + PR

On approval:

1. Edit `{VISION_ROOT}/vibedata-strategy.md` with the approved changes.
2. Save the raw new input as `{VISION_ROOT}/context/{TODAY}-positioning-input-{SHORT_SLUG}.md` for provenance.

In the `{VISION_ROOT}/` repo, run:

```bash
git checkout -b positioning-update/{SHORT_SLUG}
git add vibedata-strategy.md context/
git commit -m "Positioning update: {SHORT_SLUG}"
git push -u origin positioning-update/{SHORT_SLUG}
```

Then create the PR:

```bash
gh pr create --title "Positioning update: {SHORT_SLUG}" --reviewer hbanerjee74,ukakkad --body "$(cat <<'EOF'
## Summary
{Debate synthesis executive summary}

## Changes
{List of specific changes applied}

## Positioning Coherence
{Summary of Dunford element assessment from coherence report}

## Downstream Impact
{Impact assessment from the report}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Print the PR URL before continuing to Phase 2.

---

## Step 2: Phase 2 — Architecture Update (no debate)

Proceed immediately after Phase 1 PR is created (optimistic flow — does not wait for merge).

### Read

- The now-updated `{VISION_ROOT}/vibedata-strategy.md` (local working copy with Phase 1 changes)
- `{ARCH_ROOT}/vibedata-architecture.md`
- All files in `{ARCH_ROOT}/context/`

### Analyze & Recommend

Identify architecture changes implied by the updated strategy. Write a recommendation report to:

```
./position-changes/{TODAY}-architecture-recommendations.md
```

Same report structure as Phase 1:
- Summary of strategy changes driving this update
- Specific recommended architecture changes (add / modify / remove) with rationale
- Downstream impact assessment

### Human Gate 4

Present recommendations via `AskUserQuestion` with the same three options (Approve / Modify / Reject).

If rejected, skip the apply and PR steps but still print the downstream reminder in Step 3.

### Apply

On approval:

1. Edit `{ARCH_ROOT}/vibedata-architecture.md` with the approved changes.
2. Save provenance: `{ARCH_ROOT}/context/{TODAY}-positioning-input-{SHORT_SLUG}.md`.

### PR

In the `{ARCH_ROOT}/` repo, run:

```bash
git checkout -b positioning-update/{SHORT_SLUG}
git add vibedata-architecture.md context/
git commit -m "Positioning update: {SHORT_SLUG}"
git push -u origin positioning-update/{SHORT_SLUG}
```

Then create the PR:

```bash
gh pr create --title "Positioning update: {SHORT_SLUG}" --reviewer hbanerjee74,ukakkad --body "$(cat <<'EOF'
## Summary
{Paste the recommendation summary section from the report}

## Changes
{List of specific changes applied}

## Downstream Impact
{Impact assessment from the report}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Print the PR URL.

---

## Step 3: Downstream Reminder

Print:

```
Positioning updates applied. To propagate downstream, run:
1. /update-personas
2. /update-marketing-strategy
3. /deck-persona-audit
```

---

## Rules

- Do NOT proceed past a Human Gate without explicit user approval.
- This command uses Task sub-agents for debate rounds (Steps 1.4, 1.6) and product-marketing validation (Step 1.8). Main agent orchestrates all other steps inline.
- Debate workspace: `./position-changes/{TODAY}-debate-workspace/`. All debate artifacts stay there.
- Reference cases auto-derived from `{VISION_ROOT}/context/competition/` and `{VISION_ROOT}/context/personas/`. If fewer than 2 usable cases, ask user before proceeding.
- Read debate reference templates from `.claude/skills/debating-it-out/references/` at the steps indicated.
- All recommendation reports go to `./position-changes/`. No exceptions.
- All git operations happen in the respective sibling repo directories (`{VISION_ROOT}/`, `{ARCH_ROOT}/`), not in this repo.
- Use the user's git identity (configured in their global CLAUDE.md) for commits.
- Be specific to Vibedata. Every recommended change must trace to something in the new input or existing source material.
- Flag genuine ambiguities in the source material explicitly rather than guessing.
