---
title: "Empty Phase 2 Streaming Response E2E Tests"
type: source
tags: [e2e, testing, streaming, flask, gemini, error-handling]
source_file: "raw/empty-phase2-streaming-e2e-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end tests for reproducing production bug: "Scene #3: [Error: Empty response from server]". Validates that when Phase 2 streaming returns empty chunks, the system detects the empty response, yields error event instead of done event, and handles the error gracefully through the full application stack.

## Key Claims
- **Empty Response Error Handling**: llm_service.py detects empty Phase 2 response and yields error event instead of done event
- **Graceful Error Propagation**: streaming_orchestrator.py handles error gracefully without propagating "Empty response from server" to frontend
- **Full Stack Testing**: Uses real Flask app endpoints with boundary-level mocking (only lowest-level Gemini API mocked)
- **Skipped Test Note**: Current test skipped - needs refactoring for proper provider mock interception

## Key Quotes
> "Error: Empty response from server" — production bug triggered when Phase 2 stream returns no chunks

## Connections
- [[streaming-sse-contract-e2e-tests]] — related streaming tests
- [[llm_service]] — module under test
- [[streaming_orchestrator]] — handles error propagation

## Contradictions
- None identified
