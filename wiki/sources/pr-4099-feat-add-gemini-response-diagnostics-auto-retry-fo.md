---
title: "PR #4099: feat: Add Gemini response diagnostics + auto-retry for transient errors"
type: source
tags: []
date: 2026-01-27
source_file: raw/prs-worldarchitect-ai/pr-4099.md
sources: []
last_updated: 2026-01-27
---

## Summary
- Add comprehensive Gemini response logging (finish_reason, safety_ratings, prompt_feedback)
- Add automatic retry with exponential backoff for FAILED_PRECONDITION errors
- Add user-visible warning when retries succeed (like dice integrity warnings)
- Enhanced error logging with nested RPC details and raw response text

## Metadata
- **PR**: #4099
- **Merged**: 2026-01-27
- **Author**: jleechan2015
- **Stats**: +1119/-61 in 5 files
- **Labels**: none

## Connections
