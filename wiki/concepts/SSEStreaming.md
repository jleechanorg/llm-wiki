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

## Related Pages
- [[OpenRouterProviderTests]] — validates SSE parsing in openrouter_provider
- [[StreamingSync]] — generate_content_stream_sync function concept
