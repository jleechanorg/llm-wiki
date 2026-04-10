---
title: "JSON Object Mode"
type: concept
tags: [json, response-formatting, llm]
sources: ["openrouter-provider-implementation"]
last_updated: 2026-04-08
---

Fallback JSON response format for LLM APIs when json_schema is not supported. Requests the model to output valid JSON without strict schema enforcement. Used by models that don't support json_schema (most providers except xAI Grok).

## Technical Details
- **vs json_schema**: Less structured but more broadly supported
- **Provider Behavior**: OpenRouter automatically falls back when model doesn't support json_schema
- **Use Case**: General-purpose JSON responses where exact structure isn't critical

## Connected Sources
- [[OpenRouter Provider Implementation]] — documents fallback logic

## Related Concepts
- [[json_schema (strict:false)]] — stricter alternative
- [[OpenAI-Compatible API]] — underlying protocol
