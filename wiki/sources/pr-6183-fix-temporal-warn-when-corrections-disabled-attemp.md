---
title: "PR #6183: fix(temporal): warn when corrections disabled (attempts=0, max=0)"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6183.md
sources: []
last_updated: 2026-04-11
---

## Summary
- When both `temporal_correction_attempts=0` and `max_attempts=0`, `build_temporal_warning_message()` silently returned `None` instead of producing an exceeded warning
- Changed early return guard to only skip when `max_attempts > 0` (so `attempts=0, max=0` falls through)
- Changed comparison from `>` to `>=` so `(0 >= 0)` triggers the exceeded/disabled path
- Added test case for the `(attempts=0, max=0)` edge case

## Metadata
- **PR**: #6183
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +79/-21 in 2 files
- **Labels**: none

## Connections
