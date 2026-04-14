---
title: "Asyncio Orchestration Migration"
type: concept
tags: [architecture, asyncio, tmux-replacement]
sources: []
last_updated: 2026-02-24
---

## Definition

The Asyncio Orchestration Migration is a multi-phase refactor that replaces tmux process isolation and LangGraph state management with native asyncio primitives. The goal is to reduce abstraction overhead (LangGraph is a thin veneer over a 130-line state machine) and eliminate unnecessary dependencies.

## Problem

pair_execute_v2.py uses:
- **tmux** (31% of code): unnecessary since agents are fire-and-forget CLI processes — no terminal attachment needed
- **LangGraph StateGraph** (7% of code): thin routing layer; a 130-line `_FallbackCompiledGraph` re-implements the runtime for CI
- **SqliteSaver checkpointing**: non-idempotent side effects (tmux launches, file writes)
- **`batch()` fan-out**: unused Send() API

## Design Decision

Multi-model consensus (Cerebras/Qwen 3, Grok 4 Fast, Perplexity Sonar Pro) recommends:
- Replace tmux with `asyncio.create_subprocess_exec()`
- Replace LangGraph with asyncio state machine (~150 LOC)
- Replace SqliteSaver with idempotent SQLite checkpoint table (~20 LOC)
- Replace `batch()` fan-out with `asyncio.TaskGroup`

## Phases

1. **Phase 1**: Add `no_tmux` parameter to TaskDispatcher — launch via subprocess.Popen
2. **Phase 2**: asyncio state machine replacing LangGraph
3. **Phase 3**: Idempotent checkpoint/resume via "completed_steps" table
4. **Phase 4**: asyncio TaskGroup for fan-out

## Sources

- EPIC-asyncio-orchestration-migration: full epic description
