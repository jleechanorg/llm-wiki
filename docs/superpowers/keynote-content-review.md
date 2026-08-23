# Develop at Idea Velocity — Keynote Content Review

**Status:** 12 of 13 planned slides shown below (Agent Pyramid, slide 6, being added next; CMUX demo stays appendix-only). Content pulled directly from the built/verified Claude Design source (`keynote/slide-01.html` … `slide-12.html`), post consistency-fix pass.

**Live project:** https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89

---

## 01 / 13 · Title

**AI coding stack + _WorldAI_**
*Develop at idea velocity*

Jeffrey Lee-Chan
Head of Vibe Coding · Snapchat · ex-Google

`KEYNOTE · AUGUST 26, 2026 · CONRAD LOS ANGELES`

---

## 02 / 13 · Cold Open

# The player quit.
# _The world said no._

I was playing a WorldAI campaign with my mom. Her character owed a local grocer, Mr. Park, for supplies on credit — a debt the world remembered, not a stat I'd written down.

Mid-session, she tried to rage-quit in character: *"I'm an undocumented immigrant, I'm gonna go home."*

> "The debt to Mr. Park doesn't vanish because you close the door … you're becoming a fugitive from a paper trail you can't outrun."

She couldn't quit. Twenty scenes later, we shook hands with Park on a **10% equity partnership**. Nobody hand-coded a "player tries to quit" branch.

`Source: wiki/sources/michele-fried-chicken.md · Scenes 16 / 26 / 27 / 40`

---

## 03 / 13 · The Pivot

# How do you build this without **babysitting every commit**?

*The verification gap, industry-wide:*

| Metric | Value | Label | Source |
|---|---|---|---|
| 01 | **27.6%** | AI PRs merged — of AI-generated pull requests get merged as-is | Greptile |
| 02 | **96%** | Don't fully trust it — of developers don't fully trust AI-generated code without review | Sonar |
| 03 | **48%** | Actually verify — say they always verify AI output before shipping it | Sonar |
| 04 | **65%** | By 2027 — of code is projected to be AI-generated, industry-wide | Sonar |

---

## 04 / 13 · The Big Idea

# **Unique cognitive tasks**, not agents.

> "What matters is unique cognitive tasks not agents. You can have 5 agents or 5 terminals working on the same task, multiple angles/work items. You can parallelize a lot more when you give tasks a /goal and say work for 30 min, 2 hours, 12 hours. What's important is not the amount of parallelization but **the amount of context switches**. Extreme example: focus on one cognitive task, have 9 running in parallel, check once every 12 hours — nothing forces you to check in, so you let it run and check 12 hours later."

`— Internal Slack · August 20, 2026`

---

## 05 / 13 · The Harness

# How it actually _ships_

Five phases. One gate that has to say yes seven times before anything merges.

**01 Plan** — Goal stated, scope drawn before a line is written.
→ **02 Draft** — Agent writes the change, opens it as a draft PR.
→ **03 Verify** — Evidence gathered — tests run, output captured.
→ **04 Review** — AI review pass, then a human review pass.
→ **05 Ship** — Human merges. Nothing ships on AI's say-so alone.

**7 — The Green Gate.** Seven independent automated checks run before anything merges — zero manual gatekeeping on the gate itself.

*Underneath this: **Hermes → CLI worker fleet → subagents.** One line here on purpose — full diagram in the appendix.*

---

## [NEW] 06 / 13 · Agent Pyramid *(being added to main flow per your call — CMUX demo moved back to appendix instead)*

Openclaw/Hermes → CMUX/AO → CLI Worker Fleet → Subagents/MCP. The full architecture behind the one-line mention on slide 5.

---

## 07 / 13 · Cost + Cache

# What idea velocity _actually_ costs

- **Tokenmaxxing** — $20/mo vs $200/seat — *Flat-rate plan vs. per-seat tool pricing. Same output. A fraction of the seat cost.*
- **Cache hit rate** — 99.8% static-floor cache hit — *The shared prefix (tools, instructions, context) is a cache hit almost every time.*
- **PR #7215** — **59%** share of pre-merge spend eliminated. *Separately, one line item:* $9.49 → $0.086 — collapse in the cached-input cost line — a different metric, same PR.
- **PR #8851 · Cache stability** — 537,444-char prefix held byte-identical through turn 11. Checked at turns 1, 5, 9, 10, 11 — five sampled checkpoints, not eleven consecutive turns.

---

## 08 / 13 · Harnesses Decay

# 19 new Claude and Codex model releases since June 2025 — *one every three weeks.*
# My harness outlived all **19**.

`11 Claude · Opus 4.1 → Opus 5` &nbsp; `8 Codex/GPT · GPT-5 → GPT-5.6` &nbsp; `June 2025 – Aug 2026`

---

## 09 / 13 · Snapchat Credibility

# This isn't just a _side project_

*Before any of this: Snap Growth Notifications scaled 100x to 5B+/day.*

- **Snap Bridge** — MCP connector to internal services
  BEFORE: Copy-pasting between browser and AI chat to pull internal data.
  AFTER: Stay in the terminal — AI acts autonomously against internal services. *(Majority of engineers.)*
- **Snap Wings** — Remote-hosting tool
  BEFORE: No path to remote-host internal apps.
  AFTER: Shared server auto-registers and deploys your app — like mini Vercel. *(Engineers and non-engineers.)*
- **Open Model Pilot** — Open-weight models in the harness
  Directionally similar to SWE-bench results. Close enough to be interesting — too noisy to publish a hard number yet. Most open-model providers still WIP on full Claude Code/Codex-API-level compatibility.

---

## 10 / 13 · Postmortem

# What _actually_ broke.

*No hype. The honest failure modes from running this harness in production.*

- **Watchdog** — **89.6%** CI Dispatch Watchdog stall rate — the autonomous dispatch loop stalled more often than it completed on its own.
- **Babysitting** — **251** manual babysit polls, 11 days — "autonomous" still meant a human nudging it awake, repeatedly.
- **Context** — **9h** context-compaction ceiling — past this point, the harness loses coherent memory of its own state.

`EVIDENCE, NOT HYPE` · `VERIFIED 2026-08-23`

---

## 11 / 13 · WorldAI Returns

# Here's how slide 2 was _actually_ possible.

- **Intent routing** — <50ms FastEmbed intent classifier — routes every player message before the LLM ever sees it, no keyword heuristics.
- **Dice audit** — **1,889** lines in `dice_integrity.py` — casino-grade audit trail, every roll provably fair, end to end.
- **World logic** — **12,378** lines in `world_logic.py` — God Mode & dynamic rules, routed across **11** specialized agents.

---

## 12 / 13 · Takeable Artifact

# Go play it _yourself_.

**THE CAMPAIGN FROM SLIDE 2 AND SLIDE 10**
### bit.ly/4xT84WA

**The repo:** github.com/jleechanorg

**Steal this loop:**
1. Quick Plan
2. Async Drive
3. AI Evidence Review
4. Human Evidence Check
5. AI Code Review
6. Human Merge

---

## 13 / 13 · Closing

# What verifies the code after you ship?

`worldarchitect.ai` · `github.com/jleechanorg` · `linkedin.com/in/jeffrey-lee-chan`
