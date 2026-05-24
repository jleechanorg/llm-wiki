# GeminiContextCacheTTL

**Created**: 2026-05-24
**Source**: [gemini-cost-investigation-2026-05-24](../sources/gemini-cost-investigation-2026-05-24.md)

## Definition

Gemini API context caches store the full conversation history (system prompt + story turns) for a session. In worldarchitect.ai, each cache holds 110K–165K tokens. The TTL determines how long the cache is held before requiring full re-input.

## Cost Formula

```
daily_storage_cost = creates_per_hour × tokens_per_cache × price_per_1M × hours_active
                   = 20 × 165K/1M × $1.00 × 24
                   ≈ $66/day at TTL=1hr
```

At TTL=4hr, creates_per_hour drops to ~5 → $16/day storage.

## Key Insight

Storage cost accrues **continuously all day**, not just at peak hours. An estimate based on peak-only calls will undercount by 3-4×. With 1hr TTL, every cache that is created restarts the billing clock — even if the session is idle.

## Pricing (gemini-3-flash-preview)

| Type | Rate |
|------|------|
| Cache storage | $1.00 / 1M tokens / hour |
| Cache write | $0.05 / 1M tokens |
| Cache read | $0.05 / 1M tokens |
| Input (non-cached) | $0.50 / 1M tokens |
| Output | $3.00 / 1M tokens |

## Log Labels for Diagnosis

- `STREAM_CACHE_USAGE source=created` — new cache (full input billed)
- `STREAM_CACHE_USAGE source=reused` — cache hit (cheap read)
- `STREAM_CACHE_USAGE source=not_used` — mock mode (zero billing)
- `GEMINI_STREAM_USAGE cache_hit_rate=N` — per-call hit rate

## Fix Applied

`mvp_site/gemini_cache_manager.py:43` changed from `CACHE_TTL = "3600s"` to `CACHE_TTL = "14400s"` (PR #7074).

## Innovation Opportunity

Activity-aware TTL refresh (cache keepalive): on each cache reuse, if remaining TTL < threshold, issue a PATCH to extend TTL. This decouples cache lifetime from wall-clock time to "time since last player action," eliminating churn during active gameplay.

## Related

- [[CachedSystemInstructionTokens]] — system instruction token overhead
- [[GeminiApiVariance]] — below-threshold prompt variance
