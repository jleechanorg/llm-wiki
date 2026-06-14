---
title: "Claude-Multi-Account-Setup"
type: source
tags: [project, memory-file]
date: 2026-06-13
source_file: raw/memory_backfill_2026_06_13/claude-multi-account-setup.md
---

## Summary

Two Claude Code accounts coexist via (set up 2026-05-30): → personal . Config lives at (home dir, NOT ) + dir. OAuth token in keychain entry (no suffix).

## Key Claims

- **Default `claude` / `clauded` / etc.** → personal `jleechan@gmail.com`. Config lives at `~/.claude.json` (home dir, NOT `~/.claude/.claude.json`) + `~/.claude/` dir. OAuth token in keychain entry `Claude Code-credentials` (no suffix).
- **`claudeaf` / `claudeafc`** → enterprise `jeffrey@agent-f.com` (org Agent-F, team_standard). `claudeaf` = `CLAUDE_CONFIG_DIR=~/.claude-agent-f claude --dangerously-skip-permissions --chrome --model sonnet --teammate-mode=tmux`; `claudeafc` = `claudeaf --continue`. Config at `~/.claude-agent-f/.claude.json`. OAuth token in a *hash-suffixed* keychain entry (e.g. `Claude Code-credentials-a5083ba3`).
- Claude Code namespaces keychain credentials per config dir, so accounts don't collide.
- The personal `~/.claude.json` is the live source of truth and is newer than the `user_scope` repo backups (`projects_other/user_scope/backup/Mac/claude.json`). Don't restore from backup unless the live file is actually corrupt — it would regress recent project state.
- Aliases defined in `~/.bashrc` near line 634 (alongside existing `claude2` two-account pattern).

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
