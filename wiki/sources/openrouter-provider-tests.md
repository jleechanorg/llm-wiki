---
title: "OpenRouter Provider Tests"
type: source
tags: [python, testing, openrouter, llm-provider, streaming, json-mode]
source_file: "raw/test_openrouter_provider.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests for the OpenRouter LLM provider. Tests validate API key requirement, payload construction with response_format for JSON mode, SSE streaming chunk parsing, and system instruction preservation when using pre-built message histories.

## Key Claims
- **API key requirement**: Raises ValueError when OPENROUTER_API_KEY environment variable is missing
- **Payload construction**: Builds proper OpenRouter API payload with model, messages, and response_format.type = json_object
- **SSE streaming**: Parses SSE chunks from streaming responses, combining delta.content fields
- **System instruction**: Preserves system_instruction_text when messages are pre-built

## Key Quotes
> "CRITICAL: OPENROUTER_API_KEY environment variable not found" — error when API key missing

## Connections
- [[OpenAIChatCommon]] — shared HTTP post implementation
- [[SSEStreaming]] — Server-Sent Events chunk parsing concept
- [[JSONMode]] — response_format type for structured output

## Contradictions
- None identified
