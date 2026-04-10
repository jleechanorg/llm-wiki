---
title: "Tool Request Handling"
type: concept
tags: [llm-providers, function-calling, tool-calls]
sources: []
last_updated: 2026-04-08
---

A pattern where LLM providers execute function calls (tools) returned in the response. The model outputs a special tool_calls array containing function name and arguments, which the client executes and feeds back as tool results for a second inference pass.

## Related Pages
- [[llm-provider-tool-request-tests]] — tests validating this concept
- [[Cerebras]] — supports tool requests for dice rolling
- [[OpenRouter]] — supports tool requests for function calling
