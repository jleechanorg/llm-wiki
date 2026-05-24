---
name: cache-ttl-pr7074-merged
description: PR #7074 merged — 4hr TTL fix; TTL-expiry rebuild path is dead code in prod; active-play cost dominated by REBUILD_THRESHOLD=5
type: project
bead: rev-guvxx
---

## Context

PR #7074 extended `CACHE_TTL` from `"3600s"` to `"14400s"` and `CACHE_TTL_SECONDS` from 3600 to 14400 in `mvp_site/gemini_cache_manager.py`. Merged 2026-05-24.

## Key Findings

**CACHE_TTL_EXPIRY never fires in production.** Cloud Logging search over 24h returned 0 events for `CACHE_TTL_EXPIRY`. The TTL-expiry proactive rebuild code path is effectively dead — it never triggers during normal play because `REBUILD_THRESHOLD=5` (rebuild every 5 story entries) fires long before the TTL expires.

**The real benefit of 4hr TTL** is keeping the cache warm for players who return after a 1–4hr idle break. Without this, returning players would trigger a cold-start rebuild costing ~$0.013 per session in input tokens.

**Active-play cost is dominated by REBUILD_THRESHOLD=5**, not TTL. Every 5 story entries the cache is rebuilt unconditionally. The only way to reduce active-play rebuild cost is a cache keepalive PATCH on reuse (bead rev-4rvoi) — extending TTL does nothing for this path.

## Rule

Do not confuse TTL-related cost savings with REBUILD_THRESHOLD-related savings. Check Cloud Logging for `CACHE_TTL_EXPIRY` events before claiming TTL extension saves rebuild costs during active play.

**Why:** Assumed TTL expiry was causing costly rebuilds; actual prod data showed 0 expiry events — all rebuilds came from REBUILD_THRESHOLD=5 threshold logic.

**How to apply:** Before any cache TTL work, run: `gcloud logging read 'resource.type="cloud_run_revision" jsonPayload.event="CACHE_TTL_EXPIRY"' --limit=50 --project=worldarchitecture-ai` to verify whether the expiry path is actually being hit.

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7074
- Commits: `d22f6bf7c3` (TTL change), `b31f9416db` (test assertion), `c02561c7b1` (stream retry fix)
- File: `mvp_site/gemini_cache_manager.py:43-44`
- Next bead: rev-4rvoi (cache keepalive PATCH)
