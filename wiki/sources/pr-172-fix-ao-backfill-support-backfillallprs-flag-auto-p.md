---
title: "PR #172: fix(ao-backfill): support backfillAllPRs flag + auto-prune stale worktrees"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-172.md
sources: []
last_updated: 2026-03-16
---

## Summary
- Add `backfillAllPRs: true` project config flag — ao-backfill.sh handles ALL open PRs for designated projects, not just `[agento]`-tagged ones
- Auto-prune stale git worktrees before each spawn cycle to unblock branch checkouts
- Add liveness respawn (PASS 2): finds `stuck`/`killed` sessions older than 30min and respawns them
- Add `--limit 1000` to all `gh pr list` calls to prevent truncation
- Fix Python env interpolation in heredocs using `AO_CONFIG_ARG`/`PROJECT_ID_ARG` env vars
- Tab-separ

## Metadata
- **PR**: #172
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +653/-66 in 8 files
- **Labels**: none

## Connections
