---
title: "Model Selection"
type: concept
tags: [frontend, settings, llm-providers, user-preferences]
sources: [provider-inference-from-model-selection-tests]
last_updated: 2026-04-08
---

## Definition

Model selection is the workflow where users choose which LLM model to use via frontend settings. When users update their model (e.g., to "gemini-3-flash-preview"), the system must correctly infer the provider.

## Problem Addressed

Frontend may only send gemini_model without llm_provider, causing the server to use the wrong provider. Provider inference solves this by automatically detecting the provider from the model name.

## Related Concepts


- [[ProviderInference]] — automatic provider detection
- [[LLMProviderConstants]] — provider type constants
