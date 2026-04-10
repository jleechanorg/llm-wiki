---
title: "Malformed JSON Handling"
type: concept
tags: [json, error-handling, testing]
sources: []
last_updated: 2026-04-08
---

## Summary
Strategies for handling corrupted or invalid JSON in LLM-generated responses. Tests in narrative_response_legacy_fallback.py validate various failure modes.

## Failure Modes Tested
- Missing closing braces and brackets
- JSON artifacts embedded in narrative text
- Nested JSON with broken structure
- Multiple conflicting narrative markers
- Excessive whitespace and newlines

## Recovery Behavior
The tests verify that recovery is now disabled, causing these malformed inputs to return error messages rather than attempting extraction.

## Related
- [[JSON Cleanup]] — Related concept
- [[Error Recovery]] — General error handling patterns
