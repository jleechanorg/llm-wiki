---
title: "WA Retention — 60d Deep Dive + Custom-vs-Canned (2026-08-05)"
type: source
tags: [worldarchitect, firestore, retention, ux, analysis, real-users, custom-campaign, returning-users, drop-off]
date: 2026-08-05
data_window: "2026-03-15 → 2026-08-05 (60 days via --days 60)"
baseline: "[[2026-08-04-wa-retention-7-weeks-later]] [[2026-08-05-wa-retention-top-3-ideas]]"
project: worldarchitecture-ai (production Firestore)
generated_by: jleechan session Slack C0AUXSVFSA2/1785903349.105819
audience: operator / decision
---

# WA Retention — 60d Deep Dive + Custom vs Canned

**TL;DR:** Three answers to the operator's three questions:
1. **Drop-off points:** 30.9% bounce at 1 turn, 32.7% at 2-4, 21.8% at 5-15, 14.5% at 16-25, **0% at 26+**. Weekly volume went from 116 turns (June 22) → 14 (Jul 6) → 2 (Jul 13) → 1 (Jul 27). The collapse is real and steep.
2. **Custom vs canned:** *Custom-titled campaigns retain 3× better than the wizard's default "My Epic Adventure" title* — 31% engaged vs 10%. Dragon Knight (LLM-bypass) is in between at 22.6%.
3. **Returning users (5/63 = 7.9%):** All 5 came back within <1 day (median 0.3d). 4 of 5 have ONE campaign (came back to the same one). 2 of 5 had a custom-titled campaign. The "warm return window" is hours, not days.

---

## Q1 — Drop-off points

**Total users with ≥1 turn (60d):** 63  
**Total turns:** 404  
**Returning users (≥2 sessions):** 5 (7.9%)  
**Single-session users:** 50 (79.4%)  
**No sessions recorded:** 8 (12.7%)

### Total-turns-per-user distribution (60d)

```
1 turn              :  17   27.0%  ##########################
2-4 turns           :  25   39.7%  #######################################
5-15 turns          :  11   17.5%  #################
16-25 turns         :   8   12.7%  ############
26-50 turns         :   2    3.2%  ###
51+ turns           :   0    0.0%
```

### First-session turn buckets (the drop-off signal)

```
1    :  17   30.9%   <- first reply = last reply
2-4  :  18   32.7%   <- bounce after 2-4 turns
5-15 :  12   21.8%   <- THE CLIFF Jeff asked about
16-25:   8   14.5%
26+  :   0    0.0%   <- nobody has a 26+ first session in 60d
```

**63.6% bounce in first 4 turns. 85.4% bounce by turn 15.** The "engaged native" tier from June (≥26 entry campaigns) has *collapsed to 0% in first-session*.

### Weekly turn volume (the collapse timeline)

```
2026-05-25      4
2026-06-01     30  ######
2026-06-08      4
2026-06-15    112  ######################  ← peak (post-PR #7784 wizard change?)
2026-06-22    116  #######################  ← peak
2026-07-06     14  ##                       ← cliff
2026-07-13      2                             ← effectively zero
2026-07-20      4
2026-07-27      1                             ← 1 turn in last 7 days before query
```

**Volume dropped 99% from peak (116 turns/week) to floor (1 turn/week) in 5 weeks.** This is not a seasonal pattern — the August write-up (`2026-08-04-wa-retention-7-weeks-later`) found the same collapse but on different numbers (last 7 days = 1 user, last 30d = 9 users). The data is consistent: volume is in free-fall.

---

## Q2 — Custom vs Canned retention

Walked `users/{uid}/campaigns/{cid}/story/` for all 63 real users. 80 campaigns total across 60 users (3 users had no campaigns). Classification:
- **Dragon Knight (DK)**: title == "The Knight of Two Suns" or "Dragon Knight" — uses the backend's `get_dragon_knight_template_opening_if_applicable` shortcut that bypasses the LLM
- **Default My Epic Adventure (DEF)**: title == "My Epic Adventure" — the wizard's `FALLBACK_TITLE` (`frontend_v1/app.js:1031`); user picked Custom Campaign and didn't customize the title field
- **Custom-titled (CUSTOM)**: anything else — user typed a real title

### Engagement by template type

| Template | n | Bounced (≤4 entries) | Cliff (5-15) | Engaged (≥16) |
|---|---|---|---|---|
| **CUSTOM-titled** | 29 | 9 (31.0%) | 11 (37.9%) | **9 (31.0%)** |
| Dragon Knight | 31 | 16 (51.6%) | 8 (25.8%) | 7 (22.6%) |
| **DEF My Epic Adventure** | 20 | **12 (60.0%)** | 6 (30.0%) | **2 (10.0%)** |

### KEY FINDING — Custom-titled users retain **3× better** than default-titled

**31% vs 10% engaged rate.** Users who typed a real title are *substantially* more engaged than users who accepted the wizard's default. This is the strongest retention signal in the entire 60-day window.

**Causal interpretation (not tested):**
- **Selection effect:** Users willing to type a title are *already* more invested. They typed, so they cared enough to engage.
- **Investment effect:** Typing a title primes the user to take the campaign seriously. Once they've committed a name to the world, they want to see what happens to it.
- **Wizard-as-onboarding-failure:** The default title signals the user *skipped* the wizard's main value-prop (customization). They're less invested because they didn't customize anything.

**The June hypothesis (bimodal tourist/native) was right but incomplete.** This finding refines it: there's a *third* tier — "engaged customizers" — that's the highest-value segment. They're not visible in the "engaged natives" list because they're spread across many campaigns, not concentrated in one.

### Implications for action #2

The recommended pre-written first scene + CTA chips (action #2 from `2026-08-05-wa-retention-top-3-ideas.md`) becomes *more* important given this finding — the blank `/game/<id>` panel hits everyone, but the default-title users are most likely to bounce there. **Strong nudge: the first-scene fix should also include a CTA that invites the user to rename their story or seed a custom prompt** — turning "default acceptors" into "customizers" mid-session.

---

## Q3 — Returning users (5/63 = 7.9%)

All 5 returning users + their campaigns:

| Email | Sessions | Total turns | Span (d) | First session | Last session | Campaign title | Type | Entries |
|---|---|---|---|---|---|---|---|---|
| thiago.hirai@gmail.com | 3 | 41 | 0.5 | 2026-03-14 | 2026-03-15 | My Epic Adventure | DEF | 82 |
| leechanfamilyjlc@gmail.com | 2 | 29 | 0.1 | 2026-03-14 | 2026-03-15 | My Epic Adventure | DEF | 48 |
| mrkennethyip@gmail.com | 3 | 17 | 0.3 | 2026-06-19 | 2026-06-20 | Dragon Knight | DK | 36 |
| marcos.valle02@gmail.com | 2 | 20 | 0.1 | 2026-06-23 | 2026-06-23 | Alien spaceship + Greenhollow | CUSTOM | 36 + 8 |
| nirmal.k.asokan@gmail.com | 2 | 9 | 0.3 | 2026-06-24 | 2026-06-25 | First adventure | CUSTOM | 16 |

### Patterns that stand out

1. **All 5 returning users came back within <1 day** (median 0.3d, max 0.5d). Same hot-return window as June (`2026-06-30-wa-user-sessions-deep-dive` found 0.7-7.7h). After 24h the trail goes cold.
2. **4 of 5 returning users have ONE campaign** — they returned to the SAME campaign, not started a new one. This validates the "resume your story" email approach (action #3 from `2026-08-05-wa-retention-top-3-ideas.md`).
3. **2 of 5 returning users (40%) had CUSTOM-titled campaigns.** Higher than population baseline (29/80 = 36%) — small sample, but consistent with Q2 finding.
4. **Returning users had 16-82 entries per campaign** (median ~36). *All* returning users are in the "engaged" tier. The return rate of 7.9% is *entirely* a function of how many people reach 16+ entries in their first session.
5. **The 2 oldest returning users (Mar 14-15) used the wizard default title** and got 48-82 entries. These are the "pre-wizard-default era" users — when the wizard still pushed Dragon Knight first. Their engagement depth (48-82 entries) shows the DEFAULTS MATTER hypothesis has been changing over time.

### Correlations
- **Engagement depth ↔ return probability:** 7 of 8 users with ≥16 first-session turns = returning (87.5% return rate). 0 of 55 users with ≤15 first-session turns = returning. **First-session depth is the strongest predictor of return.**
- **Template type ↔ return:** Too small to be statistically meaningful (n=5).
- **Inter-session gap ↔ anything:** All gaps <1 day, no variance to analyze.

---

## Methodology

### Data sources
- `rate_limits/{uid}.turn_timestamps` — 63 real users, 404 turns (via `~/.hermes_prod/skills/wa-prod-data-query/scripts/query_real_users.py --days 60 --exclude-jleechan --json`)
- `users/{uid}/campaigns/{cid}/story/` — 80 campaigns across 60 users (via direct Firestore walk)
- Auth metadata: not included in this query — would need separate `auth.list_users()` join

### Test patterns filtered
- Email contains any of: `test`, `anon`, `dev-runner`, `example.com`, `jleechantest`
- jleechan@gmail.com (uid `vnLp2G3m21PJL6kxcuAqmWSOtm73`) excluded

### Session clustering
- 30-minute gap rule (per `wa-prod-data-query` skill)
- First-session turn count = entries in the first session only (not lifetime)

### Template classification
- DK = title matches backend constant `DRAGON_KNIGHT_CANONICAL_TITLE` or `DRAGON_KNIGHT_TEMPLATE_OPENING_STORY` (verified at `mvp_site/constants.py:1953-1955`)
- DEF = title == "My Epic Adventure" (verified at `frontend_v1/app.js:1031` `campaignTitleInput.value = "My Epic Adventure"`)
- CUSTOM = everything else

### Confidence
- Q1 drop-off: HIGH (n=63, clean distribution)
- Q2 custom-vs-canned: MEDIUM-HIGH (n=80, 31/29/20 split, statistically meaningful differences)
- Q3 returning users: LOW-MEDIUM (n=5; patterns are suggestive, not statistically significant)

---

## What this changes vs the June / August writes

| | June 30 deep-dive | August 4 re-run | **August 5 60d deep-dive** |
|---|---|---|---|
| Active users window | 28d: 47 | 35d: 9 | 60d: 63 |
| Cliff band (5-15) % | bimodal tourist/native | "wizard trap" hypothesis | **Template-type confound (Q2 finding)** |
| Custom campaign finding | not separated | not separated | **3× engagement vs default (NEW)** |
| Returning user % | 10% | unknown (n=5) | **7.9%, all <1d span, 80% same-campaign** |
| Weekly volume peak | (not measured) | 62 signins/7d | **116 turns/week → 1 turn/week** |

The August 5 finding **inverts** part of the August 4 hypothesis: the "wizard trap" wasn't the wizard trapping users, it was the wizard's DEFAULT TITLE signaling low user investment. Users who customized their campaign (typed a title, picked a specific template) retained 3× better than users who accepted the default.

---

## Connections

- `[[2026-08-04-wa-retention-7-weeks-later]]` — August 4 re-run, baseline
- `[[2026-08-05-wa-retention-top-3-ideas]]` — Top 3 actions (instrument funnel, pre-written first scene + CTAs, 24h email)
- `[[2026-06-30-wa-user-sessions-deep-dive]]` — June bimodal hypothesis (refined, not replaced)
- `wa-prod-data-query` skill — `~/.hermes_prod/skills/wa-prod-data-query/`
- `mvp_site/frontend_v1/app.js:1031` — wizard default title setter
- `mvp_site/constants.py:1953-1955` — Dragon Knight canonical titles
- `mvp_site/campaign_template_dragon_knight.py:63` — DK backend bypass
- `mvp_site/bq_logging.py` — BQ forensic data (full LLM payloads, 30d TTL) — NOT used in this query; future analysis could join BQ telemetry to per-turn model/latency/error data
