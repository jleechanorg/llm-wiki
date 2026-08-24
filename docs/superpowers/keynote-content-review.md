# Develop at Idea Velocity — Original Deck + Proposed Enhancements

**Approach corrected:** enhance the original 17-slide deck in place, not replace it with a new structure. This file shows the ORIGINAL content (extracted from the live deck's actual rendered PDF, `1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0`) side by side with proposed changes. Nothing has been pushed to Google Slides yet — review this first.

## NEW OPENING STRUCTURE (your latest call — replaces the "cold open first" plan)

1. **Intro** — who you are, background at Google/Snap
2. **Snapchat projects** — the credibility slide (Snap Bridge, Snap Wings, Open Model Pilot)
3. **WorldAI intro + mom story** — combined: what WorldAI is, then the cold-open story (Mr. Park debt, the rage-quit the world wouldn't allow) as the illustration of it

### BUILT — item 3 copy (WorldAI intro + mom story combined), verbatim from `keynote/deck/03-worldai-mom.html`

> **WorldAI — an AI Game Master that plays live**
> Play any character, in any world — Game of Thrones, Star Wars, Baldur's Gate, or one you make up. The world reacts to what you actually do, not a script. It's a real product — **worldarchitect.ai** — not a tech demo.
>
> Here's what that means in practice. I was playing a campaign with my mom. Her character owed a local grocer, Mr. Park, for supplies on credit — a debt the world remembered, not a stat I'd written down. Mid-session, she tried to rage-quit in character:
>
> *"I'm an undocumented immigrant, I'm gonna go home."*
>
> Instead of fading to black, the world argued back, using consequences it had generated itself:
>
> *"The debt to Mr. Park doesn't vanish because you close the door … you're becoming a fugitive from a paper trail you can't outrun."*
>
> **She couldn't quit. Twenty scenes later, we shook hands with Park on a 10% equity partnership. Nobody hand-coded a "player tries to quit" branch.**
>
> Footer citation on the slide: *First-person, verified 2026-08-23 · wiki/sources/michele-fried-chicken.md, scenes 16/26/27/40*

Built and verified: https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F03-worldai-mom.html — editorial/pull-quote layout (rust vertical rule + serif-italic blockquotes), not a card grid, to vary the visual treatment per your "we're overusing the boxes" note.

Item 1 (Intro/bio) built: https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F01-intro-bio.html — verbatim copy: name "Jeffrey Lee-Chan", kicker "Head of Vibe Coding · Snapchat · ex-Google — scaling systems from millions to billions, before any of this was AI.", 3 cards (YouTube 2008–2018 $70B+ Paid to creators / Snap 2018–2026 50M→5B+ Daily notifications / Snap 2026→ 3 Internal AI projects shipped).

Item 2 (Snapchat projects) built: https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F02-snapchat.html — headline resolved to **"What I built with this stack — inside Snap"** (replaces the rejected "This isn't just a side project"), opens with the credibility line ("Snap Growth Notifications, scaled from a small pilot to 5B+ notifications a day, ~100x growth from 2018 to 2026"), then 3 Before/After cards for Snap Bridge, Snap Wings, Open Model Pilot using the exact real-name content from the spec.

Then continues into the original deck's slide 3 onward (verification gap → pivot, etc.) — original slide numbering below still refers to the ORIGINAL deck for content reference, but the actual running order now starts with these 3 new/reordered items before slide 3.

## FULL DECK BUILD — Claude Design (2026-08-23, in progress per your "build the deck in Claude Design first" call)

Project: https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89 — all files under `keynote/deck/`. Build order is the FINAL running order (14 main-flow slides). Every slide below has been rendered and visually verified via screenshot.

| # | File | Status |
|---|---|---|
| 01 | `01-intro-bio.html` | Built |
| 02 | `02-snapchat.html` | Built (new headline: "What I built with this stack — inside Snap") |
| 03 | `03-worldai-mom.html` | Built (narrative/pull-quote layout, not a card grid) |
| 04 | `04-verification-gap.html` | Built — real citations added, header stat fixed (was conflating two studies' sample sizes) |
| 05 | `05-pipeline.html` | **Unchanged from original — see note below**, not embedded in Claude Design |
| 06 | `06-leftshift-rightshift.html` | **Unchanged from original — see note below**, not embedded in Claude Design |
| 07 | `07-sixstep-loop.html` | Built — circular, pure SVG |
| 08 | `08-craftsmanship.html` | Built — **replaced the corrupted screenshot with a second Domain-02 card** (my call, see below) |
| 09 | `09-pyramid-cogtasks.html` | Built — **pixel-faithful rebuild of your original pyramid**, not a reinterpretation, per your correction |
| 10 | `10-cmux-demo.html` | **Unchanged from original — see note below**, not embedded in Claude Design |
| 11 | `11-worldai-payoff.html` | Built — Scale & Stats card only (agent count fixed 12→11), does NOT retell the mom story since slide 03 already does |
| 12 | `12-two-engines.html` | Built — both wrong numbers fixed (7,273→12,378; 1,549→1,889) |
| 13 | `13-eight-bets.html` | **Unchanged from original — see note below**, not embedded in Claude Design |
| 14 | `14-find-me.html` | Built — footer now correctly reads "14/14" for this deck's actual final count |

Appendix (A1 tokenmaxxing, A2 cache-stability, B harness-decay, C broke-in-prod): all **unchanged from original**, same note below.

**Why 4 main-flow slides + 4 appendix slides aren't in Claude Design:** tried embedding the original PNGs directly (base64 data URIs) so the whole deck lives in one project — hit a real tool limit: the Read tool caps at ~4000 tokens/call, and these renders are 300-850KB (500K+ base64 chars), so reconstructing them in an agent's context to pass to `write_files` isn't feasible (confirmed empirically by 3 parallel subagents, including attempts at WebP recompression down to ~30-80KB that were still impractical). Since these 8 slides have **zero content changes**, there's nothing new to review anyway — I'll carry them into the final deck by re-uploading the original PNGs directly to Google Slides at assembly time (the same `gog slides insert-image` mechanism already proven working during this session's restore). Flagging this as a real constraint, not a shortcut: if you want to review these unchanged slides again first, they're visible in the current live deck at the link below.

**Call I made on slide 08 (Craftsmanship) worth flagging:** the original's right panel was a corrupted/garbled code-editor screenshot (a real bug, not a design choice). I don't have a real replacement screenshot, so instead of patching a broken image I turned it into a proper 2-card comparison (Domain 01 velocity-biased vs. new Domain 02 consequence-biased) — this actually delivers on the slide's own stated thesis ("Pre-LLM favored upstream craftsmanship... now fast coding changes the equation") better than a screenshot ever did. Domain 02's copy is invented-but-consistent (production auth/billing/migrations framing) — flag if you want different examples there.

## Visual prototypes — SUPERSEDED by the full deck build above

The individual prototype links that used to live here (`keynote/proto-pyramid-cogtasks-merged.html`, `keynote/proto-intro-bio.html`, `keynote/proto-slide06-circular.html`) have all been superseded by their final, numbered versions under `keynote/deck/` in the **FULL DECK BUILD** table above (`01-intro-bio.html`, `07-sixstep-loop.html`, `09-pyramid-cogtasks.html`) — those old prototype files still exist in the Claude Design project as historical scratch work but are no longer the source of truth. Use the `keynote/deck/` links throughout this doc.

**Live deck:** https://docs.google.com/presentation/d/1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0/edit — **PUSHED, final 18 slides, full resolution** as of 2026-08-23 ~17:28 PT (14 main-flow + 4 appendix). Assembly: appended all 18 new slides to the end first (10 freshly rendered from `keynote/deck/*.html`, 8 unchanged originals reused directly from this session's cached renders), verified count (35 = 17 original + 18 new), then deleted the original 17 by their known object IDs, verified final count (18).

**Resolution fix:** the first push used the claude-in-chrome extension's screenshot tool, fixed at 1335×896 regardless of `resize_window` — a visible upscale on the slide canvas. Fixed by rendering the same 10 pages via local headless Chrome (`--window-size=1920,1080 --force-device-scale-factor=2 --screenshot=...`) instead, producing crisp 3840×2160 captures, then swapping them into the already-correct slide positions with `gog slides replace-slide` (no reordering risk). Re-exported and spot-checked slides 1 and 9 at high zoom — text is now clean-edged, matching/exceeding the original's own render quality.

**Restore history:** deck was previously restored to the original 17 slides on 2026-08-23 ~21:50 PT, after a background agent's Task 7 mistakenly deleted-and-rebuilt it into the 13-slide redesign despite an in-flight stop request (timing race). That restoration (full-bleed image re-upload from cached PDF renders) is what the final push above started from. **Speaker notes from the true original were not recoverable this way** (never captured as text) — only available via Drive's native Version History UI if you want them back specifically.

Reference deck template (do not touch): https://docs.google.com/presentation/d/1JY7CmnE33b9_R1IhHyv0M-WYw-kdTJFEqskoR_PRqBc/edit — read-only exports only, no writes made.

---

## 01/17 · Title — KEEP AS-IS
> AI coding stack + WorldAI — Develop at idea velocity — a tour of the autonomous pipeline and the game I built with it.
> Jeffrey Lee-Chan · Head of Vibe Coding · Snapchat · ex-Google

No proposed change.

---

## 02/17 · The Verification Gap — KEEP THE TABLE, ADD REAL CITATIONS + EXPLANATION

**Built and verified:** https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F04-verification-gap.html — same 4-card layout as the original, verbatim final copy:

Header right-side stat block fixed from "Sonar / Greptile 2026 Empirical Study / n = 1,100 engineering teams" (which conflated two different studies' sample sizes) to **"Sonar State of Code Survey + Greptile PR Analysis" / "1,100+ devs · 65,000 orgs"**.

| # | Value | Title | Desc (final) | Pills |
|---|---|---|---|---|
| 01 | 27.6% | AI-Generated Code | "Share of merged PRs generated by AI agents, up 28x in 14 months." | Greptile 2026 · 28x growth |
| 02 | 48% | Always Verify | "Only 48% of developers always verify AI-generated code before committing." | Sonar 2026 · verification gap |
| 03 | 96% | Don't Fully Trust | "96% of developers don't fully trust AI-generated code is correct." | Sonar 2026 · trust deficit |
| 04 | 65% | Projected by 2027 | "Share of code projected to be AI-generated by 2027, up from 42% today." | Sonar 2026 · industry shift |

Bridge line above the footer (your "explain it a bit more" ask): *"27.6% of merged code is now AI-written and climbing fast (28x in 14 months). But trust hasn't caught up — most developers still don't fully believe the output is correct, and fewer than half actually check before committing."*

Footer payoff quote kept: *"The bottleneck is no longer generating code — it's proving correctness without human babysitting."* Footer source tag updated from "SOURCE: ROADMAP/02-VERIFICATION-GAP.MD" to **"SOURCES: GREPTILE 2026 · SONAR 2026"**.

Sources: Greptile, ["Rise of the Overnight Agents"](https://www.greptile.com/blog/rise-of-the-overnight-agents) — analysis across 65,000 orgs. Sonar, [State of Code Developer Survey](https://www.sonarsource.com/blog/state-of-code-developer-survey-report-the-current-reality-of-ai-coding/) — 1,100+ developers, published Jan 8, 2026.

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

**Built and verified:** https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F07-sixstep-loop.html — single-ring, pure SVG. Same 6 step names/order, color-coded (rust fill = AI-owned, outline = human-owned): 1 Quick Plan (Human) → 2 Async AI Drive (AI) → 3 AI Evidence Review (AI) → 4 Human Proof Check (Human) → 5 AI Code Review (AI) → 6 Human Merge (Human), dashed rust return-arc from 6 back to 1. Footer: "3 human-owned, 3 AI-owned steps — the loop closes back to step 1."

---

## 07/17 · Craftsmanship vs. Velocity — FIXED (screenshot replaced with a 2nd card, not patched)

**Found while re-auditing:** this slide's right-hand panel was a screenshot of a code editor that rendered as garbled/illegible text — a corrupted/over-compressed image, not a design choice. No real replacement screenshot was available, so instead of patching the broken image, the slide became a proper 2-card domain comparison — which actually delivers on its own stated header thesis ("Pre-LLM favored upstream craftsmanship. Now fast coding changes the equation.") better than a screenshot did.

**Built and verified:** https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F08-craftsmanship.html — final copy:

| | Domain 01 · Velocity Biased (original, kept) | Domain 02 · Consequence Biased (NEW — replaces the broken screenshot) |
|---|---|---|
| Title | Low Consequence · Fast Fail | High Consequence · Slow, Deliberate |
| Quote | "Shotgun and adjust rapidly." | "Design before you type." |
| Desc | "UI explorations, prototypes, internal analytics, throwaway scripts. No heavy upfront design." | "Production auth, billing, data migrations — anything hard to reverse. Heavy upfront design, extensive review before merge." |
| Pills | velocity max · rapid feedback | consequence max · deliberate design |

Domain 02's copy is invented-but-consistent (production auth/billing/migrations framing) — flag if you want different concrete examples. Footer tenets kept verbatim: *"1. Only automate smooth things · 2. No black-and-white thinking; everything is a gradient · 3. Try fundamentals & shotgun in parallel."*

---

## 08/17 · The Agent Supervision Pyramid — MERGED WITH COGNITIVE TASKS (04/17)

**Your final call:** "we can combine agentic pyramid with cog tasks" — and then corrected: *"you're not listening to me. I want the exact same image as original pyramid but modified."* Rebuilt as a pixel-faithful reproduction of the actual original slide-08 render (not a stylistic reinterpretation): same header-with-right-aligned-subtitle layout, same 4-card grid with dotted separators and pill-tag rows, same footer/page-number row. Cognitive-tasks framing merged in as light-touch additions only: a 3rd pill per card ("1 cognitive task" / "angle diversity" / "extended horizon" / "zero spam") and the header's 2nd subtitle line changed from "Strict isolation between control and execution." to "One cognitive task, tracked top to bottom."

**Built and verified:** https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F09-pyramid-cogtasks.html — final card copy:

| Tier | Title | Subtitle | Desc | Pills |
|---|---|---|---|---|
| 1 · Dispatch | Hermes / Openclaw | Central Communication | "Slack-based dispatch — routing, task queuing, goal coordination. Openclaw is the auxiliary HTTP API gateway underneath. Retains long-term memory and preferences." | slack-bridge · memory · 1 cognitive task |
| 2 · Orchestration | CMUX & AO Daemon | Supervision & Worktrees | "Manages terminal panes, process groups, git worktrees, watchdog restarts, and Dark Factory goal-driven pipelines." | tmux/cmux · worktrees · angle diversity |
| 3 · Workers | CLI Agent Fleet | Code Execution | "Claude Code, OpenAI Codex, Cursor CLI. Specialized workers executing in isolated worktree sandboxes." | claude-code · codex · extended horizon |
| 4 · Tools | Subagents & MCP | Targeted Primitives | "Short-lived tool specialists: Playwright browser testers, compiler drivers, BigQuery telemetry fetchers, test runners." | playwright · mcp · zero spam |

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

## 14/17 · WorldAI: An AI Game Master That Plays Live — RESOLVED AS "WorldAI Returns" PAYOFF SLIDE (new deck position 11)

**Original:** Product Vision card ("Play Any Character in Any World") + Scale & Stats card (12 specialized agents, 30+ prompt files, 300k token context, Min-First/Fill-to-Max, BYOK).

**Resolution:** the real first-person mom/Mr.-Park story now already opens the deck (new item 3, see above) — retelling it here in the original main-flow position would be redundant in a 20-min talk. Instead this slide became the **payoff/callback**: "here's how the opening story was possible." Left card keeps the original quote and product framing but reframes the body copy as a callback rather than a fresh pitch; right card keeps Scale & Stats verbatim except the agent count, corrected **12 → 11** (confirmed via `mvp_site/agents.py` this session).

**Built and verified:** https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F11-worldai-payoff.html — final copy:
- Title: "WorldAI returns — *here's how the mom story was possible*"
- Product Vision card desc: "Game of Thrones, Star Wars, Baldur's Gate, or your own universe. This is the same harness-first stack this whole talk has been about — applied live, in front of a player, with no script."
- Scale & Stats list: **11** specialized agents · 30+ prompt files in Git · 300k token context window · Min-First / Fill-to-Max · Bring Your Own Key (BYOK)
- Footer kept verbatim: "80% of wall-clock is the LLM — the deterministic harness is what makes it WorldAI."

---

## 15/17 · Two Engines, One Gateway — FIXED (new deck position 12)
**Original:** FastEmbed Intent Gate (<50ms) / Casino-Grade Dice Audit ("1,549 lines, 4-signal verification") / God Mode & Dynamic Rules ("7,273 lines in world_logic.py orchestrator").

**Confirmed wrong this session:** dice audit is actually **1,889 lines** (not 1,549); world_logic.py is actually **12,378 lines** (not 7,273) — both verified via `wc -l` against the live repo.

**Built and verified:** https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F12-two-engines.html — same 3-card layout, only the two numbers changed: header stat "12,378 lines in world_logic.py orchestrator", Innovation 02 quote "\"1,889 lines, 4-signal verification.\"" Everything else (FastEmbed <50ms card, God Mode card, footer "Deterministic Python logic guards game truth; LLM generates rich prose.") kept verbatim.

---

## 16/17 · 8 Bets for the Next 30 Days — KEEP
Discipline Tickets / Commit Provenance / N-Green Gates / Headless by Default / Prefix Cache Audits / Self-Canceling Timers / Dark Factory Stages 3-6 / Harness Postmortems. No proposed change.

---

## 17/17 · Find Me, Play the Game — FIXED (new deck position 14)
LinkedIn / WorldAI (worldarchitect.ai) / Consensus ML / GitHub. Closing line: *"Thanks for watching. Now go ship something at idea velocity."* **Note:** this slide's own page-count footer read "14/14" instead of "17/17" against the OLD 17-slide original — a stale leftover. For the NEW 14-main-flow-slide deck, "14/14" is actually now the correct count, so the footer resolves itself rather than needing a real fix.

**Built and verified:** https://claude.ai/design/p/a9e699f8-95f3-493c-9a45-334d9481fa89?file=keynote%2Fdeck%2F14-find-me.html — same content and links (LinkedIn, WorldAI, Consensus ML, GitHub), footer confirmed "14 / 14 · Thanks for watching. Now go ship something at idea velocity." Dropped the small embedded LinkedIn-post thumbnail image from the original (no equivalent asset available to carry over); everything else preserved.

---

## RESOLVED: WorldAI background intro
Folded directly into new opening item 3 (`03-worldai-mom.html`) — the orientation copy ("WorldAI — an AI Game Master that plays live... It's a real product — worldarchitect.ai — not a tech demo") now sits right before the mom-story quotes in the same slide, rather than as a separate slide. See item 3 above.

## RESOLVED: Snapchat credibility slide headline
Position resolved to new opening item 2, right after the intro/bio slide (not after pyramid or postmortem). Headline resolved to **"What I built with this stack — inside Snap"**. Built: `02-snapchat.html`, see above.

## Running appendix list (things moved OUT of main flow this round)
- Tokenmaxxing + Cache Stability (was original slides 10-11) — not compelling enough for a no-repo-access audience
- Harnesses Decay (was original slide 12) — appendix, current content flagged as low quality
- What Broke in Production (was original slide 13) — appendix for now

## Kept as-is
- CMUX demo (slide 9) — "let's just keep it for now"

---

## Open questions — all resolved as of 2026-08-23
1. ~~Do the slide 4 & 6 graphic prototypes look right?~~ Resolved — both rejected/rebuilt (merged pyramid, circular loop), final versions in the FULL DECK BUILD table above.
2. ~~Slide 8 (agent pyramid): any facts to update?~~ Resolved — terminology audit found 2 real fixes (Hermes/Slack-only, Google Antigravity dropped), applied; pixel-faithful rebuild of the real original per your correction.
3. ~~WorldAI intro + mom story: draft the combined copy?~~ Resolved — drafted, built, verified (`03-worldai-mom.html`).
4. ~~Intro/bio slide: what goes on it?~~ Resolved — name/title + the 3 credibility numbers (YouTube $70B, Snap 50M→5B, 3 shipped projects), built (`01-intro-bio.html`).

**Status:** full 14-slide deck built and verified in Claude Design. Next/final step: push to the live Google Slides deck.
