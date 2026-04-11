---
title: "OpenAI-Compatible Chat Completions Shared Core"
type: source
tags: [python, api, openai, chat-completions, http, client, cerebras, openrouter]
source_file: "raw/openai-compatible-chat-completions-shared-core.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing shared core functionality for OpenAI-compatible chat-completions providers. Builds on `openai_chat_common.py` to centralize message building, tool call extraction, response parsing, and error handling for providers like Cerebras and OpenRouter.

## Key Claims
- **Provider Abstraction**: Each provider only needs to specify endpoint, auth headers, and response_format
- **Message Building**: Delegates to `build_messages()` for system+user prompt construction
- **Tool Call Extraction**: Uses centralized `extract_tool_calls()` for OpenAI-style function responses
- **Truncation Detection**: Logs finish_reason and usage for debugging token limit issues
- **Error Logging**: Truncates response body on parsing errors to avoid log spam

## Key Functions
- `generate_openai_compatible_content()` — Main entry point calling the chat-completions endpoint
- Payload building via `build_chat_payload()` with tools/response_format mutual exclusion
- Response validation via `extract_first_choice()` and `extract_first_choice_message()`

## Connections
- [[OpenAI Chat Completions Shared Helpers]] — related helper module for same providers
- [[Cerebras]] — OpenAI-compatible provider using this shared core
- [[OpenRouter]] — OpenAI-compatible provider using this shared core

## Contradictions
- []
