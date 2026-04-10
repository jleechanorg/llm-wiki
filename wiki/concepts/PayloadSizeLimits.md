---
title: "Payload Size Limits"
type: concept
tags: [api-limits, performance, gemini-api]
sources: [llm-request-class-gemini-api.md]
last_updated: 2026-04-08
---

## Definition
Configuration constants defining maximum allowed sizes for API request payloads and individual string fields.

## Values in This Source
- `MAX_PAYLOAD_SIZE` = 10MB (10 * 1024 * 1024 bytes)
  - Increased from smaller limits to support Gemini 2.5 Flash which supports up to 500MB input
- `MAX_STRING_LENGTH` = 1,000,000 characters

## Rationale
Gemini 2.5 Flash supports up to 500MB input, so the 10MB limit provides headroom for very complex game states while remaining practical.

## Related Concepts
- [[Generalized File Caching Implementation]] — caching for performance
- [[Gunicorn Production Configuration]] — timeout handling for large payloads
