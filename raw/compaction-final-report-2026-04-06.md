# Claude Code Compaction Research — Final Report (2026-04-06)

## Problem
Auto-compaction fires at ~150K tokens regardless of 1M context window, causing aggressive context loss in interactive sessions.

## Root Causes
1. Hardcoded 150K compaction threshold (designed for 200K, not 1M)
2. Per-turn overhead: ~300 skills (~15K), hooks (~4K), system-reminders = ~20K/turn
3. CLAUDE_CODE_DISABLE_1M_CONTEXT=true was in ~/.bashrc (fixed)

## What We Tried

| Approach | Result |
|----------|--------|
| PreCompact hook (exit code 2) | Fires on v2.1.77 but only blocks ~2% (1/54 compactions) |
| tmux send-keys test sessions | Hooks don't fire — 0 system-reminders injected |
| cmux surface.send_text | Same as tmux — hooks don't fire |
| MiniMax backend sessions | No compaction (different context behavior) |
| --input-format stream-json | Requires API key auth (not OAuth/Max) |
| npx version A/B test | Couldn't trigger compaction — test sessions lack per-turn overhead |
| Amazon clone benchmark | Task completed before hitting threshold |

## Key Findings

### 1. Hooks bypass in programmatic input
ALL terminal injection methods (tmux send-keys, cmux surface.send_text, queue-operation) bypass Claude Code's input handler. UserPromptSubmit hooks only fire on primary prompt submission from the interactive UI. This means:
- AO workers in tmux don't get hook-injected system-reminders
- No scriptable A/B test can reproduce real-session compaction

### 2. PreCompact hook partial coverage
The PreCompact hook fires on v2.1.77 (contradicting initial "dead code" hypothesis) but only intercepts ~2% of compaction events. Multiple compaction code paths exist; the hook only covers one.

### 3. Per-turn overhead is the driver
Main session: 229 user messages, 22 system-reminders, 54 compactions, 2.9 MB JSONL
Test sessions: 86 user messages, 0 system-reminders, 0 compactions, 0.8 MB JSONL

## Optimizations Applied

| Change | Status | Impact |
|--------|--------|--------|
| CLAUDE_CODE_DISABLE_1M_CONTEXT removed | Done | Enables 1M context |
| 9 dead MCP servers removed | Done | Faster startup |
| claude-commands marketplace uninstalled (165 skills) | Done | ~8-10K tokens/turn saved |
| PreCompact hook installed | Done | Blocks ~2% of compactions |
| Edit/Write permissions added globally | Done | No more permission dialogs |
| cmux-steer skill updated for headless JSON API | Done | Cross-workspace sends work |

## Decision: Upgrade to v2.1.92

Cannot A/B test pre-upgrade. Evidence for upgrading:
- v2.1.92 has thrash-loop fix (v2.1.89), transcript chain fix (v2.1.91), deferred tools schema fix, subagent tmux fix
- No known regressions in v2.1.92 changelog
- Rollback: `npm install -g @anthropic-ai/claude-code@2.1.77`
- All optimizations (skills trim, MCP trim, hook) are version-independent

## Beads
- bd-tl9t: Compaction telemetry (open, updated with research)
- bd-cx01: PreCompact hook — partial coverage (open)
- bd-cx02: MCP trim — done
- bd-cx03: File upstream bug — open
- bd-cx04: Version eval — resolved (v2.1.92)
- bd-cx05: Upgrade to v2.1.92 — executing now
