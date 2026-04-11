---
title: "OpenAI Chat Completions Shared Helpers"
type: source
tags: [python, api, openai, chat-completions, http, client]
source_file: "raw/openai-chat-completions-shared-helpers.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing shared helpers for OpenAI-compatible chat-completions providers. Used by providers like Cerebras and OpenRouter that support the OpenAI /chat/completions wire format. Centralizes message building, tool call extraction, and payload construction to avoid duplication across provider implementations.

## Key Claims
- **Message Building**: `build_messages()` constructs system+user messages from prompt contents
- **Payload Construction**: `build_chat_payload()` creates request bodies with tools/response_format mutual exclusion
- **Tool Call Extraction**: `extract_tool_calls()` defensively parses OpenAI-style tool_call responses
- **Error Handling**: `post_chat_completions()` wraps HTTP calls with consistent error handling

## Key Functions
- `build_messages()` — constructs OpenAI-style message list
- `build_chat_payload()` — builds request payload with tool/format guards
- `extract_tool_calls()` — extracts tool_calls from response defensively
- `extract_first_choice_message()` — returns first choice message or raises
- `extract_first_choice()` — returns first choice or raises
- `post_chat_completions()` — HTTP POST with error handling

## Connections
- [[Cerebras]] — provider using this module for chat completions
- [[OpenRouter]] — provider using this module for chat completions
- [[OpenAI]] — compatibility target for wire format

## Contradictions
- None identified
