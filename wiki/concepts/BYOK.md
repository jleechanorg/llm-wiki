---
title: "BYOK (Bring Your Own Key)"
type: concept
tags: [byok, api-keys, rate-limiting, pricing]
sources: []
last_updated: 2026-04-08
---

## Summary
BYOK (Bring Your Own Key) is a pricing model where users provide their own LLM API key (e.g., OpenRouter) in exchange for elevated rate limits.

## Key Claims
- **Elevated daily limit**: BYOK users receive RATE_LIMIT_BYOK_PROVIDER_DAILY_TURNS instead of default
- **Elevated 5-hour limit**: BYOK users receive RATE_LIMIT_BYOK_PROVIDER_5HOUR_TURNS instead of default
- **Provider matching**: User must provide API key matching their selected llm_provider setting
- **Default provider**: If no provider specified, defaults to Gemini for key matching

## Detection Logic
is_byok_provider_active checks:
1. User settings dict contains provider (llm_provider field)
2. Corresponding API key field exists (e.g., openrouter_api_key for openrouter provider)
3. Key value is non-empty

## Related Concepts
- [[RateLimiting]] - Rate limiting system BYOK extends
