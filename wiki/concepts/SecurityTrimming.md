---
title: "Security Trimming"
type: concept
tags: [security, logging, exception-handling, privacy]
sources: []
last_updated: 2026-04-08
---

Security trimming in logging refers to the practice of sanitizing sensitive data before writing to logs. For function arguments, this means:

- **Args**: Show count only (e.g., "2 args"), never expose actual values
- **Kwargs**: Show keys only (e.g., "['c', 'd']"), never expose values
- **Traceback**: Full traceback is logged for debugging, but args/kwargs are trimmed

This prevents credential leakage, PII exposure, and other security vulnerabilities from logs.

## Related Patterns
- [[DecoratorPattern]] — where trimming is applied
- [[LoggingUtil]] — log output destination
