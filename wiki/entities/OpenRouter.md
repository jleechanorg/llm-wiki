---
title: "OpenRouter"
type: entity
tags: [llm-provider, api]
sources: [spicy-mode-toggle-e2e-tests]
last_updated: 2026-04-08
---

## Description
An LLM aggregation provider that serves multiple models including Grok. Used by spicy mode to access the Grok model for more creative game responses.

## Behavior
- Receives model selection from settings API
- SPICY_OPENROUTER_MODEL configured as the spicy mode model
- Alternative to Gemini and Cerebras providers

## Related
- [[spicy-mode-toggle-e2e-tests]] — tests using OpenRouter
- [[spicy-mode]] — feature that uses OpenRouter for Grok
- [[grok]] — model served via OpenRouter
