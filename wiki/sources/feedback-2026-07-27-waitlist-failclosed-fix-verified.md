---
title: "Waitlist fail-closed gate fabrication: bug fixed in main, beads need closing"
type: source
tags: [feedback, waitlist, fail-closed, auth.js, regression-test, postmortem]
date: 2026-07-27
source_file: ../../raw/feedback_2026-07-27_waitlist_failclosed_fix_verified.md
---

## Summary
User-visible bug where transient `/api/waitlist/status` failure (network error or HTTP 429 from the per-IP rate limiter) caused `mvp_site/frontend_v1/auth.js:331-339` to fabricate a deny verdict and render the misleading "Request waitlist access / WorldAI is currently in private access" screen — to an authorized account. Fixed by PRs #8602 (client-side correctness) and #8599 (server-side operability), both merged 2026-07-26. Verified at HEAD `b6c74b945f91`. Open beads `rev-0askj`, `rev-6lq27`, `rev-xs1g9` should be closed now.

## Key Claims
- **Root cause** was client-side fail-closed error handling at `mvp_site/frontend_v1/auth.js:331-339` that fabricated `{waitlist_mode:true, has_access:false, reason:'status_unavailable'}` on ANY fetch failure (network error or non-2xx including HTTP 429) and clobbered `waitlistStatusCache`.
- **Trigger** was the per-IP rate limiter on `/api/waitlist/status` (`mvp_site/waitlist_access.py:131` `@limiter.limit("120 per hour, 30 per minute")`, keyed per client IP via `ProxyFix x_for=1`), shared across every device/tab/script on the same public IP.
- **Aggravating factor**: both call sites — sign-in popup (`auth.js:951`) and the `onAuthStateChanged` observer (`auth.js:1634`) — passed `forceRefresh=true`, so every auth event bypassed cache with zero client-side backoff.
- **Fix shipped**: PR #8602 (`94d116f17f4`) returns unknown state on failure (never persisted), `hasSiteAccess` fail-open on unknown, cache uid-scoped via `getEffectiveWaitlistUid()`; PR #8599 (`6a2796e8d74`) makes rate limits env-overridable.
- **Verified live at HEAD `b6c74b945f91`** (post-`/integrate` branch `dev1785198509`): `auth.js:362-368` returns the unknown state shape verbatim; 22 regression tests including explicit HTTP 429 test at lines 502-511.
- **Beads needing closure**: `rev-0askj` (closed), `rev-6lq27` (closed), `rev-xs1g9` (partially closed — dedupe concern remains).

## Key Quotes
> "A failed question is not an answer. We could not check and you are not approved are different states and must not be conflated." — PR #8602 tenets

> "UI fail-closed on transient errors is defensible; UI lying about *why* it failed is not." — derived pattern

## Connections
- [[FailClosedUIAntiPattern]] — general class of bug where a failed check is conflated with a verified-deny verdict
- [[PerIPRateLimiterFootgun]] — why shared-IP rate limits + force-refresh-on-every-auth-event creates user-visible damage
- [[WorldArchitectWaitlistGate]] — specific UI surface (auth.js:1111/1127/1130) that rendered the misleading copy
- [[ZeroFrameworkCognition]] — related principle: UI must not invent state the server didn't return
- [[MemoryHygieneForBeadClosure]] — operational follow-up: closing resolved beads prevents re-investigation