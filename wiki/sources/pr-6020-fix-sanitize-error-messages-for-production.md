---
title: "PR #6020: fix: sanitize error messages for production"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6020.md
sources: []
last_updated: 2026-04-04
---

## Summary
Fixes error message exposure for production launch in mvp_site/.

### Changes Made

1. **main.py**:
   - Line 1894: Changed  to generic message "Invalid request parameters"
   - Line 3372: Changed  to generic message "Internal error processing request"

2. **mcp_client.py**:
   - Added  helper function that:
     - Filters sensitive patterns (file paths, credentials, database names, etc.)
     - Removes file paths and URLs from error messages
     - Truncates long messages
   - Updated  to sanit

## Metadata
- **PR**: #6020
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +568/-51 in 3 files
- **Labels**: none

## Connections
