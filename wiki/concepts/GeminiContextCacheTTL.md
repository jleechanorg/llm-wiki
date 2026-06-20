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

## Shared System/Tools-Only Cache (2026-06-04 spike, GO)

The current per-campaign cache stores system+tools redundantly per active campaign — that O(campaigns) storage rent was the dominant pre-#7215 cost. A measured spike ([shared-system-tools-cache-spike-2026-06-04](../sources/shared-system-tools-cache-spike-2026-06-04.md)) proves a single **shared, campaign-free, system/tools-only explicit cache** keyed by `(model, system_prompt_sha256, tool_signature_sha256)` discounts 99.8% of the static floor on read and collapses storage **O(campaigns)=$1,440/day → O(~6 caches)=$8.64/day** (Option 2 = −74%/call). Constraint: `cached_content` is a single `Optional[str]` (one cache/request), and referencing a cache while also setting `system_instruction`/`tools` returns HTTP 400 — system must move fully into the cache. Verdict GO → impl bead `rev-n6nbs.1`; PR [#7259](https://github.com/jleechanorg/worldarchitect.ai/pull/7259) (OPEN, human-gated).

## Related

- [CachedSystemInstructionTokens](CachedSystemInstructionTokens.md) — system instruction token overhead
- [GeminiApiVariance](GeminiApiVariance.md) — below-threshold prompt variance
- [GeminiCostApportionment](GeminiCostApportionment.md) — cost epic this spike feeds (rev-9piwk)
