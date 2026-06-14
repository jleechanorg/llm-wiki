---
name: mobile-welcome-flash-fix
description: PR
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ea7f9127-12cd-4bd5-9ce6-1ebf86c38c62
---

User-observed bug on origin/main: mobile shows a welcome card (8s authInitTimeout renders it), then the page reloads ~5s later. The reload fires from the 5s visibility-recovery handler because the welcome card contains `#authFallbackRetryBtn` (which makes `hasRecoveryMarker = false`), AND a `visibilitychange` to visible (or `online` event) fires after the welcome card renders. iPhone Safari's address-bar collapse/expand and tab focus can trigger `visibilitychange`.

**Fix (PR #7379, head `f6501fbd97`):** In the mobile welcome-card branch of the 8s authInitTimeout (auth.js:482), after rendering the welcome card, set `authDidInitialize = true`, clear any pending `visibilityRecoveryTimer`, and remove the `visibilitychange` and `online` listeners — mirroring the desktop persisted-user branch (auth.js:469-475).

**Why:** This matches the contract used by the normal `onAuthStateChanged` branch (auth.js:630-642). The user can still click `#signInBtn` or the explicit `#authFallbackRetryBtn` to recover. The auto-reload was the path that produced the flash.

**Test changes:**
- New: `8s mobile welcome-card branch suppresses 5s visibility-recovery reload`
- Updated: `8s mobile fallback branch suppresses recovery reload` (was: "still schedules reload after 8s fallback rendered")
- Updated: `fallback signIn() popup rejection does NOT re-arm visibility recovery timer` (was: "re-arms visibility recovery timer")

49/49 tests pass.

**How to apply:** When touching the auth-init watchdog in `mvp_site/frontend_v1/auth.js`, ensure ANY branch that renders UI in the watchdog (desktop indicator, mobile welcome card) suppresses the 5s visibility-recovery reload by setting `authDidInitialize = true`, clearing the pending timer, and removing the listeners. Otherwise the watchdog's UI will flash and reload on iPhone Safari.

**Related memory:** [[auth-catch-recovery-ecode-gate]] (popup rejection gating), [[google-sso-login-page-investigation]] (the prior round's mobile fix #7321 that introduced the welcome-card branch).

**PR:** [PR #7379](https://github.com/jleechanorg/worldarchitect.ai/pull/7379)
