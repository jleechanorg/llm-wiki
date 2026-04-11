---
title: "PR #301: [agento] fix: kill tmux session when PR merges/closes (bd-s6z1)"
type: source
tags: []
date: 2026-03-30
source_file: raw/prs-worldai_claw/pr-301.md
sources: []
last_updated: 2026-03-30
---

## Summary
AO workers continue running in tmux sessions after their associated PR has been merged or closed. These zombie sessions burn tokens and context on completed work. The lifecycle-worker detects merged/closed state but had no mechanism to kill the tmux session.

## Metadata
- **PR**: #301
- **Merged**: 2026-03-30
- **Author**: jleechan2015
- **Stats**: +242/-6 in 2 files
- **Labels**: none

## Connections
