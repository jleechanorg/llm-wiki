---
title: "Provider Settings Selection Tests"
type: source
tags: [python, testing, llm, provider-selection, settings]
source_file: "raw/test_provider_settings_selection.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating the `_select_provider_and_model` function in `llm_service.py`. Tests verify provider selection logic including default Gemini selection, OpenRouter/Cerebras preference handling, invalid provider error handling, environment variable overrides, and legacy model mapping.

## Key Claims
- **Default Gemini provider**: When no user settings exist, returns `DEFAULT_LLM_PROVIDER` and `DEFAULT_MODEL`
- **OpenRouter preference**: User's `llm_provider: "openrouter"` with `openrouter_model` is respected
- **Cerebras preference**: User's `llm_provider: "cerebras"` with `cerebras_model: "llama-3.3-70b"` is respected
- **Invalid provider error**: Empty or invalid `llm_provider` raises `LLMRequestError` with `PROVIDER_SELECTION_INVALID_PROVIDER`
- **FORCE_PROVIDER env var**: Overrides user settings when set (e.g., `FORCE_PROVIDER=gemini`)
- **TESTING_AUTH_BYPASS behavior**: Does NOT force provider - user settings are still respected
- **Legacy model mapping**: Legacy gemini models like `gemini-2.5-pro` redirect to current models

## Key Test Cases
| Test | Expected Behavior |
|------|-------------------|
| `test_selects_gemini_by_default` | Returns default provider/model when no user settings |
| `test_prefers_openrouter_when_configured` | Uses user's OpenRouter model selection |
| `test_prefers_cerebras_when_configured` | Uses Cerebras with `llama-3.3-70b` |
| `test_invalid_provider_raises_fail_closed_error` | Raises error for invalid provider |
| `test_empty_provider_raises_fail_closed_error` | Raises error for empty provider string |
| `test_no_user_id_returns_defaults` | Returns defaults when `user_id` is `None` |
| `test_force_provider_env` | `FORCE_PROVIDER` env var overrides user settings |
| `test_force_provider_with_user_settings` | Openclaw provider uses default model |
| `test_testing_auth_bypass_uses_user_settings` | Test mode still respects user preferences |
| `test_legacy_gemini_models_are_mapped` | Legacy models redirect appropriately |

## Connections
- [[Gemini]] — default LLM provider
- [[OpenRouter]] — alternative LLM provider
- [[Cerebras]] — alternative LLM provider
- [[LLMService]] — contains `_select_provider_and_model` function

## Contradictions
- None detected
