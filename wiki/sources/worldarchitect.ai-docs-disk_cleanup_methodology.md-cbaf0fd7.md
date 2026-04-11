---
title: "Disk Cleanup Methodology"
type: source
tags: [disk-cleanup, automation, dev-tools, storage]
sources: []
date: 2026-04-07
source_file: docs/disk_cleanup_methodology.md
last_updated: 2026-04-07
---

## Summary
Systematic approach to reclaiming disk space from AI tooling artifacts including orchestration worktrees, CI caches, and dev tool caches. On 2026-03-01, disk hit 99.2% (8 GB free on 995 GB drive) and cleanup recovered ~280 GB.

## Key Claims
- **Problem**: System accumulates ephemeral worktrees, caches, and CI artifacts consuming hundreds of GB
- **Root Cause #1**: Orchestration harness worktrees (~70 GB) — `orchestration/task_dispatcher.py` creates ~1 GB worktree per agent per session
- **Root Cause #2**: Actions-runner stale workspaces (~80 GB) — `.old-ws-*` and `ci-stale-*` dirs accumulate silently
- **Root Cause #3**: Project worktrees (~55 GB) — `worktree_*` dirs across project dirs without cleanup
- **Root Cause #4**: Dev tool caches (~40 GB) — uv (18 GB), Codex sessions (35 GB, PRESERVE), Cursor (15 GB)
- **Root Cause #5**: Docker (31 GB) — images, containers, build cache
- **Fix**: PR #5810 redirects default path to `/tmp/orch_worktrees/` so OS handles cleanup
- **Cleanup Result**: 99.2% → 69% disk usage, freed ~280 GB

## Key Solutions

### Automated Cleanup Script
The `scripts/disk_cleanup.sh` script targets items older than 14 days:
1. Orchestration `harness*` worktrees
2. Project `worktree_*` dirs across all project dirs
3. `~/projects/worktree_*` and `orch_*` dirs
4. Home root `worktree_*`, `pr-*`, `wa-*` dirs
5. Actions-runner `.old-ws-*` and `ci-stale-*` dirs
6. `uv` cache, `.gemini/tmp`
7. Cursor worktrees
8. `/tmp` stale orchestration trees

### NEVER Cleaned by Script
- `~/.codex/sessions/` — Codex conversation history, irreplaceable
- `~/.claude/projects/` — Claude conversation/project data, irreplaceable
- Git repos with no remote (check before manual deletion)
- Docker (requires daemon running)

### Quick Diagnostic Commands
```bash
# Overall status
df -h /

# What's eating home dir (top 15)
du -sh ~/* ~/.* 2>/dev/null | sort -rh | head -15

# Find dirs >1 GB older than 2 weeks
find ~ -maxdepth 2 -type d -mtime +14 -exec du -sh {} \; 2>/dev/null | awk '$1 ~ /G/' | sort -rh
```

## Key Learnings

### Patterns That Cause Bloat
1. **Orchestration worktrees are #1 offender** — pair-programming creates ~1 GB worktree per agent per session
2. **CI runners never clean up** — `.old-ws-*` and `ci-stale-*` accumulate silently as hidden dirs
3. **Project dirs accumulate worktrees inside them** — orchestration runs create 64+ `worktree_*` subdirs
4. **Dev tool caches grow unbounded** — uv (18 GB), npm (4 GB), puppeteer (2.5 GB), .claude/debug (3.6 GB)
5. **Old backups stick around** — `.claude.backup.*` dirs (2.6 GB)

### What NOT to Delete
- `~/.codex/sessions/` — conversation history, irreplaceable
- `~/.claude/projects/` — conversation/project data, irreplaceable
- `~/.codex/state_5.sqlite` — can VACUUM but don't delete
- Any git repo checkout without confirming remote exists

## Connections
- [[WorldArchitect.AI Crontab Configuration]] — automated cron jobs for monitoring and cleanup
- [[MacBook Dev Environment Setup Guide]] — environment setup that can accumulate caches

## Contradictions
- None identified
