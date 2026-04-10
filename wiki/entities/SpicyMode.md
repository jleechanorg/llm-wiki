---
title: "Spicy Mode"
type: entity
tags: [feature, settings, model-switching]
sources: [spicy-mode-toggle-e2e-tests]
last_updated: 2026-04-08
---

## Description
A game setting that switches the LLM provider to Grok on OpenRouter for more creative/risky AI responses. When enabled, saves the previous model/provider state for restoration when disabled.

## Behavior
- **Enable**: Switches to Grok (openrouter_model), saves pre_spicy_model and pre_spicy_provider
- **Disable**: Restores previous model and provider from saved state

## Related
- [[spicy-mode-toggle-e2e-tests]] — E2E test coverage
- [[grok]] — model activated in spicy mode
- [[openrouter]] — provider that serves Grok
