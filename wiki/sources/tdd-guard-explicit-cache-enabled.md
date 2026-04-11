---
title: "Explicit Cache Enabled TDD Guard Tests"
type: source
tags: [python, testing, caching, gemini, llm-service]
source_file: "raw/test_explicit_cache_enabled.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests asserting that the explicit cache code path is active in llm_service.py. Tests validate that explicit_cache_enabled is True (not disabled), enabling Gemini context cache usage. Also validates is_think_mode and force_tool_mode propagation through the cache path.

## Key Claims
- **explicit_cache_enabled**: Must be True so the explicit cache path is reached (currently may be disabled/blocked)
- **is_think_mode Propagation**: is_think_mode=True must forward to _call_llm_api_with_explicit_cache
- **force_tool_mode Preservation**: force_tool_mode must be preserved when cache creation fails and falls back to direct API call
- **Pending Cache Deletion**: Pending cache entries should be deleted remotely
- **REV-5ix Fix**: explicit_cache_enabled was disabled (False) blocking Gemini context cache usage
- **DICE-s8u Resolution**: DICE-s8u fix adds code_execution tool into cache itself, resolving Gemini API constraint

## Key Quotes
> "explicit_cache_enabled must be True so the cache path is reached. Check llm_service.py: 'explicit_cache_enabled = True'"

## Connections
- [[llm_service]] — module under test
- [[LLMRequest]] — request class used for cache routing
- [[GeminiProvider]] — provider that uses explicit caching

## Contradictions
- None identified in this test file
