---
title: "json_schema (strict:false)"
type: concept
tags: [json, schema, llm, response-formatting]
sources: ["openrouter-provider-implementation"]
last_updated: 2026-04-08
---

JSON schema mode in LLM API responses where the model generates valid JSON matching a provided schema, but with strict:false allowing dynamic field values rather than strict enum/const enforcement. Enables structured responses while maintaining flexibility.

## Technical Details
- **strict:false**: Model respects schema structure but may vary field values dynamically
- **strict:true** (not used): Would enforce exact enum/const values
- **Provider Support**: Only xAI Grok models currently support this mode via OpenRouter

## Connected Sources
- [[OpenRouter Provider Implementation]] — documents MODELS_WITH_JSON_SCHEMA_SUPPORT

## Related Concepts
- [[JSON Object Mode]] — fallback response format
- [[Tool Calling]] — function calling via structured JSON
