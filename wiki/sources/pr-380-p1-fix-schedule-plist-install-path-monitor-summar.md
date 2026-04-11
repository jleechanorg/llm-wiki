---
title: "PR #380: [P1] fix: schedule plist install path + monitor summary verbosity"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-380.md
sources: []
last_updated: 2026-03-24
---

## Summary
doctor.sh fails because `ai.openclaw.schedule.harness-analyzer-9am` plist is not installed. Root cause: `install-openclaw-scheduled-jobs.sh` searches for plists in `openclaw-config/` (wrong directory) instead of `launchd/` (where they actually live). Also, the monitor Slack summary shows all passing checks which is noisy.

## Metadata
- **PR**: #380
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +126/-27 in 3 files
- **Labels**: none

## Connections
