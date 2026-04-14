# BD-pairv2-schema-hard-fail

## ID
BD-pairv2-schema-hard-fail

## Title
pairv2: remove right-contract schema validation hard-fail — warn and continue

## Status
closed

## Type
bug

## Priority
high

## Created
2026-02-23

## Description
`_verify_right_contract_node` (line ~1803) returns immediate `verdict=FAIL` when `_validate_contract_payload()` fails schema validation of the right contract. This prevents the verifier from running at all, violating the LLM-recoverable workflow tenet.

Schema validation failures can be caused by field name typos, version mismatches, or missing optional fields — none of which mean the code is wrong.

## Fix
1. Change schema validation from hard-fail to warning. Log the validation message in notes.
2. Continue to verifier launch even with schema issues.
3. If right_contract_path is empty/missing, construct a minimal fallback contract from the task description and let the verifier evaluate against the original spec.

## Scope
- `.claude/pair/pair_execute_v2.py` — `_verify_right_contract_node` lines 1788-1810

## Acceptance
- [x] Schema validation failures logged as warnings, never cause FAIL
- [x] Missing right_contract_path does not prevent verifier from running
- [x] Verifier receives enough context to judge the workspace
