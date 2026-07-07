---
title: "Claude Code dual-profile setup (claudewa) — CLAUDE_CONFIG_DIR, ToS, backup"
type: source
tags: [claude-code, claude-wa, CLAUDE_CONFIG_DIR, user-scope, backup]
date: 2026-07-06
source_file: raw/feedback_2026-07-06_claude_wa_dual_profile_setup.md
bead: jleechan-skk
---

## Summary

Canonical pattern for personal Gmail (~/.claude) and WorldArchitect (~/.claude-wa) Claude Code on one machine: separate OAuth via CLAUDE_CONFIG_DIR, selective symlinks for tooling and projects/, mutually exclusive GitHub repos, backup-home.sh for WA-local state.

## Key Claims

- Do not share entire ~/.claude — collapses OAuth. Symlink skills/hooks/settings/projects; keep auth and sessions local.
- claudewa / claudewac on Mac and jeff-ubuntu; installer at user_scope/scripts/install-claude-wa-profile.sh.
- Mutually exclusive repos: WA → claudewa; personal → clauded.
- ToS: no public ban anecdotes for dual paid Max + CLAUDE_CONFIG_DIR (GitHub #43911, #49972).
- Backup: ~/.claude/projects/ + ~/.claude-wa/ → claude/claude-wa/.

## Connections

- [[ClaudeCodeDualProfile]]

Jeffrey oracle: NO
