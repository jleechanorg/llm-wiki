---
title: "PR #131: [agento] fix(auton): remove deprecated poller check, add auto-merge config verification"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-131.md
sources: []
last_updated: 2026-03-24
---

## Summary
`/auton` was reporting two false positives that wasted diagnostic time:
1. **"Poller: STOPPED"** -- ao-pr-poller was removed in PR #352. Its absence is correct, not a bug.
2. **"No merge executor"** -- auto-merge is enabled (`approved-and-green: auto: true, action: auto-merge`). The skill was not checking the config, so it fabricated a gap that does not exist.

## Metadata
- **PR**: #131
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +22/-3 in 1 files
- **Labels**: none

## Connections
