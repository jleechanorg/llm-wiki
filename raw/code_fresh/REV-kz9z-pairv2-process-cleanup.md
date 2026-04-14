# REV-kz9z: Prevent pairv2 live session process leakage

**Created**: 2026-02-22
**Status**: Implemented
**Priority**: High (resource safety)
**Related**: PairV2 launch/verify lifecycle

## Problem
During pairv2 launches, a coder agent session could remain running when verifier startup fails.

Verification can also return to `generate_left_contract` or finalize without cleaning the current
`live_session_dir`, allowing live sessions (tmux sessions + result artifacts) to accumulate across
retries.

This can contribute to process pressure such as `fork: Resource temporarily unavailable` under heavy
reuse.

## Fix
### ` .claude/pair/pair_execute_v2.py`
- Write `session_info.json` before launching agents in `_launch_live_pair_session` so a partial launch has
a cleanup target.
- On coder launch failure and verifier launch failure, call `_terminate_live_session` immediately before
returning an error.
- In `_verify_right_contract_node`, call `_terminate_live_session` before every branch return (pass,
artifact failure, cycle retry, timeout, and final fallback) so each attempt session is cleaned promptly.

### Test coverage
- `.claude/pair/tests/test_pair_v2_and_benchmark.py`
  - `REVkz9zProcessCleanupTests.test_launch_cleans_coder_if_verifier_launch_fails`
  - `REVkz9zProcessCleanupTests.test_verify_cleanup_called_before_retry`

## Validation
- `pytest .claude/pair/tests/test_pair_v2_and_benchmark.py -k "REVkz9z"`
- `pytest .claude/pair/tests/test_pair_v2_and_benchmark.py -k "REV85yw or REV9loi or REVcy7g or REVkz9z or M2CompleteTests or M5FanOutSelectTests or M3SimplifiedPollingTests"`
