# CachedSystemInstructionTokens

**Created**: 2026-05-12
**Source**: [gemini-ttfc-ablation-2026-05-12](../sources/gemini-ttfc-ablation-2026-05-12.md)

## Definition

Gemini API caches system instruction tokens separately from prompt tokens. Full WorldArchitect.AI prompt files (813KB across 26 files) generate ~200K cached system instruction tokens. These cached tokens are the dominant cost for TTFC — reducing them from 200K to ~1K (by summarizing instruction files to 5KB each) delivers 4x TTFC speedup.

## Key Insight

Moderate token reductions (15-47%) that leave cached system instructions intact produce NO TTFC improvement (AB1/AB2 null results). Only drastic reduction of cached system instruction tokens crosses the threshold where TTFC improves.

## Cache Rebuild Triggers (2026-05-24)

Two distinct rebuild triggers:
1. **REBUILD_THRESHOLD=5**: Unconditional rebuild every 5 story entries during active play — dominant cost driver.
2. **TTL expiry proactive rebuild**: Fires when cache nears TTL boundary — 0 events in 24h prod logs (`CACHE_TTL_EXPIRY` event). Effectively dead code during normal play.

TTL extension (1hr→4hr, PR #7074) helps returning players (idle 1–4hr) but has no effect on active-play rebuild cost. Real active-play cost reduction requires cache keepalive PATCH on reuse (bead rev-4rvoi).

## Related

- [[GeminiApiVariance]] — below 78K prompt tokens, API variance dominates
- [[CodeExecutionSandboxOverhead]] — additional ~6s when sandbox fires
- [pr7074-cache-ttl-stream-retry](../sources/pr7074-cache-ttl-stream-retry.md) — TTL findings and stream retry fix
