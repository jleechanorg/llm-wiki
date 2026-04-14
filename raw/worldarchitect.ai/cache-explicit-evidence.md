# Explicit Cache Evidence — fix/cache-context-reclassification

**Branch**: fix/cache-context-reclassification
**PR**: #5813
**Date**: 2026-03-05
**Git SHA**: `9e4079d243` (latest)

## Summary

This PR fixes explicit caching end-to-end:

1. **Double-billing fix**: Old story entries were sent in both cache prefix ($0.05/M) AND live JSON ($0.50/M). Fixed by concatenating full `story_history` in the merged payload.
2. **Cache/provably-fair incompatibility fix (REV-wvh)**: Provably fair seed was injected into `system_instruction`, making it dynamic and breaking cache. Fixed by moving seed to a prepended content part — system_instruction stays static and cacheable.
3. **Never-disable-cache fix (REV-8gz)**: Removed all `effective_cache_name = None` patterns that silently disabled cache in `generate_content_with_code_execution` and `generate_content_with_native_tools`.
4. **N-1 cache promotion**: New caches are staged as "pending" and promoted on the next request to avoid Gemini propagation delay.

## Test 1: Cache Prompt Equivalence

**Test**: `testing_mcp/cache/test_cache_prompt_equivalence.py`
**Result**: PASS (1/1)

Both cache and non-cache paths produce identical JSON payloads. `story_history` contains all entries (cacheable + uncacheable concatenated), matching `LLMRequest.to_json()` exactly.

## Test 2: Explicit Cache Verification (Hit Rate)

**Test**: `testing_mcp/cache/test_explicit_cache_verification.py`
**Result**: PASS — 89-93% cache hit rate across all requests
**Server log**: `/tmp/mcp_server_logs/local_mcp_49959.log`

### Cache Hit Rates (all requests)

| Request | Prompt Tokens | Cached Tokens | Hit Rate |
|---------|--------------|---------------|----------|
| Measurement 1 | 91,247 | 84,659 | **92.8%** |
| Measurement 2 | 94,524 | 85,559 | **90.5%** |
| Post-rebuild 1 | 94,166 | 85,559 | **90.9%** |
| Post-rebuild 2 | 94,982 | 85,559 | **90.1%** |
| Post-rebuild 3 | 98,232 | 87,818 | **89.4%** |
| Post-rebuild 4 | 98,150 | 87,818 | **89.5%** |

### Key Metrics

| Metric | Value |
|--------|-------|
| CACHE_REFERENCE log entries | **12** (every request used cache) |
| PROVABLY_FAIR commitments | **12** (every request had unique seed) |
| CACHE_NOT_HIT warnings | **0** |
| CACHE_BUILD events | **4** |
| CACHE_REUSE events | **8** |
| Rebuild threshold | **5** (verified) |

### Before vs After

| Metric | Before (old code) | After (this PR) |
|--------|-------------------|-----------------|
| `CACHE_REFERENCE` log entries | **0** (never appeared) | **12** |
| `effective_cache_name` | `None` (silently disabled) | Cache name passed through |
| Cache hit rate | **0%** | **89-93%** |
| Provably fair + cache | Mutually exclusive | Compatible |

### Root Cause

`generate_content_with_code_execution` in `gemini_provider.py` set `effective_cache_name = None` with zero logging because the provably fair seed was injected into `system_instruction_text`, making it dynamic and incompatible with the static cached system_instruction.

### Fix

Moved the provably fair seed from `system_instruction` to a prepended `types.Content` part in `prompt_contents`. The static `CODE_EXECUTION_DICE_OVERRIDE` (with `time.time_ns()` examples) stays in the cache. Each request prepends:

```
PROVABLY_FAIR_SEED_OVERRIDE: For ALL dice code in this response,
use `random.seed('{hex_seed}')` as the FIRST line instead of
`random.seed(time.time_ns())`.
```

## Test 3: Unit Tests (TDD Guards)

**Test**: `mvp_site/tests/test_cache_provably_fair.py`
**Result**: PASS (3/3)

1. `test_code_execution_passes_cache_name_through` — cache_name reaches API
2. `test_seed_injected_as_content_part_not_system_instruction` — seed in content, not system_instruction
3. `test_native_tools_does_not_disable_cache` — cache survives Phase 2 tool execution

## Cache Operations Log

```
CACHE_BUILD: Build 1: entries=2, previously=0
CACHE_BUILD: Build 2: entries=8, previously=2
CACHE_BUILD: Build 3: entries=14, previously=8
CACHE_BUILD: Build 4: entries=20, previously=14
```

Cache rebuilds occur at threshold=5 with N-1 promotion (old cache used for current request, new cache promoted on next request).
