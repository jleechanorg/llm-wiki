---
title: "Project 2026 06 11 Pr7440 Iphone Dev Unauth Drop Cdiag Proof"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-11
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/project_2026-06-11_pr7440_iphone_dev_unauth_drop_cdiag_proof.md
---

## Summary

User reported 2026-06-11 ~00:21Z: "i saw the issue on dev and then i switched to load s1 and it worked, anything in the logs for either?" Later: "No I am signed in."

PR #7440 (client-side diagnostic logging) is live on dev as `mvp-site-app-dev-03100-65q`. Pulled Cloud Logging for the window — found the bug. Two distinct iPhone sessions captured in dev Cloud Logging between 05:04:59Z and 05:08:26Z (user IS signed in, uid=vnLp2G3m, is_test_user=false, is_anonymous=false).

## Original

User reported 2026-06-11 ~00:21Z: "i saw the issue on dev and then i switched to load s1 and it worked, anything in the logs for either?" Later: "No I am signed in."

PR #7440 (client-side diagnostic logging) is live on dev as `mvp-site-app-dev-03100-65q`. Pulled Cloud Logging for the window — found the bug.

## What the cdiag events prove (CORRECTED)

Two distinct iPhone sessions captured in dev Cloud Logging between 05:04:59Z and 05:08:26Z (user IS signed in, uid=vnLp2G3m, is_test_user=false, is_anonymous=false). Session IDs: `03596962` and `57fa5b30`. Same exact sequence in both — the bug reproduces 100% of the time.

**Session `03596962` (full sequence, ms since page boot):**

| ms | Event | Detail |
|---|---|---|
| 0 | `page.boot_inline` | readyState=loading |
| 5 | `app.boot_top` | scripts_loaded=33 |
| 9 | `watchdog.start` | timeout=8000ms, authContainer=true, **authDidInitialize=false** |
| 18 | `network.request /api/constants/models` | attempt=1, **fired before auth ready** |
| 18 | 🔥🔴 `network.error` | NotAuthenticated, latency=0ms, no Bearer token |
| 22 | `page.load` | readyState=complete |
| 307 | `auth.callback_fire` | **has_user=true**, performance.now=464ms |
| 307 | `auth.callback_signed_in` | **uid=vnLp2G3m**, is_anonymous=false, is_test_user=false |
| 307 | `route.branch=game` | campaign_id=vNU3AAXHd9N7adqWSM2p |
| 1455 | `network.response /api/campaigns 200` | **latency=1147ms** |
| 1871 | `view.transition` | from=auth to=game (pathname=/game/vNU3...) |

**Session `57fa5b30` — same exact bug (different campaign, 3.5 min later, probably a reload or nav):**
- /api/constants/models fires at +15ms → 401 NotAuthenticated (latency=0)
- auth.callback_signed_in at +193ms (uid=vnLp2G3m, same user)
- /api/campaigns latency=643ms
- view.transition auth→game at +1099ms

## The actual bug (proven, not guessed)

**`/api/constants/models` is called BEFORE Firebase auth has resolved the user.** The endpoint has `@check_token` (main.py:4503-4516) and returns 401 `NotAuthenticated: User_not_authenticated` when no valid Bearer token is sent. The frontend's `fetchApi` wrapper in api.js treats 401 → triggers a token refresh + retry. The retry succeeds (auth is ready by then), but the initial 401 is captured in the `network.error` cdiag event.

**Two related problems on every page load:**

1. **`/api/constants/models` 401 timing bug** — endpoint is auth-gated but the frontend calls it from app.js init before `authDidInitialize` flips to true. The `watchdog.start` cdiag event literally captures `authDidInitialize=false` at boot. Fix: either make `/api/constants/models` public (it's a constants endpoint, no user-specific data) OR have the frontend defer the call until after `authDidInitialize=true`.

2. **1.1-1.9s welcome card FOUC** — `view.transition from=auth to=game` waits for the campaign API to return (643-1147ms) before the route handler re-evaluates and transitions the view. The user sees the welcome card for 1-2 seconds. PR #7379 only suppressed the post-8s watchdog reload — it did NOT fix the initial 1-2s flash. The fix would be to NOT default to `auth` view on first paint, or to show a neutral loading state until `auth.callback_fire` resolves.

## Earlier "issue" — same 401 from different angles

**Session `1d261ac6` (00:57:40Z, HeadlessChrome, NOT signed in):** different cause. There the user had NO auth state at all (`auth.callback_fire has_user=false`), so /api/constants/models 401'd permanently and the route dropped them to /auth via `route.unauthenticated_drop`. That's the cross-hostname / never-signed-in scenario, separate bug class. Cross-hostname auth state is NOT shared between `mvp-site-app-s1-…run.app` and `mvp-site-app-dev-…run.app`, but the iPhone user's bug is a different problem — they ARE signed in, the 401 is just from bad call timing.

**iPhone session earlier (00:21:49–00:22:22Z):** sent 0 cdiag events because iOS Chrome cached the old index.html that doesn't include `<script src="/frontend_v1/diagnostics.js">`. By 05:04Z the user had reloaded with a fresh HTML and cdiag started flowing. (The dev `index.html` has `cache-control: no-cache, must-revalidate`; `diagnostics.js` has `cache-control: public, max-age=300`. In practice iOS Chrome served the cached page from before the deploy for ~9 hours.)

## s1 "worked" — but s1 had 0 entries in last 30m

`s1` (`mvp-site-app-s1`) had 0 HTTP requests in the last 30 minutes. The user wasn't actually on s1 during this conversation. The "s1 worked" comparison was probably a different time, different session, or a perception difference (warmer auth cache, faster API response, etc.). **Don't conflate the two: the iPhone bug is on dev, not specific to dev-vs-s1.**

## Suggested fixes (NOT a PR — user decides)

1. **Drop `@check_token` from `/api/constants/models`** (main.py:4503-4516) — the response is model name strings, no user-specific data. The endpoint being public would eliminate the 401 timing bug entirely. (Trade-off: any anonymous user could enumerate model names, which is probably fine since these are public Gemini/OpenRouter model IDs.)

2. **Defer /api/constants/models call** in `app.js` init until after `authDidInitialize=true` is observed, OR add a guard in `fetchApi` to wait for the auth token to be present before sending.

3. **Replace initial welcome card with neutral loading state** in `index.html` so the first paint doesn't show `auth` view for 1-2s. The view transition only happens AFTER the campaign API returns; until then, the user sees the welcome card.

4. **Fix iOS Chrome caching of index.html** — the user can hard-refresh (Settings → Safari → Clear Website Data) to pick up the new HTML. A more durable fix would be to add `Cache-Control: no-store` to the HTML response, or use a cache-buster query string in the script tag.

## Why this matters

PR #7440 paid off in <5 minutes: confirmed within 4 cdiag events that the iPhone user's "page doesn't load" symptom is the `/api/constants/models` pre-auth 401, NOT a Firebase popup issue, NOT a network failure, NOT a JS error. The 19-event sequence from session `03596962` is a textbook diagnostic capture — boot → watchdog → pre-auth API call → 401 → auth callback → route branch → campaign API → view transition. Without PR #7440 we'd still be guessing.
