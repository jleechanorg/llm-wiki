---
title: "Simplified Mock Service Provider Implementation"
type: source
tags: [testing, mock, service-provider, firestore, gemini, authentication, python]
source_file: "raw/simplified-mock-service-provider-implementation.md"
sources: [test-service-provider-abstract-base-class]
last_updated: 2026-04-08
---

## Summary
Lightweight mock implementations for Firestore, Gemini, and Auth services that avoid complex dependencies while providing the same interface as TestServiceProvider. Enables framework testing without heavy external dependencies.

## Key Claims
- **SimpleMockFirestore** — Basic in-memory mock with collection/document interface and operation counting
- **SimpleMockGemini** — Mock that tracks call_count for verifying test interactions
- **SimpleMockAuth** — Mock auth service verifying tokens and returning user IDs
- **SimpleMockServiceProvider** — Unified provider combining all mocks with reset/cleanup methods
- **Operation Tracking** — Each mock tracks its own operation counts for test verification

## Key Code Structure

```python
class SimpleMockServiceProvider(TestServiceProvider):
    def __init__(self):
        self._firestore = SimpleMockFirestore()
        self._gemini = SimpleMockGemini()
        self._auth = SimpleMockAuth()
    
    def get_firestore(self) -> SimpleMockFirestore:
        return self._firestore
    
    def cleanup(self) -> None:
        self._firestore.reset()
        self._gemini.reset()
        self._auth.reset()
```

## Connections
- [[TestServiceProvider]] — Abstract base class this implements
- [[RealServiceProvider]] — Uses real services instead of mocks
- [[TestOrganizationImprovements]] — Related test infrastructure work

## Contradictions
- None identified
