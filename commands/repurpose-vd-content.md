---
allowed-tools:
  - Read
  - Write
  - Glob
  - Bash
  - Skill
  - AskUserQuestion
---

Repurpose existing Vibedata content into a new format by loading strategy context, reading the source content, applying the content-repurposing skill, refining the output with the copy-editing skill, and presenting for review.

## Step 1 — Load Vibedata Context

Execute the `/understand-vibedata` command. Wait for its confirmation checklist before proceeding.

## Step 2 — Collect Repurposing Brief

Use AskUserQuestion to gather the brief. Ask all 4 questions in a single call:

1. **Source content path** (required) — File path to the existing content to repurpose (e.g. `content/my-blog-post/blog.md`).
2. **Target format** (required) — What format should the repurposed content take?
   - Examples: Twitter/X thread, LinkedIn carousel, LinkedIn text post, newsletter section, video script (60-90s), quote cards, email
3. **Target audience** (optional) — Which of the 6 Vibedata personas, or "general"? Leave blank to inherit from the source content.
4. **Angle or emphasis** (optional) — Any specific angle, hook, or points to emphasise in the repurposed version?

## Step 3 — Locate vd-gtm Repository and Read Source Content

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

Set `VD_GTM_ROOT` to the verified path. If the source content path from Step 2 is a relative path, resolve it against `{VD_GTM_ROOT}`.

### Read Source Content

Read the file at the resolved path. Confirm the source content is loaded before proceeding.

## Step 4 — Apply the content-repurposing Skill

Read `{VD_GTM_ROOT}/.claude/openclaudia-skills/content-repurposing/SKILL.md`, then execute its workflow (Steps 1–4: Identify Source → Extract Core Elements → Map to Target Platform → Create Content) scoped to the single target format specified in Step 2.

**Inputs:**
- Source content: the file read in Step 3
- Target format/platform: from Step 2
- Audience: from Step 2, or inferred from source content
- Angle/emphasis: from Step 2 if provided
- Vibedata context: strategy, architecture, and persona documents loaded in Step 1

**Brand voice constraints (apply throughout — these override generic defaults):**
- Tone: calm, authoritative, systems-minded. No hype, urgency, or startup bravado.
- Avoid: "game-changing", "revolutionary", "disrupting", "excited to announce"
- Use: precise technical language appropriate to the platform and audience
- CTAs: invite exploration or a conversation — not high-pressure conversion language
- Platform adaptation: make the content feel native to the target platform, not a copy-paste

Derive the output filename from the target format (e.g. `linkedin-carousel.md`, `twitter-thread.md`, `newsletter-section.md`, `video-script.md`).

Write the repurposed content to `{source_dir}/{output_filename}` where `{source_dir}` is the directory containing the source file.

## Step 5 — Apply the copy-editing Skill

Read `{VD_GTM_ROOT}/.claude/openclaudia-skills/copy-editing/SKILL.md`, then execute its full 4-step process (Read → Structural Review → Line-by-Line Edits → Final Polish) on the repurposed content.

Overwrite the output file with the refined version.

Produce a change log summary using the format defined in the copy-editing skill (Location / Original / Edited / Reason table).

## Step 6 — Present for Review

Display the following in order:

1. **Refined repurposed content** — full content of the output file
2. **Output details:**
   - Output path
   - Format / platform
   - Estimated word count (or tweet/slide count for social formats)
   - Estimated Flesch-Kincaid grade level (before and after copy-editing)
3. **Copy-editing change log** — the table from Step 5
4. **Review gate** — ask the user:

> "Approve this repurposed content, or provide revision notes?"
> - **Approve** → confirm the final output path and output is complete.
> - **Revise (content)** → apply the revision notes and repeat from Step 4 (full repurposing pass).
> - **Revise (copy only)** → apply the revision notes and repeat from Step 5 (copy-editing pass only).
