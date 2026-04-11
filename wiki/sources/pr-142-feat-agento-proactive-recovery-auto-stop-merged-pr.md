---
title: "PR #142: feat(agento): proactive recovery — auto-stop merged PRs, respawn stuck sessions"
type: source
tags: []
date: 2026-03-14
source_file: raw/prs-worldai_claw/pr-142.md
sources: []
last_updated: 2026-03-14
---

## Summary
- **agento-notifier.py**: recovery dispatch on AO lifecycle events — `merge.completed` → `ao stop`, `reaction.escalated` (agent-stuck) → `ao spawn` with 60s cooldown guard
- **ao-backfill.sh**: two new passes — merged-PR cleanup via `gh pr list --head`, and liveness respawn for stuck/killed sessions >30min (reads metadata files directly, clears `pr=` field before spawn)
- **roadmap/AGENTO_PROACTIVE_RECOVERY_DESIGN.md**: design analysis covering 4 options (external scripts, AO plugin, webhook han

## Metadata
- **PR**: #142
- **Merged**: 2026-03-14
- **Author**: jleechan2015
- **Stats**: +1053/-31 in 14 files
- **Labels**: none

## Connections
