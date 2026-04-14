# BD-pairv2-verify-retry-loop

## ID
BD-aib (BD-pairv2-verify-retry-loop)

## Title
pairv2: verify-fail-retry loop with verifier feedback injection

## Status
closed

## Type
feature

## Priority
P1

## Created
2026-02-24

## Description
The PR #5734 design tenet says the pairv2 workflow does:
1. Give coder a spec → wait for it to say it's done
2. Run verifier → ask "is it really done?"
3. If not → tell coder to keep going
4. Repeat N cycles or until verifier says 100% PASS

Step 3 does NOT exist. The graph is currently LINEAR:
  implement → wait → verify → finalize

When verifier returns FAIL, the graph goes straight to finalize with status="failed".
The max_cycles counter is incremented at generate_left_contract (problem scoping),
NOT at implementation retry. There is no edge from verify back to implement.

This adds the conditional edge verify → implement when verdict is FAIL and cycles
remain, with the verifier's failure reasoning injected into the coder's next prompt —
turning the one-shot executor into a self-correcting loop.

## Architecture

### Graph Change: Conditional Edge verify → implement

Current graph (linear):
```
generate_left_contract → generate_right_contract → left_contract
  → implement → wait_for_implementation_ready → verify → finalize
```

New graph (cyclic on FAIL):
```
generate_left_contract → generate_right_contract → left_contract
  → implement → wait_for_implementation_ready → verify
      ↓ PASS → finalize
      ↓ FAIL + cycles remaining → implement (with feedback)
      ↓ FAIL + cycles exhausted → finalize
```

### New routing function: `_route_after_verify(state: PairV2State) -> str`

```python
def _route_after_verify(state: PairV2State) -> str:
    """Route after verification: retry on FAIL if cycles remain."""
    if state["verdict"] == "PASS":
        return "finalize"
    if state["impl_cycle"] >= state["max_impl_cycles"]:
        state["notes"].append(
            f"RETRY_EXHAUSTED: impl_cycle {state['impl_cycle']}/{state['max_impl_cycles']}, "
            f"verdict={state['verdict']}, proceeding to finalize"
        )
        return "finalize"
    # Inject verifier feedback for next coder attempt
    return "implement"
```

### Feedback extraction: `_extract_verifier_feedback(state) -> str`

Read verification_report.json from the verify node output. Extract:
- `reasoning` field (why verifier said FAIL)
- `issues` list (specific problems found)
- `test_results` summary (which tests failed)

Format as structured feedback block for coder prompt injection.

### Feedback injection into coder prompt

In `_launch_coder_only` (the implement node), detect impl_cycle > 0 and prepend:

```
## VERIFIER FEEDBACK (attempt {impl_cycle + 1}/{max_impl_cycles})

Your previous implementation was reviewed and REJECTED. Fix these issues:

{extracted_feedback}

The workspace at {shared_workspace} already has your prior work.
Do NOT start from scratch. Run tests first, then fix the specific issues above.
```

### State changes

Add to PairV2State (NotRequired):
```python
verifier_feedback: str   # Extracted feedback from last verification
impl_cycle: int          # Implementation attempt counter (distinct from contract cycle)
max_impl_cycles: int     # Max retries (default 3)
```

### Cycle counter semantics

- `cycle` (existing): Problem-scoping iteration (left/right contract generation)
- `impl_cycle` (new): Implementation retry counter within a single problem scope
- `max_impl_cycles` (new, default 3): Max retries before giving up on current contracts
- Keep both: a contract can be refined (cycle++) or an implementation retried (impl_cycle++)

### Workspace preservation across retries

On retry, the coder workspace is NOT cleaned. The coder:
1. Sees all files from prior attempt
2. Gets explicit feedback about what was wrong
3. Runs tests first to understand current state
4. Makes targeted fixes (not full reimplementation)

Stale signal files ARE cleaned: IMPLEMENTATION_READY, verification_report.json.

### Session cleanup between retries

Before re-launching coder on retry:
1. Kill old tmux session (coder already exited, but safety net)
2. Remove stale IMPLEMENTATION_READY signal file
3. Remove stale verification_report.json
4. Preserve workspace, session_info.json, contracts, instructions
5. Append feedback to coder prompt

### Interaction with monitor-restart (BD-pairv2-monitor-restart)

Orthogonal recovery paths:
- Stall → restart same agent with same task (recovery from hang)
- FAIL → restart coder with NEW feedback (recovery from wrong code)

Both share _restart_agent mechanics but with different prompt suffixes.

### Interaction with fan-out (M5)

In fan-out mode (--fan-out N), each attempt runs independently.
The retry loop applies PER ATTEMPT: each fan-out lane can retry independently.
Tournament selection still picks the first PASS across all lanes.

## Constants

- `PAIRV2_MAX_IMPL_CYCLES = 3` — max implementation retries per contract scope
- `PAIRV2_RETRY_WORKSPACE_CLEAN = False` — never clean workspace on retry

## Scope

- `.claude/pair/pair_execute_v2.py`:
  - New: `_route_after_verify(state) -> str` conditional edge function
  - New: `_extract_verifier_feedback(state) -> str` feedback extractor
  - Modified: graph builder — replace unconditional verify→finalize with conditional routing
  - Modified: `_launch_coder_only` — detect retry cycle, inject feedback into prompt
  - Modified: implement node — clean stale signals before re-launch (not workspace)
  - New state keys: `verifier_feedback`, `impl_cycle`, `max_impl_cycles`
- `.claude/pair/pair_instructions.py`:
  - New: retry-aware coder prompt suffix template
  - Modified: coder prompt to accept feedback block
- `.claude/pair/tests/test_pair_v2.py`:
  - New: `test_verify_fail_routes_to_implement_when_cycles_remain`
  - New: `test_verify_fail_routes_to_finalize_when_cycles_exhausted`
  - New: `test_verifier_feedback_injected_into_coder_prompt`
  - New: `test_verify_pass_routes_to_finalize`
  - New: `test_retry_preserves_workspace`
  - New: `test_impl_cycle_counter_increments_on_retry`

## Acceptance
- [x] Conditional edge: verify → implement when verdict=FAIL and impl_cycle < max_impl_cycles
- [x] Conditional edge: verify → finalize when verdict=PASS or impl_cycle >= max_impl_cycles
- [x] _extract_verifier_feedback reads reasoning/issues/test_results from verification_report.json
- [x] Feedback injected into coder prompt on retry with specific issues listed
- [x] impl_cycle counter increments on each retry, distinct from contract cycle
- [x] Workspace preserved across retries (never cleaned)
- [x] Stale signal files cleaned between retries
- [x] Retry-aware coder prompt includes "run tests first, then fix these issues"
- [x] Works with fan-out mode (per-lane retry)
- [x] Works with monitor-restart (orthogonal recovery paths)
- [x] max_impl_cycles defaults to 3, configurable via CLI --max-impl-cycles
- [x] Notes accumulate retry history: "RETRY: impl_cycle 2/3, feedback: ..."
- [x] Tests: FAIL→retry→PASS, FAIL→retry→FAIL→finalize, PASS→finalize (no retry)

## Shadow Execution Evidence (2026-02-24)

Purpose: run the Shadow Execution Gate for this bead before implementation to
measure gap size and confirm baseline behavior.

Evidence summary:
- `test_missing_artifacts_does_not_retry_when_cycles_remain` **fails** on current HEAD:
  observed launch count is 3 when `max_cycles=3`. This confirms there is already a
  retry loop, but it is contract-cycle retry (`verify -> generate_left_contract`)
  rather than direct implementation retry.
- `test_invalid_right_contract_fails` passes on current HEAD (fast-fail remains active in
  provided-contract validation paths).
- Existing M7 contract generation tests pass, confirming recent fail-soft path changes did
  not regress contract generation.
- Code inspection confirms no `impl_cycle`/`max_impl_cycles` state keys and no
  `verifier_feedback` injection path in coder launch prompt.

Gate decision:
- **NOT READY FOR PROMOTION** for this bead's scope.
- Reason: critical acceptance criteria for verify-fail-retry loop are not implemented yet
  (no direct conditional `verify -> implement` retry path and no verifier feedback injection).

## Shadow Execution Evidence (2026-02-24, Post-Implementation)

Focused gate run after implementation:
- `test_missing_artifacts_retries_implementation_when_cycles_remain` ✅
- `test_verify_node_retries_to_implement_with_feedback` ✅
- `test_verify_cleanup_called_before_retry` ✅
- `test_verify_node_needs_human_when_cycles_exhausted_on_fail` ✅
- `test_m4_parse_args_has_max_impl_cycles_flag` ✅
- `test_m4_run_pairv2_has_max_impl_cycles_param` ✅

Observed behavior:
- Verify FAIL now routes directly to implement until `max_impl_cycles` is exhausted.
- Retry state (`impl_cycle`) increments independently from contract-cycle state.
- Verifier feedback is persisted in state and injected into coder instructions.
- Retry teardown preserves workspace and cleans stale completion/report artifacts.

Gate decision:
- **READY FOR PROMOTION** for BD-aib scope.
