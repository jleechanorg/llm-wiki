---
title: "Streaming Orchestrator"
type: concept
tags: [streaming, orchestration, sse, gemini, llm]
sources: []
last_updated: 2026-04-08
---

## Definition
A module responsible for managing real-time streaming of LLM responses to clients using Server-Sent Events (SSE). Handles event generation, formatting, and delivery for narrative streaming in the game application.

## Key Components
- **StreamEvent**: Dataclass for typed streaming events (chunk, done, error, state)
- **stream_narrative_simple**: Basic narrative streaming function
- **stream_story_with_game_state**: Streaming with game state integration
- **stream_with_context**: Context-aware streaming
- **create_sse_response_headers**: SSE-specific HTTP headers

## Functions
- `stream_events_generator()` — Converts events to SSE format
- `_count_compliant_lw_events()` — Counts Living World compliant events
- `_warn_if_living_world_missing()` — Validation for Living World state

## Related Concepts
- [[ServerSentEvents]] — The protocol used for streaming
- [[GeminiProvider]] — LLM provider for generating content streams
- [[StreamEvent]] — The event data structure

## Connections
- Tested by [[StreamingOrchestratorModuleTests]]
