---
title: "Claude Code Auto-Compaction Research — Root Cause & Fixes"
type: source
tags: [claude-code, context-compaction, tokens, performance, Claude-Code]
date: 2026-04-06
source_file: /Users/jleechan/Downloads/
---

## Summary

Claude Code's auto-compaction fires at ~150K tokens regardless of the 1M context window, causing aggressive context loss at ~15% utilization. Three compounding factors were identified: `CLAUDE_CODE_DISABLE_1M_CONTEXT=true` in bashrc, `--continue` inheriting old context config, and hardcoded threshold. Research attempted PreCompact hooks (partial coverage: ~2%), tmux/cmux send-keys (hooks bypass), MiniMax backend (no compaction), and version upgrades. Resolution involved removing the env var, trimming MCP servers and skills, and upgrading to v2.1.92.

## Root Causes

1. Hardcoded 150K compaction threshold — designed for 200K context windows
2. `CLAUDE_CODE_DISABLE_1M_CONTEXT=true` in `~/.bashrc` forced 200K window
3. `--continue` from old 200K session inherited old context config (v2.1.90 regression)
4. Per-turn overhead: ~300 skills (~15K tokens), hooks (~4K), system-reminders ≈ ~20K tokens/turn

## Key Findings

- PreCompact hook (exit code 2) fires on v2.1.77 but only blocks ~2% of compactions — multiple compaction code paths exist, hook covers only one
- ALL terminal injection methods (tmux send-keys, cmux surface.send_text, queue-operation) bypass Claude Code's input handler — hooks only fire on interactive UI prompt submission
- Main session: 52 compactions, 1 hook block, 229 user messages, 2.9 MB JSONL
- Test sessions: 0 compactions (lacked per-turn overhead that drives compaction)
- v2.1.89 added autocompact thrash loop detection (3x detection, stops after 3 consecutive refill-to-limit cycles)
- No version fully fixes the 150K threshold; #42590 remains open as enhancement request
- v2.1.90 `--continue -p` regression silently drops context (#43013) — workaround: `export CLAUDE_CODE_ENTRYPOINT=cli`

## Fixes Applied

| Change | Status | Impact |
|--------|--------|--------|
| `CLAUDE_CODE_DISABLE_1M_CONTEXT` removed from bashrc | Done | Enables 1M context |
| 9 dead MCP servers removed | Done | Faster startup |
| claude-commands marketplace uninstalled (165 skills) | Done | ~8-10K tokens/turn saved |
| PreCompact hook installed | Done | Blocks ~2% of compactions |
| Edit/Write permissions added globally | Done | Eliminates permission dialogs |
| Upgraded to v2.1.92 | Done | Thrash-loop fix, transcript chain fix, deferred tools schema fix |

## Key GitHub Issues

| Issue | Summary |
|-------|---------|
| #42590 | Context compaction too aggressive on 1M window (open, enhancement) |
| #40352 | Race condition destroys entire transcript on compaction failure (CRITICAL) |
| #42376 | --continue silently drops context (v2.1.90 regression) |
| #34202 | Threshold (150K) doesn't scale with 1M — fires at 15% |
| #42375 | Compaction at ~6% even with AUTOCOMPACT_PCT_OVERRIDE=95 |
| #42817 | ALL disable methods fail — Math.min() caps override |
| #43685 | `/compact [instructions]` does not actually trigger compaction (v2.1.92) |

## Connections

- [[ClaudeCode]] — compaction behavior is a Claude Code CLI issue
- [[ContextCompaction]] — existing wiki concept for context management
- [[AdaptiveContextTruncation]] — existing wiki concept

## Contradictions

- None identified
