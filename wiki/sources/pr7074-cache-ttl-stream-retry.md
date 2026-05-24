# PR #7074 — Cache TTL fix & stream retry correction

**Ingested**: 2026-05-24  
**Source**: Claude memory, worldarchitect.ai project  
**Type**: project + feedback

## Cache TTL finding

Gemini context cache TTL extended from 1hr to 4hr. Key discovery: `CACHE_TTL_EXPIRY` log event fires **0 times** in 24h of production traffic. The TTL-expiry proactive rebuild path is effectively dead code — all rebuilds come from `REBUILD_THRESHOLD=5` (every 5 story entries). The 4hr TTL only helps returning players who resume after a 1–4hr idle break.

**Next work**: cache keepalive PATCH on reuse (bead rev-4rvoi) to eliminate REBUILD_THRESHOLD rebuilds during active play.

## Stream retry fix

Stream path (`/interaction/stream`) is mutating — it writes to Firestore. Retrying `ConnectionResetError` on stream path duplicates game effects (double dice, double story entries). Fixed by adding injectable `is_retryable_fn` parameter to `_run_with_transport_retry`. Stream path passes `_is_stream_retryable_transport_error` (only pre-connection failures retryable, not `ConnectionResetError`).

## References

- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/7074
- Files: `mvp_site/gemini_cache_manager.py`, `testing_mcp/lib/base_test.py`
- Beads: rev-guvxx (closed), rev-gnzlp (closed), rev-4rvoi (open — next)
