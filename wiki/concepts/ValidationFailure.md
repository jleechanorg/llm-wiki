---
title: "Validation Failure"
type: concept
tags: [validation, error-handling, streaming]
sources: []
last_updated: 2026-04-08
---

## Definition
Failure condition in streaming_orchestrator when response validation fails. Occurs when raw_response_text is empty or malformed, preventing proper state updates and narrative persistence.

## Failure Pattern
1. Phase 2 streaming returns empty chunks
2. parse_structured_response provides fallback narrative but raw_response_text remains empty
3. Validation check fails on empty raw_response_text
4. Only user input persists to Firestore
5. Frontend displays "[Error: Empty response from server]"

## Resolution
System must detect empty Phase 2 response before validation, yield error event instead of done event, and handle gracefully through full application stack.

## Related Concepts
- [[Phase2Streaming]] — where failures occur
- [[ParseStructuredResponse]] — provides fallback but can't fix empty raw text
- [[FirestorePersistence]] — where data loss manifests
