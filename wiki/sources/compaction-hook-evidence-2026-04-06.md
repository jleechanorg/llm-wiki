---
title: "PreCompact Hook Evidence — 2026-04-06"
type: source
tags: [claude-code, compaction, hooks, evidence]
date: 2026-04-06
source_file: raw/compaction-hook-evidence-2026-04-06.md
---

## Summary
Evidence confirming the PreCompact hook fires on Claude Code v2.1.77 but only intercepts ~2% of compaction events. The hook's 4 invocations in the main session (52 compactions) show it only blocks interactive guard compactions, not AO worker compactions.

## Key Claims
- PreCompact hook EXISTS and fires on v2.1.77 (contradicts earlier "dead code" hypothesis)
- Hook fired 4 times across 52 compaction events: 1 BLOCKED (interactive guard), 3 ALLOWED (AO workers)
- Hook only intercepts ~2% of compactions — most bypass the hook entirely
- Multiple compaction code paths likely exist; hook only covers one
- Test sessions (v2.1.77 and v2.1.92) never triggered compaction — lack real-session per-turn overhead
- Test sessions don't have 300 skill descriptions, hook outputs, or system-reminders that drive main session overhead

## Key Quotes
> "ALLOWED compaction (AO worker / headless)" — 3 entries
> "BLOCKED auto-compaction (interactive guard)" — 1 entry

## Connections
- [[Compaction]] — partial PreCompact hook coverage limits its effectiveness
- [[HookSystem]] — hook bypass in programmatic/input contexts
- [[ClaudeCode]] — v2.1.77 PreCompact behavior
- [[AgentOrchestrator]] — AO workers bypass PreCompact hook
