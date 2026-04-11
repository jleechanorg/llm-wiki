---
title: "Claude Code Auto-Compaction Research — 2026-04-05"
type: source
tags: [claude-code, compaction, context, research]
date: 2026-04-05
source_file: raw/context-compaction-research-2026-04-05.md
---

## Summary
Early-stage research into Claude Code compaction behavior. Identifies three compounding factors: `CLAUDE_CODE_DISABLE_1M_CONTEXT=true` in bashrc forcing 200K window, `--continue` from old session inheriting wrong config, and hardcoded ~150K threshold firing at 15% of 1M. Documents per-turn overhead at ~45K minimum before any conversation. Key GitHub issues catalogued.

## Key Claims
- Compaction threshold (~150K) was designed for 200K windows — fires at ~15% of 1M window
- `CLAUDE_CODE_DISABLE_1M_CONTEXT=true` in bashrc forced 200K window — removed
- `--continue` from old 200K session inherits wrong config (confirmed v2.1.90 regression #42376)
- Per-turn system-reminder overhead: ~19K (skills, deferred tools, hooks, MCP)
- MCP overhead: 186 tools = 99.8K tokens on 200K window
- Removable MCP savings: ~27K (Notion 8K, Playwright 12K, Puppeteer 3K, React 4K)
- Apr 4-5: 147 compact_boundary events vs Mar 21-22: 38 (3.9x increase) — normalized: 0.29 per 100 user msgs
- PreCompact hook (exit code 2) community workaround: blocks compaction but coverage is partial

## Key GitHub Issues
| Issue | Summary |
|-------|---------|
| #34202 | Threshold doesn't scale with 1M — fires at 15% |
| #42375 | Compaction at ~6% even with AUTOCOMPACT_PCT_OVERRIDE=95 |
| #42817 | ALL disable methods fail — Math.min() caps override |
| #40352 | CRITICAL: Race condition destroys entire transcript |
| #6689 | Feature request for --no-auto-compact (open since Aug 2025) |

## Connections
- [[Compaction]] — root cause analysis, hardcoded threshold
- [[ClaudeCode]] — affected application
- [[ContextBloat]] — per-turn overhead driver
- [[ClaudeCodeVersionStability]] — version-specific compaction behavior
- [[HookSystem]] — PreCompact hook community workaround
