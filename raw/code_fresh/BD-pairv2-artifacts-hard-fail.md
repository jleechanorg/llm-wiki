# BD-pairv2-artifacts-hard-fail

## ID
BD-pairv2-artifacts-hard-fail

## Title
pairv2: remove required-artifacts hard-fail gate — let verifier LLM decide

## Status
closed

## Type
bug

## Priority
high

## Created
2026-02-23

## Description
`_verify_right_contract_node` (line ~1945) forces `verdict=NEEDS_HUMAN` when `_required_artifacts_status()` returns `artifacts_ok=False`. This overrides the verifier's PASS verdict based on exact path matching, violating the LLM-recoverable workflow tenet.

`_required_artifacts_status` itself (line ~1527) uses `candidate.exists()` exact path matching. Weaker models may write artifacts to slightly different paths.

## Fix
1. In `_verify_right_contract_node`: remove the `if not artifacts_ok` early-return block (lines 1945-1961). Instead, add missing artifacts to `loop_notes` as warnings only.
2. In `_required_artifacts_status`: keep the function for informational purposes but never use its return value to gate verdicts.
3. If verifier verdict is UNKNOWN/unset AND artifacts are missing, THEN use it as a tiebreaker signal.

## Scope
- `.claude/pair/pair_execute_v2.py` — `_verify_right_contract_node`, `_required_artifacts_status`
- `.claude/pair/tests/test_pair_v2.py` — `test_missing_artifacts_returns_needs_human`

## Acceptance
- [x] Verifier PASS is never downgraded due to missing artifacts
- [x] Missing artifacts logged as notes/gaps
- [x] Tests updated
