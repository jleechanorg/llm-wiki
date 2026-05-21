---
title: "Conflict Resolution Large File Reads Cause Genuine Autocompact Thrash"
type: source
tags: [compaction, autocompact, conflict-resolution, cherry-pick, wafer, thrash, context-overflow]
raw: raw/feedback_2026-05-14_conflict-resolution-large-file-thrash.md
date: 2026-05-14
---

## Summary

During upstream cherry-pick integration in `~/project_agento/worktree_upstream2` (`claudewc`, GLM-5.1), the session thrashed because conflict resolution read full 400+ line files. `WaferFixPatcher` patches the *false* compact trigger (`input_tokens:0`) but cannot stop *genuine* context overflow from unguarded large reads. Both fixes are required independently.

## Root Cause

`WaferFixPatcher` scope: patches `"input_tokens":0` → estimated byte count in SSE `message_start`. This stops blind tracking. It does NOT reduce actual context tokens consumed from tool output.

Large conflicted files read in full:
- `useXtermTerminal.ts` — 425 lines
- `mux-websocket.ts` — large, read multiple times
- `tmux-utils.ts` — 208 lines
- 5+ other files in a single pass

After compaction the agent re-reads the same files → context refills within 3 turns → compact fires again.

## The Fix

```bash
# Step 1: Find conflict line numbers without loading content
grep -n "<<<<<<\|=======\|>>>>>>>" packages/web/server/tmux-utils.ts

# Step 2: Read only the conflict region (e.g. markers at lines 45/52/61)
# Read tool: offset=40, limit=30

# Step 3: See what upstream changed without reading the full conflicted blob
git show b2cdf7ada -- packages/web/server/tmux-utils.ts
```

Work one conflict at a time. Do not read all conflicted files up front.

## WaferFixPatcher vs Genuine Overflow

| Root cause | Fix | Status |
|---|---|---|
| `input_tokens:0` false reading | WaferFixPatcher (llm_inspector/src/filters.ts) | ✓ deployed |
| Unguarded large file reads | grep-first + offset/limit discipline | manual |

## Evidence

- "Autocompact is thrashing: context refilled to limit within 3 turns of previous compact, 3 times in a row" — after 32 minutes in `worktree_upstream2`
- Context at 75% before fatal compact cycle
- Session: `claudewc` 2026-05-14

## Related Concepts

- [[Compaction]] — known thrash triggers section updated
- [[WaferFixSSEPatcher]] — scope: false trigger only
- [[beads-issues-jsonl-read-without-offset-wafer-thrash]] — same root cause category
