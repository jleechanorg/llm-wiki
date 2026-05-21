---
name: conflict-resolution-large-file-thrash
description: Conflict resolution reads full conflicted files → genuine context overflow → thrash loop even when WaferFixPatcher is active
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: f6c08ed2-9a66-45b2-9ecb-2784de0ecba6
---

## Rule

During cherry-pick or merge conflict resolution, **never `Read` the full conflicted file**. Use `grep` to locate conflict markers, then read only the conflict region with `offset`/`limit`. Use `git show <sha> -- <file>` to understand what upstream changed without loading the full blob.

**Why**: WaferFixPatcher patches the *false* compact trigger (`input_tokens:0` from GLM-5.1), but it cannot stop *genuine* context overflow from bulk reads. A 400-line file read fills significant context. During conflict resolution the agent re-reads the same large files after every compaction to continue its work → context refills within 3 turns → compact fires again → infinite loop.

**How to apply**: In any session doing cherry-pick or merge integration work:
1. `grep -n "<<<<<<\|=======\|>>>>>>>" <file>` — locate conflict line numbers without loading the file
2. `Read <file> offset:<N> limit:<30>` — read only the ±15 lines around the conflict
3. `git show <upstream-sha> -- <file>` — see only what the upstream commit changed, not the full conflicted blob
4. Work one conflict at a time; do not read all conflicted files up front

## Context

Session in `~/project_agento/worktree_upstream2` using `claudewc` (GLM-5.1 via port 9001 wafer proxy) was doing upstream cherry-pick integration of 50 commits into `feat/upstream-integration-may2026`. The session was reading:
- `useXtermTerminal.ts` — 425 lines (full read)
- `mux-websocket.ts` — large (full read, multiple times)
- `tmux-utils.ts` — 208 lines (full read)
- 5+ other large conflicted files during the same pass

The `Autocompact is thrashing` error appeared after 32 minutes. Context status showed `75%` before the fatal compact cycle.

## WaferFixPatcher scope limitation

`WaferFixPatcher` (`llm_inspector/src/filters.ts`) patches `"input_tokens":0` → `Math.round(bodyBytes/4)` in SSE `message_start`. This stops Claude Code from blind-tracking (thinking context was just cleared when it wasn't). It does NOT reduce actual context consumption from large tool outputs. Both fixes are required:

| Root cause | Fix | Status |
|---|---|---|
| `input_tokens:0` false reading | WaferFixPatcher | ✓ deployed |
| Unguarded large file reads | grep-first + offset/limit discipline | ⚠ must be applied manually |

## Reusable Pattern

```bash
# Step 1: Find all conflicted files
git diff --name-only --diff-filter=U

# Step 2: For each file, find conflict line numbers (not full content)
grep -n "<<<<<<\|=======\|>>>>>>>" packages/web/server/tmux-utils.ts
# → line 45: <<<<<<<, line 52: =======, line 61: >>>>>>>

# Step 3: Read only that region
# Read tool: file_path=..., offset=40, limit=30

# Step 4: Understand upstream's intent without reading the conflicted blob
git show b2cdf7ada -- packages/web/server/tmux-utils.ts
# Shows only the diff the upstream commit introduced
```

## Verification

The session thrashed 3× in a row and emitted "Autocompact is thrashing: context refilled to limit within 3 turns of previous compact, 3 times in a row." This matches the pattern in `Compaction.md` under "Known thrash trigger: unguarded large file reads."

## References

- `~/llm_wiki/wiki/concepts/Compaction.md` — known thrash triggers
- `llm_inspector/src/filters.ts` — `WaferFixPatcher` (patches only `input_tokens:0`)
- Session: `claudewc` in `~/project_agento/worktree_upstream2` on 2026-05-14
- Related: [[wafer-sse-input-tokens-zero-fix-2026-05-14]], [[Compaction]]
