---
title: "Service Wrapper"
type: concept
tags: [python, wrapper, adapter, service-layer]
sources: [mock-firestore-service-wrapper]
last_updated: 2026-04-08
---

Python pattern where a module wraps another implementation to provide a different interface. This wrapper adapts [[MockFirestoreClient]] to present the same API as [[FirestoreService]], enabling seamless mock/real switching.

## Characteristics
- Exports same functions as wrapped service
- May add compatibility layers for parameter differences
- Uses module-level initialization for singleton pattern
