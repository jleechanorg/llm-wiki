# EPIC-asyncio-orchestration-migration

## ID
EPIC-asyncio-orchestration-migration

## Title
Replace tmux + LangGraph with asyncio orchestration

## Status
open

## Type
epic

## Priority
high

## Created
2026-02-24

## Problem Statement
pair_execute_v2.py (4160 lines) uses LangGraph StateGraph as a thin routing layer (7% of code)
and tmux for process isolation (31% of code). Multi-model consensus (Cerebras/Qwen 3, Grok 4 Fast,
Perplexity Sonar Pro) identifies fundamental abstraction mismatches:

1. **tmux is unnecessary** — agents are fire-and-forget CLI processes; we never attach to terminals
2. **LangGraph is a thin veneer** — a 130-line `_FallbackCompiledGraph` reimplements the runtime for CI
3. **SqliteSaver checkpointing is broken** — non-idempotent side effects (tmux launches, file writes)
4. **Send() API unused** — fan-out uses `batch()` instead of native parallel branches

## Design Decision
Multi-model second opinion (via AI Universe MCP server) unanimously recommends:
- Replace tmux with `asyncio.create_subprocess_exec()`
- Replace LangGraph with asyncio state machine (~150 LOC)
- Replace SqliteSaver with idempotent SQLite checkpoint table (~20 LOC)
- Replace `batch()` fan-out with `asyncio.TaskGroup`

## Scope
- `orchestration/task_dispatcher.py` — add `no_tmux` parameter (Phase 1)
- `.claude/pair/pair_execute_v2.py` — migrate from LangGraph (Phase 2+)
- `.claude/pair/pair_instructions.py` — update instructions generation
- `orchestration/tests/` — new tests for subprocess launch path

## Phases

### Phase 1: Add no_tmux parameter to TaskDispatcher (this PR)
- Add `no_tmux` to `create_dynamic_agent` agent_spec (default: True)
- When `no_tmux=True`, launch agent script via `subprocess.Popen` instead of `tmux new-session`
- Preserve tmux path as opt-in fallback (`no_tmux=False`)
- Log file capture via stdout/stderr redirect to existing log paths
- PID tracking for process lifecycle monitoring

### Phase 2: asyncio state machine in pair_execute_v2.py
- Replace StateGraph with `Enum` + `match` state machine
- Delete `_FallbackCompiledGraph` (130 lines)
- Delete LangGraph import shims and `Command` wrappers

### Phase 3: Idempotent checkpoint/resume
- Replace SqliteSaver with direct sqlite3 "completed_steps" table
- Make nodes check-before-act for true idempotence

### Phase 4: asyncio fan-out
- Replace `app.batch()` with `asyncio.TaskGroup`
- Replace polling loops with `asyncio.wait_for()`

## Evidence
- secondo analysis: `/tmp/secondo_analysis_20260224.md`
- Research: Cerebras, Grok 4 Fast, Perplexity Sonar Pro unanimous on Option B
- 28 authoritative sources, 20,596 tokens, $0.017 cost

## Dependencies
- None (Phase 1 is backwards-compatible)

## Acceptance Criteria
- [ ] Phase 1: `no_tmux=True` launches agents via subprocess.Popen
- [ ] Phase 1: Existing tmux path works with `no_tmux=False`
- [ ] Phase 1: pair_execute_v2.py works with no_tmux agents
- [ ] Phase 2+: LangGraph dependency removed
- [ ] Phase 2+: _FallbackCompiledGraph deleted
