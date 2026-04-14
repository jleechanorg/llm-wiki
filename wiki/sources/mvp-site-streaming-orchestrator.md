---
title: "mvp_site streaming_orchestrator"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/streaming_orchestrator.py
---

## Summary
Streaming orchestrator for real-time LLM response streaming via SSE. Provides StreamEvent, stream_narrative_simple, stream_story_with_game_state. Handles two-phase generation with streaming Phase 2.

## Key Claims
- _lazy_module() for Cloud Run cold-start optimization (defers google.genai loading)
- firestore_service, gemini_provider, llm_service, world_logic loaded lazily
- stream_narrative_simple: basic streaming without game state
- stream_story_with_game_state: full streaming with real game logic integration

## Connections
- [[LLMIntegration]] — SSE streaming orchestration
