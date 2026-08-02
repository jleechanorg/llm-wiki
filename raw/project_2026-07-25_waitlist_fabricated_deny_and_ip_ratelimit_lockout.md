---
name: waitlist-fabricated-deny-and-ip-ratelimit-lockout
description: auth.js fabricated a cached waitlist-deny on ANY fetch failure; our own screenshot automation drained the shared per-IP rate-limit bucket and locked the repo owner out of his own dev site
metadata: 
  node_type: memory
  type: project
  originSessionId: bc3b0c3b-7695-40fc-916d-e83f512181b9
  modified: 2026-07-26T06:24:44.179Z
---

**FIX: shipped.** `mvp_site/frontend_v1/auth.js` (worldarchitect.ai repo) had a catch block that fabricated `{waitlist_mode:true, has_access:false}` on ANY fetch failure to `/api/waitlist/status`, and CACHED that fabricated deny. `/api/waitlist/status` is rate-limited 120/hr + 30/min keyed per **client IP** (`waitlist_access.py:131`, `main.py:1394`). Both call sites pass `forceRefresh=true` (`auth.js:951` and `:1634` — the latter inside `onAuthStateChanged`, so it fires on every page load / token refresh / tab refocus). Our own screenshot-capture automation hammered the endpoint from the shared dev-site IP, drained the bucket, got 429s, and the catch block turned those 429s into a cached "you're on the waitlist, no access" screen for the real account too — locking the repo owner out of his own dev site.

Reproduced directly: requests 1-30 → 200, 31-35 → 429 (confirms the bucket, not a per-user gate).

Fix PR: [#8602](https://github.com/jleechanorg/worldarchitect.ai/pull/8602) (stop fabricating/caching a deny state from a transport failure). Rate-limit env-override PR: [#8599](https://github.com/jleechanorg/worldarchitect.ai/pull/8599). Beads: rev-0askj, rev-xs1g9, rev-420rb, rev-bu30q.

**A "fix" that shipped the original bug through the most common path**: an earlier round reported `IMPLEMENTATION_READY` with 18/18 tests passing, but the fix used an identity-blind cache that reused a signed-out deny verdict after sign-in — same bug, different trigger. Caught by a parallel adversarial reviewer tracing the actual sign-in sequence step by step, not by reading the diff. See [[feedback_2026-07-25_verify_different_layer_than_claim_layer]].

**How to apply / generalize:** [[feedback_2026-07-25_automated_browser_traffic_shares_ip_ratelimit_bucket]] — before running capture/UI automation against a shared deployment, check for per-IP rate limits or run against a local server instead.
