---
title: "Provider Selection"
type: concept
tags: [llm, configuration, settings]
sources: [provider-settings-selection-tests]
last_updated: 2026-04-08
---

Provider Selection is the logic that determines which LLM provider (Gemini, OpenRouter, Cerebras) to use for story generation. The `_select_provider_and_model` function in `llm_service.py` implements this logic.

## Selection Priority
1. **FORCE_PROVIDER env var** — highest priority, overrides all user settings
2. **User settings** — `llm_provider` and corresponding model fields
3. **Defaults** — Gemini with `DEFAULT_MODEL`

## Key Behavior
- Invalid/empty provider raises `LLMRequestError` (fail-closed)
- `TESTING_AUTH_BYPASS` does NOT force provider — user settings still apply
- Legacy gemini models redirect to current equivalents
- `user_id=None` returns defaults

## Connections
- [[Gemini]] — default provider
- [[OpenRouter]] — configurable alternative
- [[Cerebras]] — configurable alternative
- [[LLMService]] — implements selection logic
