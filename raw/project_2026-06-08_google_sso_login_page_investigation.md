---
name: google-sso-login-page-investigation
description: "User 'always sees login page' — fanout synthesis refuted by user experience; cause is PR #7349, not #7321"
metadata:
  node_type: memory
  type: project
  originSessionId: ea7f9127-12cd-4bd5-9ce6-1ebf86c38c62
---

# Google SSO "Login page every time" — fanout investigation + user-experience correction

**Date:** 2026-06-08
**Trigger:** User reported "I always see the login page now" after the 2026-06-07 mobile-auth PRs landed.
**Branch:** worktree_auth_clear (at main HEAD, 0 divergence — branch name is misleading)
**Investigation:** 8 parallel subagents (Explore) covering: code-path signOut audit, auth.js state machine, recent auth PRs, visibility/reload paths, token refresh, settings sign-out, worktree history, server-side auth.

## ⚠️ CORRECTION (user experience overrides code-analysis hypothesis)

The original fanout synthesis attributed the "I see login page every time" symptom to [PR #7321](https://github.com/jleechanorg/worldarchitect.ai/pull/7321)'s 8s `authInitTimeout` watchdog. **The user has refuted that hypothesis based on actual experience:**

- The mobile freeze ([issue #7320](https://github.com/jleechanorg/worldarchitect.ai/issues/7320)) that [PR #7321](https://github.com/jleechanorg/worldarchitect.ai/pull/7321) was designed to fix is **genuinely improved/resolved** (cold-restart no longer required).
- The "I see login page" regression appeared only after [PR #7349](https://github.com/jleechanorg/worldarchitect.ai/pull/7349) landed.
- The reverted PR is [#7349](https://github.com/jleechanorg/worldarchitect.ai/pull/7349) only; #7321 stays.

**Lesson:** Code analysis on its own produces hypotheses, not facts. The "8s watchdog renders login page when IDB is gone" theory was structurally plausible but empirically wrong. When the user has direct user-experience evidence, that overrides code-trace inference.

The reverted change is in [PR #7365](https://github.com/jleechanorg/worldarchitect.ai/pull/7365) — only the signIn catch gating + function rename of #7349 is undone. The mobile-fix infrastructure from #7321 is preserved.

---

## Original fanout synthesis (now refuted)

**Nothing actively signs the user out.** No `auth.signOut()` in any path other than the explicit `#signOutBtnSettings` click. No `localStorage.removeItem('firebase*')`. No `indexedDB.deleteDatabase`. No `auth.currentUser = null`. No `beforeunload` / idle auto-logout. No service workers. No server-side logout endpoint. The server is stateless Bearer-only with `@check_token` decorator (`main.py:1409`); 401s do NOT auto-logout client-side (the client retries once via `api.js:228-299`).

The fanout synthesis originally attributed the symptom to [PR #7321](https://github.com/jleechanorg/worldarchitect.ai/pull/7321)'s 8s watchdog, which was structurally plausible but **refuted by user experience**.

The actual cause (per user experience) is the [PR #7349](https://github.com/jleechanorg/worldarchitect.ai/pull/7349) signIn catch gating: it was supposed to REDUCE spurious reloads by only firing the visibility recovery on `auth/network-request-failed` / `auth/internal-error` / `auth/timeout` codes. In practice on iPhone Safari (where popups are frequently closed/cancelled/blocked and `authDidInitialize` is false), the gating made the recovery fire LESS often when it was actually needed, leaving the user stranded on the welcome card after each cancelled popup attempt.

## Root cause chain (refined per user experience)

1. iOS Safari/WebKit aggressively evicts `firebaseLocalStorageDB` for backgrounded tabs (acknowledged in auth.js comments).
2. On foreground, Firebase SDK can't rehydrate `currentUser` from missing IDB → `onAuthStateChanged` doesn't fire.
3. The user clicks "Continue with Google" while auth hasn't initialized. The popup opens.
4. Popup is closed/cancelled (frequent on iPhone) → `signInWithPopup` rejects with a non-network error code.
5. Pre-#7349: signIn catch fires `handleVisibilityRecovery()` which schedules a 5s recovery reload. Recovery saves the user.
6. Post-#7349: signIn catch only fires the recovery for network codes. Popup-cancelled error is not a network code → recovery does not fire → user is stranded on the welcome/login card. **THIS is the regression.**

## Diagnostic markers (to capture from user's device)

When the user next sees the login page, look in DevTools console for:

- `[auth] onAuthStateChanged did not fire within 8000ms — rendering fallback logged-out view` → 8s watchdog fired (this is the #7321 path the user wants to KEEP)
- `[auth] visibility recovery: forcing hard reload` → 5s reload path fired (this is the #7321 path the user wants to KEEP)
- Any 401s with `error_type: clock_skew` → clock drift on the device (server tolerance is 60s, `main.py:1595`)

## Risk window worth verifying

`_validate_production_environment` (`main.py:995-1027`) only checks `ENVIRONMENT=stable`, NOT `PRODUCTION_MODE=true`. If the prod deploy sets `PRODUCTION_MODE` but not `ENVIRONMENT=stable`, the startup guard returns early and a `TESTING_AUTH_BYPASS=true` leak would silently allow the bypass. **Confirm with deploy team that prod uses `ENVIRONMENT=stable`.**

## Other PRs ruled out

PRs #7342, #7262, #7237, #7184, #7178, #7113, #7064, #7094, #6636, #6776, #6372 all touch `session_header_utils.py`, level-up state, repro tooling, or CLI agent auth — none affect user-facing Google SSO loss.

## How to apply

- If user complains about "always seeing login page" again, check git log on `mvp_site/frontend_v1/auth.js` for recent signIn-catch gating changes (NOT watchdog/recovery changes)
- The 8s watchdog and 5s reload are the working mobile fix per user experience — do NOT propose reverting them
- DO NOT propose adding backend protection/clamp/sanitizer on auth; the user has been clear about RCF discipline
- If the regression re-appears, the suspect is the signIn catch block at `auth.js:245-250` and the visibility-recovery code-gating, NOT the 8s watchdog
- The worktree name `worktree_auth_clear` is misleading; do not start auth work there without a fresh branch from main

**Why:** Defensive gating on the signIn catch block was supposed to reduce spurious reloads but in the iPhone Safari case (frequent popup-closed/cancelled, stale IDB), it suppresses the recovery exactly when it's needed. Code-trace analysis is a hypothesis; user experience on the actual device is the ground truth.
