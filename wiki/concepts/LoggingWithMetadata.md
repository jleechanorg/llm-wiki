---
title: "Logging With Metadata"
type: concept
tags: [logging, monitoring, debugging]
sources: [token-counting-utilities]
last_updated: 2026-04-08
---

## Definition
Logging with metadata is the practice of including additional context (like character counts, token estimates, or performance metrics) in log messages to aid debugging and monitoring.

## WorldAI Implementation
The log_with_tokens() function wraps logging_util to automatically include character and token counts in log messages. This helps developers track token usage patterns and identify potential issues with large inputs.

## Benefits
- **Debugging**: Quickly identify which requests have unusually high token counts
- **Monitoring**: Track token usage trends over time
- **Transparency**: Make token consumption visible in logs for stakeholder awareness

## Related Concepts
- [[TokenCountingUtilities]] — the specific implementation
- [[LoggingUtil]] — the underlying logging module
- [[TokenEstimation]] — the metrics being logged
