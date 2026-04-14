---
title: "mvp_site streaming_chunk_logger"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/streaming_chunk_logger.py
---

## Summary
Server-side LLM chunk timing logger for streaming evidence validation. Captures per-chunk timing data to enable precise measurement of LLM chunk generation vs HTTP SSE delivery timing. Required for BD-iwr streaming evidence standard compliance.

## Key Claims
- ChunkTimingRecord dataclass with sequence, llm_ts_utc, text_length, campaign_id, request_id
- StreamingChunkLogger logs chunk timing data during streaming responses
- STREAMING_BUNDLE_VERSION = "1.0.0"
- save() writes to CSV with sha256 hash for evidence integrity

## Connections
- [[LLMIntegration]] — chunk timing for streaming evidence
