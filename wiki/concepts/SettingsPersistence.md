---
title: "Settings Persistence"
type: concept
tags: [storage, settings, firestore]
sources: [spicy-mode-toggle-e2e-tests]
last_updated: 2026-04-08
---

## Description
The pattern of saving user settings to Firestore and retrieving them across sessions. Settings include LLM provider, model selection, and feature flags like spicy_mode.

## Key Fields
- llm_provider: current provider (gemini/openrouter/cerebras)
- gemini_model, openrouter_model, cerebras_model: per-provider model
- pre_spicy_model, pre_spicy_provider: restoration state
- spicy_mode: feature flag

## Related Tests
- [[spicy-mode-toggle-e2e-tests]] — validates persistence
