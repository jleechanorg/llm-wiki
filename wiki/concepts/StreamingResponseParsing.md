---
title: "Streaming Response Parsing"
type: concept
tags: [streaming, http, parsing]
sources: []
last_updated: 2026-04-08
---

Technique for handling Server-Sent Events (SSE) style streaming from LLM APIs. Involves:
- Setting `stream: true` in request payload
- Parsing line-by-line events (data: prefix, event type)
- Extracting content from message events
- Handling done event to terminate generator

Used by OpenClawHTTPClient for real-time token streaming.
