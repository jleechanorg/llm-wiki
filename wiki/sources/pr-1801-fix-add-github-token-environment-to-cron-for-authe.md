---
title: "PR #1801: fix: Add GITHUB_TOKEN environment to cron for authenticated API access"
type: source
tags: []
date: 2025-10-01
source_file: raw/prs-worldarchitect-ai/pr-1801.md
sources: []
last_updated: 2025-10-01
---

## Summary
Fixes jleechanorg PR automation failing with "API rate limit exceeded" errors every 30 minutes since 17:30 on 2025-09-30.

**Root Cause**: Cron jobs don't inherit shell environment variables, causing the `gh` CLI to make unauthenticated API requests (60 requests/hour limit) instead of authenticated requests (5000/hour limit).

**Solution**: Updated crontab to source `~/.token` file before executing automation script, providing GITHUB_TOKEN for authenticated API access.

## Metadata
- **PR**: #1801
- **Merged**: 2025-10-01
- **Author**: jleechan2015
- **Stats**: +40/-0 in 1 files
- **Labels**: none

## Connections
