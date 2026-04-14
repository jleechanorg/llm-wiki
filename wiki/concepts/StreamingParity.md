---
title: "StreamingParity"
type: concept
tags: [streaming, llm, real-time, chunk-parity, evidence]
sources: [mvp-site-streaming-orchestrator, mvp-site-streaming-chunk-logger]
last_updated: 2026-04-14
---

## Summary

The requirement that streamed LLM responses arrive with complete fidelity — each chunk's text arriving exactly once, in correct order, without duplication or omission. StreamingParity enforcement is critical for evidence-grade captures where chunk timing data (via `StreamingChunkLogger`) proves that content was genuinely streamed rather than fabricated post-generation.

## Key Claims

### Server-Side Chunk Timing
- `StreamingChunkLogger` captures per-chunk timing: sequence, `llm_ts_utc`, text_length, campaign_id, request_id
- Required for BD-iwr streaming evidence standard compliance
- CSV output with sha256 hash for evidence integrity

### Two-Phase Streaming
- Phase 1: Initial narrative generation (streaming)
- Phase 2: Game state integration (streaming continuation)
- `stream_story_with_game_state` provides full streaming with real game logic integration

### Cold-Start Optimization
- `_lazy_module()` defers `google.genai` loading to avoid Cloud Run cold-start overhead
- Services (firestore_service, gemini_provider, llm_service, world_logic) loaded lazily

## Connections

- [[StreamingResponse]] — incremental token delivery pattern
- [[mvp-site-streaming-orchestrator]] — SSE streaming orchestration
- [[mvp-site-streaming-chunk-logger]] — chunk timing evidence logger
- [[LLMIntegration]] — streaming orchestration integrated with AI service