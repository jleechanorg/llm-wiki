---
name: mobile-welcome-flash-is-happy-path-fouc-not-the-8s-reload-loop
description: User-reported mobile welcome-card flash is initial-paint FOUC; PR
metadata: 
  node_type: memory
  type: project
  originSessionId: 6f519ca5-f3e1-4681-91c1-5e50ad2208cf
---

User symptom: on mobile, login/welcome screen **flashes** then the real campaign loads (~1–2s). They want the campaign load kept, flash gone.

**[PR #7379](https://github.com/jleechanorg/worldarchitect.ai/pull/7379) does NOT fix this.** #7379 only touches the **8s `authInitTimeout` mobile branch** in `mvp_site/frontend_v1/auth.js` (lines 476–500): it sets `authDidInitialize=true` and cancels the 5s `visibilityRecoveryTimer` + listeners, suppressing a **post-8s auto-reload** (`window.location.reload()` on `visibilitychange`/`online`). That branch only runs when auth takes **>8s** — it never fires on the happy path, so it cannot stop the user's flash.

**Real cause = FOUC (flash of unauthenticated content) on initial paint:**
- `index.html:97` — `#auth-view` is the **default `active-view`** (visible immediately).
- `index.html:48` — `<body>` has **no auth class** at first paint; `is-logged-out`/`is-authenticated` only applied after `onAuthStateChanged` resolves (`auth.js:653/701`).
- Firebase commonly fires `onAuthStateChanged(null)` first on cold load; `effectiveUser = user || await getEffectiveUser()` (`auth.js:650`). If `getEffectiveUser()` hasn't cached the session, the signed-out branch (`auth.js:699–707`) renders `getLoggedOutAuthMarkup()` → second callback with the real user clears it → `app.js:2616 showView('game')` → **flash**.
- All of this finishes before 8s, independent of #7379's branch.

Welcome-card injection points: `auth.js:480` (8s mobile timeout), `auth.js:707` (signed-out callback). Clears: `auth.js:237/457/697`.

**Proposed fix (bead rev-ljk7h, P1):** render a neutral loading state on first paint (the existing `#loading-overlay` spinner, `index.html:89–95`); reveal the welcome card only once auth resolves **signed-out**. Campaign load path unchanged. UI-visible → needs captioned mobile video tied to HEAD SHA (skeptic Gate 6). Supersedes #7379 for this symptom; #7379's reload-suppression is still valid hardening for the >8s slow-auth case.

Related: [[feedback_2026-06-08_mobile_welcome_flash_visibilitychange]] (the >8s reload loop #7379 actually addresses), [[project_2026-06-08_google_sso_login_page_investigation]] (#7349 regression, reverted by #7365), [[feedback_2026-06-07_auth_catch_recovery_ecode_gate]].

**Why:** Prevents repeating the trap of "fix" #7379 being assumed to cover the user's symptom when it targets a different code path. Code-trace ≠ user-experience.

**How to apply:** When touching mobile auth flash / welcome-card timing, first classify: happy-path FOUC (initial paint, <2s) vs >8s slow-auth reload loop. They are different code paths in `auth.js` and need different fixes.
