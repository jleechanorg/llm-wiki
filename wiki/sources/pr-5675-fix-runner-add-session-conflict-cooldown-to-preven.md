---
title: "PR #5675: fix(runner): add session conflict cooldown to prevent restart loops after reboot"
type: source
tags: []
date: 2026-02-20
source_file: raw/prs-worldarchitect-ai/pr-5675.md
sources: []
last_updated: 2026-02-20
---

## Summary
- After reboot, crontab restarts the runner but GitHub holds the stale session for ~4 min, causing SessionConflictException loops
- Monitor was restarting the runner every 15-min cycle, hitting the same conflict each time
- Add 5-minute cooldown: detect conflict in diag log, write stamp, skip restarts until cooldown expires

## Metadata
- **PR**: #5675
- **Merged**: 2026-02-20
- **Author**: jleechan2015
- **Stats**: +172/-26 in 2 files
- **Labels**: none

## Connections
