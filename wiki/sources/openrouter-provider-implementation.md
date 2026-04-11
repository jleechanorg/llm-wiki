---
title: "OpenRouter Provider Implementation"
type: source
tags: [python, openrouter, llm-provider, api, json-schema, tool-calling]
source_file: "raw/openrouter_provider.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python provider implementation for OpenRouter.ai API, an aggregator service that provides unified access to multiple LLM models. Uses json_schema (strict:false) for models that support it (Grok models), with fallback to json_object mode for other models.

## Key Claims
- **Multi-Provider Aggregation**: OpenRouter routes requests to 50+ LLM providers through a single OpenAI-compatible API endpoint
- **Model-Specific JSON Handling**: xAI Grok models use json_schema with strict:false for dynamic response schemas; other models fall back to best-effort JSON
- **BYOK Support**: Supports Bring Your Own Key - users can provide API key directly or rely on OPENROUTER_API_KEY environment variable
- **HTTP Referer Tracking**: Requires site URL and app title in headers for OpenRouter's usage tracking
- **Tool Calling**: Supports function calling via OpenAI-compatible tool definitions
- **Response Wrapper**: Custom OpenRouterResponse class wrapping text and raw response data

## Key Quotes
> "MODELS_WITH_JSON_SCHEMA_SUPPORT = {'x-ai/grok-4.1-fast', 'x-ai/grok-4.1'}" — Models that explicitly support strict JSON schema enforcement

## Connections
- [[OpenAI-Compatible Chat Completions Shared Core]] — shares message building and response parsing logic
- [[OpenAI Chat Completions Shared Helpers]] — provides tool call extraction utilities
- [[LLM Service - AI Integration and Response Processing]] — consumes this provider for backend LLM calls

## Contradictions
- []
