---
title: "Error Handling in Streaming"
type: concept
tags: [streaming, error-handling, llm, production]
sources: []
last_updated: 2026-04-08
---

## Definition

Error handling in streaming refers to the pattern of detecting and gracefully handling error conditions (like empty responses) during SSE streaming. The system should yield error events instead of done events when the underlying LLM returns no content, preventing confusing error messages like "[Error: Empty response from server]" from reaching the frontend.

## Key Pattern

1. **Detection**: llm_service.py detects empty streaming chunks
2. **Error Event**: Yield error event instead of done event
3. **Graceful Handling**: streaming_orchestrator.py handles error without propagating raw error messages
4. **Clean UX**: Frontend shows appropriate error message

## Related Tests

- [[Empty Phase 2 Streaming Response E2E Tests]]
