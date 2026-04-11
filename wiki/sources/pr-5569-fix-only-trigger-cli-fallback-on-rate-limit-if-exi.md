---
title: "PR #5569: fix: Only trigger CLI fallback on rate limit if exit code is non-zero"
type: source
tags: []
date: 2026-02-16
source_file: raw/prs-worldarchitect-ai/pr-5569.md
sources: []
last_updated: 2026-02-16
---

## Summary
- Fix false positive rate limit detection in CLI fallback logic
- Rate limit now only triggers fallback when exit code is non-zero (actual failure)
- Prevents unnecessary fallback when informational messages mention "rate limit"

## Metadata
- **PR**: #5569
- **Merged**: 2026-02-16
- **Author**: jleechan2015
- **Stats**: +58/-1 in 3 files
- **Labels**: none

## Connections
