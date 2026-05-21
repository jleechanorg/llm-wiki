---
title: "/ms Skill Forbidden Patterns Cause Autocompact Thrash Loop"
type: source
tags: [memory-search, autocompact, thrash, beads, jsonl, wafer, compaction, /ms]
raw: raw/feedback_2026-05-14_ms-skill-forbidden-patterns-thrash.md
date: 2026-05-14
---

## Summary

The `/ms` (memory-search) skill has two embedded forbidden patterns that cause autocompact thrashing loops in wafer (GLM-5.1) sessions. Fixed in `~/.claude/skills/memory-search/SKILL.md` on 2026-05-14.

## Forbidden Patterns

### Step 2 — Beads (raw JSONL read)
```
/e Search beads for "$QUERY". Check ... and .beads/issues.jsonl.
```
`.beads/issues.jsonl` is 1MB+ in worldarchitect.ai — reading it raw floods context.

### Step 9 — History (`grep -H`)
```bash
grep -H "$QUERY" ~/.claude/projects/*/*.jsonl 2>/dev/null | head -20
```
`grep -H` reads **full content** of all session JSONL files (large conversation transcripts). `head -20` limits output but the shell reads the full file to find matches.

## Thrash Mechanism

1. Session compacts (context overflow or threshold)
2. Session invokes `/ms` to re-orient (understand what it was doing)
3. 9 parallel subagents run; aggregated results flood back into outer session context
4. `.beads/issues.jsonl` content (1MB+) + JSONL file content refills context within 3 turns
5. Compact fires again → `/ms` again → 3 consecutive cycles → "Autocompact is thrashing" error

## Fix Applied

**Beads step** (new):
```
/e Search beads for "$QUERY" using: br search "$QUERY" --json 2>/dev/null | head -40.
NEVER read .beads/issues.jsonl directly — 1MB+ and forbidden.
```

**History step** (new):
```
/e Search using FILENAMES ONLY: grep -rl "$QUERY" ~/.claude/projects/*/*.jsonl | head -5.
DO NOT use grep -H (reads full content).
```

## Evidence

- Session: `claudewc` in `~/projects/worktree_runner4` (worldarchitect.ai, branch `prod-slim-system-instructions`, PR [#6902](https://github.com/jleechanorg/worldarchitect.ai/pull/6902))
- `/ms` invoked 3× consecutively post-compaction (matching 3-cycle thrash pattern)
- Context at 80%+ with "0% until auto-compact" before each cycle
- Date: 2026-05-14

## Related Concepts

- [[Compaction]] — autocompact thrash triggers, WaferFixPatcher scope
- [[MemorySearch]] — /ms skill architecture
- [[conflict-resolution-large-file-thrash]] — same thrash category, different trigger
- [[WaferFixSSEPatcher]] — fixes false compact trigger only, not genuine overflow
