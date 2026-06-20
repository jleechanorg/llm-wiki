---
title: "JSON-First Tool Requests"
type: concept
tags: [llm-providers, json-mode, tool-calls]
sources: []
last_updated: 2026-04-08
---

A provider configuration where the LLM is requested to respond with JSON format containing tool_calls rather than natural language. Used for deterministic function calling in games (e.g., dice rolling) where structured output is required.

## Related Pages
- [llm-provider-tool-request-tests](../sources/llm-provider-tool-request-tests.md) — tests validating this flow
- [llm_service](../entities/llm_service.md) — implements routing to this flow
- [ToolRequestHandling](ToolRequestHandling.md) — general concept of tool execution
