# BD-pair-attempt-selection-langgraph

## ID
BD-pair-attempt-selection-langgraph

## Title
pair_execute_v2: refactor fan-out orchestration from Python loops to LangGraph-native parallel flow

## Status
closed

## Type
refactor

## Priority
high

## Created
2026-02-22

## Why
`_fan_out_node`, `_fan_out_select_node`, and `run_pairv2` still perform attempt orchestration in Python (`for` loop and manual winner selection). That is still custom control flow instead of LangGraph-native fan-out.

## Scope
- `.claude/pair/pair_execute_v2.py`

## Acceptance
- `run_pairv2` no longer uses a manual python attempt loop for fan-out; it now uses `app.batch()` from LangGraph.
- Attempt selection remains tournament-style and uses `_tournament_collect_node` for deterministic winner selection.
- Keep clear fallback plan for thread-id-scoped Send expansion when available.
- `tournament` naming may remain in pair execution naming and comments while retaining compatibility and preserving behavior.

## Close Reason
run_pairv2 switched fan-out execution to LangGraph batch while preserving tournament-like attempt selection and cleanup behavior.
