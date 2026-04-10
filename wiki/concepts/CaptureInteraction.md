---
title: "Capture Interaction"
type: concept
tags: [testing, capture, context-manager]
sources: [capture-framework-tests]
last_updated: 2026-04-08
---

## Description
Context manager pattern for recording service interactions. Wraps an operation with automatic entry/exit logging, response capture, and error handling.

## Behavior
1. On `__enter__`: creates interaction record with id, service, operation, request, start_time
2. On `__exit__`: records status (success/error), duration_ms, and optional error details
3. Yields interaction dict for inline response recording

## Usage
```python
with capture_manager.capture_interaction("firestore", "get", {"collection": "users"}) as interaction:
    result = db.collection("users").get()
    capture_manager.record_response(interaction["id"], {"docs": result})
```

## Related
- [[RecordResponse]] — companion method for capturing response data
- [[DataSanitization]] — automatic credential redaction
