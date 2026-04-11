---
title: "StreamingClient Unit Tests for Extraction Functions"
type: source
tags: [javascript, nodejs, unit-testing, streaming, extraction, partial-json]
source_file: "raw/streaming-client-unit-tests-extraction.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Layer 1 unit tests for StreamingClient extraction functions in the JavaScript streaming module. Tests _extractPlanningThinking, _extractNarrativeFromRawEnvelope, _extractNarrativeFromParsedEnvelope, _looksLikeIncompleteStructuredEnvelope, and _getStreamingDisplayText with partial JSON chunks simulating real LLM streaming scenarios.

## Key Claims
- **_extractPlanningThinking**: Extracts thinking content from planning_block JSON field, handles partial/incomplete JSON during streaming
- **_extractNarrativeFromRawEnvelope**: Extracts narrative from raw JSON envelope strings
- **_extractNarrativeFromParsedEnvelope**: Extracts narrative from already-parsed JSON objects
- **_looksLikeIncompleteStructuredEnvelope**: Detects when a JSON chunk appears incomplete (missing closing braces)
- **_getStreamingDisplayText**: Gets display text from streaming events
- **VM Sandboxing**: Uses node:vm to create isolated context for loading streaming.js without full DOM
- **Browser Context Building**: Constructs minimal browser-like environment with console, fetch, setTimeout, EventSource

## Key Code Patterns
```javascript
// Test pattern for partial JSON during streaming
const raw = '{"planning_block":{"thinking":"I need to cons';
const result = client._extractPlanningThinking(raw);
// Returns partial thinking text as LLM streams

// VM sandbox setup pattern
function buildStreamingContext() {
    const context = {
        window: {},
        document: { addEventListener() { }, getElementById() { return null; } },
        console: { log() { }, error() { }, warn() { }, debug() { } },
        fetch: async () => ({ ok: true, json: async () => ({}) }),
        setTimeout: (fn) => { fn(); return 0; },
    };
    return context;
}
```

## Connections
- [[StreamEvent SSE type for streaming]] — related SSE data types
- [[Server-side LLM Chunk Timing Logger]] — server-side timing for streaming

## Contradictions
- None identified
