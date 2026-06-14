---
title: "Mobile welcome-card flash is FOUC, not the 8s reload loop"
type: source
tags: [mobile, auth, fouc, welcome-card, worldarchitect-ai]
date: 2026-06-08
source_file: raw/project_2026-06-08_mobile_welcome_flash_is_fouc_not_reload.md
---

## Summary
User-reported mobile welcome-card flash is initial-paint FOUC, NOT the 8s authInitTimeout reload loop that PR #7379 fixes. PR #7379 only touches the post-8s mobile branch in auth.js (lines 476–500); that branch never fires on the happy path, so it cannot stop the user's flash. Real cause: index.html:97 sets #auth-view as default active-view, body has no auth class at first paint; Firebase commonly fires onAuthStateChanged(null) first on cold load → renders logged-out view → second callback with real user clears it → app.js:2616 showView('game') = flash. All <2s, independent of #7379. Proposed fix: render neutral loading state (#loading-overlay spinner) on first paint, reveal welcome card only once auth resolves signed-out. Bead rev-ljk7h P1.

## Key Claims
- PR #7379 does NOT fix the user's flash — it only touches the 8s mobile branch, which never fires on the happy path
- Real cause = FOUC: #auth-view is default active-view (index.html:97), body has no auth class at first paint, onAuthStateChanged(null) fires first on cold load and renders logged-out view
- All of this finishes before 8s, independent of #7379's branch
- Fix proposal: render #loading-overlay spinner on first paint; reveal welcome card only once auth resolves signed-out; campaign load path unchanged

## Connections
- [[feedback_2026-06-08_mobile_welcome_flash_visibilitychange]]
- [[project_2026-06-08_google_sso_login_page_investigation]]
- [[feedback_2026-06-07_auth_catch_recovery_ecode_gate]]
- [[PR7379MobileAuthFlash]]
