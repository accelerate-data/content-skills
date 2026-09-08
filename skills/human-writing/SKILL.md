---
name: human-writing
description: |
  Use when writing new prose from a brief, an outline, or nothing: blog posts,
  LinkedIn and social copy, newsletters, launch notes, vision and technical
  posts, landing-page and email copy. Covers voice, structure, and per-surface
  format before a first draft exists. For text that is already written and needs
  AI tells stripped out, use the humanizer skill instead.
---

# Human Writing

Write so the AI tells never appear. This skill is for drafting. To strip tells out of text that already exists, use the `humanizer` skill. It does remediation; this does prevention.

## Core principle

**Write like you are explaining something to a colleague who is good at their job, not presenting to a board.**

The reason AI prose is detectable is not any single word. A model predicts the next most probable token, so it produces text that is grammatically clean and statistically average: the same connectors, the same formality, the same hedges, paragraph after paragraph. The tell is the *cluster*, not the word. One "crucial" is nothing. Three of these in a paragraph is a rewrite.

## Steps

### 1. Draft for one reader

Name the reader before writing a sentence: their job, what they already know, what they will do differently after reading. Write to that person. Use the project's own vocabulary rather than invented synonyms; for Vibedata work the terms come from `vibedata-strategy.md` and `vibedata-architecture.md`.

### 2. Run the five-giveaway pass

Read the draft against *The five giveaways* below. Fix every hit.

### 3. Run the inventory pass

Search the draft for the words and phrases in *The banned inventory*. Each hit is either deleted or replaced with something concrete.

### 4. Run the structural pass

Word-level passes will not catch these, and they survive to publication unless you look for them on purpose. Count, do not eyeball:

- Em dashes and en dashes. Target is zero; rewrite each one out. If the piece has an established voice that already uses them, match that rate and never exceed it. Leave dashes inside code, commands, paths, and URLs alone. (The `humanizer` skill strips them outright, so a draft at zero survives that pass unchanged.)
- "Not X, but Y", "not just X, but Y", "X rather than Y". Target is zero. Rewrite as a plain assertion. This is the loudest structural tell in modern AI prose.
- Bolded phrases. Bold the term being defined, never the sentence you liked. Bold everywhere is bold nowhere.
- Groups of three. Any triad of adjectives, clauses, or examples: make it two or four. Real emphasis is uneven.
- Sentence openings. Two sentences in a row starting the same way ("This…", "It…", "The…"), or every bullet opening with the same word. Recast one.
- Sentence length. Read three consecutive sentences. If they are the same length and the same shape, break one. Watch stacked statistics especially. Three stat sentences in a row is the most common way this slips through.
- Heading echo. If the first line under a heading restates the heading, cut the line.
- Decoration. Title Case Headings, arrows (→) used as punctuation, horizontal rules between every section. Sentence case, plain words, rules only where a real break exists.
- Closing paragraph. If it summarises rather than lands somewhere, cut it.

### 5. Read it aloud

Any sentence that makes you stumble, or that sounds like a memo rather than a conversation, gets rewritten. This catches rhythm problems no word list will.

### 6. Revise by subtraction

First pass: get the ideas down. Second: cut 30%. Third: add specifics, taken only from the brief, the source material, or the user. Fourth: read aloud again.

**Never invent a fact, name, number, date, quote, or citation.** Specificity is the highest-value edit in this skill, which makes it the easiest place to start making things up. If a sentence needs a detail you do not have, ask for it or write the simpler sentence. An opinion or a reaction is yours to write; a factual claim is not.

**Done when** every claim has something concrete behind it, no sentence trips the inventory, the structural counts in Step 4 all come back clean, and you would send the whole thing to a colleague as-is.

## The five giveaways

| # | Giveaway | What it looks like | Write instead |
|---|---|---|---|
| 1 | **Too formal** | "In today's fast-paced digital landscape, we must leverage strategies." | "Here's a quick way to save time." Nobody talks like the first one. |
| 2 | **Punctuation theatre** | Emoji opening or closing every line; em dashes everywhere for drama | Default to zero em dashes. A full stop, comma, colon, or parentheses does the job. Emoji only where the platform expects them, never as bullet markers or headers. |
| 3 | **Long transitions** | "It is important to consider the following…" | Start the next sentence. Most transitions are deletable. Humans keep it short; models over-explain the join. |
| 4 | **Cringe words** | "empower", "unleash your potential", "supercharge" | Say the actual thing that happens. See the inventory below. |
| 5 | **No rhythm variation** | Every sentence the same length, the same shape | Vary it deliberately. A long sentence that carries a full thought, then a short one. Like that. If three sentences in a row land within a few words of each other, break one. |

Giveaway 5 is the one people miss. Word-level edits will not fix it, and it is the strongest structural signal in the list.

## The banned inventory

Each hit is a delete or a replace. Never a synonym swap: "utilise" for "utilize" fixes nothing.

Two kinds of list follow. **Diagnostic**: the AI vocabulary below is measurably over-represented in machine text, so a cluster is evidence. **Prescriptive**: the transitions, buzzwords, openers, and hype words are house style, weak writing whether a person or a model produced them. Do not treat a prescriptive hit as proof of AI authorship.

**Transitions to cut first.** These are the most common connectors in academic and business prose, which is exactly why models reach for them.

| Cut | Use |
|---|---|
| Moreover / Furthermore | Also, and, on top of that, what's more |
| Consequently / Therefore | So, which means, that's why |
| In addition | And, also, there's also |
| Subsequently | After that, then, next |
| Nevertheless | Still, even so, that said |
| It is worth noting that | Note that. Or just say the point |
| It is important to note that | Say the point directly |
| As previously mentioned | As we covered, earlier |

**Buzzwords.** Credible-sounding, content-free.

| Cut | Use |
|---|---|
| Leverage | Use, apply, build on |
| Utilize | Use |
| Facilitate | Help, allow, support |
| Implement | Start, roll out, put in place |
| Optimize | Improve, speed up, cut down on |
| Streamline | Simplify, speed up |
| Harness | Use, tap into |
| Robust | Strong, reliable, solid |
| Seamlessly | Works well, fits easily |
| Scalable | Grows with you |
| Empower / Unleash | Name what the person can now do |

**Openers.** These signal generated text before the reader reaches your point.

| Cut | Instead |
|---|---|
| In today's fast-paced world / In today's society | Start with the claim |
| In an ever-changing landscape | Name the thing that is changing |
| This post will discuss / This essay will | Start with the argument |
| It is evident that / There is no doubt that | State it |
| In conclusion / To sum up | End with the action, not a summary |
| At the end of the day | Delete. Nothing after it needs the runway |

**Hype words.** They add weight to a claim without evidence, so they subtract credibility.

Revolutionary, transformative, game-changing, groundbreaking, innovative, cutting-edge, remarkable, comprehensive, crucial, significant.

Replace each with the specific thing: what changed, by how much, measured how.

**Hedges.** Stock hedging templates used where a claim belongs.

It can be argued that · some might say · in many ways · to some extent · it seems that · one could say · generally speaking.

Either make the claim or cut the sentence. If you are hedging because you did not check, go check, then write what you found.

Ordinary qualifiers are a different thing. *Perhaps*, *tends to*, *usually*, *often* are human habits, not tells. Keep them where the meaning genuinely needs them. Keep scope statements, safety notices, and real corrections too. The tell is the stacked template, not the word.

**AI vocabulary.** Words measurably over-represented in post-2022 machine text. One is coincidence; a cluster is the strongest single tell there is.

*Current-era (these still signal):* emphasizing, enhance, highlighting, showcasing, underscore, align with, crucial, key, pivotal, robust, valuable.

*Older-era (mark text as early-model):* delve, boasts, bolstered, garner, intricate, intricacies, interplay, landscape (as an abstract noun), meticulous, tapestry, testament, enduring, vibrant, deep dive, additionally (opening a sentence), fostering.

Take this literally: a word being overused does **not** mean its synonyms are. Context matters too: "underscore" is fine when you mean the character or the film score.

**Dead phrases.** Each promises a payload and delivers none.

| Phrase | Why it fails |
|---|---|
| "That's not an X problem, that's a Y problem." | A false binary dressed as insight. Most problems are both. |
| "Here's what nobody talks about…" | Everybody talks about it. If nobody did, a model trained on the internet wouldn't know it. |
| "At the end of the day…" | A runway to nowhere. Nobody follows it with anything surprising. |
| "Let me be clear." | Announcing emphasis instead of being emphatic. |
| "Let's unpack that." | A stall. Announces depth, delivers none. |
| "It's not about X — it's about Y." | Pick any two nouns and the sentence writes itself. That's the problem. |
| "Here's the thing…" | Throat-clearing that promises a revelation and restates the point. |
| "Let that sink in." | Applauding your own sentence. A good insight doesn't need a hype man. |

## Judgement tells

Step 4 covers the shapes you can count. These need a reading instead, because no search will find them.

- **Undue significance.** Sentences inflating the subject's importance, legacy, or place in a "broader trend" with nothing behind the claim.
- **Vague attribution.** "Experts say", "critics argue", "many believe". Name who, or drop it. Never invent the source.
- **Vague connection.** "associated with", "linked to", "tied to". Stating that two things relate without saying how. Name the actual relationship. If you do not know it, keep the vague wording rather than inventing a specific one.
- **Superficial analysis.** An "-ing" clause tacked on that restates the fact while sounding like interpretation: "…, highlighting the importance of collaboration."
- **Section summaries.** "In summary…" closing each section. Delete every one.
- **Inline-header lists.** Every bullet shaped **Bold label:** plus a clause, all identical. Vary the shape or write it as prose.

## What human writing actually looks like

These read as human because models avoid them by default, reaching for a more "formal, neutral" register instead.

- **Plain copulatives.** "There is a", "it has a". Models route around these; people use them constantly.
- **Short verbs over stiff synonyms.** wrote (not authored), moved (not relocated), used (not utilized), tried (not attempted), died (not passed away).
- **Definite statements.** "was the first", "is the only", "one of the best". Models hedge these into mush.
- **The occasional wordy construction.** "as a result of", "in order to", "the fact that". Tighten most, but perfectly even tightness is its own tell.
- **Specifics that cost something to know.** A number, a named company, a date, an edge case, a thing that broke. This is the single highest-value edit available: "Query time dropped from 847ms to 12ms after adding the index" cannot be generated without knowing it.
- **Honest limits.** "This won't catch dynamic imports. You'll fix those by hand." Admitting a boundary buys more trust than any superlative.

## If an agent is drafting

Everything above applies, plus these, which only a model produces:

- No assistant residue. No "Certainly!", no "I hope this helps", no restating the brief back, no offering to revise. Ship the prose alone.
- No knowledge-cutoff language. "As of my last update", "I may not have the latest". If currency matters, go check. Otherwise write the sentence without the disclaimer.
- No citation artifacts. Stray reference markers, placeholder brackets, and leftover markup from a source are the most certain tell there is. Strip them.
- No plausible guesses in place of facts. See the rule in Step 6.

## Format by surface

The voice rules hold everywhere. These are the surface-specific constraints on top.

- **LinkedIn / social.** The feed truncates after roughly two lines, so the first sentence has to earn the click on its own. Never open with context or a windup. Short paragraphs, one idea each, blank line between. No hashtag stuffing; two or three at most, at the end. Links suppress reach, so put them in the first comment when it matters.
- **Blog / technical post.** Subheadings are scannable statements, not labels: "Why codemods stop at 70%" over "Background". A reader who only reads the subheadings should still get the argument.
- **Newsletter.** One idea per send. The subject line is a promise; the first paragraph pays it immediately.
- **Landing and email copy.** Every sentence either says what the thing does or what the reader gets. Cut anything that does neither.

Whatever the surface: end on an action the reader can take, not a summary of what they just read.

## Do not over-correct

These are **not** reliable tells. Stripping them makes writing worse, not more human.

- Perfect grammar. Plenty of people write clean prose.
- Formal or academic register, in itself. Only the specific words above correlate; "sounds fancy" does not.
- A transition word in isolation. The tell is density, not presence.
- Mixed casual and formal register. That is how technical people actually write.
- Long sentences. Length is fine. Uniform length is the problem.
- Ordinary qualifiers. *Perhaps*, *tends to*, *often*. Stock hedging templates are the tell, not every qualifier.

Do not introduce typos, filler, or fake informality to sound human. That reads as a different kind of fake.

## Self-check

1. Would a person say this out loud?
2. Does every claim have a number, name, or example behind it?
3. Could this sentence appear on any other company's blog? Then it says nothing.
4. Am I hedging because I did not check?
5. Can I delete this transition? Usually yes.
6. Does it open with enthusiasm instead of information?
7. Does it end on an action rather than a summary?
8. Did the Step 4 counts actually get run, or just skimmed? Run them.

## Sources

Distilled from Wikipedia's *Signs of AI writing*, published inventories of over-represented AI vocabulary, and the "AI phrase autopsy" catalogue of hollow thought-leadership phrases. Cross-check `humanizer` for the remediation-side treatment of the same patterns.
