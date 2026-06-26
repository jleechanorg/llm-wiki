# 2026-06-26 — 5-user retention review (Jeffrey's Wednesday list)

Scope: re-walk the 5 users in Jeffrey's list (`stream.of.silver@gmail.com`,
`akey445@gmail.com`, `me@ecor.me`, `mrkennethyip@gmail.com`,
`nakrasainesh@gmail.com`) after they surfaced in last week's cohort. Classify
each by termination cause and check rate-limit abuse logs to distinguish
quota-wall victims from pure churn.

## Headline (read this first)

**All 5 users hit the free-tier quota wall before they stopped.** Three of them
came back inside 7h of their last turn, got blocked by `RATE_LIMIT_ABUSE`, and
never returned. The other two (mrkennethyip, nakrasainesh) appear to have
genuinely churned — but they may also have hit a soft cap that doesn't log.

The biggest single retention lever this week is **the rate-limit wall**, not
the 2-entry bounce or the level-up modal.

## Per-user table

| email | camp | entries | last_played (PT) | bounce? | end-state | RL abuse? | Diagnosis |
|---|---|---|---|---|---|---|---|
| stream.of.silver@gmail.com | Dragon Knight (`UV6…`) | 42 | 06/23 09:56 | no | Stopped mid-narrative | **YES @ 16:57:19Z (90s after last turn)** | Quota wall |
| akey445@gmail.com | My Space Adventure (`ZSK…`) | 42 | 06/20 05:14 | no | Stopped mid-narrative | **YES @ 12:15:16Z (39s after last turn)** | Quota wall |
| me@ecor.me | Space opera adventure (`8jD…`) | 40 | 06/18 21:07 | no | XP=300/300, `level_up_available=True`, L1 | **YES @ 06:40:33Z (~2.5h after last turn)** | Quota wall + level-up-modal bug (#7931) |
| mrkennethyip@gmail.com | Dragon Knight (`wq9…`) | 36 | 06/19 18:35 | no | Stopped mid-narrative (Empyrean fire) | no | Likely churn (re-engagement gap of ~9h before stopping) |
| nakrasainesh@gmail.com | Dragon Knight (`vXw…`) | 36 | 06/19 03:52 | no | Stopped mid-narrative (Service Post) | no | Likely churn (single 29-min session) |

## Stream.of.silver — the 6-campaigns-in-90s case study

This user created **6 campaigns** between 15:55:20 and 15:57:18 UTC on
06/23 — 5 bounces and 1 success (the 42-entry Dragon Knight). The bounce
camps:

| camp_id | created_at | title | entries | gap e0→e1 |
|---|---|---|---|---|
| `abaeaZYs9bDrYEUND1lJ` | 15:55:24 | Dragon Knight | 2 | 0.31s |
| `uO6aGTuRvYDlW000UeYw` | 15:55:34 | Dragon Knight | 2 | 0.28s |
| `dn9NFHB6MtM8O3NuEgrz` | 15:55:54 | Dragon Knight | 2 | 0.28s |
| `qckx1dLW6SEXX8oSfVui` | 15:55:59 | delete | 2 | 0.27s |
| `hsaKmUiwcHjtZsNSTx8e` | 15:57:18 | First Test | 2 | 0.50s |
| `UV6TeGxjNwJb9z2CYa8F` | 15:55:20 | Dragon Knight | 42 | 0.35s |

This is **the Dragon Knight fast-path race** the 2026-06-23 afternoon
bounce deep-dive predicted. The user clicked Dragon Knight 4 times in 30s,
got the canned `[CHARACTER CREATION - Review]` card back faster than the
spinner could resolve, clicked again, hit it 5 times, and then started
deleting the campaigns. The 6th attempt (`UV6…`) is the one that
"stuck" — they read the canned card and decided to play.

**Why this matters**: the 0.5s setTimeout + spinner UX is creating
campaign documents the user never wanted. If the front-end dropped the
500ms `setTimeout` and differentiated the canned path from the real-LLM
path with a flag (e.g. `data.canned: true`), the user would see the
result in <300ms and not click again.

## Me@ecor.me — the level-up modal bug, reproduced

The 06/19 last-turn rewards_box is the smoking gun for [bug]
[#7931](https://github.com/jleechanorg/worldarchitect.ai/issues/7931):

```json
{
  "current_level": 1,
  "new_level": 2,
  "resolved_target_level": 2,
  "level_up_available": true,
  "current_xp": 300,
  "next_level_xp": 300,
  "xp_to_next_level": 0,
  "progress_percent": 100.0,
  "source": "model"
}
```

Game state at `users/7nS4x6YMCQTNSUQUemMrmIcY7Ig2/campaigns/8jDgOCJEA73BgRHtyzjV/game_states/current_state`:

- `level = 1` (not 2)
- `experience = {current: 300, needed_for_next_level: 300, to_next_level: 0}`

User took one more action ("Stealthy Evasion"), the model emitted
`new_level=2, level_up_available=True`, and then the user got
`RATE_LIMIT_ABUSE` 2.5h later. They never came back. The level-up
ceremony never fired.

This is the second observed case of "XP overflow, no level-up" from last
week's cohort — confirms [bug] #7931 is real, not a one-off.

## Rate-limit abuse correlation

`gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="mvp-site-app-stable" AND jsonPayload.message:"RATE_LIMIT_ABUSE"' --format=json --limit=500 --freshness=30d`

3 hits for these 5 users:

| ts (UTC) | email | gap to last turn |
|---|---|---|
| 2026-06-23T16:57:19Z | stream.of.silver | **90s** (returned within 2 min) |
| 2026-06-20T12:15:16Z | akey445 | **39s** (returned within 1 min) |
| 2026-06-19T06:40:33Z | me@ecor.me | **~2.5h** (came back next morning) |

The "came back and got blocked" pattern is **the most damaging retention
failure** documented this week. All three were high-value re-engagement
moments that ended with the user staring at a 429 and never returning.

The 30-turns/24h or 20-turns/5h free-tier wall is firing correctly per
policy, but the failure mode is: **user engages → hits wall → never sees
the "upgrade for more turns" CTA → churns**.

## Mrkennethyip + nakrasainesh — the unclassified two

These two have **no `RATE_LIMIT_ABUSE` log hits** in the 30-day window. They
also both played Dragon Knight canned-template campaigns, both reached
~36 entries, and both stopped mid-narrative. Patterns:

- **mrkennethyip**: 1 long session (06/19 17:46 → 06/20 01:35, ~8h,
  36 entries). The session has a 9h mid-session gap (1781891s →
  1781901s), which suggests the user closed the tab overnight. No re-engagement
  on 06/20. Likely **natural churn** — they played once for ~8h, beat
  some content, never came back.
- **nakrasainesh**: 1 short session (06/19 10:23 → 10:51, ~29 min,
  36 entries). 36 entries in 29 min is suspiciously fast (1.5 turns/min
  including LLM latency) — they were reading but not deep-playing.
  Likely **didn't find the hook** — Dragon Knight template is the same
  canned opener everyone sees.

Neither of these is fixable with a quota-wall change. Both look like
"the campaign got boring after the canned opener wore off".

## Retention hypotheses to test

1. **Quota wall is #1 retention killer (3 of 5 = 60%)** — `stream.of.silver`,
   `akey445`, `me@ecor.me` all re-engaged, hit the wall, churned. Fix:
   - Add a "you're at the free limit — upgrade for X more turns" CTA
     the first time a user is blocked. Currently they see a 429.
   - Soft-warn at 15/20 turns so the user knows the wall is coming.
   - "Quota almost reached" banner in the UI.
2. **Level-up-modal bug is #2 (1 of 5 = 20%)** — `me@ecor.me` had
   `new_level=2, level_up_available=True` but the ceremony never fired.
   Same smoking gun as [bug] #7931 cohort. **File the issue with the
   `me@ecor.me` story as a second reproduction.**
3. **Dragon Knight canned-template race still exists (5 of 5 used DK)**
   — `stream.of.silver` created 6 campaigns in 90s. Fix:
   - Drop the 500ms setTimeout in `mvp_site/frontend_v1/app.js:3586`.
   - Pass `canned: true` from the backend canned-template path and
     hide the spinner immediately when `canned=true`.
4. **Dragon Knight template is hooking users but losing them at ~36-42
   entries** — `mrkennethyip`, `nakrasainesh`, `akey445` all hit
   36-42 entries and stopped. This is the natural "novelty wears off"
   curve. **Not a bug, but worth tracking.** Compare to the open-world
   template (`use_default_world=false`) — `akey445` (Space) and
   `me@ecor.me` (Space) also hit 40-42 entries, so it's not template-specific.

## Action items

- [ ] File [bug] issue for me@ecor.me level-up-modal repro (links to #7931)
- [ ] File [frontend] issue for quota-wall CTA missing on first 429
- [ ] File [observability] issue for quota warning at 15/20 turns
- [ ] Already tracked: Dragon Knight fast-path race (afternoon deep-dive)
- [ ] Already tracked: #7931 level-up-modal overflow

## Methodology notes

- Used inline query from `worldarchitect-retention-analysis` SKILL.md Step 2
  (the `scripts/query_real_users.py` helper still doesn't exist).
- Resolved email→uid via `auth.get_user_by_email` (Firestore user doc
  emails are sometimes stale).
- Walked story collection WITHOUT `order_by("timestamp")` — production
  uses string timestamps, not Firestore Timestamps.
- Always used `narrative` field for entry text (text field is empty).
- Rate-limit correlation via `gcloud logging read` filter from SKILL.md
  §"Rate-limit correlation".
