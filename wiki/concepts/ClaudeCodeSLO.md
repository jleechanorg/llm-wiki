---
title: "Claude Code SLO and Compaction Settings"
type: concept
tags: [Claude-Code, Claude-Code-SLO, Claude-Code-v2, compaction]
last_updated: 2026-04-06
---

Claude Code v2.1.92 introduced GrowthBook experiments capping autocompact to 400K + SDK 100K threshold + time-based microcompact. DISABLE_AUTO_COMPACT=1 env var disables the main one.

## GrowthBook Experiments

Anthropic uses GrowthBook for server-side experiments that silently change behavior. Grep binary for S8() calls to discover new experiments. Example: `tengu_amber_redwood` caps autocompact to 400K.

## Compaction Bug (v2.1.77)

- v2.1.77 had 43 silent compaction bypasses
- Diagnosed via compact_boundary JSONL count (43 entries = bug)
- v2.1.92 shows 3/3 BLOCKED in hook log — upgrade resolves

## DISABLE_AUTO_COMPACT

DISABLE_AUTO_COMPACT=1 env var disables the main auto-compaction trigger. Binary analysis at `~/.local/bin/claude` is ground truth.

## Context: v2.1.92

v2.1.92 has GrowthBook experiment capping autocompact to 400K + SDK 100K threshold + time-based microcompact.

## Connections

- [[Compaction]] — existing compaction concept
- [[ContextCompaction]] — Claude Code compaction patterns
- [[ClaudeCodeAnalysis]] — Claude Code session analysis
