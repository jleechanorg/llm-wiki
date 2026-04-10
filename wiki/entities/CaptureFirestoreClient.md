---
title: "CaptureFirestoreClient"
type: entity
tags: [testing, capture, firestore, database]
sources: [capture-framework-tests]
last_updated: 2026-04-08
---

## Description
Specialized capture client for Firestore database operations. Part of the capture framework that records Firestore get, set, and query operations for testing and analysis.

## Key Operations
- `firestore.get` — document retrieval
- `firestore.set` — document creation/update
- `firestore.query` — collection queries

## Related
- [[CaptureManager]] — parent orchestrator
- [[CaptureGeminiClient]] — parallel client for Gemini
- [[CaptureAnalyzer]] — operation analysis
