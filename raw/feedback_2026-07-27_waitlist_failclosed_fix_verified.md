---
name: waitlist-fail-closed-gate-fabrication-bug-fixed-in-main-beads-need-closing
description: "User-facing bug where transient /api/waitlist/status failure (network error / HTTP 429 rate-limit) caused auth.js to fabricate a deny verdict and render the misleading \"Request waitlist access / WorldAI is currently in private access\" screen — fixed by PRs #8602 + #8599 (merged 2026-07-26); open beads rev-0askj/rev-6lq27/rev-xs1g9 should be closed now."
metadata: 
  node_type: memory
  type: feedback
  bead: rev-0askj
  originSessionId: 009645e4-01e2-45f5-9651-59585e481835
  modified: 2026-07-28T00:30:42.684Z
---

# Context

User reported 2026-07-26: an authorized account (jleechan@gmail.com — the owner) was shown the "Request waitlist access / WorldAI is currently in private access" gate on mvp-site-app-dev while the server's own `/api/waitlist/status` endpoint correctly reported `{waitlist_mode:false, has_access:true, reason:"disabled"}` (no `WAITLIST_MODE_ENABLED` env var set). Sidekick mission `waitlist-gate-authorized-account` traced root cause to client-side fail-closed error handling in `mvp_site/frontend_v1/auth.js` and verified via two independent live reproductions + adversarial verifier (full record: `~/roadmap/sidekick-state-backup-2026-07-26/waitlist-gate-authorized-account/STATE.md`).

# Mechanism (root cause, before fix)

- `mvp_site/frontend_v1/auth.js:291-355 getWaitlistStatus()` calls `GET /api/waitlist/status`.
- `auth.js:321-322` throws on `!response.ok`.
- `auth.js:331-339` catch block **fabricated** `{waitlist_mode:true, has_access:false, reason:'status_unavailable'}` on ANY failure (network error or any non-200, including HTTP 429 from the per-IP rate limiter) and **clobbered `waitlistStatusCache`** with it.
- `hasSiteAccess()` (`auth.js:357-360`) then returned `false` → `renderWaitlistRequestView()` (`auth.js:957` / `:1645`) painted the misleading "Request waitlist access" screen (copy at `auth.js:1111,1127,1130`).
- Aggravating factor: both call sites — sign-in popup (`auth.js:951`) and the `onAuthStateChanged` observer that fires on every page load / token refresh / tab-visibility recovery (`auth.js:1634`) — passed `forceRefresh=true`, so every auth event = one live network call with zero client-side cache or backoff.
- Rate-limit trigger: `mvp_site/waitlist_access.py:131` `@limiter.limit("120 per hour, 30 per minute")`, keyed per client IP (`main.py:1394` via `ProxyFix x_for=1`) — shared across every device/tab/script on the same public IP, not per-user. Dev URL was under concurrent test/automation traffic from sibling lanes in the same session, plausibly sharing the owner's home/office public IP → bucket exhausted from ordinary multi-tab/dev usage.

# Fix (shipped to `origin/main`)

Two PRs merged **2026-07-26**, in this order:

1. **PR #8602** (commit `94d116f17f4`) — **client-side correctness fix**: on fetch failure, return unknown state `{waitlist_mode: null, has_access: null, reason: 'status_unavailable'}` instead of fabricated denial; failure state is **never** written to cache; `hasSiteAccess()` (`auth.js:385`) treats unknown (`waitlist_mode === null || has_access === null`) as access granted (fail-open in UI, server 403 enforces real security); cache and in-flight promise scoped to effective Firebase UID via new `getEffectiveWaitlistUid()` helper (`auth.js:299`). 19 new regression tests added in `mvp_site/frontend_v1/tests/waitlist_access.test.js` (22 total in file).
2. **PR #8599** (commit `6a2796e8d74`) — **server-side operational fix**: `WAITLIST_STATUS_RATE_LIMIT` and `WAITLIST_REQUEST_RATE_LIMIT` env vars override the hardcoded limits; defaults byte-identical to pre-PR; `run_local_server.sh` exports very-high defaults so localhost automation + human browsing don't share one per-IP bucket.

# Verification performed 2026-07-27

Post-`/integrate` branch (`dev1785198509`) sits at `origin/main` (SHA `b6c74b945f91`); both fix commits are reachable from HEAD. Live code at HEAD matches the post-fix contract:

- `mvp_site/frontend_v1/auth.js:288` — `waitlistStatusCacheUid` declared (uid-scoped cache).
- `mvp_site/frontend_v1/auth.js:299` — `getEffectiveWaitlistUid()` helper defined.
- `mvp_site/frontend_v1/auth.js:307` — cache hit requires `waitlistStatusCache && waitlistStatusCacheUid === currentUid`.
- `mvp_site/frontend_v1/auth.js:362-368` — failure path returns `{waitlist_mode: null, has_access: null, reason: 'status_unavailable'}` (verbatim from HEAD).
- `mvp_site/frontend_v1/auth.js:385` — `hasSiteAccess` fail-open on unknown.
- `mvp_site/frontend_v1/tests/waitlist_access.test.js` — 22 tests; explicit 429 transient-failure test at lines 502-511 asserts `status: 429` → `waitlist_mode === null`, `has_access === null`, `reason === 'status_unavailable'`.

# Beads needing closure (operationally stale)

Three beads describe the exact bug and are still OPEN:

- `rev-0askj` — "Failed /api/waitlist/status request renders a fake 'private access' waitlist gate to authorized users" — **closed by PR #8602**.
- `rev-6lq27` — "Waitlist: hasSiteAccess() ignores 'reason'" — **closed by PR #8602** (hasSiteAccess now treats `waitlist_mode === null || has_access === null` as access granted, propagating `reason` to telemetry paths).
- `rev-xs1g9` — "forceRefresh=true on every auth event defeats in-flight request dedupe" — **partially closed by PR #8602** (cache is now uid-scoped and forceRefresh still bypasses cache, but the cache write is keyed by UID so cross-identity pollution is fixed; the dedupe concern remains open as a separate hardening item if desired).

`rev-420rb` ("Derive waitlist gate from authoritative server 403") is a related but distinct design call — PR #8602's tenets explicitly say UI fail-open + server 403 enforcement, so this bead's spirit is partially addressed but not closed.

**Why:** Beads staying open after the fix ships causes future agents to re-investigate a closed issue. Close them with citation: `Closed by PR #8602 (commit 94d116f17f4) + PR #8599 (commit 6a2796e8d74), both merged 2026-07-26. Verified on origin/main at HEAD dev1785198509.`

# Nuance worth flagging if anyone asks

- The user-visible symptom (misleading waitlist gate on transient failure) is fully eliminated by #8602.
- The underlying per-IP 30/min rate limit on `/api/waitlist/status` is still active by default in production. Real users sharing a public IP (school, office NAT, mobile carrier) can still hit 429s on auth callbacks; they just won't see the misleading gate anymore. `hasSiteAccess()` returns `true` (fail-open) and the server enforces real access via 403 on actual API endpoints. This is intentional per the PR's tenets ("A failed question is not an answer"), but worth noting if log noise about 429s comes up.

# Reusable pattern (for future fail-closed UI bugs)

> **A failed question is not an answer.** "We could not check" and "you are not approved" are different states and must not be conflated. UI fail-closed on transient errors is defensible; UI lying about *why* it failed is not. Cache must never persist a fabricated deny; cache must be identity-scoped to prevent cross-account pollution.

This applies to any client-side wrapper that translates a server status call into a user-facing verdict: if the underlying call can fail in a way that confuses "couldn't verify" with "verified-deny", that's the same bug class.

# References

- **PR #8602** — https://github.com/jleechanorg/worldarchitect.ai/pull/8602 (commit `94d116f17f4`, merged 2026-07-26 06:37 UTC)
- **PR #8599** — https://github.com/jleechanorg/worldarchitect.ai/pull/8599 (commit `6a2796e8d74`, merged 2026-07-26 07:14 UTC)
- **Sidekick diagnosis** — `~/roadmap/sidekick-state-backup-2026-07-26/waitlist-gate-authorized-account/STATE.md`
- **Open beads** — `rev-0askj`, `rev-6lq27`, `rev-xs1g9`, `rev-420rb` (all under `.beads/issues.jsonl` via `br show <id>`)
- **Code at HEAD** — `mvp_site/frontend_v1/auth.js:288-407`, `mvp_site/frontend_v1/tests/waitlist_access.test.js:489-521`
- **Integration branch** — `dev1785198509` (this session, 2026-07-27 00:28 UTC)