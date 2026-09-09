---
name: taking-vibedata-to-world
description: >-
  Use when the user provides a website or opportunity for VibeData involving
  branding, accelerators, startup programs, competitions, partners, investors,
  grants, or funded customer projects, or asks to take VibeData to the world.
---

# Taking VibeData to World

Turn an opportunity URL into a sourced fit assessment and a small, actionable
Linear issue set. Research first; challenge poor fit; show complete drafts for
one approval before any Linear writes. Stop at research, preparation, and issues.
Application submission and outreach belong to a separate task.

## 1. Establish context and route

Read the live parent issues, the matching example, and existing related issues
through Linear. Check comments and relations when they affect scope or readiness.

| Primary route | Parent | Issue structure |
|---|---|---|
| Branding, accelerator/startup program, competition, strategic partner | [GTM-134](https://linear.app/acceleratedata/issue/GTM-134) | [GTM-114](https://linear.app/acceleratedata/issue/GTM-114) |
| Direct investment, government funding/qualification, funded customer opportunity | [GTM-135](https://linear.app/acceleratedata/issue/GTM-135) | [GTM-117](https://linear.app/acceleratedata/issue/GTM-117) |

An accelerator offering investment still belongs under GTM-134. Assess genuinely
separate routes on one website separately; one application gets one submission
issue. Explain ambiguous routing in the preview; ask only if the ambiguity matters.

**Required context skill:** use `understanding-vibedata`
([local source](../understanding-vibedata/SKILL.md)). Follow its source map,
freshness checks, and authority rules. Ground positioning and eligibility claims
in current sources. Product plans do not prove shipped capability; prior grant
applications do not prove current company eligibility. Ask for a missing company
fact only when available sources cannot answer it and it can change the decision.

## 2. Research the opportunity and form

Read the supplied URL, official program/eligibility pages, terms, FAQ, application
link, and relevant form steps. Use `read-website-fast` for known URLs and Exa first
for discovery. If a preferred tool is unavailable or insufficient, state the
limitation and use the next applicable approved route. Use an available browser
for public dynamic forms that text extraction cannot reveal. Follow applicable
Microsoft, OpenAI, and third-party documentation routing when those topics arise.

Capture the current program cycle, application status, deadline with time zone,
eligibility, geography, fees/equity/funding terms, time/relocation commitments,
selection process, and likely benefit. Distinguish funding for Accelerate Data
from support assessed separately for each customer project. Check contrary
evidence, not just the organizer's marketing. Cite primary sources for eligibility
and terms; treat search snippets and old issue text as discovery leads.

Record **observed** form questions, required/optional flags, choices, character or
word limits, uploads and file limits, and declarations. Identify which steps were
inspected and which remain inaccessible. Separate observed requirements from
recommended preparation. Use the inventory format in the
[issue guide](references/issue-guide.md).

Inspect without submitting data. Account creation, login, entering information,
uploads, or acceptance of terms to reveal later pages require an access handoff;
report the exact obstacle and request help. Never invent company details or
hidden questions. A noncritical access gap can remain explicit in the draft;
an unknown that prevents qualification requires clarification first. An actual
authentication failure is a hard stop: report the failing integration and its
verified login/refresh step. Do not retry or switch sources after an auth failure;
if the recovery step is unavailable, state that rather than guessing a command.

## 3. Decide whether to pursue

Give a recommendation with evidence and unresolved conditions. Assess eligibility,
strategic relevance, likely benefit, economics, founder effort, timing, and
commitments. Use known user constraints; invent no spending, equity, relocation,
or geography thresholds. Prestige alone does not justify applying.

- **Pursue:** evidence supports eligibility and value.
- **Conditional:** promising, but named facts or preparation must be resolved.
- **Later:** a specific future trigger could make the route suitable.
- **Reject:** ineligible or poor strategic fit; explain which and why. Create no
  issue unless the user explicitly overrides this recommendation. Preserve the
  factual mismatch if they do. Do not restructure the company merely to fit a grant.

## 4. Keep the issue set small

Search existing issues by organization, URL/domain, program, cycle, and deliverable;
check completed work and follow pagination. Reuse existing prerequisites and
propose updates to matching opportunities. Never reopen a completed application
automatically. A new cycle warrants a new issue only if it needs a new application.

**Default: one submission issue plus one consolidated prerequisite issue when
prerequisite work exists.** Put the preparation tasks in that issue's checklist.
Create zero prerequisite issues if none are needed. Split only clearly separate
blockers with independently meaningful completion conditions, such as external
certification versus preparation of the application pack. Explain each split in
the approval preview. A long form, many uploads, or twelve missing facts do not
justify twelve dependent issues.

New prerequisites and the submission are **direct children of the same category
parent**. Add actual Linear `blocks` / `blockedBy` relations, not just prose links.
Reuse a shared prerequisite in place, even under another parent; do not duplicate
or reparent it. Future conditions such as meaningful revenue stay explicit
triggers unless a concrete task to achieve them has been agreed.

## 5. Draft the complete set for one approval

Use the [issue guide](references/issue-guide.md) for category-specific bodies and
the consolidated prerequisite. Default to research, discovered requirements,
positioning, and preparation checklists. Draft full application answers only when
requested, using sourced facts and explicit gaps.

| Field for every new issue | Default |
|---|---|
| Team | GTM; resolve live |
| Assignee | `ss` — resolve `ss@acceleratedata.ai`, including all prerequisites |
| Parent / project | Selected category parent / its current project; set both explicitly |
| Status | Todo when actionable; Backlog when blocked or waiting for a trigger |
| Priority | Medium (3); explain any proposed higher priority |
| Due date | Only a verified external deadline applicable to that issue; retain exact time/zone in its body |
| Cycle / milestone / labels | Unset unless specified |

These GTM defaults are agreed; do not import engineering issue requirements for
User Flow labels, specs, cycles, or milestones. Do not copy a submission deadline
to each prerequisite or invent internal target dates. Preserve existing issue
metadata unless the preview explicitly proposes a change.

Show the fit verdict and evidence, then the complete issue titles/bodies, resolved
metadata, create-versus-update actions, dependency graph, and total issue count.
Include missing facts and any reasons for extra blockers. Ask once for approval
of that exact set. Resolve routine details autonomously; carry forward approval
already given for the same concrete set. Material changes need an updated preview.

## 6. Write and verify

After approval, recheck for duplicates and changed target issues. Create approved
prerequisites first, then submissions, using returned IDs for parents and actual
blocking relations. Apply only approved updates; preserve unrelated description
content, metadata, and relations. Use real Markdown newlines.

Read back every affected issue with relations and verify body, assignee, project,
parent, status, priority, dates, and dependency direction. An uncertain write or
timeout requires reconciliation by reading before any retry; do not blindly
repeat a create. On a partial failure, report successful issue URLs and the exact
remaining work. Authentication failures follow the hard stop above.

Finish with the verdict, created/updated/reused issue links, verified dependencies,
and next action. Do not claim an application was submitted or an outcome achieved
from issue creation alone.
