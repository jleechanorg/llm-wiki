---
title: "Streaming SSE Contract E2E Tests"
type: source
tags: [e2e, testing, streaming, sse, python, flask, gemini]
source_file: "raw/streaming-sse-contract-e2e-tests.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end tests for streaming SSE contract verifying character, think, and god modes. Tests validate /interaction/stream endpoint returns correct SSE done payloads for each mode. Uses boundary-level mocking (only generate_content_stream_sync mocked) allowing internal routing, prompt-building, JSON-parsing, and orchestration to run normally.

## Key Claims
- **Streaming Done Payloads**: Each mode (character/think/god) returns correct SSE done payloads with appropriate response structures
- **Boundary-level Mocking Pattern**: Only lowest-level Gemini API call is mocked, not entire LLM service module — enables full internal logic execution
- **TDD Regression Prevention**: Tests document and enforce correct mock pattern to prevent CI failures like the original "god mode stream done payload missing god_mode_response" error
- **Mode-specific Responses**: Character mode returns narrative, think mode returns thinking+choices, god mode returns god_mode_response

## Key Quotes
> "The CI 'Mock API' job originally used MOCK_SERVICES_MODE=true, which swaps the entire LLM service module with a simplified fake that uses ad-hoc string matching on prompt content"

> "Input 'GOD_MODE_UPDATE_STATE:{...}' does NOT contain 'god mode:' or 'god:', so the mock fell back to FULL_STRUCTURED_RESPONSE which has god_mode_response: '""

## Connections
- [[GeminiAPI]] — the LLM provider being mocked at boundary
- [[StreamingContract]] — the SSE contract being tested
- [[TDDRegression]] — why these tests exist to prevent CI failures

## Contradictions
- None identified
