---
title: "PR #357: [agento] fix(novel-daily + CI): launchd date wrapper, auto commit/push, evidence-gate strong-proof + wholesome fixes"
type: source
tags: []
date: 2026-04-03
source_file: raw/prs-worldai_claw/pr-357.md
sources: []
last_updated: 2026-04-03
---

## Summary
Fixes the novel-daily launchd job (`scripts/novel/run-daily.sh`) to:
1. Resolve install-time hardcoded `--daily` date (uses runtime date wrapper)
2. Commit and push generated daily entries to `origin/main` automatically
3. Move `git fetch + ff-only merge` BEFORE file generation (CR feedback) to prevent conflicts

Supersedes PR #354.

## Metadata
- **PR**: #357
- **Merged**: 2026-04-03
- **Author**: jleechan2015
- **Stats**: +600/-68 in 11 files
- **Labels**: none

## Connections
