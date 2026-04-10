---
title: "Thresholded Warning System"
type: concept
tags: [logging, warnings, error-handling, monitoring]
sources: [simplified-structured-narrative-generation-schemas]
last_updated: 2026-04-08
---

Per-server-process warning escalation system that tracks warning counts and escalates from INFO to WARNING to ERROR based on configurable thresholds.

Uses _RUN_WARNING_COUNTS Counter to track occurrences per key, with:
- warn_at: Threshold to start WARNING level (default: 3)
- error_at: Threshold to escalate to ERROR level (default: 10)

Related: [[CentralizedLoggingUtility]]
