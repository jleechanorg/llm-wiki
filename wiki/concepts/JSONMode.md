---
title: "JSON Mode"
type: concept
tags: [json, structured-output, llm]
sources: [openrouter-provider-tests]
last_updated: 2026-04-08
---

JSON mode is a provider feature that instructs the LLM to output valid JSON instead of freeform text.

## Implementation
- Set response_format.type = "json_object" in API payload
- Works with OpenRouter, OpenAI, and compatible providers
- Some providers (Cerebras, OpenRouter) require json_mode=True in request

## Related Pages
- [[OpenRouterProviderTests]] — tests response_format construction
- [[LLMResponse]] — structured response object concept
