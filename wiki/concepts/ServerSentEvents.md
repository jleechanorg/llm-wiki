---
title: "Server-Sent Events"
type: concept
tags: [streaming, http, real-time, sse]
sources: []
last_updated: 2026-04-08
---

## Definition
Server-Sent Events (SSE) is an HTTP-based protocol for real-time unidirectional communication from server to client. Unlike WebSockets, SSE is simplex (one-way) and works over standard HTTP connections.

## Technical Details
- **Content-Type**: `text/event-stream`
- **Format**: `data: <json payload>\n\n`
- **Headers**: Cache-Control: no-cache, Connection: keep-alive, X-Accel-Buffering: no (for nginx)
- **Use Case**: Real-time LLM response streaming in narrative applications

## Related Concepts
- [[StreamingOrchestrator]] — Implementation that generates SSE events
- [[StreamEvent]] — Dataclass representing individual streaming events

## Connections
- Used by [[StreamingOrchestratorModuleTests]] for validating streaming responses
