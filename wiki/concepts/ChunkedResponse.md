---
title: "ChunkedResponse"
type: concept
tags: [streaming, chunks, real-time, llm, http-sse]
sources: [mvp-site-streaming-orchestrator, mvp-site-streaming-chunk-logger]
last_updated: 2026-04-14
---

## Summary

The incremental text delivery pattern used by WorldAI's streaming system. Each chunk represents a portion of the LLM's generated text, delivered via HTTP SSE as tokens are produced. Server-side `StreamingChunkLogger` captures per-chunk timing data for evidence-grade verification that content was genuinely streamed.

## Key Claims

### Chunk Timing Records
- `ChunkTimingRecord` dataclass: sequence, llm_ts_utc, text_length, campaign_id, request_id
- Used to measure LLM chunk generation vs HTTP SSE delivery timing
- Required for BD-iwr streaming evidence standard compliance

### Lazy Loading
- `_lazy_module()` defers google.genai loading to avoid Cloud Run cold-start
- Services (firestore_service, gemini_provider, llm_service, world_logic) loaded on-demand

### Two-Phase Chunk Delivery
- Phase 1: Initial narrative chunks streamed to client
- Phase 2: Game state integration chunks streamed as continuation

## Connections

- [[StreamingResponse]] — real-time token delivery
- [[StreamingParity]] — chunk ordering and completeness
- [[EventStream]] — SSE delivery mechanism
- [[mvp-site-streaming-orchestrator]] — chunk generation implementation