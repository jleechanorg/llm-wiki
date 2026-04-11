---
title: "Cerebras Direct API Provider Implementation"
type: source
tags: [cerebras, llm-provider, openai-compatible, api-integration, json-schema]
source_file: "raw/cerebras-direct-api-provider.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Cerebras OpenAI-compatible chat completions endpoint implementation keeping llm_service orchestration provider-agnostic. Uses json_schema with strict:false instead of legacy json_object to prevent schema echo issues where API returns {"type": "object"} instead of actual content.

## Key Claims
- **OpenAI-Compatible Endpoint**: Uses Cerebras /v1/chat/completions API maintaining provider-agnostic architecture
- **json_schema (strict:false)**: Prevents schema echo by keeping planning_block flexible for dynamic choice keys
- **Schema Echo Handling**: CerebrasSchemaEchoError exception for when API returns response_format schema instead of content
- **Error Detection**: HTTP error handlers for model_not_found (404) and response_format retryable errors (422)
- **Text Extraction**: Model-agnostic content extraction tolerating different response structures

## Key Quotes
> "IMPORTANT: Uses json_schema (strict:false) instead of legacy json_object to prevent schema echo issues where API returns {\"type\": \"object\"} instead of actual content."

## Connections
- [[OpenAICompatibleProvider]] — shares base implementation patterns
- [[JsonSchemaResponseFormat]] — technique for preventing schema echo
- [[LLMProviderColdStartOptimization]] — lazy loading strategy similar pattern

## Contradictions
- None detected
