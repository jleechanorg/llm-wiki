---
title: "PR #212: feat: add escalation anomaly detector"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-212.md
sources: []
last_updated: 2026-03-16
---

## Summary
Add escalation anomaly detection to monitor action_log.jsonl for patterns.

### Changes

1. **src/orchestration/anomaly_detector.py** - New module that:
   - Reads ~/.openclaw/state/action_log.jsonl
   - Counts escalations per error_class in rolling 7-day window
   - Sends Slack DM via openclaw_notifier.py if any error_class has >=2 escalations
   - Provides summary with error class, count, first/last seen, recent reasons

2. **src/tests/test_anomaly_detector.py** - 14 tests covering:
   - File

## Metadata
- **PR**: #212
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +599/-2 in 4 files
- **Labels**: none

## Connections
