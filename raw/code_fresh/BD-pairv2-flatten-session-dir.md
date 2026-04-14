# BD-pairv2-flatten-session-dir

## ID
BD-pairv2-flatten-session-dir

## Title
pairv2: LLM-recoverable workflow — process-exit detection + inference-driven verification

## Status
done

## Type
task

## Priority
high

## Created
2026-02-23

## Description
MiniMax coder wrote IMPLEMENTATION_READY to wrong path during benchmark. The agent constructed `pair-<id>-attempt-0/coordination/coder_outbox/` (hyphenated flat) instead of the correct `pair-<id>/attempt-0/coordination/coder_outbox/` (nested). Despite the artifact contract containing the correct absolute path 3 times in the prompt, the agent ignored it and guessed.

Root cause: strict file-path gating is fragile with weaker models that reconstruct paths incorrectly.

**Approach pivoted** from "flatten dirs" to "LLM-recoverable workflow":
- Process exit is the primary completion signal (tmux session dead = coder done)
- Signal files (IMPLEMENTATION_READY) are optional best-effort hints, not gates
- Verifier uses LLM inference to evaluate code against contracts if report is missing
- Never downgrade a verifier PASS verdict due to missing signal files

## Changes
- `pair_execute_v2.py`: Rewrote `_wait_for_implementation_ready_node` to use process-exit detection; removed PASS→NEEDS_HUMAN downgrade for missing signal; added design tenet docstring
- `pair_instructions.py`: Updated coder prompt to emphasize running tests before exit; updated verifier prompt with LLM-recoverable tenet and inference fallback; made signal files best-effort
- `tests/test_pair_v2.py`: Updated test to accept PASS without IMPLEMENTATION_READY signal

## Acceptance
- [x] Process exit as primary completion signal (tmux session dead = done)
- [x] IMPLEMENTATION_READY signal as optional fast-path hint only
- [x] Verifier PASS not downgraded when signal file missing
- [x] Coder prompt emphasizes running tests
- [x] Verifier prompt uses inference against contracts if report not found
- [x] Design tenet documented in module docstring
- [x] All 29 tests passing, 1 skipped
