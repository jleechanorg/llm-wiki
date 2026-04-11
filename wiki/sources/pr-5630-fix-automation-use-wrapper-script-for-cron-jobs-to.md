---
title: "PR #5630: fix(automation): use wrapper script for cron jobs to preserve MINIMAX_API_KEY"
type: source
tags: []
date: 2026-02-19
source_file: raw/prs-worldarchitect-ai/pr-5630.md
sources: []
last_updated: 2026-02-19
---

## Summary
- Fix fixpr cron job failing with "Invalid API key" errors
- Created wrapper script that exports MINIMAX_API_KEY before calling jleechanorg-pr-monitor
- Updated all cron jobs to use the wrapper script
- Added wrapper script to repo (`automation/jleechanorg-pr-monitor-wrapper.sh`)
- Updated install_cron_entries.sh to install wrapper to ~/.local/bin
- Fixed CLI validation to not require exit code 0 (Claude CLI exits 1 but produces valid output)

## Metadata
- **PR**: #5630
- **Merged**: 2026-02-19
- **Author**: jleechan2015
- **Stats**: +38/-8 in 5 files
- **Labels**: none

## Connections
