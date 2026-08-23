# Keynote Redesign — "Develop at Idea Velocity" (Agentic AI Summit LA, 2026-08-26)

**Status:** Cold open resolved. Two non-blocking open items remain (see Open Items).

## Context

- Event: Agentic AI Summit LA, Conrad Los Angeles, Wed Aug 26 2026. Confirmed speaking slot: **30 min, target 20 min + Q&A**.
- Existing artifact: a real, verified 17-slide Google Slides deck (`1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0`), built 2026-08-23, design-system verified (cream/rust/serif-italic/monospace) against exported PDF renders. This spec redesigns its structure and content — it is not a from-scratch build.
- Audience: **medium-technical** (engineers/tech leads/builders who use AI coding tools, not necessarily building harness infrastructure themselves) — this is the deck that ships live. A denser "power-user" pass exists only as speaker notes/talking points layered onto these same slides, not a second deck.
- Content-strategy input: analysis of Jeffrey's own LinkedIn performance data (`wiki/sources/linkedin-analytics-2026-04-06.md` + verified public reaction counts) surfaced 3 patterns, used as design constraints below.

## Narrative arc: Demo → Mechanics → Payoff

Chosen over industry-framing-first and cognitive-tasks-first. Both alternatives put the WorldAI story in a supporting role, which makes it an illustration rather than the proof. This arc uses it as both.

## LinkedIn-derived content rules (apply to every slide)

1. **Every major section ends in an ask or a takeable artifact.** Bare-link posts capped at 1-14 reactions; the CTA + artifact post hit 12,767 impressions.
2. **Lead with the failure/surprise story, land the number, then explain.** ("I broke GitHub" = 8,396 impressions, beat all how-to content.)
3. **State the harness-over-model thesis as a flat, owned assertion — never a hedge or a question to the room.** (Most-hedged contrarian post = 1 reaction; owned reshares did better.)
4. **Do not assume the existing talk's framing already resonates.** The talk-video post got 15 reactions; the community-CTA post got 12,767. That gap says nothing about whether the AIEWF framing worked in the room — it says the framing doesn't travel. Redesign the packaging here rather than inheriting it.

## Slide structure (13 slides — agent-pyramid restored to main flow per Jeffrey's decision; realistic delivery estimate needs re-checking against the 13.9-18.3 min range computed for "12 + one restored slide" — same math applies to pyramid as it did to CMUX)

| # | Slide | Content | Time |
|---|---|---|---|
| 1 | Title | Minimal — event/date/name/one-line thesis | 10s |
| 2 | **Cold open** | "The player quit. The world said no." — first-person story: Jeffrey playing a WorldAI campaign with his mom. An improvised NPC (a grocer, Mr. Park) hands their character supplies on credit; the player tries to rage-quit in-character ("I'm an undocumented immigrant, I'm gonna go home"); instead of fading to black, the world argues back using consequences it generated itself — a line-cook NPC: *"The debt to Mr. Park doesn't vanish because you close the door... you're becoming a fugitive from a paper trail you can't outrun."* The player can't quit. 20 scenes later, they shake hands on a 10% equity partnership with Park. Nobody hand-coded a "player tries to quit" branch. Source: `wiki/sources/michele-fried-chicken.md`, scenes 16/26/27/40. | 75s |
| 3 | The pivot | "How do you build this without babysitting every commit?" → Verification Gap stat (Greptile 27.6% AI-gen merged PRs; Sonar 96% don't fully trust / 48% verify / 65% by 2027) as the industry-wide version of the same problem | 60s |
| 4 | **Cognitive tasks** (the big idea) | Verbatim-preserved context-switching argument (see Source Notes) | 90s |
| 5 | How it actually ships | Condensed 5-phase pipeline + 7-green gate, narrative framing not jargon | 75s |
| 6 | **Agent pyramid** (RESTORED to main flow) | Openclaw/Hermes → CMUX/AO → CLI Worker Fleet → Subagents/MCP, full diagram — placed right after the mechanics slide since "here's the architecture" follows naturally from "here's how it ships" | 60-75s |
| 7 | Cost + cache (merged) | Tokenmaxxing + cache stability, **numbers corrected** (see Fixes) | 60s |
| 8 | Harnesses decay | "19 new Claude/Codex model releases since June 2025 — one every 3 weeks. My harness outlived all 19." First-person, sourced (11 Claude: Opus 4.1→Opus 5; 8 Codex/GPT: GPT-5→GPT-5.6, June 2025–Aug 2026), no hedge. | 45s |
| 9 | **Snapchat credibility** | 3 projects, real names, before/after framing (see Snapchat Slide Content) | 75s |
| 10 | Postmortem honesty | What broke (89.6% watchdog stall rate, 251 babysit polls/11 days, 9h context-compaction ceiling) — keeps the evidence-based, non-hype voice | 45s |
| 11 | **WorldAI returns** | Payoff: "here's how slide 2 was actually possible" — FastEmbed <50ms classifier, dice audit (**line count fixed**), 300k token context, Min-First/Fill-to-Max | 60s |
| 12 | Takeable artifact | Primary ask: the campaign link (bit.ly/4xT84WA) — "go play it yourself," closes the loop back to slides 2 and 11. Secondary bullets: repo link, and the 6-step triage loop as a compact "steal this" process checklist. Ends on an ask, per LinkedIn rule 1 | 45s |
| 13 | Closing question | "What verifies the code after you ship?" — stated flat, per LinkedIn rule 3 | 30s |

### Cut from the existing 17-slide deck (and why)
- Dedicated CMUX demo slide → becomes a link reference on slide 5, not a slide; full version stays in Appendix A2 (tested as a main-flow restoration, pushed realistic delivery to 14.9-19.6 min combined with pyramid — decision was to keep only one of the two restored, pyramid was chosen)
- Loopcraft / software-factory quote slides → secondary insight for this audience, cut from the timed flow; moved to Appendix A3/A5
- "8 bets for next 30 days" as its own slide → folds into slide 12 as 2-3 bullets; full detail moved to Appendix A4
- "Evolution of AI in coding" 4-stage maturity model (from reference template slide 5) → not in either the original 17 or the first redesign pass; added directly to Appendix as A6 per Jeffrey's request

### Appendix — not in the timed 13-slide flow, Q&A backup / "if there's time" only

| # | Slide | Content | Use case |
|---|---|---|---|
| A2 | CMUX demo | Full slide + YouTube `qGJZ31t4wj4` — "hands on the keyboard, Hermes on standby" | If there's time to show it live, or "can I see this working?" |
| A3 | Loopcraft | "The unit is now the loop, not the message" (chat → tools → goals → automations → loops) | Audience members wanting the more philosophical framing |
| A4 | 8 bets for the next 30 days (full detail) | All 8 items, not just the 2-3 bullets on slide 11 | "What's next" / roadmap questions |
| A5 | Software-factory quote | Cooke/Galow/WorkOS convergence — "factory = harness + org process" | Industry-validation / "is this just you or is this a trend" questions |
| A6 | Evolution of AI in coding | 4-stage maturity model from the reference template (Stage A: IDE tools/autocomplete → B: agentic shift, parallel/Openclaw/looping agents → C: advanced orchestration, harness engineering, 10-20 agent orchestrators → D: self-evolution, "no one yet"). Framing: "most teams sit at B, frontier moving to C." Source: template deck `1JY7CmnE33b9...`, slide 5. | "Where are we on the maturity curve" / positioning questions |

## Fixes required (verified against source during this session's audit)

| Claim | Deck currently says | Verified correct | Source |
|---|---|---|---|
| `world_logic.py` line count | 7,273 lines | **12,378 lines** | `wc -l mvp_site/world_logic.py`, 2026-08-23 |
| Dice audit line count | 1,549 lines | **1,889 lines** (`dice_integrity.py`) | `wc -l mvp_site/dice_integrity.py`, 2026-08-23 |
| PR #7215 metric | "59%" and "$9.49→$0.086" presented as the same number | 59% = share of pre-merge **total spend** eliminated; $9.49→$0.086 is a ~99% collapse in one specific cost line-item — these are two different metrics, must not be conflated in copy | `learnings-2026-06.md:140`, `nextsteps-2026-06-04-gemini-cost-cacheoff-proof.md:23` |
| PR #8851 cache stability | "537,444-char prefix stability across 11 turns" | Verified stable **through turn 11**, checked at turns **1, 5, 9, 10, 11** (5 sampled checkpoints) — not 11 consecutive turns tested | `2026-08-15-pr-review-last-3-days.md:58` |
| "12 specialized agents" | stated as precise | Plausible but unconfirmed — 11-14 concrete `Agent` subclasses in `mvp_site/agents.py` depending on whether variants (`HeavyDialogAgent`, `SpicyModeAgent`, `DeferredRewardsAgent`) count separately. **Recount before stage use.** | `grep -n "class.*Agent" mvp_site/agents.py`, 2026-08-23 |
| "130 PRs/week" (if used from consulting-site material) | bare number on `agent_universe_frontend` site | Flagged by internal reviewer as needing qualifier: "130 merge-ready PRs per week — each reviewed by 7 independent automated checks before merge, with zero manual gatekeeping" + 26x context. Do not use the bare number. | `ai_universe_frontend/docs/rob-consulting-page-feedback.md` item 9 |

## Snapchat slide (#8) content

Real product names confirmed OK to use (already public on `agent-universe.ai/consulting`).

- **Snap Bridge** (MCP connector to internal services): Before = engineers copy-pasting between browser and AI chat to pull internal data. After = stay in the terminal, AI acts autonomously against internal services on your behalf. Adopted by the majority of engineers.
- **Snap Wings** (remote-hosting tool): Before = no path to remote-host internal apps. After = shared server auto-registers and deploys your app — "like mini Vercel." Used by engineers and non-engineers.
- **Open Model Pilot**: results close enough to be interesting, too noisy to publish a hard number yet. Most open-model providers still lack full Claude Code/Codex-API-level compatibility.
- Opens with a credibility line: Snap Growth Notifications scaled 100x to 5B+/day (pre-AI-agent-era engineering credibility), per `agent_universe_frontend` career section.

## Source notes — preserve close to verbatim

Cognitive-tasks / attention-orchestration argument (slide 4), from Slack, 2026-08-20:

> "What matters is unique cognitive tasks not agents. You can have 5 agents or 5 terminals working on the same task, multiple angles/work items. You can parallelize a lot more when you give tasks a /goal and say work for 30 min, 2 hours, 12 hours. What's important is not the amount of parallelization but the amount of context switches. Extreme example: focus on one cognitive task, have 9 running in parallel, check once every 12 hours — nothing forces you to check in, so you let it run and check 12 hours later."

## Open items

1. **BLOCKING — slide 7's real number.** Found by the `/document-standards` AI-tell audit: the old "models get replaced every 40-90 days" claim has zero source anywhere in this repo. Replaced with a first-person framing, but it needs Jeffrey's actual count: how many times has he re-pointed his harness at a new model, and over what period? Do not build this slide until answered.
2. **"12 specialized agents" recount** — needs a final, precise headcount from `mvp_site/agents.py` before stage use. (Non-blocking for build, blocking for stage use.)
3. **LinkedIn per-post impression data** — `linkedin-deep-pull` agent blocked repeatedly (LinkedIn anti-scraping, then an Aside browser-bridge disconnect). Not required to ship the deck (the Jan-Apr analytics summary + verified reaction-count sample already support the 3 content rules above); the reliable path if more precision is wanted is a manual export (LinkedIn → Profile → Analytics → Post impressions → Export).

## Note on slide 2 sourcing

Jeffrey confirmed first-person: he was present and surprised by this moment, playing with his mother. Frame accordingly in delivery — this is a personal story, not a transcript summary. Backups if this needs replacing: the GM catching itself off-canon mid-session (`wiki/sources/luke-v2-entry-009.md` to `-011.md`, more meta/technical-crowd-friendly) or the Luke-turns-Sith arc as backing evidence for the slide-11 pitch line (`wiki/sources/luke-v2-entry-020.md`/`-026.md`, player-requested rather than emergent, so weaker as a hook but fine as supporting evidence).
