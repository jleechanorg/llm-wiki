---
title: "PR #282: feat(agento): add rate-limit fallback for --claim-pr"
type: source
tags: []
date: 2026-03-20
source_file: raw/prs-worldai_claw/pr-282.md
sources: []
last_updated: 2026-03-20
---

## Summary
- When GitHub is rate-limited, spawn scripts now fall back to unclaimed mode and continue work in the worktree
- PR will be created/updated at the end of the session
- Clear log message: `RATE LIMIT: --claim-pr failed for PR #N, falling back to unclaimed spawn`

## Metadata
- **PR**: #282
- **Merged**: 2026-03-20
- **Author**: jleechan2015
- **Stats**: +148/-311 in 8 files
- **Labels**: none

## Connections
