---
title: "Shared Constants Configuration"
type: source
tags: [configuration, constants, llm-providers, api, caching]
source_file: "raw/shared-constants-configuration.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module defining shared constants across the application including app version, LLM provider configuration, model selections, and feature flags. Prevents circular dependencies and maintains consistency for provider selection, cache busting, and model capabilities.

## Key Claims
- **App Version**: Git short hash for cache busting, defaults to "dev" if git unavailable
- **LLM Provider Options**: Supports Gemini, OpenRouter, Cerebras, and OpenClaw with configurable defaults
- **Model Redirection**: Automatically redirects legacy Gemini 2.5 models to Gemini 3 Flash
- **Code Execution Support**: Only Gemini 3.x supports single-inference code execution + JSON mode
- **Context Caching**: Explicit cache feature flag for cost optimization

## Key Quotes
- "Gemini 3.x supports code_execution + JSON together (single phase)"
- "OpenClaw ignores the model field in API requests — it uses its own configured model"
- "Models that support code_execution + JSON mode TOGETHER (single phase)"

## Connections
- [[WorldArchitect.AI]] — uses these constants for LLM provider selection
- [[Gemini]] — default provider with multiple model options
- [[OpenClaw]] — alternative LLM provider with local model support
- [[OpenRouter]] — alternative LLM provider for model flexibility
- [[Cerebras]] — alternative LLM provider

## Contradictions
- None identified
