---
title: "Log Exceptions Decorator Tests"
type: source
tags: [python, testing, decorator, logging, exception-handling, security]
source_file: "raw/test_log_exceptions_decorator.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit tests validating the `log_exceptions` decorator functionality: preserves function metadata, logs exceptions with trimmed arguments for security, and re-raises exceptions after logging. Tests cover successful execution, exception handling, argument trimming, and multiple exception types.

## Key Claims
- **Metadata Preservation**: Decorator preserves `__name__` and `__doc__` of decorated functions
- **Successful Execution**: No logging overhead for functions that complete without errors
- **Exception Logging**: Logs function name, argument count, kwarg keys, error message, and full traceback
- **Security Trimming**: Args show count only, kwargs show keys only — never expose sensitive values
- **Exception Re-raising**: Decorator logs then re-raises original exception to maintain error flow

## Key Test Cases
- `test_decorator_preserves_function_metadata`: Verify `__name__` and `__doc__` intact
- `test_decorator_successful_execution`: Verify no logging for successful runs
- `test_decorator_logs_exception_and_reraises`: Verify logging + re-raise behavior
- `test_decorator_logs_function_arguments`: Verify trimmed argument display (count + keys)
- `test_decorator_with_different_exception_types`: Verify handling of ValueError, TypeError, RuntimeError

## Connections
- [[LoggingUtil]] — provides the logger used by decorator
- [[DecoratorPattern]] — the log_exceptions implementation pattern

## Contradictions
- []
