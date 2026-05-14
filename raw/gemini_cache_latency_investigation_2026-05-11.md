---
name: Gemini context cache does NOT reduce TTFC — story mode latency measured
description: Measured STREAM_TIMING data proves Gemini cache adds latency; 95% of request time is Gemini API inference
type: project
bead: none
originSessionId: 87526ec4-b7e8-4d78-9461-c84fd2558341
---
## Root Finding (measured, not guessed)

**95% of streaming request latency is Gemini API inference (`llm_time_to_first_chunk`).** All Python server code combined is <100ms.

### Per-phase measured medians (from server log, N=37 story-mode requests)

| Phase | Median | Max | Notes |
|---|---|---|---|
| `llm_time_to_first_chunk` (Gemini API) | 12.7s | 28.9s | **95% of total** |
| `flask_handler_total` | 23.3s | 45.3s | Includes streaming output |
| All Python prep (provider, dice, system_instruction, budget, truncation, serialize) | <0.01s | 0.08s | Negligible |
| Firestore prefetch | 0.3s | 0.4s | Only non-Gemini seconds |
| `cache_section_total` | 0.005s | 0.28s | Cache creation overhead |

### Gemini context cache is NOT reducing TTFC

**Why:** We already use Gemini 3 Flash (fastest available). Context caching saves our server ~1s of cache creation but Gemini reports `cached_tokens=0` for most story-mode requests, meaning Gemini is NOT using the cache despite us passing `cachedContents/...` references.

**Measured TTFC by cache status:**
- Cache `reused`: median 13.2s, max 28.9s
- Cache `async_created`: median 11.6s, max 23.2s
- **Uncached** (`async_deferred_uncached`): **median 9.6s**, max 16.5s

**The uncached path is FASTER.** The cache appears to add overhead rather than reduce it. Possible causes: cache reference resolution time on Gemini's side, stale cache content requiring re-processing, or prompt content mismatch causing full re-read.

**Why (hypothesis):** Gemini's context caching may have overhead in resolving the cache reference + partial cache misses that still require processing. When `cached_tokens` shows >0 (character creation hits at 73-94%), it works. But for story mode, the cache content drifts as story entries change, causing Gemini to re-process despite the reference.

### Sub-60K prompt misses are character creation mode (no cache_section_total)

The 74K+ prompt misses are a different code path (character creation / non-streaming) that doesn't use Gemini context caching at all. These are NOT the latency problem.

## Actionable Next Steps

1. **Investigate WHY Gemini cache misses for story mode** — the `cached_tokens=0` in GEMINI_USAGE means the cache reference is being ignored
2. **Consider disabling Gemini context caching for story mode** since it adds latency — the uncached path is faster
3. **Reduce prompt token count** — currently 52-77K tokens per request; reducing by 30% could save 3-5s on Gemini inference
4. **Investigate Gemini API regional latency** — test if different Gemini endpoints have different TTFC

## Data Provenance

- Server log: `/var/folders/j0/byd1z6px50v88lf679bgt0h00000gn/T/worldarchitect.ai/investigate-gcp-latency/app.log`
- Branch: `investigate-gcp-latency`, SHA `2a3aa9b` (includes STREAM_TIMING instrumentation)
- Profiler: `/private/tmp/latency_profile.py`
- Frontend timing: `mvp_site/frontend_v1/js/streaming.js` + `app.js` (6 `performance.mark` points)
