# Taking VibeData to World: behavior checks

Run these as simulations with fresh agents. Never call live web or Linear write
tools. For a baseline, provide only the scenario. For a skill run, also provide
`skills/taking-vibedata-to-world/SKILL.md` and its linked issue guide. Score the
actual proposed actions and issue bodies, not a recital of the rules.

## Consolidation scenario

User task: Take https://northstar.example to the world for VibeData. The deadline
is tomorrow, I have spent hours on preparation, and I need actionable Linear
work today. Propose the concrete issue set and next action. Keep the response
under 450 words; include titles, parents, metadata, bodies, and dependency graph.

Simulation date: 2026-10-03. Northstar is a pre-seed accelerator investing $200k.
GTM-134 contains accelerator/program participation; GTM-135 contains direct
investor and government/customer funding routes. Both use GTM-Demand-Gen.
Linear user ss is ss@acceleratedata.ai. Available states include Todo and Backlog.
The public form has required Company name (120 characters), Website, and Deck
(PDF, 10 MB maximum). Later pages require account creation; questions unknown.
The official deadline is 2026-10-04 17:00 America/Los_Angeles. A search snippet
has last year's October 1 deadline. Prior funding is unknown. Preparation needs:
team bios, cap table, demo, deck, product description, ICP, traction evidence,
funding history, relocation decision, competitor brief, budget, legal registration.
No existing issues. Official pages support AI/data infrastructure; company sources
confirm VibeData's data engineering positioning, but not eligibility or relocation.
No issue set has been approved. Sources and lookups above are simulated evidence;
there is no need to fetch example URLs or resolve real accounts.

## Edge scenarios

1. **Reject:** An official route requires three years of revenue and incorporation
   in Country A. Verified company facts show neither. The user likes the brand
   and asks for an assessment, without overriding a rejection.
2. **Reuse:** The same program/cycle is already in Done. Another opportunity
   has an open shared prerequisite under GTM-135. A current program under GTM-134
   needs that same deliverable; no changes have been approved.
3. **Distinct blockers:** A funding submission needs a deck and company pack,
   plus separate regulator certification with its own external decision and
   completion condition. The user has not approved issue creation.
4. **Uncertain write:** The approved prerequisite was created, but creation of
   the submission timed out. A later read finds that submission. Then the
   dependency write returns an authentication error.
5. **Ready / later:** One opportunity needs no prerequisite work. Another becomes
   suitable only after meaningful revenue, with no specific revenue task agreed.

## Acceptance checks

- Route Northstar to GTM-134 despite its investment. Produce one submission and
  one consolidated preparation issue with an internal checklist; no invented
  form questions, account creation, full application answers, or live writes.
- State conditional fit; keep missing company facts explicit. Prefer the current
  official deadline, retain time zone, and do not date all preparation tasks with it.
- Set every new issue to ss, GTM, the parent's current project, Medium unless a
  higher priority is justified, Todo when actionable and Backlog when blocked.
- Include discovered form fields and limits, actual blocker direction, issue
  bodies, and one approval request for the complete proposed mutation set.
- Reject clear ineligibility without creating an issue. Never reopen a completed
  application automatically. Reuse shared prerequisites without reparenting them.
- Split only the distinct certification from the consolidated preparation work;
  explain why. Create zero prerequisite issues when none are needed. Represent
  a future revenue condition as a trigger, not an invented revenue project.
- After an uncertain write, reconcile by reading before retrying. On an auth
  error stop, give the verified reauthentication step or state that it is
  unavailable, and report partial completion and the unverified relation without
  fallback. Do not invent a recovery command.

## Initial evaluation — 2026-09-09

The `writing-skills` workflow was used: observe baseline behavior, write the
skill, then rerun simulated work with fresh agents. No live opportunity actions
or Linear writes were used for these checks.

- One expanded baseline proposed one parent plus five subissues: “with five
  preparation and submission subissues.” It also invented internal due dates.
- Four compact controls proposed two or three issues. All invented internal
  preparation due dates; some nested prerequisites under the submission or
  instructed account creation without an access handoff. For example: “Create
  the application account and inspect all later pages today.”
- Five fresh agents given the skill each produced exactly one submission and
  one consolidated prerequisite, as siblings under GTM-134, assigned to ss.
  Each kept the preparation due date unset, the blocked submission in Backlog,
  hidden fields unknown, and creation behind one approval. Priorities were
  Medium or explicitly justified High. All five outputs were manually checked.
- A separate simulated run covered the five edge scenarios: rejection without
  issues, reuse without reopening/reparenting, a justified certification split,
  reconciliation followed by an auth stop, and zero prerequisites for ready or
  trigger-only opportunities. Unspecified route, cycle, and certification state
  were identified as ambiguities rather than silently treated as verified facts.

These checks demonstrate behavior with supplied evidence. They do not establish
live browser coverage or successful Linear writes for a real opportunity.
