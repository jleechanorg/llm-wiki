---
title: "real_provider.py"
type: source
tags: []
sources: []
last_updated: 2026-04-14
---

## Summary
Real service provider implementation that uses actual Firestore and Gemini services with test isolation and cleanup. Supports optional capture mode for recording test interactions.

## Key Claims
- Extends `TestServiceProvider` abstract base class
- `get_firestore()` returns real Firestore client wrapped with `CaptureFirestoreClient` in capture mode
- `get_gemini()` returns real Gemini client (using `google.genai` latest API) wrapped with `CaptureGeminiClient` in capture mode
- `cleanup()` deletes all test collections after test run, saves capture data first if in capture mode
- Uses batch deletion to handle large collections without timeout
- `track_test_collection()` registers collections for cleanup
- Capture mode uses `CaptureManager` to record interactions

## Connections
- [[service_provider]] — abstract base class
- [[capture]] — capture infrastructure for recording test interactions