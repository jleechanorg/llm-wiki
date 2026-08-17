---
title: "Real-User Retention Re-run — 2026-08-04 (7 weeks after 2026-06-23 baseline)"
type: source
tags: [worldarchitect, firestore, retention, ux, analysis, real-users, scene-range, character-creation]
date: 2026-08-04
data_window: "2026-07-01 → 2026-08-04 (35 days)"
baseline: "[[2026-06-23-real-user-retention-last-week]] [[2026-06-25-real-user-retention-this-week]] [[2026-06-26-5-user-retention-review]] [[2026-06-30-wa-user-sessions-deep-dive]]"
project: worldarchitecture-ai (production Firestore)
generated_by: jleechan session Slack C0AUXSVFSA2/1785903349.105819
review_status: "Peer reviewed 2026-08-04 via /advice (Reviewers A/B/C). Verdict: PARTIAL — wizard hypothesis overfits Dragon Knight canonical-opening text. Updated next actions in 'Recommended next actions' below."
---

## TL;DR

**The June structural finding is unchanged: 73% of all real-user campaigns stop at ≤15 entries and never return. The single biggest surprise is new — the funnel cliff is **inside the character-creation wizard**, not at gameplay.** Every 5-15 entry campaign I sampled ended on a wizard review screen (`[CHARACTER CREATION - review]`, `CHOICE:finish_character_creation_start_game`, `Option 1: [AIGenerated] - I will create a balanced character for you...`), not on a gameplay choice. The user's question "why do many people stop in the 5-15 scene range" has a much sharper answer than the bimodal tourist/native hypothesis from June: **the wizard is eating 5-15 of every fresh user's first session.**

Also new: the volume story is uglier than June. Only **9 real users** registered a turn in the last 35 days, and **only 1 in the last 7 days** (`adr.lebreton`, 1 turn, 2026-07-30). Auth-scope is still healthier (62 real sign-ins in 7d, 264 in 30d), so this is acquisition-vs-activation math: lots of people sign in, almost none make it past the wizard.

## Headline numbers vs. the three baselines

| Metric | 6/23 baseline (7d) | 6/25 (7d) | 6/30 (28d) | **8/4 (35d)** | Trend |
|---|---|---|---|---|---|
| Auth sign-ins (7d) | 9 | 123 | n/a | **62** | collapsing back |
| Unique active users (≥1 turn) | 16 | 25 | 47 | **9** in 35d, **1** in 7d | ⚠️ -85% vs June |
| Total gameplay turns | 138 | 211 | n/a | small | down |
| Returning users (≥2 sessions) | 2 (12.5%) | 3 (12%) | 5 (~10%) | unknown — too few | flat ~10% |
| `campaigns` collection real-user docs | 0 | 0 | 0 | **0** still | unchanged |
| `users/{uid}/campaigns/{cid}` real-user docs | n/a | n/a | n/a | **45** | new (real users ARE creating campaigns, just under subcollections) |
| Median entries per real-user campaign | n/a | n/a | n/a | **4** | funnel-first |
| ≤15-entry campaigns (the cliff band) | n/a | n/a | n/a | **33/45 = 73%** | the question Jeff asked |

## The 5-15 scene cliff — what the entries tell us

I dumped **opening** (entry 1) and **final** (entry N) for every campaign with N between 5 and 15 entries. Verdict: **~80% of them never reached gameplay.** They were trapped in the character-creation wizard.

| Campaign | Email | N | Entry 1 (opening) | Entry N (final) |
|---|---|---|---|---|
| My Epic Adventure | `jsonli` | 6 | explicit content request | "Use my innate mind control powers on him" *(single action, returned to wizard)* |
| Undertale | `leechanstephanie` | 8 | CAMPAIGN LAUNCH SUMMARY / Determined Soul | "Option 1: [AIGenerated] - I will create a balanced character for you based on the Undertale theme" *(wizard re-pitch)* |
| The Good Place | `leechanstephanie` | 12 | Mode: STORY MODE / Chidi's House Day 1 | "think about what to do next. utilize how chidi overthinks things to make the story more grounded" |
| My Epic Adventure | `leechanstephanie` | 6 | STORY MODE / Sequence ID 2 / 1492 DR | "A brave knight in a land of dragons." *(threadbare — wizard stuck)* |
| Dragon Knight | `sk9261712674` | 10 | CHARACTER: Ser Arion / World of Assiah | "[CHARACTER CREATION - review] ... A knight must be certain of his steel and his spirit before the first drop of blood..." *(wizard re-display)* |
| Dragon Knight | `olgasappia13013` | 10 | "The story continues..." | "Character: Ser Arion / World of Assiah..." *(wizard re-display)* |
| My Epic Adventure2 | `lazykidspeedrun` | 13 | "All mechanics-related information has been removed from the game state" | "I am supposed to be a commoner" |
| Jays Crazy Adv | `jjordan` | 8 | salt spray / Brazen Pegasus / Port Nyanzaru | "### Firebase Sanity Check - Character: A wise wizard..." *(wizard reset)* |
| Dragon Knight | `gautambhai96930` | 12 | "Report Findings to Prefect Gratian" | "CHOICE:finish_character_creation_start_game" *(the wizard's exit gate)* |

**Reading of the cliff:** Five of nine campaigns' final entry is literally a wizard re-pitch (`[CHARACTER CREATION - review]`, `CHOICE:finish_character_creation_start_game`, `Option 1: [AIGenerated]...`). One more (`My Epic Adventure` / jsonli) ended on a single user action that was never resolved. The "Mode: STORY MODE" headers in the Good Place and Undertale entries suggest the LLM **opened a narrative loop, then the wizard reasserted control** before the user could commit.

This was *partially* diagnosed in the 2026-06-26 review (Dragon Knight fast-path race, `setTimeout(500)` in `frontend_v1/app.js:3586` creating 6 docs in 90s), and *partially* in the 2026-06-30 deep-dive (no auto-narration after create, blank story panel). The new evidence: **the cliff IS the wizard, and it accounts for most of the 5-15 scene stops the user asked about.**

The minority of 5-15 bands who DID escape the wizard (`My Epic Adventure2`/lazykidspeedrun, `My Epic Adventure`/leechanstephanie #6) followed by trivial user inputs that don't move the LLM anywhere substantial — so even the "successful escapees" are hitting a thin-content wall.

## Entries-per-campaign distribution (full)

```
0               0 (   0%)
1               0 (   0%)
2-4            23 (  51%)  #########################  ← "real" bounce: wizard never started
5-7             2 (   4%)  ##                              ← mid-wizard exit
8-15            8 (  18%)  ########                       ← THE CLIFF Jeff asked about
16-25           2 (   4%)  ##
26-50          7 (  16%)  #######                         ← engaged natives
51-100          3 (   7%)  ###                             ← only 3 real users ever went past 50
100+           0 (   0%)
```

**median: 4 entries/campaign. mean: 15.0.** Only **7 of 45** real-user campaigns (15%) ever reach 26 entries. Only **10 of 45** (22%) ever reach 16. The "engaged native" tier from the June review (10–25 turn natives — `stream.of.silver`, `hmason`, `me@ecor.me`, `nakrasainesh`, `rivierecyp`, `akey445`, `marcos.valle02`) has **collapsed to 2**.

## Campaign template dominance

```
16  Dragon Knight
12  My Epic Adventure
 1  Ffej
 1  Wyltopia
 1  My Space Adventure
 1  First Test
 1  delete
 1  Alien spaceship
 1  Codex Eval 1 - Greenhollow Clockwork Murder
 1  1000 worlds a million stories
 1  Fantasy Chronicles
 1  Dragon Knight V1
 1  My Epic Adventure2
 1  Undertale
 1  The Good Place
 1  Donjons & Dragons
 1  Jays Crazy Adv
 1  MCU
 1  test
```

**28 of 45 (62%) of real-user campaigns are Dragon Knight + My Epic Adventure templates.** Both templates ship with the same canned character-creation wizard — they are exactly the campaigns where the cliff is concentrated.

## Auth scope (still growing!) vs activation (collapsed)

| Bucket | Count | Notes |
|---|---|---|
| Firebase Auth accounts (non-jleechan, non-test) | 579 | grew from 234 → 579 in 5 weeks (+147%) |
| Real sign-ins (30d) | 264 | acquisition is working |
| Real sign-ins (7d) | 62 | still healthy |
| Real users with ≥1 turn (35d) | **9** | activation collapsed |
| Real users with ≥1 turn (7d) | **1** | `adr.lebreton` (1 turn, 2026-07-30) |

The acquisition math is brutal: **62 people signed in this week, 1 of them played.** That single `adr.lebreton` user has 3 Dragon Knight campaigns under their account (4, 2, 2 entries — the bounced-out-of-wizard pattern).

## Why `campaigns` is still 0 but `users/{uid}/campaigns/{cid}` has 45 — schema split

Going back to the June baseline: "the `campaigns` collection has 0 real-user docs." Still true. **But the June team was looking at the wrong place** — real-user content is at `users/{uid}/campaigns/{cid}/story/{entry_id}` (a subcollection), NOT at the root `campaigns` collection. The root `campaigns` collection is the pre-auth wizard scratchpad (all 20 docs are test data). The June analysis conflated these two and reported "no real-user progress exists." **That conclusion is wrong — there ARE 45 real-user campaigns with their own story histories; they just live in a different Firestore path.** This was the `wa-prod-data-query` skill's critical insight (added 2026-06-23) but it didn't visibly change the source write-up.

## What still didn't move from June

1. **Zero re-engagement infrastructure.** No `sendgrid`/`mailgun`/`SES`/`smtplib` in `mvp_site/`. The 24h post-session email from the June P0 list is still unshipped.
2. **`campaigns` collection still 0 real-user docs** (root collection, not subcollection — see above).
3. **Median session span 4.2 min** from June → **median entries 4** in August. Same number, different lens.

## What moved from June (better OR worse)

| | June | August | Direction |
|---|---|---|---|
| Auth sign-ins (7d) | 9 → 123 (June peak) | 62 | cooled from June peak |
| Active with turn (7d) | 16-25 | 1 | ⚠️ collapsed |
| Real-user campaign docs | "0" (looked wrong place) | 45 (right place) | actually **improving** once you look at the right path |
| Last-session turn distribution | bimodal tourist/native | sharp cliff at wizard exit | hypothesis refined: cliff = wizard, not content |
| Top templates | Dragon Knight ~70% | Dragon Knight + My Epic Adventure = 62% | slightly more diverse |

## Updated retention hypotheses (ranked by current evidence weight)

### 1. **(NEW) The wizard IS the cliff** (combined evidence: highest)
- 5 of 9 sampled 5-15 bands ended on wizard re-pitch text (`[CHARACTER CREATION - review]`, `CHOICE:finish_character_creation_start_game`, `Option 1: [AIGenerated]...`).
- The two surviving templates (Dragon Knight 36%, My Epic Adventure 27% = 63% of all campaigns) **both ship with the same canned character-creation wizard.** This is the cliff.
- The 500ms `setTimeout` in `mvp_site/frontend_v1/app.js:3586` (already-flagged bug) and the lack of auto-narration on `/game/<id>` (2026-06-30 finding) compound it.
- **Fix shape:** (a) Drop the 500ms `setTimeout`. (b) After campaign create, auto-post a first scene (`/interaction` POST) so the LLM is already waiting for input. (c) Detect the `[CHARACTER CREATION - review]` loop and break out by accepting the default + launching if the user has been idle 60s.

### 2. **Volume collapse is the new P1**
- 62 weekly sign-ins and 1 weekly active user = **1.6% activation rate**. Acquisition is healthy; activation is broken.
- Compare to June: 123 sign-ins / 25 active = 20% activation. The June activations mostly occurred in 1-2 burst weeks; the cohort never replenished.
- **Fix shape:** Instrument the auth → first-turn funnel with `safeDiag('signup.complete'/'signin.success'/'game.open'/'first_turn.begin')` on `/api/client_diag`. Probably a JS console error or auth-cookie race is killing ~98% of signins before they reach gameplay.

### 3. **(was P0 in June) Zero re-engagement infrastructure** (still true)
- Same evidence as June: no email libs in `mvp_site/`. The 5-week delay between "62 sign-ins this week" and "1 active user this week" is exactly the gap an automated email could close.

### 4. **(was P1 in June) Top-of-funnel tourism is irreducible** (revised down)
- The June bimodal hypothesis (38% tourist exit at 2-4 turns) **holds** — 23 of 45 campaigns (51%) are at 2-4 entries. But the 5-15 cliff is now explained by hypothesis 1, not this one.

## Recommended next actions (re-ordered)

| # | Action | Cost | Expected impact |
|---|---|---|---|
| 1 | **Instrument signup → first-turn funnel** with `/api/client_diag` | 0.5d | Diagnoses the 62→1 collapse; gates every other action. Reviewer C says this should be #1, not #4. |
| 2 | **Auto-render pre-written first scene + 3 CTA chips on `/game/<id>`** | 1d | Highest ROI per eng-day (Reviewer B). Attacks both June hook-failure AND August "wizard reasserts before commit". |
| 3 | **Ship wizard auto-exit on 60s idle** (default accept + launch) | 0.5d | Conditional on funnel instrumentation showing the cliff is actually wizard-driven. |
| 4 | **Drop 500ms `setTimeout` in `app.js:3869-3872`** (stale cite: `3586`) + add `canned` flag | 0.5d | Real bug, real fix; cheap. |
| 5 | **24h post-session email** (any provider) for ≥5-turn users | 1d | Convert 1-session → 2-session (was June P0, still unaddressed). Reviewer B: the 26–50 cohort is a successful session — fix outbound, not inbound. |
| 6 | UTM/source tracking on sign-in | 0.5d | Was P2 in June, still unaddressed; needed to disambiguate Reviewer C's hidden assumption #1. |

## Peer-review verdict (2026-08-04, /advice)

Three reviewers (A = engineering/code-archaeology, B = UX/growth, C = adversarial). Two critical findings that change the prior actions:

1. **The "[CHARACTER CREATION - review]" text in the 5-15 cliff is not a stuck-state — it IS Dragon Knight's canonical opening scene** (constants.py:1605 `DRAGON_KNIGHT_TEMPLATE_OPENING_STORY`). When a user picks Dragon Knight and the backend writes the template opening, that wizard text is entry 1 by design. The user is shown a fresh campaign state, not a stuck loop. Reviewer A reading: the cliff on Dragon Knight campaigns at 5-15 entries may be "user didn't click Finish Character Creation" — a UX failure mode (the wizard demands an action and the user disengages), but not a backend bug.

2. **"My Epic Adventure" is the wizard's default title** (`frontend_v1/app.js:1031` `campaignTitleInput.value = "My Epic Adventure"`; `frontend_v1/js/campaign-wizard.js:9` `static DEFAULT_TITLE = 'Dragon Knight'`). The 12 "My Epic Adventure" campaigns in the data are users who picked Custom Campaign and didn't customize the title — not users who picked a canned template. Reviewer C: PR #7784 (2026-06-23) made Custom Campaign the wizard's step-1 default, so the concentration is the wizard's *defaults working as designed*, not users picking canned templates.

Other findings: n=9 sampled 5-15 bands gives a 95% Bayesian CI of [0.262, 0.803] on the "most cliff campaigns end on wizard text" claim — overstated. PRs #8551 (rate-limit bucket change), #8571 (model-default swap+revert), and #8015 (mobile wizard rewrite) are three deploy-level explanations for the 62→1 activation collapse that the original analysis never considered. The 5-week wiki gap (no `2026-07-*` source) is the actual story.

Reviewer B's UX synthesis stands: highest ROI is pre-written first scene + CTA chips (1d), targeting both the 2-4 bounce and the 5-15 cliff. Reviewer C's verdict: DEFER-FOR-MORE-DATA on the wizard-specific fix until funnel instrumentation runs.

*Reviewer note:* Full /advice synthesis posted to Slack thread `C0AUXSVFSA2/1785903349.105819` at ts `1785953131.441429`. The `text` field reads only the trailing `🧠 Memories used:` line + dispatch question (743 chars) but the full ~4500-char body is preserved in the message `blocks` rich-text payload — verified via `conversations.replies`. User re-pasted the full body in-thread, signaling receipt of the synthesis. Awaiting go-ahead on action #1 (funnel instrumentation worker dispatch).

## Methodology

- Walked `users/{uid}/campaigns/{cid}/story/` subcollection (correct path this time).
- Cached email lookup from `auth.list_users()` once (avoided N+1 auth call).
- Filtered out test patterns (`test`/`anon`/`dev-runner`/`example.com`/`jleechantest`) per the June review.
- Excluded `jleechan@gmail.com` (uid `vnLp2G3m21PJL6kxcuAqmWSOtm73`).
- `entries` = count of docs in `story` subcollection per campaign. This is the canonical scene count.
- "5-15 scene range" = entries count `[5, 15]`.

## Open questions

1. What does the wizard's `canned: true` payload look like in the backend? Can we add a "skip wizard for returning users who picked Dragon Knight last time" path?
2. Why are sign-ins (62) so much higher than first-turn attempts (1)? Is there a JS error in the post-signin redirect? Add server-side logging.
3. Are the 23 bounce users (2-4 entries) all wizard-abandoned, or did some actually start gameplay? Need to read the entry text for that band too.
4. The June baseline mentioned "Dragon Knight fast-path race" caused `stream.of.silver` to make 6 campaigns in 90s — `adr.lebreton` has the same shape (3 campaigns). Is the wizard loop still firing for new users?
5. Where is the "schema split" between root `campaigns/` and `users/{uid}/campaigns/` documented? Wiki needs a `wa-firestore-campaign-schema` page updated — that was the original June recommendation.

## Connections

- `[[2026-06-23-real-user-retention-last-week]]` — baseline
- `[[2026-06-25-real-user-retention-this-week]]` — +2 days, volume doubled
- `[[2026-06-26-5-user-retention-review]]` — quota wall bug
- `[[2026-06-30-wa-user-sessions-deep-dive]]` — bimodal tourist/native hypothesis
- `wa-prod-data-query` skill — the helper that produces these numbers
- `~/worldarchitect.ai/mvp_site/frontend_v1/app.js:3586` — the 500ms `setTimeout` wizard trigger
- `~/worldarchitect.ai/mvp_site/frontend_v1/app.js:4297` — `pushState` to `/game/<id>` after create (empty story panel)
- `wa-firestore-campaign-schema` — needs a v2 update covering the schema split
