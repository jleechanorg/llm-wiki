---
title: "Tool Calling"
type: concept
tags: [llm, function-calling, agents]
sources: ["openrouter-provider-implementation"]
last_updated: 2026-04-08
---

LLM capability to invoke external functions/tools defined in the request. The model outputs structured tool_calls with name and arguments, which the application executes, then feeds results back for continued generation. Enables agentic behavior in LLM applications.

## Technical Flow
1. **Definition**: Pass tools=[{name, description, parameters}] in request
2. **Invocation**: Model outputs tool_calls=[{name, arguments: {}}]
3. **Execution**: Application runs function, captures result
4. **Continuation**: Append tool result to messages, continue generation

## Connected Sources
- [[OpenRouter Provider Implementation]] — supports tools parameter and extract_tool_calls
- [[OpenAI Chat Completions Shared Helpers]] — provides extract_tool_calls utility

## Related Concepts
- [[OpenAI-Compatible API]] — underlying protocol
- [[json_schema (strict:false)]] — can be used with tool calling
