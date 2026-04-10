---
title: "Model Switching"
type: concept
tags: [llm, provider, configuration]
sources: [spicy-mode-toggle-e2e-tests]
last_updated: 2026-04-08
---

## Description
The ability to dynamically change between different LLM providers and models at runtime. The settings API supports llm_provider, gemini_model, openrouter_model, and cerebras_model fields.

## Implementation
- Settings API at /api/settings accepts provider and model fields
- Providers: gemini, openrouter, cerebras
- Model selection per provider persists to Firestore

## Related
- [[spicy-mode-toggle-e2e-tests]] — tests model switching
- [[spicy-mode]] — applies model switching for creative mode
