---
title: "Runtime Mirror Install (Stable-Path Scripts)"
type: concept
tags: [self-hosted-runners, install, scripts, infrastructure, pattern]
date: 2026-06-23
last_updated: 2026-06-23
---

## Runtime Mirror Install Pattern

Convention for self-hosted runner hook scripts: **scripts live in the repo as source, but run from a stable installed path on disk**, not from the repo's checked-out branch.

### Why

A hook script installed via bind-mount from `./scripts/pre-job-hook.sh` breaks whenever the worktree branch is switched, deleted, or merged. A hook installed at `~/.local/share/<fleet>-runners/pre-job-hook.sh` survives all of that.

### Convention (per fleet)

| Fleet | Install dir | Source of truth |
|-------|-------------|-----------------|
| mac (`self-hosted-oss`) | `~/.local/share/worldarchitect-runners/` | `RUNTIME_SCRIPTS` array in `self-hosted-oss/install.sh` |
| Linux colima (`self-hosted-colima`) | `~/.local/share/worldarchitect-colima-runners/` | `HOOK_INSTALL_DIR` + explicit `cp` in `self-hosted-colima/install.sh` |

### install.sh pattern

```bash
HOOK_INSTALL_DIR="$HOME/.local/share/worldarchitect-colima-runners"
log "Installing hook scripts to $HOOK_INSTALL_DIR ..."
mkdir -p "$HOOK_INSTALL_DIR"
cp "$STACK_DIR/scripts/pre-job-hook.sh" "$HOOK_INSTALL_DIR/pre-job-hook.sh"
cp "$STACK_DIR/scripts/lima-watchdog.sh" "$HOOK_INSTALL_DIR/lima-watchdog.sh"
chmod +x "$HOOK_INSTALL_DIR/pre-job-hook.sh" "$HOOK_INSTALL_DIR/lima-watchdog.sh"
```

The bind-mount in `docker-compose.yml` then references the stable path:

```yaml
volumes:
  - ${HOME}/.local/share/worldarchitect-colima-runners/pre-job-hook.sh:/usr/local/bin/pre-job-hook.sh:ro
```

### Why the runtime mirror is NOT the source

`launchd` runs scripts out of `~/.local/share/worldarchitect-runners/`. That directory is a **runtime mirror** populated by `self-hosted-oss/install.sh`'s `RUNTIME_SCRIPTS` array from `self-hosted-oss/*.sh` in the repo. Direct Edit/Write on the mirror is blocked by a user-scope PreToolUse hook (`~/.claude/hooks/block-runtime-mirror-edits.sh`).

**Always edit the repo source** (`self-hosted-colima/scripts/lima-watchdog.sh`) **and re-run install.sh** — never edit the installed copy directly.

### Critical-bug history

PR #7831 (Linux colima) was squash-merged at commit `0794779451` *before* the stable-path redesign was pushed at `b2c58658cd`. The result: main was left with the fragile repo-relative bind mount `./scripts/pre-job-hook.sh:/usr/local/bin/pre-job-hook.sh:ro`. PR #7834 (`fix/colima-runner-hook-stable-path`) shipped the stable-path fix. Lesson: the redesign must land in the SAME PR as the original hook install — don't split "ship it" from "ship it the right way" across two PRs.

### References

- [[LimaVM]] (uses this pattern for hook install)
- [[SelfHostedRunners]] (all hook scripts use this pattern)
- [[LimaWatchdog]] (uses stable path: `~/.local/share/worldarchitect-colima-runners/lima-watchdog.sh`)
- PR #7831 → #7834 (the stable-path fix)
- PR #7843 (added lima-watchdog.sh via install.sh stable-path)
