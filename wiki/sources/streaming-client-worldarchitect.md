---
title: "StreamingClient for WorldArchitect.AI"
type: source
tags: [javascript, sse, streaming, worldarchitect, firebase, real-time]
source_file: "raw/streaming-client-worldarchitect.md"
sources: []
last_updated: 2026-04-08
---

## Summary
JavaScript StreamingClient class for handling Server-Sent Events (SSE) in WorldArchitect.AI. Provides real-time LLM response streaming with event callbacks for chunks, tool execution, state updates, warnings, and completion. Includes Firebase authentication integration and rate limit modal handling.

## Key Claims
- **SSE Streaming**: Handles real-time text chunk delivery via Server-Sent Events
- **Event Callback System**: Multiple callback hooks (onChunk, onToolStart, onToolResult, onStateUpdate, onWarning, onComplete, onError, onStreamStart, onStreamEnd, onStatus, onMetadata, onPlanningThinking)
- **Firebase Auth Integration**: Supports both window.authTokenManager and firebase.auth() fallback for API authentication
- **Rate Limit Handling**: Detects 429 responses with rate_limit error type and shows modal with reset times
- **Cancellation Support**: Uses AbortController for cancelling in-flight streams
- **Planning Thinking Extraction**: Deduplication state for extracting thinking content from planning_block JSON fields

## Key Code Patterns
```javascript
class StreamingClient {
  constructor(campaignId) {
    this.campaignId = campaignId;
    this.abortController = null;
    this.fullText = '';
    this.isStreaming = false;
    
    // Event callbacks
    this.onChunk = null;
    this.onToolStart = null;
    this.onToolResult = null;
    this.onStateUpdate = null;
    this.onWarning = null;
    this.onComplete = null;
    this.onError = null;
    this.onStreamStart = null;
    this.onStreamEnd = null;
    this.onStatus = null;
    this.onMetadata = null;
    this.onPlanningThinking = null;
  }
}
```

## Connections
- [[WorldArchitect]] — the application this client is built for
- [[Firebase]] — authentication provider integrated for API calls
- [[ServerSentEvents]] — the SSE protocol used for streaming

## Contradictions
- None identified
