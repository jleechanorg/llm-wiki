---
title: "PR #135: [agento] feat(scm-github): REST fallback for mergePR on rate limit"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-135.md
sources: []
last_updated: 2026-03-23
---

## Summary
- Add try/catch in `mergePR` that detects rate limit errors via `isRateLimitError`
- On rate limit, falls back to `gh api PUT /repos/{owner}/{repo}/pulls/{num}/merge` with `merge_method` parameter
- Uses existing `gh` wrapper so the call goes through `ghWithRetry` for retries

## Metadata
- **PR**: #135
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +92/-5 in 2 files
- **Labels**: none

## Connections
