---
title: "PR #364: feat: add workspace observability report (weekly Monday 10am PT)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-364.md
sources: []
last_updated: 2026-03-23
---

## Summary
- New `scripts/workspace-report.sh` — weekly jleechanclaw workspace health audit across 8 dimensions (worktrees, file parity, backups, launchd jobs, sessions, gateway probe, open PRs, evidence metrics)
- Output: dated markdown report with **exec summary + top-3 recommendations at the top**, full detail below
- Exit 1 when failures detected (suitable for monitoring automation); configurable via `OPENCLAW_WORKSPACE_REPORT_OUTDIR` and `OPENCLAW_WORKSPACE_REPORT_CHANNEL`
- New `ai.openclaw.schedule.

## Metadata
- **PR**: #364
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +635/-9 in 5 files
- **Labels**: none

## Connections
