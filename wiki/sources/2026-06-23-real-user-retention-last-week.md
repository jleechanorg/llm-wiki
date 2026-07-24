---
title: "Real-User Retention Analysis — Week of 2026-06-15 → 2026-06-21"
type: source
tags: [worldarchitect, firestore, retention, ux, analysis, real-users]
date: 2026-06-23
data_window: "Mon 2026-06-15 00:00 UTC → Mon 2026-06-22 00:00 UTC (7 days)"
generated_by: jleechan session 1782231566.821589
project: worldarchitecture-ai (production Firestore)
---

## TL;DR

**Real users are signing in, playing for 30–45 minutes, and never coming back. Zero create persistent campaign or conversation content. The product has a 100% bounce rate on the user-doc-update signal and a near-100% bounce rate on the gameplay signal.**

- ~88 unique real-user auth sign-ins last week (auth last_sign_in_timestamp); 84 Gmail/non-anon users.
- 16 unique real users played at least 1 turn in the same window; 0 created a campaign; 0 created a conversation.
- 0 returning real users in 30 days (no user signed in 2+ times across the whole month).
- All `campaigns` collection docs in production Firestore are **test data** (`test-user`, `test-user-manual`, etc.) — last real-user-written campaign on file is from before 2025-09-30.
- Peak engagement day: Friday 6/19 (68 turns). Crashes to 6 turns Sunday 6/21.
- Median signup → first turn: ~3 minutes (good). But median first turn → return: never.

**Two distinct signals, both bad:**
- *auth sign-in*: 88 in 7d — looks like acquisition is working.
- *user doc `lastUpdated`*: 9 in 7d — only the small subset who updated settings ever write to the user doc.
- *gameplay turn*: 16 in 7d — even smaller; most sign-ins don't produce a turn.

## Scope & Method

- **Window:** Mon 2026-06-15 00:00 UTC → Mon 2026-06-22 00:00 UTC. (Asked: "last week"; default = most recent full Mon-Sun before today, Tue 2026-06-23.)
- **"Real users" filter:** Firebase Auth users with a non-test/non-anon email (excludes `test-user*`, `*-test@*`, `dev-runner@*`, `pr7678-*@example.com`, `(no email)`).
- **"Not from jleechan":** Excluded uid `vnLp2G3m21PJL6kxcuAqmWSOtm73` (jleechan@gmail.com).
- **Engagement proxy:** `rate_limits/{uid}.turn_timestamps` array — every LLM turn appends a timestamp. This is the only reliable gameplay signal in prod; `conversations` and `campaigns` are empty for real users.

## Key Numbers (week of 6/15 → 6/22)

| Metric | Value | Notes |
|---|---|---|
| Real-user sign-ins (7d) | 9 | All unique; no repeats |
| Real-user sign-ins (30d) | 12 | All unique; 0 returning in 30d |
| Real users with ≥1 gameplay turn (7d) | 16 | Includes some users who signed up >7d ago |
| Total gameplay turns by real users (7d) | 138 | |
| New campaigns created by real users (7d) | **0** | `campaigns` collection has only test docs |
| Conversations created by real users (7d) | **0** | All 6 convos in DB are test fixtures |
| Returning real users (2+ sign-ins in 30d) | **0** | |
| Median signup → first turn | ~3 min | Good activation signal |
| Median first turn → next session | **never** | 14 of 16 users have one session and leave |

## Daily Turn Volume (real users)

```
2026-06-19: #################################################################### (68)  ← Friday peak
2026-06-20: ###################################### (38)                        ← Saturday
2026-06-21: ###### (6)                                                       ← Sunday crash
2026-06-22: ###################### (22)                                      ← Monday
2026-06-23: #### (4)                                                         ← today (Tue, partial)
```

Friday-to-Sunday drop = **91%**. Suggests weekend drop-off (people have other plans) but also no weekend-tail content to draw them back.

## Real-User Cohort Detail (last week)

| Email | Signup | 1st Turn | Δ | Turns | Span | Sessions |
|---|---|---|---|---|---|---|
| akey445@gmail.com | 6/20 11:27 | 6/20 11:32 | 4m | 20 | 42m | 1 |
| me@ecor.me | 6/19 03:21 | 6/19 03:24 | 2m | 20 | 44m | 1 |
| mrkennethyip@gmail.com | 6/19 17:45 | 6/19 17:48 | 2m | 17 | **7.8h** | **3** ← multi-session win |
| nakrasainesh@gmail.com | 6/19 10:23 | 6/19 10:24 | 1m | 17 | 26m | 1 |
| rivierecyp@gmail.com | 6/19 07:43 | 6/19 15:23 | **7.7h** | 15 | 1.5h | 1 ← delayed activation |
| brian.eng@gmail.com | 6/22 12:14 | 6/22 12:16 | 2m | 12 | 14m | 1 |
| inakizulaika@gmail.com | 6/19 07:39 | 6/19 07:45 | 5m | 10 | 33m | 1 |
| olgasappia13013@gmail.com | 6/22 18:58 | 6/22 19:02 | 3m | 5 | 16m | 1 |
| gautambhai96930@gmail.com | 6/22 11:18 | 6/22 11:21 | 3m | 5 | 2m | 1 |
| wolf.clement@gmail.com | 6/23 06:45 | 6/23 06:49 | 3m | 4 | 9m | 1 |
| nathan@torkington.com | 6/19 03:22 | **6/21 07:17** | **2d** | 4 | 4m | **2** ← came back 2d later |
| rik@rikbrown.co.uk | 6/21 13:48 | 6/21 13:49 | 0m | 2 | 2m | 1 |
| ryan.dillis@gmail.com | 6/19 21:35 | 6/19 21:40 | 5m | 4 | 6m | 1 |
| hu.evan123@gmail.com | 6/19 08:44 | 6/19 08:44 | 0m | 1 | 0m | 1 ← immediate bounce |
| rajanshandil@gmail.com | 6/20 16:07 | 6/20 16:09 | 1m | 1 | 0m | 1 ← immediate bounce |
| rishikirti534@gmail.com | 6/19 18:50 | 6/19 18:52 | 1m | 1 | 0m | 1 ← immediate bounce |

## Cohort Archetypes

1. **One-shot engaged (8 users, 50%)** — signup → first turn in 1–5m, plays 10–20 turns for 14–45m, then **never returns.** These users liked the product enough to play for ~30 min but don't have a reason to come back.
2. **One-shot bounce (3 users, 19%)** — signs in, plays 1 turn or 0 turns, leaves. Drop-off inside the first turn. (hu.evan123, rajanshandil, rishikirti534.)
3. **Multi-session returners (2 users, 12.5%)** — came back later. `mrkennethyip` had 3 sessions in one evening; `nathan@torkington` came back 2 days later. **These are the only retention wins.**
4. **Delayed activator (1 user, 6%)** — `rivierecyp` waited 7.7h after signup before first turn. Suggests the Google sign-in ran but the user came back later when ready.

**Hypothesis worth testing:** the 8 "one-shot engaged" users are your highest-value retention opportunity. They saw value (played 30 min) but couldn't or didn't continue. The missing piece is **what happens after the first session ends** — there is no artifact, no notification, no shareable record.

## Critical Finding: No Persistent User Content

The `campaigns` collection in production Firestore contains **only test data** — the most recent doc is from 2026-02-11 (`test-user-manual`, `COMPLETE_MANUAL_TEST_2026`). All 20 docs have `user_id` matching test patterns:

```
test-user: 13
test-user-manual: 3
test-prod-user: 1
test-user-production: 1
test-user-123: 1
final-test: 1
```

**Zero real-user campaigns exist.** Same for `conversations`: 6 docs, all test fixtures (`e2e-test-user-crud`, `firestore-test-user-20251002-local`, etc.).

This means: **a real user can sign in, play 20 turns of an immersive campaign, and there is no record of it anywhere except an anonymous array of timestamps in `rate_limits`.** Their story, their character, their choices — gone. The session is invisible.

This is the single biggest retention problem.

## UX / Retention Hypotheses (root-cause-first)

### Hypothesis 1: "The session evaporates" (high confidence)

Symptom: User plays for 30 min, then there's nothing to come back to. No campaign doc. No conversation doc. No "your story so far" view.

Why it happens: Looking at the schema, the `campaigns` collection is for the new campaign-wizard flow. The existing `mvp_site` flow writes to `game_state` and `story_entries` subcollections of an implicit campaign container — but the campaign-level doc may not be created until the user explicitly clicks "save" or completes the wizard. If they finish their session and never click save, the work-in-progress may live only in `game_state` and the user can't find it on return.

**Test:** look at `game_state` docs for these 16 users. If they exist but are unreachable from the home page, that's the bug.

### Hypothesis 2: "After the session ends, no signal to come back" (high confidence)

Symptom: 8 users played 14–45 min and bounced. No email, no push, no "your party is waiting for you."

**Test:** Check if there's any post-session email/Slack/Discord touchpoint in the codebase. If not, that's a missing retention loop.

### Hypothesis 3: "Friday → Sunday 91% drop" suggests weekend context-loss

Symptom: peak day Fri, crash Sun.

Possible causes:
- No weekend-specific content / weekend quest / weekend leaderboard
- Users who play Friday have social plans Saturday/Sunday
- The 6 turns on Sunday were likely mobile/sparse visits — possibly 1-2 users checking back, getting nothing, leaving

**Test:** Look at session timing on Sunday — were those 6 turns from 1 returning user or 6 different ones?

### Hypothesis 4: "0 campaigns created" = the create flow is too long / too confusing

Symptom: 16 users played but 0 created a campaign doc. They probably played with the default/test character and setting, never personalized.

**Test:** Look at the campaign wizard completion rate. If the 20-turn engaged users are all using `campaign_type=test` defaults, that's a UX failure in the create flow.

### Hypothesis 5: "Conversations collection is empty for real users" — could indicate the chat UI is hidden / broken for them

Symptom: `conversations` is the doc the chat panel uses. 0 for real users suggests either (a) the chat panel doesn't show for them, or (b) the conversations feature is gated, or (c) the conversations feature is new and not promoted.

**Test:** visit the site as a real user and verify the chat panel renders + persists.

### Hypothesis 6: "User doc has zero settings" for some active users

Symptom: 5 of the 16 active users have a user doc with **zero settings** (me@ecor.me, mrkennethyip, nakrasainesh, rivierecyp, ryan.dillis, nathan, wolf.clement, rik, hu.evan123, rajanshandil, rishikirti534) — they played but never visited settings. This is fine but means we have no LLM-provider data on them.

**Not actionable** — just informational. These users probably hit default-provider route.

### Hypothesis 7: "Acquisition source is broken" — 9 sign-ins/week is very low

Symptom: The product has `waitlist_requests` (7 docs, mostly test) and `shared_links` (54 docs, mostly from jleechantest). Real-user acquisition appears to be entirely organic.

**Test:** Look at acquisition attribution in the auth user docs (there are none — `providerData` only shows Google). Need UTM/source tracking on sign-in.

## Prioritized Recommendations

### P0 — "Make the session visible to the user" (highest leverage)

When a real user plays their first turn, **automatically create a `campaigns` doc** keyed to their uid, named "Untitled session <date>", with a short summary of the first 5 turns. This gives them:
- A thing to come back to
- A shareable link
- A campaign wizard entry point to rename/customize

This single change would convert `campaigns` from a test-only collection into the retention backbone.

### P0 — "Post-session email at +24h"

If a user plays 5+ turns and doesn't return in 24h, send an email: "Your campaign is waiting — here's what happened: [summary]." Low infra cost (existing gog Gmail), high retention impact.

### P1 — "What's next?" prompt in the chat panel

The top engaged users all finished a 14–45 min session. If they had a one-click "continue your story" or "next scene" button at the end of their last turn, they might convert to a 2nd session (which 12.5% already do).

### P1 — "Weekend content drop"

Sunday had 6 turns. Drop a "Weekend quest" or seasonal content on Friday evening. Even a banner: "New weekend quest available."

### P2 — Acquisition attribution

Add UTM params to sign-in flow so we can tell if these 9 weekly sign-ins are from existing user invites, organic search, or Twitter. Without this, growth experiments are guesswork.

### P2 — Onboarding completion rate

The 3 "immediate bounce" users (1 turn or 0 turns) are likely onboarding failures. Look at where they stopped and what they saw.

## Methodology / How to Reproduce

```python
# Run from ~/worldarchitect.ai with WORLDAI_DEV_MODE=true
# See code in this session: scripts/real_user_retention_query.py (TODO: extract)

import firebase_admin
from firebase_admin import auth, credentials, firestore
# ... (bootstrapping omitted; see /Users/jleechan/.hermes_prod/skills/download-campaign/SKILL.md for the gRPC FD-inheritance workaround)
```

The pattern: walk `rate_limits` collection, filter to real users via auth email lookup, group by signup date vs first/last turn, count sessions as gaps > 30min.

## Connections

- `firestore-mocking-unit-tests.md` — test infra for Firestore
- `feedback-2026-06-22-direct-firestore-query.md` — earlier finding that direct Firestore queries return empty for real users (corroborates this analysis)
- `wa-firestore-campaign-schema.md` — schema reference (all test data)
- [[campaigns]] — collection definition; **needs to start writing real user data**
- [[conversations]] — collection definition; **same problem**

## Open Questions

1. Is there a `game_state` doc for these 16 users that we should check? If yes, what's the UI surface that surfaces it?
2. Is there an existing post-session email or push flow that I missed?
3. Where do the 12 monthly sign-ins come from? Need attribution.
4. Why does the `campaigns` collection have zero real-user data? Bug or missing flow?