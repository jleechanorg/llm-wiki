---
title: "Streaming Evidence Validation"
type: concept
tags: [streaming, evidence, timing, validation]
sources: []
last_updated: 2026-04-08
---

## Summary
Streaming evidence validation captures server-side timing data to measure LLM chunk generation timing vs HTTP SSE delivery timing. Required for BD-iwr streaming evidence standard compliance.

## Key Components
- **ChunkTimingRecord**: Dataclass storing sequence, ISO 8601 timestamp, text length, campaign ID, request ID
- **StreamingChunkLogger**: Main class for capturing and saving chunk timing data
- **Git Context Capture**: Records git HEAD, branch, and working tree state
- **Checksum Verification**: SHA256 checksums for evidence integrity

## Related Concepts
- [[ServerSentEvents]] — HTTP protocol for streaming responses
- [[ChunkTiming]] — server-side timing capture distinct from client-side delivery timing
- [[EvidenceBundle]] — structured output with CSV, JSON, and checksums
