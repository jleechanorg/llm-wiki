---
title: "PR #908: fix(cerebras): retry on 503 queue_exceeded rate limit errors"
type: source
tags: []
date: 2025-12-06
source_file: raw/prs-/pr-908.md
sources: []
last_updated: 2025-12-06
---

## Summary
- Add retry logic for HTTP 503 errors with `queue_exceeded` (Cerebras-specific rate limiting)
- Cerebras direct API returns 503 instead of standard 429 for rate limits
- Fixes synthesis failures on high-traffic dev server

## Metadata
- **PR**: #908
- **Merged**: 2025-12-06
- **Author**: jleechan2015
- **Stats**: +1327/-6288 in 7 files
- **Labels**: none

## Connections
