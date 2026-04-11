---
title: "PR #5966: feat(scripts): add check-pr-status.sh — poll PRs, seek CodeRabbit approval"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldarchitect-ai/pr-5966.md
sources: []
last_updated: 2026-03-15
---

## Summary
Add `scripts/check-pr-status.sh` that:
- Polls all open PRs in **worldarchitect.ai** and **jleechanclaw** every 5 minutes
- Posts `@coderabbitai all good?` on each PR (throttled 1/hr to avoid spam)
- `PING_CODERABBIT=false` to skip pings; `--once` for single run

## Metadata
- **PR**: #5966
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +199/-3 in 5 files
- **Labels**: none

## Connections
