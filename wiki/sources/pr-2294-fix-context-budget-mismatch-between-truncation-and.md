---
title: "PR #2294: Fix context budget mismatch between truncation and validation"
type: source
tags: []
date: 2025-12-03
source_file: raw/prs-worldarchitect-ai/pr-2294.md
sources: []
last_updated: 2025-12-03
---

## Summary
- Add centralized _calculate_context_budget() function for consistent budget calculation
- Truncation now uses same 20% output reserve ratio as validation
- Use ContextTooLargeError instead of ValueError for proper error handling
- Add ContextTooLargeError handling in model cycling for potential fallback

## Metadata
- **PR**: #2294
- **Merged**: 2025-12-03
- **Author**: jleechan2015
- **Stats**: +1145/-52 in 16 files
- **Labels**: none

## Connections
