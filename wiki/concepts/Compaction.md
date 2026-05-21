---
title: "Compaction"
type: concept
tags: ["memory", "context", "optimization"]
sources: ["genesis-persistent-orchestration-layer-openclaw"]
last_updated: 2026-04-07
---

OpenClaw's memory management system that handles context window limits.

## Memory Flush
- **Enabled by default**: Reminds agent to persist important context before session context window fills
- **Trigger**: When context approaches limit
- **Action**: Agent must save important context to persistent memory files

## Purpose
Prevents context loss by proactively prompting the agent to:
1. Save important decisions to MEMORY.md
2. Update USER.md with new preferences discovered
3. Log significant session events to daily notes

## Related Concepts
- [[MemorySearch]] — retrieval system
- [[Memory System]] — storage layer

## Known thrash trigger: unguarded large file reads

`.beads/issues.jsonl` (1MB+) read without `offset`/`limit` in a GLM-5.1 (wafer) session was confirmed as a root cause of the compact→refill→compact loop. Evidence: session `c03c7cd8` in `worktree-location-freeze` project, 2026-05-13. Rule: always `grep` by bead ID or use `offset`/`limit`. See [[beads-issues-jsonl-read-without-offset-wafer-thrash]].

## Known thrash trigger: provider returns input_tokens:0 in SSE message_start

GLM-5.1 (wafer) always returns `"input_tokens":0` in `message_start`. Claude Code treats `0` as "context was just cleared", so the real context (~70K tokens) refills within 3 turns → autocompact fires → `0` again → infinite loop. Fix: `WaferFixPatcher` in llm-inspector proxy patches `0` → `Math.round(bodyBytes / 4)` before the response reaches Claude Code. See [[wafer-sse-input-tokens-zero-fix-2026-05-14]].

## Correct bead access pattern: use br CLI, never read .beads/*.jsonl

`beads.db` (SQLite, 5.7MB) is the primary store. `br show <id>`, `br search <term>`, and `br list --json` query it directly without touching any JSONL file. Two files must never be Read:

- `.beads/issues.jsonl` — 1.0MB, 1,239 records
- `.beads/beads.left.jsonl` — **5.0MB, 15,447 lines**, git-tracked legacy export (5× more dangerous)

Compaction cannot be automated via `br sync --flush-only` because it re-exports the full DB including closed beads. A custom script filtering open-only beads would reduce issues.jsonl from 1.0MB to ~620KB, but is not yet implemented. See [[br-cli-bead-access-pattern-2026-05-14]].

## context-mode mitigation: fills Read-tool blind spot

RTK (`rtk` prefix) intercepts Bash commands to reduce token output, but the built-in `Read` tool bypasses RTK entirely. `context-mode` (PostToolUse/PreCompact/SessionStart hooks) intercepts ALL tool results — including `Read` — and stores them in FTS5 SQLite, returning summaries to the LLM. Wired 2026-05-14 into all 3 runtimes (Claude Code, claudew, Codex). See [[context-mode-wired-all-runtimes-2026-05-14]].

## Known thrash trigger: conflict resolution reads during cherry-pick/merge

During upstream integration work (cherry-pick of 50 commits), `claudewc` (GLM-5.1) thrashed because conflict resolution read full files (425-line `useXtermTerminal.ts`, large `mux-websocket.ts`, etc.). `WaferFixPatcher` patches the *false* trigger (`input_tokens:0`) but cannot stop *genuine* overflow from bulk reads. Both are required to stop thrashing.

**Required discipline for conflict resolution:**
```bash
# 1. Find conflict line numbers without loading the file
grep -n "<<<<<<\|=======\|>>>>>>>" <conflicted-file>

# 2. Read only the conflict region
# Read tool: offset=<marker_line - 5>, limit=30

# 3. Understand upstream changes without the conflicted blob
git show <upstream-sha> -- <file>
```

Evidence: session `claudewc` `~/project_agento/worktree_upstream2`, 2026-05-14, 32min run, "Autocompact is thrashing" after 3 consecutive compact→refill cycles at 75% context. See [[conflict-resolution-large-file-thrash]].
