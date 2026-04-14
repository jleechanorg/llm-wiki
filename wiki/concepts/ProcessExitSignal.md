---
title: "Process Exit Signal"
type: concept
tags: [pairv2, task-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The process exit signal pattern uses tmux session death as the primary completion indicator for agent workflows. Signal files are treated as optional hints, not gates. The key insight: trust process exit over file existence.

## Why It Matters

MiniMax coder wrote IMPLEMENTATION_READY to the wrong path despite artifact contract containing correct absolute path. Strict file-path gating is fragile with weaker models. Process exit is a more reliable signal of completion.

## Key Technical Details

- **Primary signal**: tmux session termination (process exit)
- **Secondary signals**: Signal files are optional best-effort hints
- **Fallback**: Verifier uses LLM inference when reports are missing
- **Scope**: `.claude/pair/pair_execute_v2.py`

## Related Beads

- BD-pairv2-flatten-session-dir (renamed to LLM-recoverable workflow)
- LLMRecoverableWorkflow (concept)
