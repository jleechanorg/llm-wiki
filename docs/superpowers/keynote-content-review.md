# Develop at Idea Velocity — Original Deck + Proposed Enhancements

**Approach corrected:** enhance the original 17-slide deck in place, not replace it with a new structure. This file shows the ORIGINAL content (extracted from the live deck's actual rendered PDF, `1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0`) side by side with proposed changes. Nothing has been pushed to Google Slides yet — review this first.

## NEW OPENING STRUCTURE (your latest call — replaces the "cold open first" plan)

1. **Intro** — who you are, background at Google/Snap
2. **Snapchat projects** — the credibility slide (Snap Bridge, Snap Wings, Open Model Pilot)
3. **WorldAI intro + mom story** — combined: what WorldAI is, then the cold-open story (Mr. Park debt, the rage-quit the world wouldn't allow) as the illustration of it

### DRAFT — item 3 copy (WorldAI intro + mom story combined)

> **WorldAI — an AI Game Master that plays live.**
> Play any character, in any world — Game of Thrones, Star Wars, Baldur's Gate, or one you make up. The world reacts to what you actually do, not a script. It's a real product — worldarchitect.ai — not a tech demo.
>
> Here's what that means in practice. I was playing a campaign with my mom. Her character owed a local grocer, Mr. Park, for supplies on credit — a debt the world remembered, not a stat I'd written down. Mid-session, she tried to rage-quit in character: *"I'm an undocumented immigrant, I'm gonna go home."* Instead of fading to black, the world argued back, using consequences it had generated itself: *"The debt to Mr. Park doesn't vanish because you close the door... you're becoming a fugitive from a paper trail you can't outrun."* She couldn't quit. Twenty scenes later, we shook hands with Park on a 10% equity partnership. Nobody hand-coded a "player tries to quit" branch.

This is a first draft — trim/adjust freely. Structurally it does two things in one breath: orients the audience on what WorldAI even is, then lets the mom story land as proof rather than a cold non-sequitur.

Then continues into the original deck's slide 3 onward (verification gap → pivot, etc.) — original slide numbering below still refers to the ORIGINAL deck for content reference, but the actual running order now starts with these 3 new/reordered items before slide 3.

## Visual prototypes ready for review (Claude Design, not yet in Google Slides)
- ~~Slide 4 (Cognitive Tasks) funnel graphic~~ — **rejected**, replaced by the merged pyramid version below
- ~~Slide 6 (6-Step Loop) linear flow~~ — **rejected**, "doesn't add value." Replaced by the circular version below.
- **NEW — Pyramid + Cognitive Tasks, merged into one slide**: https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fproto-pyramid-cogtasks-merged.html — reuses the original pyramid's exact 4-column card style (Tier 1 Openclaw/Hermes → Tier 2 CMUX/AO → Tier 3 CLI Fleet → Tier 4 Subagents/MCP), each card re-captioned to also carry the cognitive-tasks thesis ("1 cognitive task" / "angle diversity" / "extended horizon" / "zero spam" pills), closing on the context-switch line. This replaces BOTH the old slide 4 and slide 8 with one slide.
- **NEW — Intro/bio slide**: https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fproto-intro-bio.html — name/title up top, 3 credibility cards (YouTube $70B+ paid to creators 2008-2018, Snap Growth Notifications 50M→5B+ 2018-2026, "3 internal AI projects shipped" teasing the Snapchat slide that follows)
- **NEW — 6-Step Loop, circular (Option B)**: https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fproto-slide06-circular.html — single-ring layout backed by `docs/superpowers/circular-loop-diagram-research.md`, alternating human/AI ownership around the ring (rust fill = AI-owned, outline = human-owned), horizontal labels anchored outside the ring, distinct dashed rust return-arc from step 6 back to step 1. Built as pure SVG (nodes, labels, and connectors all share one `viewBox` coordinate system) after an earlier HTML-div/SVG mix caused step 4 to render off-position; verified via screenshot, all 6 nodes and labels now land correctly.

**Live deck:** https://docs.google.com/presentation/d/1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0/edit — **restored to the original 17 slides** as of 2026-08-23 ~21:50 PT, after a background agent's Task 7 mistakenly deleted-and-rebuilt it into the 13-slide redesign despite an in-flight stop request (timing race — the rebuild had already completed before the stop message was processed). Restored via full-bleed image re-upload from this session's own PDF renders of the pre-incident state, verified slide-by-slide against the original (slides 1/9/17 spot-checked pixel-identical, including a pre-existing "14/14" footer bug on slide 17 that's baked into the original image and correctly preserved, not something to silently fix mid-restore). **Speaker notes from the true original were not recoverable this way** (never captured as text) — only available via Drive's native Version History UI if you want them back specifically.

Reference deck template (do not touch): https://docs.google.com/presentation/d/1JY7CmnE33b9_R1IhHyv0M-WYw-kdTJFEqskoR_PRqBc/edit — read-only exports only, no writes made.

---

## 01/17 · Title — KEEP AS-IS
> AI coding stack + WorldAI — Develop at idea velocity — a tour of the autonomous pipeline and the game I built with it.
> Jeffrey Lee-Chan · Head of Vibe Coding · Snapchat · ex-Google

No proposed change.

---

## 02/17 · The Verification Gap — KEEP THE TABLE, ADD REAL CITATIONS + EXPLANATION

**Your latest call:** keep the stat-table approach, but link real stats and explain more so it doesn't read as made-up numbers. Real primary sources found:

| # | Value | Label | Real source (verified primary, not a re-share) |
|---|---|---|---|
| 01 | 27.6% | of merged PRs are AI-authored (April 2026, up from <1% in Feb 2025) | Greptile, ["Rise of the Overnight Agents"](https://www.greptile.com/blog/rise-of-the-overnight-agents) — analysis across 65,000 orgs |
| 02 | 96% | of developers don't fully trust AI-generated code | Sonar, [State of Code Developer Survey](https://www.sonarsource.com/blog/state-of-code-developer-survey-report-the-current-reality-of-ai-coding/) — 1,100+ developers, published Jan 8, 2026 |
| 03 | 48% | of developers always verify AI output before committing | same Sonar survey |
| 04 | 65% | of code projected to be AI-generated by 2027 (42% today) | same Sonar survey |

**Explanation to add** (per your "explain it a bit more" ask): a one-line bridge under the table — e.g. *"27.6% of merged code is now AI-written and climbing fast (28x in 14 months). But trust hasn't caught up — most developers still don't fully believe the output is correct, and fewer than half actually check before committing."* Keep the existing bottom quote as the payoff line: *"The bottleneck is no longer generating code — it's proving correctness without human babysitting."*

---

## 03/17 · One Slack Message, All the Way to Green Checks — KEEP
5 phases: Natural Language → Context & Memory → Parallel Agents → CI & 7-Green Gate → Proof-First. No proposed change.

---

## 04/17 · Cognitive Tasks & Workspaces — MERGED INTO SLIDE 8 (see below)

**Your final call:** merge this with the agent pyramid slide (08/17) into one slide, reusing the pyramid's visual style. See the "Pyramid + Cognitive Tasks, merged" prototype above. This slide no longer exists standalone.

---

## 05/17 · Left-Shift and Right-Shift, Zero Human in the Middle — RESTORE (was cut in the redesign, going back in)
3 phases: Left-Shift Planning (front-load) → Zero Middle Human (execute) → Right-Shift Proof (back-load). Bottom: *"Goal: Reduce middle human intervention to zero with acceptable quality regression, and maximize output correctness."*

No content change proposed — just confirming this stays in.

---

## 06/17 · The 6-Step Loop — MAKE IT A GRAPHIC

**Original:** 6-card grid — Quick Planning → Async AI Drive → AI Evidence Review → Human Proof Check → AI Code Review → Human Merge.

**Your feedback:** "slide 6 - 6 step loop can be a graphic."

**Proposed:** Convert to a circular flow diagram with 6 numbered nodes and arrows, alternating AI-owned vs human-owned steps visually (color-coded: rust fill = AI, outline = human). Keep the exact 6 step names/descriptions, just change the visual treatment from 6 identical boxes to a ring. **Built and verified** — see the "6-Step Loop, circular (Option B)" prototype link above.

---

## 07/17 · Craftsmanship vs. Velocity — FIX A REAL BUG
**Found while re-auditing:** this slide's right-hand panel is a screenshot of a code editor that renders as garbled/illegible text — looks like a corrupted or over-compressed image, not a design choice. Needs a fresh screenshot or should be replaced with something else entirely. Text content (Domain 01: Low Consequence/Fast Fail, Core Tenets) is fine.

---

## 08/17 · The Agent Supervision Pyramid — MERGED WITH COGNITIVE TASKS (04/17)

**Your final call:** "we can combine agentic pyramid with cog tasks." Built as one slide — see the "Pyramid + Cognitive Tasks, merged" prototype linked above. Reuses the pyramid's exact 4-column card style and all 4 real tier facts, re-captioned per-card to also carry the cognitive-tasks thesis.

**Terminology audit complete (2026-08-23), 2 fixes applied:**
- Tier 1: "Openclaw / Hermes" (co-equal, "Slack, WhatsApp, SMS, email") → **"Hermes (Slack Bot)"** — Hermes is Slack-only (WhatsApp config confirmed present but empty/unwired); OpenClaw is the auxiliary HTTP API gateway underneath, not co-primary dispatch.
- Tier 3: dropped **"Google Antigravity"** from the CLI fleet list (`which antigravity` confirmed not in PATH — appears abandoned) — now reads "Claude Code, Codex, Cursor CLI."
- Tier 2 (CMUX & AO Daemon) and Tier 4 (Subagents & MCP): confirmed current, no changes.
- A third flagged item ("Dark Factory autonomous merge pipelines") doesn't appear anywhere in this prototype's copy — likely a stale phrase from the original live-deck slide 8 image, not something carried into this rebuild. No action needed here since the new copy never made that claim; flagging in case the original deck text resurfaces elsewhere.

---

## 09/17 · CMUX: Hands on the Keyboard, Hermes on Standby — KEEP FOR NOW

**Your call:** "lets just keep it for now." No change — deprioritized, revisit later if needed.

---

## 10/17 & 11/17 · Tokenmaxxing + Cache Stability — APPENDIX, NOT COMPELLING ENOUGH

**Your call:** "maybe just remove/appendix this ... it doesn't seem that compelling." Confirmed reasoning matches this session's own audit — the PR #7215/#8851 references are internal jargon meaningless to an audience with no repo access, and even reframed, the content isn't pulling weight. **Moved to appendix, out of the main flow.**

---

## 12/17 · Harnesses Decay — APPENDIX, CURRENT CONTENT IS LOW QUALITY

**Your call (updated):** "appendix for now, the info is low quality on slide atm." Original "40-90 Day Model Half-Life" claim is unsourced (zero backing found in the repo this session). Sourced replacement (19 model releases since June 2025 — one every 3 weeks) available if you want to swap it in later; for now this whole slide sits in the appendix as low-priority/needs-rework.

---

## 13/17 · What Broke in Production — APPENDIX FOR NOW
**Your call:** "lets appendix broken in prod for now." Content (89.6% watchdog stall, 251 babysit polls, 9h ceiling) is all verified accurate — just moved out of the main flow, available if there's time or a question calls for it.

---

## 14/17 · WorldAI: An AI Game Master That Plays Live — REPLACE WITH THE REAL STORY

**Original:** Product Vision card ("Play Any Character in Any World") + Scale & Stats card (12 specialized agents, 30+ prompt files, 300k token context, Min-First/Fill-to-Max, BYOK).

**Proposed:** Replace the generic pitch with the real, first-person story: playing a WorldAI campaign with your mom, the Mr. Park debt, the rage-quit the world wouldn't allow, the 10% equity partnership 20 scenes later. Keep the Scale & Stats card as a secondary panel, with the agent count corrected to the real number (11, confirmed via `mvp_site/agents.py` this session) instead of 12.

---

## 15/17 · Two Engines, One Gateway — FIX TWO NUMBERS
**Original:** FastEmbed Intent Gate (<50ms) / Casino-Grade Dice Audit ("1,549 lines, 4-signal verification") / God Mode & Dynamic Rules ("7,273 lines in world_logic.py orchestrator").

**Confirmed wrong this session:** dice audit is actually **1,889 lines** (not 1,549); world_logic.py is actually **12,378 lines** (not 7,273) — both verified via `wc -l` against the live repo. Straightforward fix, same layout.

---

## 16/17 · 8 Bets for the Next 30 Days — KEEP
Discipline Tickets / Commit Provenance / N-Green Gates / Headless by Default / Prefix Cache Audits / Self-Canceling Timers / Dark Factory Stages 3-6 / Harness Postmortems. No proposed change.

---

## 17/17 · Find Me, Play the Game — KEEP, MINOR BUG
LinkedIn / WorldAI (worldarchitect.ai) / Consensus ML / GitHub. Closing line: *"Thanks for watching. Now go ship something at idea velocity."* **Note:** this slide's own page-count footer reads "14/14" instead of "17/17" — a stale leftover from an earlier version of the deck, worth fixing regardless of what else changes.

---

## NEW: WorldAI background intro — right after the cold open (slide 2)

**Your ask:** "afer my intro hook on my moms campaign i need an intro for worldai project to explain more background." The mom/D&D story works as a hook, but jumps straight into a specific moment without ever explaining what WorldAI actually IS. Need a short orientation slide between the cold open (slide 2) and the verification-gap pivot (slide 3): what WorldAI is (AI Game Master, play any character in any world, D&D-style), how it's built (the harness-first stack this whole talk is about), maybe 1-2 concrete facts (worldarchitect.ai, real product, X campaigns). Exact copy TBD — flag if you want me to draft this now or wait for the other open items to settle first.

## New addition: Snapchat credibility slide — needs a new headline
Position TBD (after slide 8/pyramid, or after slide 13/postmortem, both reasonable). Content itself (Snap Bridge, Snap Wings, Open Model Pilot, real names, before/after framing, Snap Growth Notifications 100x-to-5B/day opener) stays — but **"This isn't just a side project" is out**, you don't want that headline. Need a replacement; propose a few options once the rest of the structure settles, or tell me what tone you want (credibility-flex vs. matter-of-fact vs. something else).

## Running appendix list (things moved OUT of main flow this round)
- Tokenmaxxing + Cache Stability (was original slides 10-11) — not compelling enough for a no-repo-access audience
- Harnesses Decay (was original slide 12) — appendix, current content flagged as low quality
- What Broke in Production (was original slide 13) — appendix for now

## Kept as-is
- CMUX demo (slide 9) — "let's just keep it for now"

---

## Open questions for you
1. Do the slide 4 & 6 graphic prototypes (linked above) look right, or need adjustment?
2. Slide 8 (agent pyramid): any specific facts that need updating, or keep as-is?
3. WorldAI intro + mom story (new opening item 3): want me to draft the combined copy now?
4. Intro/bio slide (new opening item 1): what do you want on it — just name/title/Google+Snap background, or more (e.g. the YouTube $70B / Snap 50M→5B credibility numbers)?
