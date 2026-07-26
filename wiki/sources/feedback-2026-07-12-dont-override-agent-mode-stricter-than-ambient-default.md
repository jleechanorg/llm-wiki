---
title: "Don't pass a stricter Agent() mode than the session's ambient permission default"
type: source
tags: [claude-code, agent-tool, permissions, parallelization]
date: 2026-07-12
source_file: raw/feedback_2026-07-12_dont-override-agent-mode-stricter-than-ambient-default.md
---

## Summary

Passing `mode: "acceptEdits"` to 10 parallel `Agent()` subagent calls caused a permission-prompt pileup and user-visible tool-use rejections, because the session's actual `permissions.defaultMode` was already `bypassPermissions` (fully permissive) — `acceptEdits` is a stricter override that only auto-accepts file-edit prompts, leaving Bash and other calls to prompt individually across all 10 parallel agents simultaneously.

## Key Claims

- Check the ambient `permissions.defaultMode` before passing an explicit `mode:` to `Agent()`.
- Never pass a stricter mode "just to be safe" — it silently reintroduces the friction the ambient config was set up to avoid.
- For missions needing guaranteed unattended execution (e.g. a durable sidekick), match or exceed ambient permissiveness at the process level (`--dangerously-skip-permissions`) rather than an intermediate mode.

## Connections

- [[FatCommandToThinSkillMigration]] — same migration session, root cause of user-reported friction.
