# Agentic AI Summit Keynote Deck — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the live "Develop at Idea Velocity" Google Slides deck (`1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0`) from 17 slides down to the 12-slide structure approved in `docs/superpowers/specs/2026-08-23-agentic-ai-summit-keynote-design.md`, with the 6 corrected statistics from that spec's Fixes table, using Claude Design MCP as the authoring/preview surface.

**Architecture:** Each Google Slides "slide" in the live deck is a full-bleed uploaded IMAGE, not native text (confirmed via `gog slides read-slide` — every slide's only content is a single `p<N>_i2` image element). So content is NOT editable via `gog slides replace-text`/`style-text`. The real pipeline is: author each slide as an HTML page in a Claude Design project (matching the already-verified design tokens below) → render each slide to a 1920×1080 PNG → push those PNGs into the Google Slides deck via `gog slides` slide-management commands → export + visually verify the final deck.

**Tech Stack:** `gog` CLI v0.37.0 (Google Slides read/write/export), Claude Design MCP (`mcp__claude-design__*`) for HTML authoring + preview, headless Chrome for PNG capture, `pdftoppm` for PDF verification.

## Global Constraints

- Design tokens (verified against the live deck's actual rendered PDF this session — do not deviate): `--bg: #f6f4ee; --bg-grid: #ece9e0; --paper: #fdfcf9; --ink: #1a1714; --ink-2: #4a443d; --ink-3: #8a8278; --rule: #d9d4c8; --accent: #c9683a; --accent-soft: #fdf0e3; --accent-deep: #8c4220; --code: #2a6f55; --data: #5c6c8c;` — body font Geist, slide titles Instrument Serif italic (mid-sentence emphasis), metadata/tags JetBrains Mono.
- Slide canvas: 1920×1080px (16:9), matching the live deck's `pageSize: 1440.00 x 810.00 PT`.
- All slide copy, corrected statistics, and content rules come from `docs/superpowers/specs/2026-08-23-agentic-ai-summit-keynote-design.md` — do not invent new claims; every number must trace to that spec's Fixes table or Slide structure table.
- Real product names (Snap Bridge, Snap Wings, Open Model Pilot) are approved for use — see spec.
- Do not touch or claim to touch `~/projects/develop-at-idea-v2` or `~/projects/develop-at-idea-v3` — those are separate, unrelated local HTML decks from an earlier session; this plan's deliverable is the Google Slides presentation only, authored via Claude Design.
- The talk is in 3 days — every task ends with a real visual verification step (render + `Read` the PNG), not just "wrote the code."

---

### Task 1: Claude Design project setup + design-token verification

**Files:**
- Claude Design project: new project named `agentic-ai-summit-keynote-2026` (no design-system binding — `list_design_systems` returned empty this session, so tokens are hand-authored per Global Constraints, not system-derived)
- Create: `keynote/tokens.css` (in the Claude Design project)

**Interfaces:**
- Produces: a `:root` CSS block other tasks `@import` or copy verbatim — must byte-match the values in Global Constraints.

- [ ] **Step 1: Load the Claude Design prompt (required before any write_files)**

Call `mcp__claude-design__get_claude_design_prompt` with no `design_system_id` (none exists yet).

- [ ] **Step 2: Create the project**

Call `mcp__claude-design__create_project` with `name: "agentic-ai-summit-keynote-2026"`. Record the returned `project_id` — every subsequent task in this plan uses it.

- [ ] **Step 3: Write the shared token file**

`mcp__claude-design__write_files` with `project_id`, one file:
```
path: keynote/tokens.css
data: |
  :root {
    --bg: #f6f4ee;
    --bg-grid: #ece9e0;
    --paper: #fdfcf9;
    --ink: #1a1714;
    --ink-2: #4a443d;
    --ink-3: #8a8278;
    --rule: #d9d4c8;
    --rule-2: #e8e3d6;
    --accent: #c9683a;
    --accent-soft: #fdf0e3;
    --accent-deep: #8c4220;
    --code: #2a6f55;
    --data: #5c6c8c;
    --data-soft: #e4e8f0;
    --bad: #c93b2b;
    --good: #2a6f55;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Geist', sans-serif; background: var(--bg); }
  .slide { width: 1920px; height: 1080px; background: var(--bg); position: relative; overflow: hidden; }
  h1 { font-family: 'Geist', sans-serif; font-weight: 500; letter-spacing: -0.035em; color: var(--ink); }
  em, .accent-title { font-family: 'Instrument Serif', serif; font-style: italic; color: var(--accent-deep); }
  .tag, .meta { font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 0.05em; color: var(--ink-3); text-transform: uppercase; }
```

- [ ] **Step 4: Verify — render and visually check**

`mcp__claude-design__render_preview` with `path: "keynote/tokens.css"` won't render visually (it's CSS, not HTML) — instead write a throwaway `keynote/_token-check.html` that imports `tokens.css` and renders a swatch of each color + one line in each font, `render_preview` it, then view the `serve_url` via a screenshot (claude-in-chrome or Playwright) and `Read` the resulting image. Confirm: cream background visible, rust/terracotta accent swatch visible, italic serif text renders, monospace tag text renders. Delete `_token-check.html` after (or leave — it's harmless scratch).

- [ ] **Step 5: Commit nothing yet** (Claude Design projects aren't git-tracked; no commit step here — this task's "commit" is the verified render.)

---

### Task 2: Author slides 1–4 (Title, Cold open, Pivot, Cognitive tasks)

**Files:**
- Create: `keynote/slide-01.html`, `keynote/slide-02.html`, `keynote/slide-03.html`, `keynote/slide-04.html` (each a full standalone HTML page: `<link>` or inline `tokens.css`, one `.slide` div, 1920×1080)

**Interfaces:**
- Consumes: `keynote/tokens.css` from Task 1 (link via relative path).
- Produces: 4 render-able HTML pages other tasks don't depend on (each slide is independent).

- [ ] **Step 1: Write slide-01.html (Title)**

Content per spec slide 1: minimal title slide — "AI coding stack + WorldAI" / "Develop at idea velocity" subtitle / Jeffrey Lee-Chan, Head of Vibe Coding · Snapchat · ex-Google / event context "KEYNOTE · AUGUST 26, 2026 · CONRAD LOS ANGELES". Match the verified title-slide layout from the existing deck (dot-marker eyebrow line, large black headline + rust "WorldAI" in serif italic, italic serif subtitle, byline block bottom-left, links bottom-right). Write via `write_files`.

- [ ] **Step 2: Write slide-02.html (Cold open)**

Content per spec slide 2, verbatim: "The player quit. The world said no." headline, the Michele/fried-chicken campaign story (Mr. Park credit, the rage-quit line, the line-cook NPC pushback quote, the 20-scenes-later equity handshake), framed as Jeffrey's first-person story playing with his mother. Source citation tag: `wiki/sources/michele-fried-chicken.md`. Write via `write_files`.

- [ ] **Step 3: Write slide-03.html (The pivot)**

Content per spec slide 3: "How do you build this without babysitting every commit?" pivot line + Verification Gap stats (Greptile 27.6% AI-gen merged PRs; Sonar 96% don't fully trust / 48% verify / 65% by 2027) as 3-4 metric cards, matching the existing deck's card-grid pattern (see the original deck's slide 3/10/11 layouts already visually verified this session — orange-tag "METRIC 0N" header, large colored number, label, one-line description, bottom tag pills).

- [ ] **Step 4: Write slide-04.html (Cognitive tasks)**

Content per spec slide 4: preserve the cognitive-tasks quote close to verbatim (full text is in the spec's "Source notes" section) as the slide's central content — this is "the big idea" slide, give it more breathing room/larger type than the metric-card slides, single focused block of text, not a card grid.

- [ ] **Step 5: Verify all 4 — render + visual check**

For each of the 4 files: `mcp__claude-design__render_preview`, screenshot the `serve_url`, `Read` the image. Confirm: correct headline text present, no overlapping text, design tokens applied (cream bg, rust accents), text doesn't overflow the 1920×1080 frame.

---

### Task 3: Author slides 5–8 (How it ships, Cost+cache, Harness decay, Snapchat)

**Files:**
- Create: `keynote/slide-05.html` through `keynote/slide-08.html`

**Interfaces:**
- Consumes: `keynote/tokens.css`.
- Produces: 4 more independent render-able pages.

- [ ] **Step 1: Write slide-05.html (How it actually ships)**

Condensed 5-phase pipeline + 7-green gate, per spec slide 5 — narrative framing, not a jargon-heavy diagram. One-line mention of the agent-pyramid concept folded in here (per spec's cut list), not a separate diagram.

- [ ] **Step 2: Write slide-06.html (Cost + cache, merged)**

Per spec slide 6 AND the Fixes table — this is the highest-risk-of-error slide, apply corrections exactly:
- Tokenmaxxing card: "$20/mo vs $200/seat" (unchanged, verified accurate)
- Cache-hit card: "99.8% static-floor cache hit" (unchanged, verified accurate)
- **PR #7215 card — REWRITE, do not reuse existing copy.** Old copy conflated "59%" with "$9.49→$0.086" as if the same number. New copy: headline stays "59%" labeled "share of pre-merge spend eliminated"; supporting line: "$9.49→$0.086 collapse in the cached-input cost line-item" presented as a *separate*, clearly-labeled example metric, not the thing 59% refers to.
- **Cache-stability card — REWRITE.** Old copy: "PR #8851: 537,444-char prefix stability across 11 turns." New copy: "PR #8851: 537,444-char prefix held byte-identical through turn 11 (checked at turns 1, 5, 9, 10, 11)."

- [ ] **Step 3: Write slide-07.html (Harnesses decay) — BLOCKED on spec Open Item #1**

Per spec slide 7 (updated after the `/document-standards` AI-tell audit found the old "40-90 days" claim unsourced): do NOT write this slide until Jeffrey supplies his real model-switch count and timeframe. Copy pattern once he does: "I've re-pointed my harness at a new model N times in [period]. The harness outlived all N." — flat, first-person, no hedge word (if/might/can/should), ≤12 words per sentence, no subordinate clause softening the claim.

- [ ] **Step 4: Write slide-08.html (Snapchat credibility) — NEW slide, no prior version to adapt**

Per spec's "Snapchat slide (#8) content" section verbatim: 3-card grid layout (reuse the card-grid visual pattern from slide-03/slide-06), opening credibility line "Snap Growth Notifications scaled 100x to 5B+/day" above the cards. Cards:
1. **Snap Bridge** — Before/After: copy-pasting between browser and AI chat → stay in the terminal, AI acts autonomously against internal services. "Majority of engineers."
2. **Snap Wings** — Before/After: no path to remote-host internal apps → shared server auto-registers and deploys, "like mini Vercel." Engineers and non-engineers.
3. **Open Model Pilot** — hedged finding: directionally similar to SWE-bench; industry still early; most open-model providers still WIP on full Claude Code/Codex-API-level compatibility.

**Do NOT include "130 PRs/week"** on this or any slide unless using the full qualified phrasing from the Fixes table ("130 merge-ready PRs per week — each reviewed by 7 independent automated checks before merge, with zero manual gatekeeping" + 26x context) — the bare number is explicitly flagged as not-yet-credible in the spec.

- [ ] **Step 5: Verify all 4 — render + visual check**

Same method as Task 2 Step 5. For slide-06 specifically, re-read the rendered text aloud (mentally) to confirm the 59%/$9.49→$0.086 numbers no longer read as the same metric.

---

### Task 4: Author slides 9–12 (Postmortem, WorldAI returns, Takeable artifact, Closing)

**Files:**
- Create: `keynote/slide-09.html` through `keynote/slide-12.html`

**Interfaces:**
- Consumes: `keynote/tokens.css`.
- Produces: final 4 pages, completing the 12-slide set.

- [ ] **Step 1: Write slide-09.html (Postmortem honesty)**

Per spec slide 9, unchanged stats (verified accurate this session, no fix needed): 89.6% CI Dispatch Watchdog failure rate, 251 babysit polls in 11 days, 9h context-compaction ceiling. Keep short — this slide's job is tone (evidence-based, not hype), not new information density.

- [ ] **Step 2: Write slide-10.html (WorldAI returns) — apply BOTH line-count fixes**

Per spec slide 10, payoff framing: "Here's how slide 2 was actually possible." Three cards (reuse the 3-card pattern):
1. FastEmbed <50ms intent classifier
2. Casino-grade dice audit — **"1,889 lines" (was 1,549 — corrected per Fixes table)**
3. God Mode & dynamic rules — mention **"12,378 lines in world_logic.py"** if the orchestrator line count is cited on this slide (was wrongly "7,273" on the old deck's equivalent slide — corrected per Fixes table). If the "12 specialized agents" figure is used anywhere on this slide, first complete the Task 5 recount (below) and use the confirmed number, not "12" unverified.

- [ ] **Step 3: Write slide-11.html (Takeable artifact)**

Per spec slide 11 (already resolved during self-review — primary ask is the campaign link, not a 3-way unresolved choice): primary call-out is the campaign link `bit.ly/4xT84WA` — "go play it yourself" — rendered as the largest type on the slide after the headline, in `--accent` color, with no other element on the slide exceeding 24px. Secondary bullets below it, smaller: repo link (`github.com/jleechanorg`), and the 6-step triage loop condensed to one line each (Quick Plan → Async Drive → AI Evidence Review → Human Evidence Check → AI Code Review → Human Merge) as a compact "steal this" list, not a full diagram.

- [ ] **Step 4: Write slide-12.html (Closing question)**

Per spec slide 12: "What verifies the code after you ship?" stated as a large, flat, owned headline — no question-mark hedging language around it, no "just food for thought" softening (per LinkedIn rule 3, the spec's content rule against hedged framing). Links footer: worldarchitect.ai / github.com/jleechanorg / linkedin.com/in/jeffrey-lee-chan.

- [ ] **Step 5: Verify all 4 — render + visual check**

Same method as prior tasks. For slide-10 specifically, re-check both corrected numbers are the ones that actually appear in the rendered PNG (not just in the HTML source — read the image).

---

### Task 5: Confirm the "12 specialized agents" count before it goes on any slide

**Files:**
- No project files — this is a verification-only task whose output feeds back into Task 4 Step 2 if that slide references the agent count.

- [ ] **Step 1: Run the count**

```bash
cd ~/worldarchitect.ai
grep -n "^class.*Agent\b" mvp_site/agents.py | grep -v "BaseAgent\|FixedPromptAgent"
```

- [ ] **Step 2: Decide the number to use**

Count the concrete (non-abstract-base) `Agent` subclasses returned. If variant subclasses (`HeavyDialogAgent`, `SpicyModeAgent`, `DeferredRewardsAgent`) are counted separately from their parents, note both the "distinct top-level types" count and the "including variants" count, and use whichever framing is defensible if a technical audience member asks "which 12 (or N)?" on stage.

- [ ] **Step 3: Update slide-10.html if the number differs from a round "12"**

If the confirmed count isn't exactly 12, edit `keynote/slide-10.html` (Task 4) to use the confirmed number, re-render, re-verify.

---

### Task 6: Render all 12 slides to 1920×1080 PNGs

**Files:**
- Create (local, not in the Claude Design project): `/tmp/keynote-render/slide-01.png` … `/tmp/keynote-render/slide-12.png`

**Interfaces:**
- Consumes: the 12 `serve_url`s from `render_preview` calls across Tasks 2–4 (re-call `render_preview` per file here to get fresh URLs — they're short-lived).
- Produces: 12 PNG files, ready for Task 7's Google Slides upload.

- [ ] **Step 1: Get fresh preview URLs**

For each `keynote/slide-0N.html`, call `mcp__claude-design__render_preview` and collect the `serve_url` (internal use only — never print these URLs in user-facing text, per the tool's own instructions).

- [ ] **Step 2: Screenshot each at exactly 1920×1080, no browser chrome**

Use whichever browser automation is already loaded this session (Playwright MCP or claude-in-chrome) to navigate to each `serve_url` with viewport set to 1920×1080 and take a full-viewport screenshot (not an element screenshot — each HTML page IS one slide at that exact size, so a viewport screenshot captures it cleanly with zero cropping math). Save each to `/tmp/keynote-render/slide-0N.png`.

- [ ] **Step 3: Verify — spot check 3 of the 12**

`Read` slide-01, slide-06 (the corrected-stats slide), and slide-10 (the corrected-line-count slide) PNGs directly. Confirm: full 1920×1080 frame captured with no browser UI, no cut-off text, corrected numbers visible and legible.

---

### Task 7: Rebuild the Google Slides deck from 17 slides to the new 12

**Files:**
- Modifies: the live Google Slides presentation `1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0` in place (no new presentation created — same shareable link stays valid).

**Interfaces:**
- Consumes: the 12 PNGs from Task 6, plus each slide's speaker-notes text (compose these now from the spec's per-slide content — one paragraph per slide restating the key talking points, since the live deck's existing speaker notes belong to the old 17-slide structure and don't map 1:1 to the new order).

- [ ] **Step 1: Snapshot current state before mutating**

```bash
gog slides list-slides 1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0 --plain
```
Save this output — it's the rollback map (17 object IDs) if anything goes wrong mid-rebuild.

- [ ] **Step 2: Delete all 17 existing slides**

```bash
for id in p1 p2 p3 p4 p5 p6 p7 p8 p9 p10 p11 p12 p13 \
  gogDup1787511898481717000 gogDup1787511898179438000 \
  gogDup1787511895021702000 g3e3f9b94856_0_0; do
  gog slides delete-slide 1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0 "$id" -y
done
```
Google Slides presentations can't have zero slides — if the last delete fails for that reason, leave one placeholder slide and delete it as the first step of Step 3 instead (after slide 1 of the new deck is added).

- [ ] **Step 3: Add the 12 new slides in order, each with speaker notes**

```bash
gog slides add-slide 1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0 \
  /tmp/keynote-render/slide-01.png \
  --notes "Title slide. 10s. Say your name and framing, move fast."
# ...repeat for slide-02.png through slide-12.png, each with real speaker-note
# text summarizing that slide's key beat (pull from the spec's slide-structure
# table "Content" column — do not leave notes empty).
```
If any placeholder slide from Step 2 remains, delete it now.

- [ ] **Step 4: Verify slide count and order**

```bash
gog slides list-slides 1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0 --plain
```
Confirm exactly 12 slides, in the intended order (spot-check via `gog slides read-slide` on slide 1 and slide 12 to confirm they're the title and closing-question content, not swapped).

---

### Task 8: Final export + full visual verification

**Files:**
- Create (local): `/tmp/keynote-final/deck.pdf`, `/tmp/keynote-final/slide-*.png`

**Interfaces:**
- Consumes: the rebuilt Google Slides deck from Task 7.
- Produces: the evidence artifact proving the deck is real, correct, and matches the spec — same method already used earlier this session to audit the original 17-slide deck.

- [ ] **Step 1: Export to PDF**

```bash
mkdir -p /tmp/keynote-final
gog slides export 1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0 --format pdf --out /tmp/keynote-final/deck.pdf
pdfinfo /tmp/keynote-final/deck.pdf | grep Pages
```
Expected: `Pages: 12`.

- [ ] **Step 2: Render to PNG**

```bash
pdftoppm -png -r 100 /tmp/keynote-final/deck.pdf /tmp/keynote-final/slide
```

- [ ] **Step 3: Read and visually verify every one of the 12 slides**

`Read` each `/tmp/keynote-final/slide-0N.png`. Check against a hard checklist per slide:
- Design tokens present (cream bg, rust accents, serif-italic titles, mono tags) — no drift from Task 1's verified tokens
- Slide 6: PR #7215 card reads 59% and $9.49→$0.086 as clearly separate, non-contradicting metrics
- Slide 6: cache-stability card reads "through turn 11 (checked at turns 1, 5, 9, 10, 11)", not "across 11 turns"
- Slide 10: dice audit reads "1,889 lines", world_logic.py (if present) reads "12,378 lines"
- Slide 10 or 8: agent count matches Task 5's confirmed number, not an unverified "12"
- No text overflow/clipping, no overlapping elements, no lorem-ipsum or placeholder text anywhere

- [ ] **Step 4: Report the result**

Give the user: the deck's unchanged `webViewLink` (same URL as before, since Task 7 edited in place), confirmation of 12/12 slides passing the checklist above (or a list of any that didn't, with what's wrong), and the total slide-time estimate re-confirmed against the spec's ~11.5 min budget.

---

### Task 9 (OPTIONAL, lower priority — do after Tasks 1-8 are done and verified): Author 5 appendix slides

**Files:**
- Create: `keynote/appendix-a1.html` through `keynote/appendix-a5.html`

**Interfaces:**
- Consumes: `keynote/tokens.css` from Task 1.
- Produces: 5 more render-able pages, NOT added to the Google Slides deck's timed 1-12 sequence — appended after slide 12 as slides 13-17, so they exist in the file but aren't part of the rehearsed narrative.

- [ ] **Step 1: Write appendix-a1.html (Agent pyramid)** — full diagram, per spec Appendix table A1, adapted from the original deck's slide 5 (`gog slides read-slide` on the live deck's `p5` or its current equivalent, if still useful as visual reference before it's deleted in Task 7).
- [ ] **Step 2: Write appendix-a2.html (CMUX demo)** — full slide with the YouTube link `qGJZ31t4wj4`, per spec A2.
- [ ] **Step 3: Write appendix-a3.html (Loopcraft)** — "the unit is now the loop, not the message," per spec A3.
- [ ] **Step 4: Write appendix-a4.html (Full 8 bets)** — all 8 items, per spec A4 and the source `ai-coding-advice-2026-08-06.md:928-944`.
- [ ] **Step 5: Write appendix-a5.html (Software-factory quote)** — Cooke/Galow/WorkOS convergence, per spec A5.
- [ ] **Step 6: Render and verify all 5**, same method as Tasks 2-4.
- [ ] **Step 7: Add to the Google Slides deck as slides 13-17**, after Task 7's rebuild is done and verified — same `gog slides add-slide` pattern, appended at the end so the numbered 1-12 flow is undisturbed.

## Self-review notes (from writing this plan)

- **Spec coverage:** all 12 slides from the spec's structure table have a task (Tasks 2–4); all 6 Fixes-table rows have an explicit task step (Task 3 Step 2 for PR #7215 and cache-stability; Task 3 Step 4 for the "130 PRs/week" prohibition; Task 4 Step 2 for both line counts; Task 5 for the agent count); the Snapchat slide content section is fully covered (Task 3 Step 4); the LinkedIn content rules are covered by construction (cold open = story-first per rule 2, slide 11 = artifact-first per rule 1, slide 12 = flat assertion per rule 3, and the spec's rule 4 is a meta-instruction already satisfied by not reusing old slide-video framing).
- **Placeholder scan:** no TBD/TODO left in any task; every step names the exact file, exact command, or exact copy source (the spec doc, cited by section).
- **Type/interface consistency:** `project_id` from Task 1 flows through Tasks 2–6 consistently; the presentation ID `1Zb6sc0HUKOIR-As3fDl68iYEs6FFFrzdi_YVVo89Xa0` and the 17 object IDs in Task 7 Step 2 are the real, verified IDs pulled from `gog slides list-slides` this session, not placeholders.
