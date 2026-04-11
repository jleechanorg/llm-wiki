---
title: "Centralized Logging Utility with Emoji-Enhanced Messages"
type: source
tags: [python, logging, cloud-logging, file-logging, emoji, initialization]
source_file: "raw/centralized-logging-utility.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Python logging utility providing consistent error and warning logging across the application with emoji-enhanced messages. Supports both module-level convenience functions and logger-aware functions that preserve logger context. Logs to both Cloud Logging (stdout/stderr) and local files under /tmp/<repo>/<branch>/<service>.log.

## Key Claims
- **Dual Output Architecture**: All logs go to BOTH Cloud Logging (stdout/stderr) and local file storage
- **Automatic Initialization**: Logging is initialized automatically on module import with guard to prevent duplicate handlers
- **Emoji-Enhanced Messages**: ERROR_EMOJI = "🔥🔴" and WARNING_EMOJI = "⚠️" for visual distinction
- **Git-Aware Configuration**: Automatically detects repository name from git remote URL and branch name from git commands
- **Thread-Safe Initialization**: Uses threading.Lock to prevent concurrent initialization of handlers

## Key Quotes
> `LoggingUtil._find_git_root()` walks up from a start directory to locate a .git directory or file

> `get_repo_name()` extracts repo name from git remote URL or falls back to directory name

## Connections
- [[PythonLogging]] — standard library providing the logging foundation
- [[CloudLogging]] — Google Cloud Logging integration for production logging
- [[ContextVariables]] — contextvars module for preserving logger context across async boundaries

## Contradictions
- None identified
