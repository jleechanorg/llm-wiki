---
title: "Mobile welcome-card flash: visibilitychange reload fix (PR #7379)"
type: source
tags: [mobile, auth, visibilitychange, watchdog, pr-7379, worldarchitect-ai]
date: 2026-06-08
source_file: raw/feedback_2026-06-08_mobile_welcome_flash_visibilitychange.md
---

## Summary
User-observed bug on origin/main: mobile shows a welcome card (8s authInitTimeout renders it), then the page reloads ~5s later. The reload fires from the 5s visibility-recovery handler because the welcome card contains #authFallbackRetryBtn (hasRecoveryMarker = false) AND visibilitychange to visible (or online event) fires after the welcome card renders. iPhone Safari address-bar collapse/expand and tab focus can trigger visibilitychange. Fix (PR #7379, head f6501fbd97): in the mobile welcome-card branch, set authDidInitialize = true, clear pending visibilityRecoveryTimer, and remove visibilitychange + online listeners — mirroring the desktop persisted-user branch (auth.js:469-475). 49/49 tests pass.

## Key Claims
- Bug: 5s visibility-recovery handler fires because welcome card has #authFallbackRetryBtn (hasRecoveryMarker = false) AND visibilitychange to visible fires after welcome card renders
- Fix: authDidInitialize = true, clear pending visibilityRecoveryTimer, remove visibilitychange + online listeners in the mobile welcome-card branch
- Mirrors the desktop persisted-user branch contract (auth.js:469-475) and the normal onAuthStateChanged branch (auth.js:630-642)
- User can still click #signInBtn or explicit #authFallbackRetryBtn to recover; only the auto-reload was the flash path

## Connections
- [[auth-catch-recovery-ecode-gate]]
- [[google-sso-login-page-investigation]]
- [[PR7379MobileAuthFlash]]
