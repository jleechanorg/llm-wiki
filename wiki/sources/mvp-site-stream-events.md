---
title: "mvp_site stream_events"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/stream_events.py
---

## Summary
Shared StreamEvent type for SSE (Server-Sent Events) streaming. Small dependency leaf avoiding circular imports between streaming_orchestrator and llm_service. Provides StreamEvent dataclass with to_sse() and to_dict() methods.

## Key Claims
- StreamEvent dataclass with type and payload fields
- to_sse() serializes to SSE format: "data: {json}\n\n"
- Used for real-time LLM response streaming

## Connections
- [[LLMIntegration]] — SSE streaming events
