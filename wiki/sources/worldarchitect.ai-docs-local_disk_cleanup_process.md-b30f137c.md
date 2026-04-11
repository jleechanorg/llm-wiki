---
title: "Local Disk Cleanup Process"
type: source
tags: [cleanup, disk-space, automation, ai-tools, caching]
sources: []
date: 2026-04-07
last_updated: 2026-04-07
---

## Summary
Documents the local cleanup process for AI tooling artifacts and caches, executed on 2026-02-19. Provides a repeatable script that targets transient caches from Cursor, Claude Code, Superpowers, Playwright, and pip to reclaim disk space.

## Key Claims
- **Cleanup targets**: Cursor worktrees/chats, Claude debug traces, Superpowers worktrees, ShipIt caches, Playwright caches, pip caches
- **Script method**: Uses `find ... -delete` instead of `rm -rf` for stricter execution policy compatibility
- **Safe to clear**: `~/.claude/debug` contains debug traces/log artifacts, safe to delete
- **Preserves project worktrees**: Does NOT remove `~/projects/worktree_*` unless explicitly added
- **Auto-recreation**: Some cache directories may be automatically recreated by tools after cleanup

## Key Targets
- `~/.cursor/worktrees`, `~/.cursor/chats`
- `~/.claude/debug`
- `~/.config/superpowers/worktrees`
- `~/Library/Caches/com.todesktop.230313mzl4w4u92.ShipIt`
- `~/Library/Caches/com.google.antigravity.ShipIt`
- `~/Library/Caches/ms-playwright`, `~/Library/Caches/ms-playwright-go`
- `~/Library/Caches/pip`

## Usage
```bash
scripts/cleanup_local_agent_artifacts.sh --dry-run
scripts/cleanup_local_agent_artifacts.sh
```

## Verification Commands
```bash
du -sh ~/.cursor ~/.claude ~/.codex ~/Library/Caches
```

## Connections
- [[OpenClaw Setup Guide]] — similar automation scripts for AI tooling
- [[Cursor]] — one of the cleanup targets
- [[Claude Code]] — debug directory is a cleanup target

## Contradictions