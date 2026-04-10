---
title: "Explicit Caching"
type: concept
tags: [caching, gemini, llm-service, performance]
sources: [sources/tdd-guard-explicit-cache-enabled.md]
last_updated: 2026-04-08
---

## Definition
Explicit caching is a mechanism in llm_service.py that enables Gemini context cache usage for API requests. When enabled (explicit_cache_enabled = True), the system routes requests through _call_llm_api_with_explicit_cache instead of the standard path.

## Key Properties
- **Enabled via**: explicit_cache_enabled flag in llm_service.py
- **Cache key**: campaign_id + story_history combination
- **Fallback**: Falls back to _call_llm_api when cache creation fails
- **Token Reserve**: DICE-s8u adds code_execution tool into cache to resolve Gemini API constraints

## Related Tests
- [[TDDFGuardExplicitCacheEnabled]] — validates cache path is active
- [[ThinkModePropagation]] — validates is_think_mode passes through cache
- [[ForceToolModePropagation]] — validates force_tool_mode preserved on fallback
