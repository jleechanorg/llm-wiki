# Gemini Context Cache: Investigation Results (Updated 2026-05-12)

**Date**: 2026-05-11 (updated 2026-05-12)
**Branch**: investigate-gcp-latency
**PR**: [#6840](https://github.com/jleechanorg/worldarchitect.ai/pull/6840)

## Summary

Measured STREAM_TIMING instrumentation shows Gemini API inference dominates TTFC. Initial hypothesis that explicit cache was broken for story mode was **DISPROVEN** — explicit cache DOES work for story-mode streaming requests after the first request (73-94% hit rates, 53-54K cached tokens).

## Key Measurements

| Metric | Value |
|---|---|
| **Gemini API inference** (llm_time_to_first_chunk) | 12.7s median, 28.9s max |
| All Python server code combined | <100ms |
| Prompt token range | 52K-77K |

## Cache Status: WORKING (Corrected)

**Original hypothesis (WRONG)**: Cache stores entries as individual Part objects, request sends merged JSON — structurally incompatible, no token prefix match.

**Actual measurement (2026-05-12)**: Explicit cache DOES hit for story-mode streaming after first request.

| Request # | prompt_tokens | cached_tokens | hit_rate | cache_name |
|---|---|---|---|---|
| 1 (no cache yet) | 53,112 | 0 | 0% | none |
| 2 | 56,843 | 53,672 | 94.4% | cachedContents/qki5i78... |
| 3 | 69,624 | 53,672 | 77.1% | cachedContents/qki5i78... |
| 4 | 58,750 | 53,672 | 91.4% | cachedContents/qki5i78... |
| 5 | 58,907 | 54,040 | 91.7% | cachedContents/00jx49zj... |
| 6 | 73,895 | 54,040 | 73.1% | cachedContents/00jx49zj... |

First request always has cached_tokens=0 (no cache exists yet). Subsequent requests get 53-54K cached tokens.

## Why Cache Didn't Help TTFC (Earlier A/B Test)

Even with cache hits, TTFC was HIGHER with cache enabled (13.2s) vs disabled (9.6s). Possible reasons:
1. Cache reference resolution adds overhead on Gemini's side
2. Cache reuse still requires processing uncached tokens (20-27% of prompt)
3. The overhead of cache lookup + partial re-processing exceeds the savings

## Remaining Investigation

1. Measure TTFC with cache hits vs without (controlled test with same prompt size)
2. Consider whether cache overhead is worth the token cost savings
3. Reduce prompt token count (52-77K) — still the primary TTFC lever
4. Never guess at latency — always measure with STREAM_TIMING
