---
title: "mvp_site openrouter_provider"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/openrouter_provider.py
---

## Summary
OpenRouter provider implementation using json_schema with strict:false for models that support it (Grok). Falls back to json_object mode for other models. OpenRouter_URL = https://openrouter.ai/api/v1/chat/completions.

## Key Claims
- OpenRouterResponse wrapper with .text interface for llm_service
- get_tool_calls() extracts tool_calls from raw response
- MODELS_WITH_JSON_SCHEMA_SUPPORT includes x-ai/grok-4.1-fast and x-ai/grok-4.1
- Supports native two-phase tool calling flow

## Connections
- [[LLMIntegration]] — OpenRouter as alternative LLM provider
