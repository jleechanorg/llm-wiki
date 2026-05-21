---
title: "Claude Code Compaction Bug"
type: concept
tags: [Claude-Code, compaction, bug, session, context]
last_updated: 2026-04-06
---

v2.1.77 had 43 silent compaction bypasses. v2.1.92 blocks reliably. After compaction, a session can confuse branches/PRs — always re-verify PR state with `gh` after compaction.

## Compaction Destroys PR Context

After compaction, a session confused branch `chore/evidence-theater-metadata` with merged PR #390. Session operated on wrong PR after compaction.

## 3 Independent Compaction Systems

1. **GrowthBook experiment** capping autocompact to 400K (server-side, silent)
2. **SDK 100K threshold** (client-side)
3. **Time-based microcompact** (client-side)

## DISABLE_AUTO_COMPACT

DISABLE_AUTO_COMPACT=1 env var disables the main auto-compaction trigger. Binary analysis at `~/.local/bin/claude` is ground truth.

## Diagnosis via JSONL

Count compact_boundary entries in session JSONL to diagnose lost history:
- 43 entries = v2.1.77 bug
- 3/3 BLOCKED = v2.1.92 fixed

## WaferFixPatcher Lean-Body Thrash (2026-05-14)

When `lean` or `lean,on-demand` proxy mode is active, the llm-inspector
`WaferFixPatcher` must estimate from `rawRequestBody` (pre-lean), not
`forwardBody` (post-lean). Lean mode removes tool schemas (60–80% of body),
so estimating from the lean body causes Claude Code to see artificially low
`input_tokens` and delay compaction until context is truly full. The oversized
compact summary immediately re-fills the context → 3-cycle thrash in `claudew()`
sessions. Fix: `src/proxy.ts:480` — use `rawRequestBody.length`.

See: `sources/wafer-fix-lean-body-underestimate.md`

## Connections

- [[ClaudeCodeSLO]] — Claude Code SLO and GrowthBook experiments
- [[ClaudeCodeFSCache]] — Claude Code FSCache bug
- [[ContextCompaction]] — existing compaction concept
