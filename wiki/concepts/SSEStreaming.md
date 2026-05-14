---
title: "SSE Streaming"
type: concept
tags: [streaming, http, server-sent-events]
sources: [openrouter-provider-tests]
last_updated: 2026-04-08
---

Server-Sent Events (SSE) streaming is a server-push technology where the server sends data to the client over HTTP using the text/event-stream content type.

## Usage in LLM Providers
- Providers stream token-by-token responses via SSE
- Each chunk is prefixed with "data: " and suffixed with newlines
- Stream terminates with "data: [DONE]"
- Client iterates over iter_lines() to parse delta.content fields

## message_start Event and Token Tracking

The first SSE event from Anthropic's API is always `message_start`, containing `usage: {input_tokens, output_tokens}`. Claude Code uses `input_tokens` from this event to track context window fill level.

**Critical**: providers that return `input_tokens: 0` (e.g. GLM-5.1/wafer) cause Claude Code autocompact to thrash — it believes context was just cleared after every response. Fix: buffer until `\n\n` boundary, patch `"input_tokens":0` with estimated value. See [[WaferFixSSEPatcher]] and [[wafer-sse-input-tokens-zero-fix-2026-05-14]].

## Related Pages
- [[OpenRouterProviderTests]] — validates SSE parsing in openrouter_provider
- [[StreamingSync]] — generate_content_stream_sync function concept
- [[WaferFixSSEPatcher]] — proxy-level patcher for `input_tokens:0` in message_start
- [[Compaction]] — autocompact thrash caused by zero token counts
