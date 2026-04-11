---
title: "PR #652: Fix schedule_branch_work.sh bashrc sourcing for PATH availability"
type: source
tags: []
date: 2025-07-17
source_file: raw/prs-worldarchitect-ai/pr-652.md
sources: []
last_updated: 2025-07-17
---

## Summary
Fixes the `schedule_branch_work.sh` script to properly source `~/.bashrc` so that the `claude` command is available when `ccschedule` runs in a non-interactive context.

**Problem**: The script was failing with "No such file or directory" error because `ccschedule` runs in a non-interactive shell context where `~/.bashrc` isn't automatically sourced, making the `claude` command unavailable.

**Solution**: Added `source ~/.bashrc` at the beginning of the script to ensure PATH and environment vari

## Metadata
- **PR**: #652
- **Merged**: 2025-07-17
- **Author**: jleechan2015
- **Stats**: +20/-5 in 3 files
- **Labels**: none

## Connections
