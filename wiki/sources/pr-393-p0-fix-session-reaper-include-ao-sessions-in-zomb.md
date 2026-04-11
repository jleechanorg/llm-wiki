---
title: "PR #393: [P0] fix(session-reaper): include ao-* sessions in zombie cleanup"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-393.md
sources: []
last_updated: 2026-03-26
---

## Summary
The `ao-session-reaper.sh` cron job runs nightly to clean up zombie tmux sessions that are no longer associated with live agent work. However, it only scanned for `jc-*` named tmux sessions, completely ignoring `ao-*` sessions (e.g. `ao-748`, `ao-749`, `ao-750`) that accumulate when AO workers are killed but their tmux sessions persist.

## Metadata
- **PR**: #393
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +92/-14 in 2 files
- **Labels**: none

## Connections
