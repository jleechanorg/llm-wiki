---
title: "PR #200: [agento] docs: close bd-ara.3 — stale session fixes via bd-s4t"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-200.md
sources: []
last_updated: 2026-03-26
---

## Summary
bd-ara.3 reported that sessions for merged/closed PRs were accumulating past the 15-session spawn gate because:
1. lifecycle-manager transitioned to "merged" but never sent a kill signal to the tmux runtime
2. session-reaper skipped terminal-status sessions (including merged)
3. maxKillsPerRun was 5 — too slow for 25+ zombie sessions

## Metadata
- **PR**: #200
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +13/-13 in 1 files
- **Labels**: none

## Connections
