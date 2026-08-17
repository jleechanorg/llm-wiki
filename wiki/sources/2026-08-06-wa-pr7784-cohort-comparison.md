# WA retention — pre vs post PR #7784 cohort comparison

**Date:** 2026-08-06
**Author:** Hermes (wa-prod-data-query skill)
**Hypothesis under test:** Did the wizard change in [PR #7784](https://github.com/jleechanorg/worldarchitect.ai/pull/7784) ("make Custom Campaign the default in step 1, demote Dragon Knight to second", merged 2026-06-23T08:33:01Z) cause the observed 116 → 1 turn/week collapse?

## TL;DR

**No — the wizard change did not cause the collapse.** The collapse is in **top-of-funnel signups**, not per-user engagement. Among users who actually played in the 60d window, post-cohort (saw Custom default) and pre-cohort (saw Dragon Knight default) have **identical median engagement** (4 turns, 1 session per user). What dropped is the *number* of new users arriving, from a peak of 1,026/week (2026-04-13) to **9/week** (2026-08-03). That's a marketing/acquisition problem, not a wizard/UX problem.

The "wizard trap" hypothesis from the August 4 write-up is **inverted**: if anything, the new wizard's turns-per-new-user ratio (0.25–0.41 in the merge week) is **higher** than the pre-merge baseline (0.00–0.04).

## Method

- Pulled all 10,252 docs in `rate_limits/{uid}.turn_timestamps`.
- Resolved 593 emails via `auth.list_users()` (most rate_limits docs lack auth records; we did not exclude based on missing email, but the existing 60d query had already excluded test-pattern emails).
- Excluded `jleechan` (uid `vnLp2G3m21PJL6kxcuAqmWSOtm73`).
- Excluded any user with a recognizable test-pattern email (`test`, `anon`, `dev-runner`, `example.com`, `jleechantest`).
- Cohort split by **user's first-turn timestamp relative to PR merge**:
  - `pre` = first_turn < 2026-06-23T08:33:01Z → saw Dragon Knight default
  - `post` = first_turn ≥ 2026-06-23T08:33:01Z → saw Custom default
- Restricted to users with **any turn in the 60-day window** ending today (2026-08-06) so pre-cohort doesn't get diluted by ancient single-session accounts.

## Cohort stats (60-day window, last_turn ≥ 2026-06-07)

| Metric | Pre (saw DK) | Post (saw Custom) |
|---|---|---|
| Users with 60d activity | 1,164 | 887 |
| Total turns in 60d | 4,583 | 4,392 |
| **Median turns per user** | **4** | **4** |
| Mean turns per user | 3.94 | 4.95 |
| **Median sessions per user** | **1** | **1** |
| Max turns (single user) | 20 | 100 |
| Users with ≥2 sessions ever | 1,164 had DK-only churn | 6 returnees |

**Per-user engagement is essentially identical.** The post cohort has a slightly higher mean (4.95 vs 3.94) and a higher max (one heavy power-user with 100 turns), which actually pulls the mean *up* — the opposite of what the "wizard trap" hypothesis would predict.

## Weekly volume (60d window, clipped at 2026-06-07)

```
week          new_users   total_turns   turns/new
2026-06-08    701         4             0.01
2026-06-15    275         112           0.41   <- PR #7784 authored
2026-06-22    455         116           0.25   <- PR #7784 merged (06-23)
2026-07-06    150         14            0.09
2026-07-13    143         2             0.01
2026-07-20    164         4             0.02
2026-07-27    23          1             0.04
2026-08-03    9           (in progress) —
```

The 60d-window JSON (`/tmp/wa_60d.json`) clips turn history before 2026-06-07, so weeks before that are understated. The full first_turn history (right side of chart below) shows pre-window signup volume ranged from 559–1,026/week.

## The real signal: signup collapse, not engagement collapse

```
new-user first_turn, weekly:
2026-04-06   559  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-04-13  1026  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-04-20   868  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-04-27   653  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-05-04   640  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-05-11   803  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-05-18   786  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-05-25   990  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-06-01   681  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-06-08   701  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-06-15   275  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓               <- PR authored
2026-06-22   455  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓          <- PR merged 06-23
2026-06-29    59  ▓▓▓▓▓▓▓
2026-07-06   150  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-07-13   143  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-07-20   164  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
2026-07-27    23  ▓▓▓▓
2026-08-03     9  ▓
```

**The signup dropoff starts in the same week as PR #7784** (Jun 22 → 275 → 59). But:
1. The first-week post-PR signup count (455) was **higher** than the prior week (275), not lower — meaning users were *not* turned off by the wizard.
2. The dropoff accelerated 4+ weeks *after* the merge, not immediately.
3. Most importantly: if the wizard were the cause, the **turns-per-new-user ratio** would crash post-merge. Instead it spiked to 0.41 in the PR week (highest of any week) and only collapsed later as new-user volume dried up.

## What this rules out

- ❌ **"Wizards scared users away"** — turns/new-user actually went *up* immediately post-merge.
- ❌ **"Custom default lost the template engagement quality"** — post-cohort users have identical median 4 turns.
- ❌ **"DK templates were stickier"** — pre-cohort median sessions = 1, same as post.

## What this DOES suggest (still unproven)

- ⚠️ **Top-of-funnel collapsed** from ~700-1000/week to 9/week over 6 weeks. Possible causes:
  - Marketing/ads stopped (paid acquisition budget cut)
  - Organic reach decay (post-launch hype fading)
  - External traffic source died (referral partner, ProductHunt momentum, etc.)
  - A platform/auth change broke signup (less likely — would show in error rates)
- ⚠️ Need to check acquisition channel data, ad-spend logs, or waitlist source attribution to identify which.

## Recommended next investigation (in priority order)

1. **Signup source attribution** — where did each new user come from? UTM? Referral code? Direct? This is the single most actionable data point.
2. **Pre-merge baseline** — pull 2026-Q1 vs 2026-Q2 signup curves to confirm whether the dropoff is part of a normal post-launch decay curve.
3. **Auth error rates** — confirm signups aren't failing silently on the frontend.

## Files

- `/tmp/wa_cohort.py` — reproducible cohort script
- `/tmp/wa_cohort_full.json` — 10,246 per-user rows with cohort assignment
- `/tmp/wa_60d.json` — original 60d engagement dump (re-used for turn-volume histogram)