---
title: "Python Logging"
type: concept
tags: [python, logging, standard-library]
sources: ["centralized-logging-utility"]
last_updated: 2026-04-08
---

## Definition
Python's built-in logging module providing a flexible framework for emitting log messages from Python programs. The module provides logger objects, handlers, formatters, and filters for categorizing and routing log messages.

## Key Components
- **Logger**: Primary interface for emitting log messages via debug(), info(), warning(), error(), critical() methods
- **Handler**: Routes log records to destinations (console, file, network)
- **Formatter**: Specifies the layout of log output
- **Filter**: Provides fine-grained control over which records are processed

## Usage in This Source
The centralized logging utility wraps Python logging with:
- Custom emoji-enhanced message formatting
- Automatic handler setup for Cloud Logging + file output
- Module-level convenience functions (ERROR, WARNING, INFO, DEBUG constants)
- Thread-safe initialization guard to prevent duplicate handlers

## Connections
- [[ContextVariables]] — contextvars for async-aware logging context
- [[CloudLogging]] — production logging destination for deployed applications
- [[FileLogging]] — local file output for development and debugging
