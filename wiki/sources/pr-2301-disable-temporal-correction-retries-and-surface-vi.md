---
title: "PR #2301: Disable temporal correction retries and surface violations to users"
type: source
tags: []
date: 2025-12-03
source_file: raw/prs-worldarchitect-ai/pr-2301.md
sources: []
last_updated: 2025-12-03
---

## Summary
- Disable temporal correction retries (`MAX_TEMPORAL_CORRECTION_ATTEMPTS=0`) to prevent multiple LLM calls
- Add user-facing temporal anomaly alerts via `god_mode_response` 
- Update test to match disabled corrections behavior

## Metadata
- **PR**: #2301
- **Merged**: 2025-12-03
- **Author**: jleechan2015
- **Stats**: +76/-22 in 2 files
- **Labels**: none

## Connections
