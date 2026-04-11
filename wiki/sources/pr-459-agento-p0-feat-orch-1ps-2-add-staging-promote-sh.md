---
title: "PR #459: [agento] [P0] feat(orch-1ps.2): add staging-promote.sh — auto-promote staging→prod"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-459.md
sources: []
last_updated: 2026-03-31
---

## Summary
- Adds `scripts/staging-promote.sh`: the Stage 2 gate in the 3-stage openclaw dev pipeline (orch-1ps epic).
- Runs `staging-canary.sh --port 18790` (6-point health check against staging gateway).
- If all 6 checks pass: merges `staging → origin/main` in the staging worktree, then `git pull --ff-only` in `~/.openclaw/` (prod).
- If any check fails: exits without promoting.

## Metadata
- **PR**: #459
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +160/-0 in 1 files
- **Labels**: none

## Connections
