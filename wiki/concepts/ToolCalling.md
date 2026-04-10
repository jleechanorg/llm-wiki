---
title: "Tool Calling"
type: concept
tags: [api, ai, llm, function-calling, tools]
sources: []
last_updated: 2026-04-08
---

Tool Calling (also called Function Calling) allows LLMs to invoke defined functions during generation. The model outputs structured calls that the client executes, then feeds results back for continued generation.

## Connections
- [[OpenAI-Compatible Chat Completions Shared Core]] — extracts tool calls from responses
- [[Chat Completions]] — the base API that supports tool calling
- [[openai-chat-completions-shared-helpers.md]] — handles tool definitions
