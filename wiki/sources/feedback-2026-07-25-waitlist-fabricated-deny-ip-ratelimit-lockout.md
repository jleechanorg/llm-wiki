---
title: "Waitlist Fabricated Deny + Shared-IP Rate-Limit Lockout"
type: source
tags: [worldarchitect-ai, waitlist, rate-limiting, auth, incident]
date: 2026-07-25
source_file: raw/project_2026-07-25_waitlist_fabricated_deny_and_ip_ratelimit_lockout.md
---

## Summary
`mvp_site/frontend_v1/auth.js` in worldarchitect.ai fabricated and cached a `{waitlist_mode:true, has_access:false}` verdict on ANY fetch failure to `/api/waitlist/status`, an endpoint rate-limited 120/hr + 30/min per client IP. Because both call sites pass `forceRefresh=true` (including one inside `onAuthStateChanged`, firing on every page load/token refresh/tab refocus), an unrelated automation run (screenshot-capture traffic against the shared GCP dev site) drained the shared IP bucket, got 429s, and the frontend turned those transport failures into a real, cached "you're on the waitlist" lockout screen for the repo owner's own account on his own dev site.

## Key Claims
- Root cause was NOT a real waitlist/access-control decision — it was a UI-layer fabrication of a deny state from a transport error, then caching that fabrication.
- Rate limit confirmed empirically: requests 1-30 → 200, 31-35 → 429 (`waitlist_access.py:131`, `main.py:1394`).
- An early "fix" attempt reported `IMPLEMENTATION_READY` with 18/18 passing tests but actually shipped the same bug through a different path — an identity-blind cache reusing a signed-out deny verdict after sign-in. Caught only by a parallel reviewer tracing the actual sign-in sequence, not by reading the diff or trusting the test suite.
- Fixed in PR #8602 (stop fabricating/caching deny from transport failure) and PR #8599 (rate-limit env override for local testing).

## Key Quotes
> "Our own screenshot-capture automation drained the shared IP bucket and locked the repo owner out of his own dev site."

## Connections
- [[automated-browser-traffic-shares-ip-ratelimit-bucket-2026-07-25]] — the generalized lesson (check per-IP limits before running automation against shared deployments)
- [[verify-different-layer-than-claim-layer-2026-07-25]] — how the wrong-fix regression was actually caught
- [[worldarchitect-ai]]
