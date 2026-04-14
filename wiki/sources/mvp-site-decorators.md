---
title: "Decorators Module"
type: source
tags: [utilities, error-handling, cross-cutting]
sources: [mvp-site-decorators]
last_updated: 2025-01-15
---

## Summary

Utility decorators for cross-cutting concerns. Currently provides exception logging with full context preservation.

## Key Claims

- **@log_exceptions**: Wraps function in try-except, logs full stack trace
- **Context preservation**: Logs function name, args summary, kwargs keys
- **Re-raises after logging**: Allows calling code to handle exceptions
- **Logger integration**: Uses emoji-enhanced logging_util

## Usage

```python
@log_exceptions
def my_function():
    # Function logic
    pass
```

## Connections

- [[mvp-site-logging-util]] - Logging utilities
