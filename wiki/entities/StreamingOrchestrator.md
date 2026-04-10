---
title: "StreamingOrchestrator"
type: entity
tags: [project, worldarchitect, streaming]
sources: [stream-event-type]
last_updated: 2026-04-08
---

Part of the `mvp_site` project. Defines streaming flows and uses the `StreamEvent` type for Server-Sent Events. Must import from a separate module to avoid circular dependencies with [[LlmService]].

**Related:**
- [[StreamEventType]] — the shared type it imports
- [[LlmService]] — shares StreamEvent dependency
