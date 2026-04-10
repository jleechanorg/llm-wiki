---
title: "Exception Logging"
type: concept
tags: [python, logging, exception-handling, debugging, observability]
sources: [decorators-module]
last_updated: 2026-04-08
---

## Summary
Exception logging is the practice of capturing and recording information about errors that occur during application execution. Good exception logging provides sufficient context for debugging, including stack traces, variable state, and the execution path that led to the error.

## Best Practices
- **Include Context**: Log function name, arguments (summarized), and relevant state
- **Preserve Stack Traces**: Use `traceback.format_exc()` or `traceback.print_exc()`
- **Use Structured Formats**: JSON or structured logging enables easier parsing and searching
- **Don't Swallow Exceptions**: Re-raise after logging so calling code can handle appropriately

## Implementation Pattern
```python
try:
    return func(*args, **kwargs)
except Exception as e:
    # Log with context
    logger.error(f"Error in {func.__name__}: {e}\n{traceback.format_exc()}")
    raise  # Re-raise
```

## Related Concepts
- [[DecoratorPattern]] — implementation mechanism used
- [[LoggingUtil]] — logging utility integration
- [[StackTrace]] — stack trace handling
- [[Observability]] — system monitoring and debugging capabilities
