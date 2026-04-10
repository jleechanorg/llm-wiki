---
title: "Context Variables"
type: concept
tags: [python, async, concurrency, context]
sources: ["centralized-logging-utility"]
last_updated: 2026-04-08
---

## Definition
Python's `contextvars` module provides context variables that are specific to a specific execution context (such as a request or task). Unlike thread-local variables, context variables work correctly with asyncio and other concurrency patterns that may switch between threads.

## Key Concepts
- **ContextVar**: Creates a context variable that holds a value specific to the current context
- **copy_context()**: Creates a copy of the current context
- **Context.run()**: Executes code within a specific context

## Usage in This Source
The logging utility imports `contextvars` for potential async-aware logger context preservation, allowing logging to maintain request-specific context across async boundaries.

## Connections
- [[PythonLogging]] — used with contextvars for async-aware logging
- [[AsyncIO]] — async framework that benefits from context variable usage
- [[LLMService]] — async service that could use context variables for request tracking
