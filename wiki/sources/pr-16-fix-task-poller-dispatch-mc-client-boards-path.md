---
title: "PR #16: fix: task poller dispatch + mc_client boards path"
type: source
tags: []
date: 2026-03-03
source_file: raw/prs-worldai_claw/pr-16.md
sources: []
last_updated: 2026-03-03
---

## Summary
- Fix `update_task` to use `/api/v1/boards/{board_id}/tasks/{task_id}` (old `/api/v1/tasks/{id}` returns 404)
- Auto-wire `build_claudem_dispatch()` in `TaskPoller.__post_init__` when `MINIMAX_API_KEY` is set (prevents `ai_orch` receiving invalid `"claudem"` CLI)
- Fix `start-mc.sh` to read `LOCAL_AUTH_TOKEN` from `.env` instead of placeholder

## Metadata
- **PR**: #16
- **Merged**: 2026-03-03
- **Author**: jleechan2015
- **Stats**: +534/-73 in 7 files
- **Labels**: none

## Connections
