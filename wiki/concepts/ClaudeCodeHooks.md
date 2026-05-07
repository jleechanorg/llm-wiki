---
title: "Claude Code Hooks"
type: concept
tags: [claude-code, hooks, configuration]
sources: [tdd-tests-claude-settings-hook-validation]
last_updated: 2026-04-08
---

Hooks in Claude Code are event-based triggers configured in `.claude/settings.json`. They can run on events like PreToolUse, PostToolUse, Stop, and UserPromptSubmit. The hook configuration includes a command and description. Robust hook patterns are required to prevent system lockouts when environment variables like `$ROOT` are undefined.

## Cost impact

PostToolUse hooks that spawn Claude sessions multiply quota cost: each Write operation fires all `Write` hooks, creating a new Claude session per hook. At 50 Write ops/session with $0.89/hook session = $44.50 overhead per interactive session. Three hooks (`detect_speculation_and_fake_code.sh`, `smart_fake_code_detection.sh`, `post_file_creation_validator.sh`) consumed ~$86/day before being disabled 2026-05-06.

See also: [[HookRobustnessPatterns]] · [[ClaudeCodeQuotaCost]]
