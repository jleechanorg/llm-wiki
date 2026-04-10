---
title: "Context Manager Pattern"
type: concept
tags: [python, patterns, resource-management]
sources: []
last_updated: 2026-04-08
---

## Definition
Python's context manager protocol using `@contextmanager` decorator or `__enter__`/`__exit__` methods for guaranteed resource cleanup. The Capture Framework uses this pattern to automatically record interaction start/end times and ensure all interactions are properly finalized regardless of success or failure.

## Application in Capture Framework
The `capture_interaction()` method wraps service calls in a context manager that:
1. Records start timestamp on entry
2. Executes the service call
3. Records duration and status (success/error) on exit
4. Guarantees cleanup even if exceptions occur

## Related Concepts
- [[DataSanitization]] — automatic redaction of sensitive fields
- [[ServiceInteractionRecording]] — capturing API calls and responses
- [[JSONSerialization]] — storing captured interactions
