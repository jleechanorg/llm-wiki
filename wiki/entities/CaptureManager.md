---
title: "CaptureManager"
type: entity
tags: [testing, capture, orchestration]
sources: [capture-framework-tests]
last_updated: 2026-04-08
---

## Description
Main orchestration class for the capture framework that manages recording of service interactions. Provides context manager interface for capturing operations and exports interactions as JSON.

## Key Responsibilities
- Manages capture directory for session files
- Provides `capture_interaction()` context manager
- Records responses via `record_response()`
- Exports session data via `save_captures()`
- Sanitizes sensitive fields via `_sanitize_data()`

## API
- `__init__(capture_dir)` — initialize with output directory
- `capture_interaction(service, operation, request)` — context manager for recording
- `record_response(interaction_id, response)` — record response data
- `save_captures()` — export to JSON file, returns filepath
- `_sanitize_data(data)` — redact password/api_key fields
- `get_summary()` — return statistics by service/operation

## Related
- [[CaptureFirestoreClient]] — Firestore-specific capture
- [[CaptureGeminiClient]] — Gemini-specific capture
- [[CaptureAnalyzer]] — session analysis
