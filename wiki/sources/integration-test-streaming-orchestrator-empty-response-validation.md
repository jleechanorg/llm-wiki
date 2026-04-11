---
title: "Integration Test for Streaming Orchestrator Empty Response Validation"
type: source
tags: [integration, testing, streaming, flask, gemini, validation, firestore]
source_file: "raw/integration-test-streaming-orchestrator-empty-response-validation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end integration test reproducing production bug: "Scene #3: [Error: Empty response from server]". Tests the full flow from llm_service → streaming_orchestrator → validation → persistence. When Phase 2 streaming returns empty chunks, the system must detect the empty response, yield error event instead of done event, and handle gracefully through the application stack.

## Key Claims
- **Empty Phase 2 Detection**: streaming_orchestrator must detect when Phase 2 returns empty chunks and fail gracefully
- **Validation Failure Pattern**: Empty raw_response_text triggers validation failure, causing only user input to persist
- **Full Stack Integration**: Uses boundary-level mocking (only lowest-level Gemini API mocked) allowing internal routing, prompt-building, JSON-parsing to run normally
- **State Preservation**: GameState must be properly initialized and passed through the streaming flow

## Key Quotes
> "THIS IS THE BUG: When Phase 2 returns empty, streaming_orchestrator validation fails and only user input gets persisted. Frontend then shows: 'Scene #3: [Error: Empty response from server]'"

## Connections
- [[StreamingOrchestrator]] — the main component under test
- [[GameState]] — must be properly instantiated and passed through
- [[StreamEvent]] — event types for status, chunk, tool_start, tool_result, phase_transition, done
- [[FirestoreService]] — mock target for campaign and game state retrieval

## Contradictions
- None identified
