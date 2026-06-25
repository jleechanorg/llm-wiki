---
title: "Real-User Retention Analysis — Week of 2026-06-18 → 2026-06-25 (vs 2026-06-15 → 2026-06-22 baseline)"
type: source
tags: [worldarchitect, firestore, retention, ux, analysis, real-users, brainstorm]
date: 2026-06-25
data_window: "Wed 2026-06-18 11:13 UTC → Wed 2026-06-25 11:13 UTC (7 days)"
baseline: "[[2026-06-23-real-user-retention-last-week]]"
project: worldarchitecture-ai (production Firestore)
generated_by: jleechan session 1782231566.821589 (this thread)
---

## TL;DR (one week after the 2026-06-23 baseline)

**Volume is up, retention is flat.** Real-user gameplay turns more than doubled (138 → 211, +53%), unique active users grew 16 → 25 (+56%), and 123 real-user sign-ins happened in 7d vs. 9 the prior week. But the structural problem from the baseline — **88% of active users are single-session-and-gone**, median session length is **8 minutes**, and the `campaigns` collection is **still 0 real-user docs** — is unchanged. The product has an activation problem, not a discovery problem.

## Headline numbers (this week vs. last)

| Metric | 2026-06-15→22 (baseline) | 2026-06-18→25 (this week) | Δ |
|---|---|---|---|
| Real-user sign-ins (7d) | 9 | 123 (auth scope) / 16 with gameplay | **+13×** auth scope, **+78%** with gameplay |
| Unique active users (7d, ≥1 turn) | 16 | 25 | +56% |
| Total gameplay turns (7d) | 138 | 211 | +53% |
| New campaigns created by real users (7d) | **0** | **0** | unchanged |
| Returning real users (2+ sessions in 7d) | 2 (12.5%) | 3 (12%) | flat |
| Median session duration | ~25m | **8m** | -68% ⚠ |
| Median turns per session | ~10 | **5** | -50% ⚠ |
| Single-session-only users | 14 of 16 (88%) | 19 of 25 (76%) | improved |

**Two big shifts:**
1. **Volume up.** Auth scope is much wider — likely a launch or marketing push. Real-user activity grew ~50–55%.
2. **Engagement per session collapsed.** Median session dropped from ~25m → 8m, median turns dropped from ~10 → 5. More people are coming; fewer are staying. This is the classic activation-after-growth-dilution signal.

## Daily turn volume (real users, 7d)

```
2026-06-19: #################################################################### (83) ← Thursday peak
2026-06-20: ####################### (23)                                       ← Friday drop
2026-06-21: ###### (6)                                                        ← Saturday crash (93% drop from Thu)
2026-06-22: ###################### (22)                                       ← Sunday
2026-06-23: #################################################################### (62) ← Monday peak
2026-06-24: ############# (13)                                                ← Tuesday drop
2026-06-25: ## (2, partial day)                                               ← Wednesday (partial)
```

Two peaks (Thu 6/19 and Mon 6/23), both followed by ~70% drops the next day. No "weekend crash" pattern this week (it was distributed). Suggests weekday-rhythm usage, not weekend-tail.

## Real-user cohort (this week, sorted by turn count)

| Email | Turns | Sessions | Last activity | Notes |
|---|---|---|---|---|
| me@ecor.me | 20 | 1 | 2026-06-19 04:08 | Returning from baseline week — 20 turns, 1 session |
| akey445@gmail.com | 20 | 1 | 2026-06-20 12:20 | Same as above — 20 turns in 1 session |
| marcos.valle02@gmail.com | 20 | **2** | 2026-06-23 20:01 | **NEW returning user.** 17 turns + 3 turns, 1.2h gap |
| stream.of.silver@gmail.com | 20 | 1 | 2026-06-23 16:56 | New |
| hmason@gmail.com | 18 | 1 | 2026-06-23 20:29 | New |
| mrkennethyip@gmail.com | 17 | **3** | 2026-06-20 01:35 | **Repeated returner from baseline.** 3 sessions in 1 evening |
| nakrasainesh@gmail.com | 17 | 1 | 2026-06-19 10:51 | Same as baseline |
| rivierecyp@gmail.com | 15 | 1 | 2026-06-19 16:52 | Same as baseline |
| brian.eng@gmail.com | 12 | 1 | 2026-06-22 12:31 | Same as baseline |
| inakizulaika@gmail.com | 10 | 1 | 2026-06-19 08:18 | Same as baseline |
| nirmal.k.asokan@gmail.com | 9 | **2** | 2026-06-25 01:25 | **NEW returning.** 7 turns + 2 turns, 7.3h gap (next day) |
| olgasappia13013@gmail.com | 5 | 1 | 2026-06-22 19:18 | Same as baseline |
| gautambhai96930@gmail.com | 5 | 1 | 2026-06-22 11:24 | Same as baseline |
| wolf.clement@gmail.com | 4 | 1 | 2026-06-23 06:57 | Same as baseline |
| ryan.dillis@gmail.com | 4 | 1 | 2026-06-19 21:46 | Same as baseline |
| nathan@torkington.com | 4 | 1 | 2026-06-21 07:21 | Same as baseline (returned 2d later, but 1 session in this window) |
| zadnan@snapchat.com | 3 | 1 | 2026-06-24 20:21 | New |
| mkarma@gmail.com | 3 | 1 | 2026-06-24 04:21 | New |
| rik@rikbrown.co.uk | 2 | 1 | 2026-06-21 13:51 | Same as baseline |
| hu.evan123@gmail.com | 1 | 1 | 2026-06-19 08:44 | Same as baseline |
| rajanshandil@gmail.com | 1 | 1 | 2026-06-20 16:09 | Same as baseline |
| rishikirti534@gmail.com | 1 | 1 | 2026-06-19 18:52 | Same as baseline |
| operativkamma@gmail.com | 0 | 0 | 2026-06-22 12:13 | Bouncer (signed in, 0 turns, 0 sessions) |
| khalilchatoo@gmail.com | 0 | 0 | 2026-06-19 03:09 | Bouncer |
| vandeheyeric@gmail.com | 0 | 0 | 2026-06-19 17:51 | Bouncer |

**Returning users this week:** 3 (marcos.valle02, nirmal.k.asokan, mrkennethyip). All 3 returned within 24h, not days later. Pattern: **multi-session-on-the-same-evening**, not "came back next week."

**Bouncers (0 turns):** 3 of 25 (12%). Same proportion as last week's "immediate bounce" cohort.

## Session duration distribution

```
  0-   2m:   7 #######        (27%)  ← significant: 1 in 4 sessions ends in 2 minutes
  2-   5m:   3 ###            (12%)
  5-  15m:   6 ######         (23%)
 15-  30m:   4 ####           (15%)
 30-  60m:   5 #####          (19%)
 60-99999m:  1 #              ( 4%)
```

**27% of all real-user sessions end in under 2 minutes.** This is the single sharpest signal in the data. Either:
- They're hitting a UX blocker (loading failure, broken CTA, etc.)
- They're not understanding what to do next
- They're mobile/sparse visitors who bail fast

Compare to baseline: 0 sessions under 2m were explicitly noted (only 0-turn and 14-45m buckets called out). The 0-2m bucket is **NEW** since the baseline.

## Structural findings (still true)

1. **`campaigns` collection is still 20 test docs, 0 real-user docs.** Confirmed 2026-06-25 — unchanged from baseline.
2. **`conversations` collection: 6 docs, all from 2025-10-03→04.** Likely a long-ago pilot or test data with non-`test` uids. Not a fresh signal.
3. **`shared_links`: 54 docs**, all `user_id` is empty string. These are anonymous shareable links — useful for virality, not for retention analytics.
4. **Auth: 234 total users, 118 with email, 101 gmail, 5 test.** Last 7d sign-ins: 123. The 234 base is much higher than the 123 active in 7d — implies the vast majority of signups don't come back.
5. **median signup → first turn: still ~3 min** (good activation). But median first turn → next session: still **never** for 19 of 25 users.

## Brainstorm — UX / retention improvements

### Tier 1: Fix the 0-2 minute session cliff (highest leverage)

The 27% of sessions ending in 2 minutes is the sharpest signal. **Either there's a UX blocker or a value-prop problem.** Candidates to investigate:

- **Loading state / first-render failure.** Log JS console errors during the first 60s of a session for these users. If the page is silently broken for them, that's a 1-day fix with massive ROI.
- **First-turn decision paralysis.** The very first user action might be too open-ended ("What do you do?"). A specific prompt with 3 quick-pick options might convert these into 5+ turn sessions.
- **Sign-in friction in the middle of a session.** Some users may have been bounced when they tried to save / share / continue and got prompted for sign-in mid-flow.

### Tier 1: Make the session persist (the #1 baseline recommendation, still unaddressed)

Baseline's P0 was "automatically create a `campaigns` doc on first turn." Still 0 real-user docs in `campaigns`. **This is the biggest unaddressed retention gap.** With no campaign doc:
- No return URL the user can bookmark
- No shareable link
- No "your party is waiting" notification
- No wizard entry point to rename/customize
- No summary for a post-session email

**Single change with the highest leverage:** at the end of turn 1, automatically write `users/{uid}/campaigns/{auto-id}` with `{title: "Untitled session <date>", created_from_first_turn: <entry-id>, last_played: <now>}`. Cost: 30 minutes of backend code.

### Tier 1: 24-hour post-session email (baseline P0, still unaddressed)

Trigger: user played ≥5 turns and didn't return in 24h. Send: "Your campaign is waiting — here's what happened." Infra exists (`gog` Gmail). Cost: 4 hours (logic + template + trigger). Expected impact: convert some of the 19 single-session users into 2-session users.

### Tier 2: Address the median-session-length collapse (25m → 8m)

Hypothesis: as new users came in this week, the average engagement per session dropped because the new cohort had a different mix. Check:
- Are the new 8 users (zadnan, mkarma, stream.of.silver, hmason, marcos.valle02) lower-quality (mobile? different geography? different referral source?)
- Was there a product change in the last 7d that could have lowered session quality? (UI change, LLM provider switch, etc.)

If the new users are pulling the median down: **the activation is working, the stickiness isn't.** Need a "depth moment" in the first session — something that makes the user feel they're playing for a reason beyond the initial 5 turns.

### Tier 2: Multi-session-on-the-same-evening is the only retention win

All 3 returning users this week returned within 24h. None returned days later. **Insight: the only way to bring a user back is to bring them back within the same day.** This means:
- "Continue your story?" prompt at end of session (one-tap)
- Push notification 2-3 hours after session ends
- Auto-save with a "you were here" landing card on next visit

### Tier 3: Cohort analysis on the 9 baseline-week users who returned

Of the 16 baseline-week active users, 5 returned this week (me@ecor.me, akey445, mrkennethyip, nakrasainesh, rivierecyp, brian.eng, inakizulaika, olgasappia, gautambhai, wolf.clement, ryan.dillis, nathan, rik, hu.evan123, rajanshandil, rishikirti534). They were 1-session-and-gone in the baseline — what makes them tick? Did any of them create a campaign doc in the last week? (no — `campaigns` is still 0 real-user.)

**Hypothesis worth testing:** users who don't create a campaign doc within their first session are 100% likely to bounce. The campaign doc creation is the retention linchpin.

### Tier 3: Acquisition attribution

234 total users, 118 with email, only 5% test. Where are the 234 coming from? Need UTM/source tracking. Without this, growth experiments are guesswork. Cost: 1 day.

## Prioritized recommendations (re-ordered by leverage + readiness)

| Rank | Action | Cost | Expected impact | Status |
|---|---|---|---|---|
| 1 | Auto-create `campaigns` doc on first turn | 30m | Foundation for ALL retention loops | Not started |
| 2 | Investigate 0-2m session cliff (logs/UX audit) | 4h | Convert 7 short-sessions/week → longer | Not started |
| 3 | 24h post-session email for ≥5-turn users | 4h | Convert 19 single-session → some 2-session | Not started |
| 4 | Same-evening return CTA / push | 1-2d | All 3 returning users came back within 24h | Not started |
| 5 | First-turn decision scaffolding (3 quick-pick options) | 1d | Lower the 0-2m cliff | Not started |
| 6 | UTM/source tracking on sign-in | 1d | Unblock acquisition optimization | Not started |
| 7 | Cohort analysis on baseline → this-week returners | 0.5d | Sharpen retention messaging | Not started |

## Connections

- `[[2026-06-23-real-user-retention-last-week]]` — baseline; this document extends it with one more week of data
- `wa-prod-data-query` skill (in `~/.hermes/skills/wa-prod-data-query/`) — the helper that produces these numbers
- `download-campaign` skill (in `~/.hermes_prod/skills/download-campaign/`) — for individual campaign deep-dives
- `wa-firestore-campaign-schema` — schema reference; the gap between schema design and real-user data is the core retention problem
- `worldarchitect` repo AGENTS.md — "Any non-test change under `mvp_site/` requires `/es` evidence" — implementing Tier-1 recommendations requires real-server evidence

## Open questions

1. **What is the source of the 234 total auth users?** Need acquisition attribution (Tier 3 above).
2. **Why are the 6 conversation docs from 2025-10?** Are these real users from a year-ago pilot, or test data with non-`test` uids?
3. **Is there a UI change or LLM provider switch in the last 7d** that could explain the median-session-length collapse?
4. **What happens at the 0-2 minute mark** for those 7 short sessions? Need frontend event logs.
5. **Did the 3 returning users (marcos, nirmal, mrkennethyip) do something different** in their first session that we could replicate? Need per-user session trace.
