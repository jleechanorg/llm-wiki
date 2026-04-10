---
title: "Capture File"
type: concept
tags: [testing, json, service-capture]
sources: []
last_updated: 2026-04-08
---

JSON file format for storing service interactions during testing. Follows `capture_*.json` naming pattern. Contains service names, operations, request/response pairs, timestamps, and error information.

## File Format
- Pattern: `capture_YYYY-MM-DD.json`
- Location: Configurable via `--capture-dir` or `TEST_CAPTURE_DIR` env var
- Default: `{tempfile.gettempdir()}/test_captures`

## Related Concepts
- [[CaptureAnalyzer]] — analyzes capture files
- [[Cleanup Old Captures]] — removes stale capture files
