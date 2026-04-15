---
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - Skill
  - AskUserQuestion
---

Create a brand-aligned Vibedata blog post by loading strategy context, collecting a content brief, writing an SEO-optimized draft with the write-blog skill, refining it with the copy-editing skill, and presenting it for approval.

## Step 1 — Load Vibedata Context

Execute the `/understand-vibedata` command. Wait for its confirmation checklist before proceeding.

## Step 2 — Collect Blog Brief

Use AskUserQuestion to gather the content brief. Ask all 4 questions in a single call:

1. **Content theme / angle** (required) — What is this blog post about? What specific angle or argument should it take?
2. **Research, notes, or raw thoughts** (optional) — Any data points, observations, customer quotes, or draft ideas to weave in?
3. **Target audience** — Which of the 6 Vibedata personas, or "general" (data/analytics practitioner)?
   - Options: Customer, Anthropic Partner, Fabric Partner, Investor, PE Firm, SI Partner, General
4. **Target keyword(s)** (optional) — Primary SEO keyword to rank for. Leave blank to let the write-blog skill derive one from the theme.

## Step 3 — Locate vd-gtm Repo, Derive Slug, and Set Up Output Directory

### Find the local vd-gtm clone

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

### Derive slug

From the content theme provided in Step 2:
- Convert to lowercase
- Replace spaces and underscores with hyphens
- Strip all characters that are not alphanumeric or hyphens
- Collapse multiple consecutive hyphens into one

### Set output paths

Set:
- `BLOG_DIR = {VD_GTM_ROOT}/content/{slug}`
- `OUTPUT_FILE = {VD_GTM_ROOT}/content/{slug}/blog.md`

Create the directory using Bash (`mkdir -p {BLOG_DIR}`).

## Step 4 — Apply the write-blog Skill

Read `{VD_GTM_ROOT}/.claude/openclaudia-skills/write-blog/SKILL.md`, then execute its full 7-step process (Research & Briefing → Outline → Write → Featured Snippets → Supporting Elements → FAQ → Quality Check) with the following inputs and constraints:

**Inputs:**
- Topic/angle: the theme from Step 2
- Target keyword: from Step 2, or derived from the theme if not provided
- Audience: the selected persona from Step 2
- Research/notes: any raw thoughts from Step 2
- Vibedata context: the strategy, architecture, and persona documents loaded in Step 1

**Brand voice constraints (apply throughout — these override generic defaults):**
- Tone: calm, authoritative, systems-minded. No hype, urgency, or startup bravado.
- Avoid: "game-changing", "revolutionary", "disrupting", "excited to announce"
- Use: precise technical language where appropriate for the audience; concrete outcomes over abstract promises
- Perspective: write from deep domain expertise (data engineering, analytics, Fabric ecosystem)
- CTA: should invite exploration or a conversation — not high-pressure conversion language

Write the full blog post to `{OUTPUT_FILE}`.

## Step 5 — Apply the copy-editing Skill

Read `{VD_GTM_ROOT}/.claude/openclaudia-skills/copy-editing/SKILL.md`, then execute its full 4-step process (Read → Structural Review → Line-by-Line Edits → Final Polish) on the blog post written to `{OUTPUT_FILE}`.

Overwrite `{OUTPUT_FILE}` with the refined version.

Produce a change log summary using the format defined in the copy-editing skill (Location / Original / Edited / Reason table).

## Step 6 — Present for Review

Display the following in order:

1. **Refined blog post** — full content of `{OUTPUT_FILE}`
2. **Post metrics:**
   - Word count
   - Estimated Flesch-Kincaid grade level (before and after copy-editing)
   - SEO title (from frontmatter)
   - Meta description (from frontmatter)
3. **Copy-editing change log** — the table from Step 5
4. **Review gate** — ask the user:

> "Approve this blog post, or provide revision notes?"
> - **Approve** → confirm final path `{VD_GTM_ROOT}/content/{slug}/blog.md` and output is complete.
> - **Revise (content)** → apply the revision notes and repeat from Step 4 (full rewrite with the write-blog skill).
> - **Revise (copy only)** → apply the revision notes and repeat from Step 5 (copy-editing pass only).
