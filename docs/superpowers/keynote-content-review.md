# Develop at Idea Velocity — Original Deck + Proposed Enhancements

**Approach corrected:** enhance the original 17-slide deck in place, not replace it with a new structure. This file shows the ORIGINAL content (extracted from the live deck's actual rendered PDF, `1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0`) side by side with proposed changes. Nothing has been pushed to Google Slides yet — review this first.

**Live deck (unchanged):** https://docs.google.com/presentation/d/1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0/edit

---

## 01/17 · Title — KEEP AS-IS
> AI coding stack + WorldAI — Develop at idea velocity — a tour of the autonomous pipeline and the game I built with it.
> Jeffrey Lee-Chan · Head of Vibe Coding · Snapchat · ex-Google

No proposed change.

---

## 02/17 · The Verification Gap — SIMPLIFY

**Original:** 4-card grid — 27.6% AI-Generated Code / 48% Explicitly Verified / 96% Lack Full Trust / 65% Projected by 2027. Bottom quote: *"The bottleneck is no longer generating code — it's proving correctness without human babysitting."*

**Your feedback:** "these numbers don't mean anything ... we can just say somewhere else that lots of code can be generated but needs verification to land."

**Proposed:** Drop the 4-card stat grid. Replace with a single plain statement (something like: *"AI can generate almost unlimited code now. The bottleneck moved — it's proving that code is correct before it ships."*), keep the existing bottom quote as the payoff line. The underlying stats stay available as backup/footnote, not the headline.

---

## 03/17 · One Slack Message, All the Way to Green Checks — KEEP
5 phases: Natural Language → Context & Memory → Parallel Agents → CI & 7-Green Gate → Proof-First. No proposed change.

---

## 04/17 · Cognitive Tasks & Workspaces — MAKE IT A GRAPHIC

**Original:** 3-card grid — "The Unit is the Task" / "Long-Horizon /goal" / "Context-Switch Economy," each with a pull-quote and description.

**Your feedback:** "maybe slide 4 can be a graphic."

**Proposed:** Convert to a visual diagram — e.g. one person icon with N task-stream lines branching off, most dimmed/backgrounded ("checked once every 12h"), one highlighted ("focused"), instead of 3 text cards. Core line to preserve: *"What matters is not the amount of parallelization, but the amount of context switches."* Your original Slack quote (full text) can live as a caption/footnote under the graphic rather than being the whole slide.

---

## 05/17 · Left-Shift and Right-Shift, Zero Human in the Middle — RESTORE (was cut in the redesign, going back in)
3 phases: Left-Shift Planning (front-load) → Zero Middle Human (execute) → Right-Shift Proof (back-load). Bottom: *"Goal: Reduce middle human intervention to zero with acceptable quality regression, and maximize output correctness."*

No content change proposed — just confirming this stays in.

---

## 06/17 · The 6-Step Loop — MAKE IT A GRAPHIC

**Original:** 6-card grid — Quick Planning → Async AI Drive → AI Evidence Review → Human Proof Check → AI Code Review → Human Merge.

**Your feedback:** "slide 6 - 6 step loop can be a graphic."

**Proposed:** Convert to a circular/linear flow diagram with 6 numbered nodes and arrows, alternating AI-owned vs human-owned steps visually (e.g. color-coded). Keep the exact 6 step names/descriptions, just change the visual treatment from 6 identical boxes to a flow.

---

## 07/17 · Craftsmanship vs. Velocity — FIX A REAL BUG
**Found while re-auditing:** this slide's right-hand panel is a screenshot of a code editor that renders as garbled/illegible text — looks like a corrupted or over-compressed image, not a design choice. Needs a fresh screenshot or should be replaced with something else entirely. Text content (Domain 01: Low Consequence/Fast Fail, Core Tenets) is fine.

---

## 08/17 · The Agent Supervision Pyramid — USE ORIGINAL IMAGE

**Original:** 4-tier card grid — Tier 1 Openclaw/Hermes (Dispatch) → Tier 2 CMUX & AO Daemon (Orchestration) → Tier 3 CLI Agent Fleet (Workers) → Tier 4 Subagents & MCP (Tools).

**Your feedback:** "i want my original agent pyramid but maybe edit/update the image."

**Proposed:** Keep this slide's real content/layout as the base — I was about to recreate it as new HTML from scratch, which was the wrong call. Instead, treat this rendered slide as the source of truth and just update specific facts if anything's stale (need to check: does "CMUX & AO Daemon" / "Dark Factory autonomous merge pipelines" language still match current terminology?).

---

## 09/17 · CMUX: Hands on the Keyboard, Hermes on Standby — WEAK, NEEDS A REAL REWRITE OR CUT

**Original:** 3-card grid — 1 Pane = 1 Agent Workspace / Manual or Standby Modes / Full Telemetry & Watchdogs. YouTube demo link.

**Your feedback:** "slide 9 doesn't add much value, also I don't like the tagline 'hands on keyboard, Hermes on standby' — doesn't mean much."

**Proposed:** Your call — either cut this slide entirely (folding the YouTube link into a footnote elsewhere) or give it a sharper headline that says something concrete (e.g. what specifically CMUX lets you DO that you couldn't before, not just a mood description).

---

## 10/17 · Tokenmaxxing — DROP INTERNAL PR REFERENCES

**Original:** 4-card grid — $20/mo vs $200/seat / 99.8% cache hit / 59% PR #7215 token drop / <50ms dynamic routing.

**Your feedback:** "saying PR 7215 doesn't make sense — we need to audit these slides for someone who has no access to the code. Maybe this slide isn't useful."

**Proposed:** Drop the bare "PR #7215" reference — an external audience can't look it up and it reads as jargon. If the card stays, reframe as the underlying fact without the ticket number (e.g. "a caching fix cut this cost category by roughly half" — using the properly-qualified version from this session's audit, not a bare unexplained percentage). Same audit applies to slide 11's "PR #8851" reference. Open question for you: keep this slide reframed, or cut it since the $20-vs-$200 and cache-hit points may already land elsewhere.

---

## 11/17 · Cache Stability — SAME PR-NUMBER ISSUE AS #10
"PR #8851: 537,444-char prefix stable across 11 turns" has the same "meaningless without repo access" problem, plus the "11 turns" phrasing was already found imprecise this session (real data: stable through turn 11, checked at turns 1/5/9/10/11 — 5 checkpoints, not 11 consecutive). Needs both a jargon fix and a precision fix if kept.

---

## 12/17 · Harnesses Decay — UPDATE THE STAT
**Original:** "40-90 Day Model Half-Life" (unsourced — this session's audit found zero backing for this exact claim anywhere in the repo).

**Available fix (already sourced this session):** 19 new Claude/Codex model releases since June 2025 — one every 3 weeks. Can either replace the "40-90 days" card with this, or keep both if there's room.

---

## 13/17 · What Broke in Production — KEEP
89.6% CI Watchdog stall rate / 251 babysit-cron spam polls / 9-hour context compaction ceiling. All verified accurate this session. No proposed change.

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

## New addition (not in original 17): Snapchat credibility slide
Proposed as a new insert (position TBD — after slide 8/pyramid, or after slide 13/postmortem are both reasonable): Snap Bridge, Snap Wings, Open Model Pilot, real names, before/after framing, opening with the Snap Growth Notifications 100x-to-5B/day credibility line. Content already drafted and verified in the Claude Design project if you want to see the visual: https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fslide-09.html (this is from the abandoned redesign — content is reusable, slide position is not).

---

## Open questions for you
1. Slide 2: exact wording for the simplified verification-gap statement?
2. Slide 4 & 6: graphic style preference (icon-based diagram vs. flow chart vs. something else)?
3. Slide 8: any specific facts on the agent pyramid that need updating, or just keep as-is?
4. Slide 9 (CMUX): cut, or rewrite the headline?
5. Slides 10-11: cut the PR-number slides entirely, or reframe without the ticket numbers?
6. Snapchat slide: where does it go in the running order?
