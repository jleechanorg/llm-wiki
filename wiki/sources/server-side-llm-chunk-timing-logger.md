---
title: "Server-side LLM Chunk Timing Logger for Streaming Evidence Validation"
type: source
tags: [python, streaming, timing, logging, evidence, server-sent-events, bd-iwr]
source_file: "raw/server-side-llm-chunk-timing-logger.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module capturing per-chunk LLM timing data on the server side to enable precise measurement of chunk generation timing vs HTTP SSE delivery timing. Required for BD-iwr streaming evidence standard compliance.

## Key Claims
- **Server-Side Timing Capture**: Records precise timestamps when each LLM chunk is generated, separate from HTTP delivery timing
- **Evidence Bundle Generation**: Creates structured evidence packages with CSV logs, JSON summaries, and SHA256 checksums
- **Git Context Capture**: Records git HEAD, branch, and working tree state for evidence reproducibility
- **BD-iwr Standard Compliance**: Enables streaming evidence validation per the BD-iwr specification

## Key Code Patterns
```python
@dataclass
class ChunkTimingRecord:
    sequence: int
    llm_ts_utc: str  # ISO 8601 format
    text_length: int
    campaign_id: str | None
    request_id: str | None

class StreamingChunkLogger:
    def log_chunk(self, sequence: int, text: str, timestamp: datetime):
        # Record chunk with precise timing
    def save(self):
        # Write CSV, JSON summary, checksums
```

## Connections
- [[StreamEventType]] — the SSE event type this logger complements for streaming responses
- [[SarielLLMResponseCapture]] — similar to LLM response capture but focuses on timing rather than content
- [[IntegrationTestRunnerRealAPICalls]] — uses this logger for streaming evidence validation

## Contradictions
- None identified
