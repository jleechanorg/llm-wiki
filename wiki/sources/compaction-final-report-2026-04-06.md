---
title: "Claude Code Compaction Research — Final Report 2026-04-06"
type: source
tags: [claude-code, compaction, context, hooks, optimization]
date: 2026-04-06
source_file: raw/compaction-final-report-2026-04-06.md
---

## Summary
Deep investigation into Claude Code auto-compaction at ~150K tokens on 1M context windows. Root causes identified: hardcoded threshold, per-turn overhead (~20K tokens/turn from skills/hooks/system-reminders), and environment variable interference. All workarounds found partial at best. Decision: upgrade to v2.1.92 for stability fixes, accept compaction as platform-wide issue.

## Key Claims
- Hardcoded 150K compaction threshold fires at ~15% of 1M window — designed for 200K context
- Per-turn overhead: ~300 skills (~15K), hooks (~4K), system-reminders = ~20K/turn minimum
- `CLAUDE_CODE_DISABLE_1M_CONTEXT=true` in ~/.bashrc was forcing 200K — removed
- PreCompact hook fires on v2.1.77 but only blocks ~2% of compactions (1/52 events)
- ALL terminal injection methods (tmux send-keys, cmux surface.send_text) bypass UserPromptSubmit hooks
- AO workers in tmux do NOT get hook-injected system-reminders
- Test sessions never hit compaction threshold because they lack real-session overhead
- Decision: upgrade to v2.1.92 (has thrash-loop fix, transcript chain fix, deferred tools schema fix, subagent tmux fix)

## Optimizations Applied
| Change | Impact |
|--------|--------|
| CLAUDE_CODE_DISABLE_1M_CONTEXT removed | Enables 1M context |
| 9 dead MCP servers removed | Faster startup |
| claude-commands marketplace uninstalled (165 skills) | ~8-10K tokens/turn saved |
| PreCompact hook installed | Blocks ~2% of compactions |
| Edit/Write permissions added globally | No permission dialogs |

## Connections
- [[ClaudeCode]] — target application, version upgrade decision
- [[Compaction]] — core issue: hardcoded threshold not respecting 1M context
- [[ClaudeCodeVersionStability]] — version analysis (v2.1.77 through v2.1.92)
- [[ContextBloat]] — per-turn overhead driver of compaction frequency
- [[HookSystem]] — PreCompact hook partial coverage finding
