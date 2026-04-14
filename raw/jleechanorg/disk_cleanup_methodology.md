# Disk Cleanup Methodology

## Problem

The system accumulates ephemeral worktrees, caches, and CI artifacts that can consume hundreds of GB. On 2026-03-01 the disk hit 99.2% (8 GB free on a 995 GB drive).

## Root Causes

### 1. Orchestration harness worktrees (~70 GB)
- **What**: `orchestration/task_dispatcher.py` creates `harness*` worktrees for pair-programming (coder/verifier) in `~/projects/orch_{repo}/`
- **Why they accumulate**: No cleanup after orchestration completes
- **Fix**: PR #5810 redirects default path to `/tmp/orch_worktrees/` so OS handles cleanup
- **Env override**: `ORCHESTRATION_WORKTREE_BASE` to restore persistence if needed

### 2. Actions-runner stale workspaces (~80 GB)
- **What**: `.old-ws-*` (hidden workspace snapshots) and `ci-stale-*` dirs under `actions-runner/_work/worldarchitect.ai/`
- **Why they accumulate**: GitHub Actions creates worktrees per CI job; no post-job cleanup step removes them
- **Fix needed**: Add cleanup step to CI workflows or cron job (see bead REV-6l4)
- **Permission issue**: Some `.ci-container-secrets` dirs require sudo to remove

### 3. Project worktrees (~55 GB)
- **What**: `worktree_*` dirs in `~/project_ai_universe*/`, `~/projects/`, home root
- **Why they accumulate**: Orchestration and manual worktree creation without cleanup
- **Fix**: `scripts/disk_cleanup.sh` prunes worktrees older than 14 days

### 4. Dev tool caches (~40 GB)
- **uv** (`~/.cache/uv`): Python package cache, 18 GB. `uv cache clean` rebuilds on demand
- **Codex** (`~/.codex/sessions`): 35 GB session logs. **PRESERVE** — conversation records
- **Cursor** (`~/.cursor/worktrees`): 15 GB stale worktrees. Clean if >14 days old
- **Gemini** (`~/.gemini/tmp`): temp files, safe to delete

### 5. Docker (31 GB)
- `~/Library/Containers/com.docker.docker`: images, containers, build cache
- `docker system prune -a` when daemon is running

## Automated Cleanup

### Script: `scripts/disk_cleanup.sh`

```bash
# Dry run (see what would be deleted):
./scripts/disk_cleanup.sh

# Actually delete:
./scripts/disk_cleanup.sh --apply
```

Targets (all >14 days old only):
1. Orchestration `harness*` worktrees
2. Project `worktree_*` dirs across all project dirs
3. `~/projects/worktree_*` and `orch_*` dirs
4. Home root `worktree_*`, `pr-*`, `wa-*` dirs
5. Actions-runner `.old-ws-*` and `ci-stale-*` dirs
6. `uv` cache, `.gemini/tmp`
7. Cursor worktrees
8. `/tmp` stale orchestration trees

### NEVER cleaned by script
- `~/.codex/sessions/` — Codex conversation history
- `~/.claude/` — Claude conversation/project data
- Git repos with no remote (check before manual deletion)
- Docker (requires daemon running)

## Manual Checklist (quarterly)

1. Run `df -h /` to check current usage
2. Run `./scripts/disk_cleanup.sh` to see recoverable space
3. Check `docker system prune -a` if Docker is running
4. Review `~/Library/Messages/Attachments/` (iMessage media, 23 GB)
5. Review `~/.nvm` for old Node versions (`nvm ls` then `nvm uninstall`)
6. Check `~/Library/Application Support/` for large app data (Claude 12G, Cursor 4.5G, Comet 3G)

## Learnings

### Key patterns that cause bloat
1. **Orchestration worktrees are the #1 offender** — pair-programming creates ~1 GB worktree per agent per session. 274 accumulated over weeks = 70 GB. Fix: default to `/tmp`.
2. **CI runners never clean up** — `.old-ws-*` and `ci-stale-*` accumulate silently as hidden dirs. 73 dirs = 80 GB. Need post-job cleanup in workflow or cron.
3. **Project dirs accumulate worktrees inside them** — `project_ai_universe` had 64 `worktree_*` subdirs from orchestration runs. Same pattern everywhere orchestration touches.
4. **Dev tool caches grow unbounded** — `uv` (18 GB), `npm` (4 GB), `puppeteer` (2.5 GB), `.claude/debug` (3.6 GB). All safe to nuke periodically.
5. **Old backups stick around** — `.claude.backup.*` dirs (2.6 GB), `.claude/projects.backup.*` (594 MB). Delete anything >30 days old.

### What NOT to delete
- `~/.codex/sessions/` — conversation history, irreplaceable
- `~/.claude/projects/` — conversation/project data, irreplaceable
- `~/.codex/state_5.sqlite` — can VACUUM but don't delete
- Any git repo checkout without confirming remote exists

### Quick diagnostic commands
```bash
# Overall status
df -h /

# What's eating home dir (top 15)
du -sh ~/* ~/.* 2>/dev/null | sort -rh | head -15

# Find dirs >1 GB older than 2 weeks
find ~ -maxdepth 2 -type d -mtime +14 -exec du -sh {} \; 2>/dev/null | awk '$1 ~ /G/' | sort -rh

# Count worktrees across all known locations
for d in ~/projects ~/project_*; do echo "$d:"; find "$d" -maxdepth 1 -name "worktree_*" 2>/dev/null | wc -l; done
```

## 2026-03-01 Cleanup Results

| Pass | What | Freed |
|------|------|-------|
| 1 | Harness worktrees (274 dirs) | 71 GB |
| 1 | Actions-runner `.old-ws-*` + `ci-stale-*` (204 dirs) | ~80 GB |
| 1 | `uv cache`, `.gemini/tmp`, `codex_fork` | 52 GB |
| 2 | `project_ai_universe*` worktrees (95 dirs) | ~55 GB |
| 2 | Stale `~/projects` dirs, home root worktrees | ~9 GB |
| 3 | `npm cache`, puppeteer, `.claude/debug`, old backups | ~13 GB |
| **Total** | | **~280 GB** |

**Disk: 99.2% (8 GB free) -> 69% (285 GB free)**
