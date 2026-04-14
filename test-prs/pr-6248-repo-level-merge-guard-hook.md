---
title: "PR #6248: [agento] fix(harness): add repo-level merge guard hook"
type: test-pr
date: 2026-04-14
pr_number: 6248
files_changed: [block-merge.sh, settings.json, CLAUDE.md, PR-6248.md]
---

## Summary
Adds a repo-level PreToolUse hook (`.claude/hooks/block-merge.sh`) that intercepts `gh pr merge` commands and requires explicit human `MERGE APPROVED` before any merge. Wires the hook into `.claude/settings.json` and updates CLAUDE.md to reference the enforced merge policy.

## Key Changes
- **block-merge.sh**: New executable Bash script that reads JSON from stdin, detects `gh pr merge` / REST API merge calls, writes BLOCKED message to stderr, returns `hookSpecificOutput {permissionDecision: deny}` JSON
- **settings.json**: Adds conditional `exec $ROOT/.claude/hooks/block-merge.sh` in PreToolUse Bash hooks array
- **CLAUDE.md**: Updated merge prohibition to clarify it applies to any agent, not just `/polish` loop

## Motivation
Prevents accidental merges by agents. The hook only fires for Claude Code CLI sessions - manual `gh pr merge` from terminal is unaffected.