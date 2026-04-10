---
title: "Transparent Service Wrapper"
type: concept
tags: [testing, wrapper-pattern, service-mocking, capture]
sources: []
last_updated: 2026-04-08
---

## Definition
A design pattern where service clients (Firestore, Gemini, Auth) are wrapped with capture-aware versions that record all operations without changing the original API interface or test code behavior.

## Implementation
```python
provider = get_service_provider('capture')  # Enables capture mode
firestore = provider.get_firestore()        # Returns CaptureFirestoreClient
docs = firestore.collection('test').get()   # <- Automatically captured
provider.cleanup()                          # Saves capture data
```

## Key Properties
- **Zero API Change**: Tests use same method signatures as before
- **Transparent**: No awareness required in test code
- **Automatic Recording**: Every operation logged with metadata
- **Context Manager Support**: Proper cleanup and data saving

## Wrappers Implemented
- CaptureFirestoreClient — wraps Firestore operations
- CaptureGeminiClient — wraps Gemini API calls
- CaptureAuthClient — wraps authentication operations

## Related Concepts
- [[DataCaptureFramework]] — the framework this pattern enables
- [[ContextManagerPattern]] — Python pattern for resource lifecycle
