---
title: "EventStream"
type: concept
tags: [streaming, sse, server-sent-events, real-time, llm]
sources: [mvp-site-streaming-orchestrator]
last_updated: 2026-04-14
---

## Summary

The SSE (Server-Sent Events) mechanism used in WorldArchitect.AI to deliver real-time LLM responses to clients. `stream_narrative_simple` and `stream_story_with_game_state` are the primary entry points, with lazy-loaded dependencies for cold-start optimization. EventStream enables clients to receive tokens as they are generated rather than waiting for complete responses.

## Key Claims

### Streaming Entry Points
- `stream_narrative_simple`: basic streaming without game state
- `stream_story_with_game_state`: full streaming with game logic integration

### Lazy Loading Pattern
- `_lazy_module()` defers google.genai loading until first use
- Cloud Run cold-start overhead avoided by not importing at module load time
- Services loaded on-demand: firestore_service, gemini_provider, llm_service, world_logic

### Two-Phase Generation
- Phase 1: narrative streaming with initial token delivery
- Phase 2: game state integration streamed as continuation

## Connections

- [[StreamingResponse]] — real-time incremental delivery
- [[StreamingParity]] — chunk ordering and completeness guarantee
- [[mvp-site-streaming-orchestrator]] — implementation of EventStream for WorldAI