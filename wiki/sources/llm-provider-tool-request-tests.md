---
title: "LLM Provider Tool Request Tests"
type: source
tags: [python, testing, llm-providers, tool-requests, cerebras, openrouter]
source_file: "raw/test_llm_provider_tool_requests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating the tool request flow for Cerebras and OpenRouter providers. Tests verify that both providers correctly handle tool calls for dice rolling using a two-stage inference pattern, with the LLM service routing to JSON-first tool_requests flow.

## Key Claims
- **Cerebras tools parameter**: cerebras_provider.generate_content accepts a 'tools' parameter for function calling.
- **CerebrasResponse tool extraction**: CerebrasResponse can extract tool_calls from API responses.
- **Tool request routing for Cerebras**: _call_llm_api routes to generate_content_with_tool_requests for Cerebras provider.
- **Tool request routing for OpenRouter**: _call_llm_api routes to generate_content_with_tool_requests for OpenRouter provider.
- **All Cerebras models use tool_requests**: JSON-first tool_requests flow is used for ALL Cerebras model variants.

## Key Quotes
> "verify _call_llm_api routes to JSON-first tool_requests flow for Cerebras"

## Connections
- [[cerebras_provider]] — implements generate_content_with_tool_requests
- [[openrouter_provider]] — implements generate_content_with_tool_requests  
- [[llm_service]] — orchestrates provider selection and tool request routing
- [[CerebrasResponse]] — handles tool_call extraction from responses
- [[OpenRouterResponse]] — handles tool_call extraction from responses

## Contradictions
- None identified
