---
title: "Provider Inference from Model Selection Tests"
type: source
tags: [python, testing, provider-inference, llm-providers, model-selection, constants]
source_file: "raw/test_provider_inference_from_model.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating automatic provider inference from model names. Tests ensure the system correctly identifies the LLM provider (gemini, openrouter, cerebras) based on the model string when users update their model via settings without explicitly setting the provider.

## Key Claims
- **Gemini provider inference**: Models starting with "gemini-" or legacy names like "gemini-2.5-flash", "gemini-2.5-pro", "pro-2.5", "flash-2.5" infer the gemini provider.
- **OpenRouter provider inference**: Models from OpenRouter (e.g., "meta-llama/llama-3.1-70b-instruct", "x-ai/grok-4.1-fast") infer the openrouter provider.
- **Cerebras provider inference**: Models from Cerebras (e.g., "qwen-3-235b-a22b-instruct-2507", "llama-3.3-70b") infer the cerebras provider.
- **Default provider fallback**: Unknown models default to DEFAULT_LLM_PROVIDER.
- **Provider hint override**: The provider_hint parameter allows explicit provider specification for unknown models.

## Connections
- [[ProviderInference]] — concept being tested
- [[LLMProviderConstants]] — constants defining provider types
- [[ModelSelection]] — related frontend settings workflow
