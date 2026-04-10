---
title: "Hook Bypass"
type: concept
tags: [claude-code, hooks, bypass, automation, context]
sources: [compaction-final-report-2026-04-06, compaction-hook-evidence-2026-04-06]
last_updated: 2026-04-06
---

## Summary
ALL terminal injection methods (tmux send-keys, cmux surface.send_text, queue-operation) bypass Claude Code's UserPromptSubmit hook input handler. Hooks only fire on primary prompt submission from the interactive UI, meaning AO workers in tmux sessions do not receive hook-injected system reminders.

## Key Claims
- tmux send-keys bypasses UserPromptSubmit hooks — 0 system-reminders injected in AO worker sessions
- cmux surface.send_text has the same bypass behavior
- UserPromptSubmit hooks only fire on primary interactive UI prompt submission
- This makes scriptable A/B tests impossible for reproducing real-session compaction behavior
- PreCompact hook partial coverage (2%) is also a bypass issue — most compaction events don't check hooks

## Why This Matters
Claude Code hooks are designed for interactive sessions. When Claude Code is driven programmatically (via tmux, cmux, API, etc.), the hook system is bypassed, creating a gap between interactive behavior and headless/automated behavior.

## Connections
- [[HookSystem]] — Claude Code hook system
- [[Compaction]] — PreCompact hook bypass means ~98% of compactions aren't intercepted
- [[ClaudeCode]] — hook bypass in programmatic contexts
- [[AgentOrchestrator]] — AO workers run in tmux, bypass hooks
