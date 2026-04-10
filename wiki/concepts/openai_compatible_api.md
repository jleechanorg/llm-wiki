---
title: "OpenAI-Compatible API"
type: concept
tags: [api, standard, llm]
sources: ["openrouter-provider-implementation"]
last_updated: 2026-04-08
---

OpenAI's /v1/chat/completions API specification that has become a de facto standard adopted by many LLM providers. Uses HTTP POST to endpoint with JSON body containing messages, model, and optional parameters. Returns JSON with content, tool_calls, and metadata.

## Specification Elements
- **Endpoint Pattern**: /v1/chat/completions
- **Message Format**: [{"role": "system|user|assistant", "content": "..."}]
- **Parameters**: model, temperature, max_tokens, tools, response_format
- **Response**: {choices: [{message: {content, tool_calls}}], usage}

## Connected Sources
- [[OpenRouter Provider Implementation]] — implements OpenAI-compatible interface
- [[OpenAI-Compatible Chat Completions Shared Core]] — shared implementation

## Provider Implementations
- [[OpenRouter]]
- [[Cerebras]]
- [[OpenClaw]]

## Related Concepts
- [[Tool Calling]] — function calling extension
- [[JSON Object Mode]] — response format option
- [[json_schema (strict:false)]] — schema enforcement option
