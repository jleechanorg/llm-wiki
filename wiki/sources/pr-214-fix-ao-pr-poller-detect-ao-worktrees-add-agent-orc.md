---
title: "PR #214: fix(ao-pr-poller): detect AO worktrees + add agent-orchestrator mapping"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-214.md
sources: []
last_updated: 2026-03-16
---

## Summary
- `branch_checked_out` now checks `~/.worktrees/<project>/*/HEAD` for AO-managed worktrees — fixes spurious re-spawns on branches already active in AO sessions
- `repo_to_ao_project` adds `jleechanorg/agent-orchestrator → agent-orchestrator` — fixes "Unknown project:" error on every poll
- SOUL.md MCP mail protocol rewritten as mandatory Steps 1/2/3

## Metadata
- **PR**: #214
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +58/-51 in 12 files
- **Labels**: none

## Connections
