---
title: "mvp_site logging_util"
type: source
tags: []
date: 2026-04-14
source_file: raw/mvp_site_all/logging_util.py
---

## Summary
Centralized logging utility with emoji-enhanced messages and unified logging architecture. Logs go to both Cloud Logging (stdout/stderr) and local file under /tmp/<repo>/<branch>/<service>.log. Auto-initializes on import with duplicate handler prevention.

## Key Claims
- LoggingUtil class with ERROR_EMOJI = "🔥🔴" and WARNING_EMOJI = "⚠️"
- Automatic initialization: _logging_initialized guard prevents duplicate handlers
- Log file path: /tmp/<repo>/<branch>/<service>.log
- Configurable service name via LOGGING_SERVICE_NAME env var
- Thread-safe via _logging_lock

## Connections
- [[LLMIntegration]] — centralized logging for all services
