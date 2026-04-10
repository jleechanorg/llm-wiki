---
title: "Non-Blocking Validation"
type: concept
tags: [validation, production, warnings, safety, gameplay-continuity]
sources: []
last_updated: 2026-04-08
---

## Definition
Validation pattern where errors generate warnings but do NOT halt execution. Used in production to ensure gameplay continues even when invalid data is detected.

## Use Cases
- Schema validation warnings during Firestore persistence
- Game state validation that logs but doesn't crash
- Debug logging for invalid data without blocking user experience

## Related
- [[SchemaValidation]] — implemented as non-blocking
- [[FirestorePersistence]] — applies non-blocking validation
- [[GameState]] — validates non-blocking
