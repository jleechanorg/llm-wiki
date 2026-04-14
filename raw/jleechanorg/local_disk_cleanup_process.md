# Local Disk Cleanup Process

This document records the local cleanup process used on `2026-02-19` and provides a repeatable script.

## What We Clean

The cleanup focuses on local AI tooling artifacts and large transient caches:

- `~/.cursor/worktrees`
- `~/.cursor/chats`
- `~/.claude/debug`
- `~/.config/superpowers/worktrees`
- `~/Library/Caches/com.todesktop.230313mzl4w4u92.ShipIt`
- `~/Library/Caches/com.google.antigravity.ShipIt`
- `~/Library/Caches/ms-playwright`
- `~/Library/Caches/ms-playwright-go`
- `~/Library/Caches/pip`

## Script

Use:

```bash
scripts/cleanup_local_agent_artifacts.sh --dry-run
scripts/cleanup_local_agent_artifacts.sh
```

The script intentionally uses `find ... -delete` rather than `rm -rf` to be friendlier with stricter execution policies.

## Notes

- Some cache directories may be recreated automatically by tools after cleanup.
- `~/.claude/debug` contains debug traces/log artifacts and is safe to clear.
- This process does **not** remove project worktrees under `~/projects/worktree_*` unless those are explicitly added as targets.

## Verify Reclaim

```bash
du -sh ~/.cursor ~/.claude ~/.codex ~/Library/Caches
```

For target-specific checks:

```bash
du -sh ~/.cursor/worktrees ~/.cursor/chats ~/.claude/debug ~/.config/superpowers/worktrees \
  ~/Library/Caches/com.todesktop.230313mzl4w4u92.ShipIt \
  ~/Library/Caches/com.google.antigravity.ShipIt \
  ~/Library/Caches/ms-playwright ~/Library/Caches/ms-playwright-go ~/Library/Caches/pip
```
