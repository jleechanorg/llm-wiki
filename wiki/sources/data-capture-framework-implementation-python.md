---
title: "Data Capture Framework Implementation (Python)"
type: source
tags: [worldarchitect, testing, capture-framework, mock-validation, python-implementation]
source_file: "raw/data-capture-framework-implementation.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Python implementation of the Capture Framework for recording real service interactions during testing. Provides CaptureManager class with context manager pattern for capturing API calls and responses, JSON serialization with automatic sanitization, and session-based organization for mock validation workflows.

## Key Claims
- **CaptureManager Class**: Central orchestrator for recording service interactions with context manager pattern
- **Context Manager Pattern**: `@contextmanager` decorator enables `with capture_interaction()` syntax for automatic start/end recording
- **Response Recording**: `record_response()` method allows capturing response data after interaction completes
- **JSON Storage**: `save_captures()` writes session data to JSON files with timestamp, session_id, and interaction array
- **Data Sanitization**: `_sanitize_data()` automatically redacts sensitive fields (password, api_key, secret) matching key patterns
- **Circular Reference Prevention**: Tracks visited object IDs to prevent infinite recursion during sanitization
- **Configurable Capture Directory**: Defaults to `TEST_CAPTURE_DIR` env var or `/tmp/test_captures`

## Key Code Patterns
```python
with capture_manager.capture_interaction("firestore", "get_document", {"id": "123"}) as interaction:
    result = client.get_document("123")
    capture_manager.record_response(interaction["id"], result)
```

## Connections
- [[CaptureFrameworkDocumentation]] — documented overview of the framework
- [[CaptureAnalysisCLI]] — CLI tools for analyzing captured interaction files
- [[CaptureAnalyzer]] — service interaction analysis and mock comparison

## Contradictions
- None identified
