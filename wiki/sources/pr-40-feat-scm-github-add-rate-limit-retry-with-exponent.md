---
title: "PR #40: feat(scm-github): add rate limit retry with exponential backoff and REST fallback"
type: source
tags: []
date: 2026-03-20
source_file: raw/prs-worldai_claw/pr-40.md
sources: []
last_updated: 2026-03-20
---

## Summary
- Add `isRateLimitError()` to detect rate limit errors from gh CLI
- Add `ghWithRetry()` with exponential backoff (max 3 retries, max 30s backoff)
- Add `ghRestFallback()` to use curl-based REST API when gh is rate limited
- Add `ghWithRetryDir()` for directory-based gh calls with retry support
- Add 3 tests for rate limit handling (retry success, max retries, no retry for non-rate-limit)

## Metadata
- **PR**: #40
- **Merged**: 2026-03-20
- **Author**: jleechan2015
- **Stats**: +341/-4 in 2 files
- **Labels**: none

## Connections
