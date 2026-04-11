---
title: "PR #6042: [agento] feat(commands): add /polish — iterative PR green loop with all claude-commands#272 review fixes"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldarchitect-ai/pr-6042.md
sources: []
last_updated: 2026-03-23
---

## Summary
Ports the `/polish` slash command from [jleechanorg/claude-commands#272](https://github.com/jleechanorg/claude-commands/pull/272) with all review comments addressed.

- Adds `/polish [N] [PR_NUMBER]` — iterative PR green loop command
- Drives a PR to all 6 green conditions (CI, merge conflicts, CodeRabbit, Bugbot, inline comments, evidence)
- Loops up to N times (default 5) using `/copilot` + `/fixpr` + `/er`

## Metadata
- **PR**: #6042
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +75/-26 in 2 files
- **Labels**: none

## Connections
