---
title: "Explicit Cache Evidence — PR #5813"
type: source
tags: [caching, gemini, mvp-site, bug-fix, billing, provably-fair]
source_file: "raw/explicit-cache-evidence-pr-5813.md"
sources: []
last_updated: 2026-04-07
---

## Summary
This PR fixes explicit caching end-to-end in the MVP site codebase. Three major fixes: double-billing fix (concatenating full story_history), cache/provably-fair incompatibility fix (moving seed to prepended content), and never-disable-cache fix (removing effective_cache_name = None patterns). Achieved 89-93% cache hit rate.

## Key Claims
- **Double-billing fix**: Old story entries were sent in both cache prefix ($0.05/M) AND live JSON ($0.50/M). Fixed by concatenating full `story_history` in the merged payload.
- **Cache/provably-fair incompatibility fix (REV-wvh)**: Provably fair seed was injected into `system_instruction`, making it dynamic and breaking cache. Fixed by moving seed to a prepended content part.
- **Never-disable-cache fix (REV-8gz)**: Removed all `effective_cache_name = None` patterns that silently disabled cache.
- **N-1 cache promotion**: New caches staged as "pending" and promoted on next request to avoid Gemini propagation delay.
- **89-93% cache hit rate**: Achieved across all test requests.

## Key Technical Details
- **Root cause**: `generate_content_with_code_execution` in `gemini_provider.py` set `effective_cache_name = None` with zero logging
- **Fix**: Moved provably fair seed from `system_instruction` to prepended `types.Content` part in `prompt_contents`
- **Cache rebuild threshold**: 5 entries
- **Rebuilds observed**: 4 (Build 1→4, entries growing from 2→20)

## Test Results
- `test_cache_prompt_equivalence.py`: PASS — cache and non-cache paths produce identical JSON
- `test_explicit_cache_verification.py`: PASS — 89-93% cache hit rate
- `test_cache_provably_fair.py`: PASS (3/3) — TDD guards for cache_name passthrough, seed placement, native tools

## Connections
- [[GeminiProvider]] — provider where caching was broken
- [[ExplicitCaching]] — concept this PR fixes
- [[ProvablyFairDice]] — dice system that conflicted with caching
