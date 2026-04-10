---
title: "Decorator Pattern"
type: concept
tags: [python, design-patterns, decorator, logging]
sources: []
last_updated: 2026-04-08
---

The decorator pattern in Python allows extending function behavior without modifying the function itself. The `log_exceptions` decorator wraps functions to add exception handling and logging capabilities while preserving the original function's metadata and behavior.

## Key Characteristics
- Uses `@functools.wraps` to preserve `__name__`, `__doc__`, `__module__`, `__qualname__`
- Wraps function execution in try/except block
- Logs exception details then re-raises for upstream error handling
- Can trim sensitive arguments for security (count instead of content, keys instead of values)

## Related Concepts
- [[LoggingUtil]] — centralized logging configuration
- [[ExceptionHandling]] — error flow management
