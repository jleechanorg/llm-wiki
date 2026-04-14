---
title: "mvp_site openai_chat_common"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/openai_chat_common.py
---

## Summary
Shared helpers for OpenAI-compatible chat-completions providers (Cerebras, OpenRouter). Centralizes message building, tool_calls extraction, and JSON request posting with consistent error handling across providers.

## Key Claims
- OpenAIChatResponse dataclass with .text and .tool_calls properties
- build_messages() constructs OpenAI-style messages from prompt contents
- build_chat_payload() creates JSON payload for chat completions
- extract_tool_calls() defensively extracts tool_calls from raw responses
- post_chat_completions() posts JSON requests with error handling

## Connections
- [[LLMIntegration]] — shared provider utilities
