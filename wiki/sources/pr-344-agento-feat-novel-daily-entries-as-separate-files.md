---
title: "PR #344: [agento] feat(novel): daily entries as separate files + canonical plist path"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldai_claw/pr-344.md
sources: []
last_updated: 2026-04-02
---

## Summary
The `ai.agento.novel-daily` launchd job was writing to a stale path
(`/Users/jleechan/.cursor/worktrees/worktree_cursor/ctj/agent-orchestrator/`) instead
of the canonical repo. Additionally, all daily entries were being appended
to the monolithic `novel/the-daily-lives-of-workers.md` file — making it
hard to navigate and impossible to run idempotently per-day.

## Metadata
- **PR**: #344
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +124/-7 in 4 files
- **Labels**: none

## Connections
