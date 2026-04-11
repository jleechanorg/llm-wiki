---
title: "Decorators Module"
type: source
tags: [python, decorators, exception-handling, logging, utility]
source_file: "raw/decorators-module.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python module providing utility decorators for cross-cutting concerns in WorldArchitect.AI, specifically focusing on exception logging to provide consistent error handling across services. The module exports a `log_exceptions` decorator that wraps functions with try-except blocks and logs exceptions with full context.

## Key Claims
- **Exception Logging Decorator**: `log_exceptions` wraps any function to catch and log exceptions with full context including function name, argument summary, kwargs keys, error message, and complete stack trace
- **Preserved Stack Traces**: Uses `traceback.format_exc()` to preserve the full stack trace for debugging purposes
- **Emoji-Enhanced Logging**: Integrates with `logging_util` module for consistent error message formatting with emoji indicators
- **Re-raises Exceptions**: After logging, the decorator re-raises the exception so calling code (e.g., route handlers) can handle it appropriately

## Key Code
```python
@log_exceptions
def my_function():
    # Function logic here
    pass
```

## Connections
- [[LoggingUtil]] — the logging_util module this decorator uses for logger initialization
- [[ExceptionHandling]] — exception handling patterns used in service layer

## Contradictions
- None identified
