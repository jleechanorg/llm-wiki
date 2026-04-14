---
title: "mvp_site constants"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/constants.py
---

## Summary
Shared constants across the application preventing cyclical dependencies. Defines LLM provider selection (Gemini, Cerebras, OpenRouter, OpenClaw), default model configurations (gemini-3-flash-preview as default), and constants for code execution + JSON support detection.

## Key Claims
- APP_VERSION from git rev-parse for cache busting
- LLM provider constants: LLM_PROVIDER_GEMINI, LLM_PROVIDER_OPENROUTER, LLM_PROVIDER_CEREBRAS, LLM_PROVIDER_OPENCLAW
- DEFAULT_GEMINI_MODEL = gemini-3-flash-preview (best value: $0.50/M input, $3/M output)
- GEMINI_MODEL_MAPPING auto-redirects legacy 2.5/2.0 models to Gemini 3 Flash
- MODELS_SUPPORT_CODE_EXECUTION_JSON: Gemini 3.x can combine code_execution + JSON in single inference
- ACTOR constants: ACTOR_USER, ACTOR_GEMINI, ACTOR_UNKNOWN

## Connections
- [[LLMIntegration]] — provider and model selection constants
