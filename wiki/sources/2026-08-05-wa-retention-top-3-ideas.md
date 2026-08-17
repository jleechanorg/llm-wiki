---
title: "WA Retention — Top 3 Improvement Ideas (2026-08-05)"
type: source
tags: [worldarchitect, retention, top-3, action-plan, decision-doc]
date: 2026-08-05
based_on: "[[2026-08-04-wa-retention-7-weeks-later]]"
project: worldarchitecture-ai (production Firestore)
generated_by: jleechan session Slack C0AUXSVFSA2/1785903349.105819
audience: operator / decision
---

# Top 3 Retention Improvements — WA (2026-08-05)

**TL;DR:** Three concrete fixes, ordered by ROI per engineering day. Funnel instrumentation (#1) gates the other two — without it, we're guessing. The pre-written first scene (#2) has the highest ROI *per day* regardless of which hypothesis is right. The 24h email (#3) was the June P0 and is still unaddressed.

## Headline data this is grounded in

- 62 signins in last 7 days; only **1 active user** in last 7 days (1.6% activation)
- 45 real-user campaigns under `users/{uid}/campaigns/{cid}/story/`
- 33/45 (73%) of campaigns stop at ≤15 entries; only 7 of 45 reach 26 entries
- Zero re-engagement infrastructure (no email libs in `mvp_site/`)
- Five deploys between 6/23 and 8/04 (PRs #7784, #8015, #8290, #8551, #8571) touch the signin→first-turn path — none verified as the activation-collapse cause

---

## #1 — Instrument the signup → first-turn funnel (0.5d)  *GATING ACTION*

**The problem we can't see:** Of 62 signins in the last 7 days, only 1 played. We don't know *where* the 61 silent ones dropped. Could be JS error post-signin redirect, empty `/game/<id>` blank-page moment, rate-limit bucket silently failing, or wizard friction. We have four competing hypotheses and zero instrumentation to distinguish them.

**The fix:** Wire five `safeDiag()` events through the existing `/api/client_diag` Cloud Logging sink at `main.py:4025` and `main.py:3999` (Reviewer C in June already proposed this; it's still missing):

```python
safeDiag('signup.complete', {...})     # Firebase Auth success
safeDiag('signin.success', {...})      # Cookie set, redirect to /
safeDiag('game.open', {...})           # URL change to /game/<id>
safeDiag('first_turn.begin', {...})    # User typed + submit clicked
safeDiag('first_turn.outcome', {...})  # Got 200 with non-empty story? 5xx? quota?
```

**Cost:** 0.5 eng-day. Pure instrumentation; no new vendor, no new endpoint. The sink already exists.

**Expected effect within 48 hours of prod:**
- Tells us which of the 5 deploys (or which non-deploy factor) is killing the 61 silent signins
- Tells us whether the 5-15 cliff is wizard-driven (users reach `first_turn.outcome` and *then* quit) or upstream (users never reach `first_turn.begin`)
- Lets us re-prioritize #2 and #3 based on what we actually see

**Why #1:** Every other retention fix is a guess without this. Reviewer C called this out as "the only action worth landing before we know the actual cause." Reviewer B agreed: "62→1 activation gap deserves instrumentation first, not intervention."

**Risk:** None measurable. Pure logging.

---

## #2 — Auto-render a pre-written first scene + 3 CTA chips on `/game/<id>` (1d)  *HIGHEST ROI PER DAY*

**The problem:** When a user lands on `/game/<id>` after creating a campaign, the story panel is *empty* (`frontend_v1/app.js:3862` pushState, `app.js:3869-3872` 500ms setTimeout, no auto-`/interaction` POST). Dragon Knight campaigns get a canned opening from the backend template (constants.py:1605 `DRAGON_KNIGHT_TEMPLATE_OPENING_STORY`) so DK users see something. *Custom campaigns get nothing.* The blank panel is the moment where users (a) close the tab, (b) type something and lose it to nothing, or (c) the wizard re-asserts with `[CHARACTER CREATION - review]` re-pitch and the user gives up.

**The fix:** On `handleRouteChange()` landing on `/game/<id>` for a campaign with empty `story` array:

```js
// Pseudo: if backend didn't write an opening scene, render one
if (data.story.length === 0) {
  const openingSeed = buildOpeningFromTemplate(data.template, data.setting);
  appendToStory("assistant", openingSeed);  // "You stand at the entrance of [Setting]. Before you lies..."
  renderCTA([
    "Explore cautiously",      // → safe exploration
    "Ask a question",          // → social / lore query
    "Take a bold action",      // → dramatic action
  ]);
}
```

**Cost:** 1 eng-day. Frontend-only. No new LLM call. Reuses existing `appendToStory` and CTA components.

**Expected effect:**
- Recovers ~30-50% of the 23/45 "real bounce" (2-4 entries) cohort (Reviewer B)
- ALSO attacks the 5-15 cliff (custom-campaign users who bounce when wizard re-fires — give them a non-wizard beat to engage with)
- Reviewer B verdict: "highest ROI per eng-day. Attacks both June hook-failure and August wizard-trap."

**Why this works:** The blank `/game/<id>` panel is the *one* UX moment that affects all 45 real-user campaigns regardless of template choice. Dragon Knight bypasses it via the backend template; everything else hits it.

**Risk:** Low. The user can dismiss or override the CTA. Engaged natives won't notice.

**Conditional on #1:** If funnel instrumentation shows most users *never reach* `/game/<id>`, this fix is wasted. Ship #1 first.

---

## #3 — Ship a 24h "story-in-progress" email for ≥5-turn users (1d + vendor)  *REVENUE-NEUTRAL BUT UNADDRESSED FOR 7 WEEKS*

**The problem:** Zero re-engagement infrastructure. The June deep-dive flagged this as P0 ("9 of 42 one-session users played 10-25 turns over 20-89 min and never returned"). It's still unaddressed 7 weeks later. The 7 users at 26-50 entries (engaged natives) and the 2 users at 16-25 entries are *successful sessions by every standard product metric* — 30-90 min, 2-4× AI Dungeon's depth — but they don't come back because there's no hook to bring them back.

**The fix:** Pick any email provider (Resend/SendGrid/SES — Resend is cheapest at 100 emails/day free). Template:

```
Subject: You stood at the Thornwood. The stranger was still waiting.
Body: [1-sentence story-state teaser from last entry]
      [1-click "Resume your story" CTA → /game/<cid>]
      [Unsubscribe footer]
```

Trigger: 24h after the user's last session, only if they had ≥5 turns.

**Cost:** 1 eng-day for vendor integration + template + unsubscribe flow + cron. One-time provider setup.

**Expected effect:**
- Industry baseline D1 re-engagement email CTR is 8-15%. Even 10% resume on the 16-50 tier roughly doubles current returning-user counts.
- Converts 1-session → 2-session users, which is the *only* cohort we have evidence of being warm enough to come back (June: 5 multi-session users all came back within 0.7-7.7h).
- Reviewer B: "the 7 natives are the *cheapest cohort to retain* — they self-selected as engaged."

**Why this works:** Email is the *only* off-platform surface we have. In-app notifications die with the tab. Email survives the closed browser.

**Risk:** Must include unsubscribe and stay under CAN-SPAM thresholds. Otherwise users report spam, domain reputation tanks.

**Not conditional on #1:** This is outbound; it works regardless of where users drop on the signup funnel. *This is the one action we could parallelize with #1 if eng capacity allows.*

---

## Why not the other 6 actions from the original list?

| Action | Why deferred |
|---|---|
| Wizard auto-exit on 60s idle (0.5d) | *Conditional on #1.* The wizard hypothesis is downgraded (the "[CHARACTER CREATION - review]" text is Dragon Knight's canonical opening scene, not a stuck loop). Without funnel data, this is a guess. |
| Drop the 500ms `setTimeout` in `app.js:3869-3872` (0.5d) | Real bug, but isolated to Dragon Knight fast-path race. Doesn't address the 62→1 collapse or the 5-15 cliff. Land after #1 shows where the actual breaks are. |
| Auto-post first scene after campaign create (1d) | Superseded by #2. Same effect, larger scope. |
| UTM/source tracking on sign-in (0.5d) | Was P2 in June, still unaddressed. Needed to disambiguate Reviewer C's hidden assumption #1 ("stable user mix"). Doesn't fix retention directly. |
| Mobile wizard rewrite (already PR #8015) | Already shipped 7/18. Verify in prod before more wizard work. |
| Pre-built "skip wizard for returning DK users" path (1d) | Cool idea, but custom logic — needs product call on whether returning users want the wizard at all. Save for later. |

## Open decision points

1. **Email provider choice** — Resend vs SendGrid vs SES vs Postmark. Recommend Resend (cheapest at low volume, React Email templates). Need operator call.
2. **Email subject line tone** — Adventure ("The stranger was still waiting") vs utility ("Your story awaits") vs personalized (uses character name). Recommend adventure tone for ≥10-turn users, utility for 5-9.
3. **CTA chip text** for #2 — needs product call. Current suggestion: explore / ask / act.
4. **Sequencing** — ship #1 first (0.5d, gates everything), then #2 and #3 in parallel (or pick one if eng capacity is 1).

## Methodology / how to verify

After #1 ships and 48h of prod data, re-run the retention queries and check:
- What % of signins actually reach `first_turn.outcome`?
- Of those who do, what % return within 24h?
- Did the 5-15 cliff rate change? (Probably not from #1 alone — instrumentation alone doesn't change UX.)

After #2 ships and 1 week of prod data, check:
- Did the 2-4 bounce rate drop? (Expected: yes, 30-50% recovery)
- Did the 5-15 cliff rate drop? (Expected: yes, modest — for custom-campaign users specifically)

After #3 ships and 1 week of prod data, check:
- D1 re-engagement rate for ≥5-turn users
- Did the 1-session → 2-session rate go from ~10% (June) to ≥20%?

## Connections

- `[[2026-08-04-wa-retention-7-weeks-later]]` — full evidence base
- `[[2026-06-30-wa-user-sessions-deep-dive]]` — June P0 list, still mostly unaddressed
- `wa-prod-data-query` skill — the data walker
- `mvp_site/main.py:4025`, `main.py:3999` — `/api/client_diag` sink
- `mvp_site/frontend_v1/app.js:3862`, `app.js:3869-3872` — empty `/game/<id>` create path
- `mvp_site/constants.py:1605` — Dragon Knight canonical opening (Dragon Knight users get this; nobody else does)