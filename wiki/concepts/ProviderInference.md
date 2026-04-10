---
title: "Provider Inference"
type: concept
tags: [llm-providers, model-selection, constants, inference]
sources: [provider-inference-from-model-selection-tests]
last_updated: 2026-04-08
---

## Definition

Provider inference is the process of automatically determining which LLM provider (gemini, openrouter, cerebras) to use based on the model name, without requiring explicit provider specification from the user.

## How It Works

When a user updates their model via settings without explicitly setting the provider, the system calls `infer_provider_from_model(model_name)` which:
1. Checks if the model matches known patterns (gemini-*, meta-llama/*, x-ai/*, qwen-*)
2. Returns the corresponding provider constant
3. Falls back to DEFAULT_LLM_PROVIDER if no match found
4. Respects provider_hint parameter for unknown models

## Related Concepts

- [[ModelSelection]] — frontend workflow for choosing models
- [[LLMProviderConstants]] — constants defining provider types
- [[PromptLoading]] — how prompts are loaded for different providers
