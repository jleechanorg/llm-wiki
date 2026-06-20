---
title: "StreamingClient"
type: concept
tags: [streaming, sse, client, real-time]
sources: []
last_updated: 2026-04-08
---

JavaScript client for real-time LLM responses using Server-Sent Events (SSE). Tests verify: fallback to regular interaction when unavailable, waits for auth initialization before requesting headers, has fallback for transient auth races, and extracts narrative display text from streaming chunks.

## Related
- [streaming.js](../entities/streaming.js.md) — implementation file
- [app.js](../entities/app.js.md) — uses StreamingClient
