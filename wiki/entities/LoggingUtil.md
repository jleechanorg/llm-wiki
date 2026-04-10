---
title: "logging_util"
type: entity
tags: [module, logging, utility]
sources: [real-browser-settings-game-integration-test]
last_updated: 2026-04-08
---

Python utility module providing centralized logging functionality. Used in tests to get consistent log file paths for verification. The test uses `logging_util.LoggingUtil.get_log_file("integration-test")` to locate server logs.

## Wiki Connections
- [Real Browser Settings Game Integration Test] uses logging_util for log file path resolution
