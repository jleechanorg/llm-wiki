---
title: "Google SSO 'login page every time' investigation"
type: source
tags: [auth, sso, google, login-page, user-experience, pr-7349, worldarchitect-ai]
date: 2026-06-08
source_file: raw/project_2026-06-08_google_sso_login_page_investigation.md
---

## Summary
User reported 'I always see the login page now' after 2026-06-07 mobile-auth PRs landed. 8 parallel subagents (Explore) fanout investigation originally attributed to PR #7321's 8s authInitTimeout watchdog — but user refuted this based on actual experience: mobile freeze fix in #7321 is genuinely improved; the login-page regression appeared only after PR #7349 landed. Root cause: PR #7349's signIn catch gating was supposed to reduce spurious reloads by only firing visibility recovery on network codes; in practice on iPhone Safari (frequent popup-closed/cancelled/blocked), it suppressed recovery exactly when needed, leaving user stranded. Reverted in PR #7365 — only signIn catch gating + function rename of #7349 is undone; #7321 mobile-fix infrastructure preserved.

## Key Claims
- Fanout synthesis originally attributed to PR #7321's 8s watchdog — REFUTED by user experience. Actual cause is PR #7349's signIn catch gating
- Mobile freeze fix in #7321 is genuinely improved (cold-restart no longer required). Reverted PR is #7349 only; #7321 stays
- Root cause: PR #7349 signIn catch only fires recovery for network codes. Popup-cancelled error is not a network code → recovery does not fire → user stranded on welcome card
- Diagnostic markers: '[auth] onAuthStateChanged did not fire within 8000ms' (8s watchdog, KEEP); '[auth] visibility recovery: forcing hard reload' (5s reload, KEEP)
- Code analysis produces hypotheses, not facts. When user has direct experience evidence, that overrides code-trace inference
- Risk window: _validate_production_environment (main.py:995-1027) only checks ENVIRONMENT=stable, NOT PRODUCTION_MODE=true. If prod sets PRODUCTION_MODE but not ENVIRONMENT=stable, startup guard returns early and TESTING_AUTH_BYPASS=true leak would silently allow bypass

## Connections
- [[feedback_2026-06-08_mobile_welcome_flash_visibilitychange]]
- [[feedback_2026-06-08_mobile_welcome_flash_is_fouc_not_reload]]
- [[feedback_2026-06-07_auth_catch_recovery_ecode_gate]]
- [[PR7349SSORegression]]
