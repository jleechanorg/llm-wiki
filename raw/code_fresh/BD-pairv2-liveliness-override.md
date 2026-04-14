# BD-pairv2-liveliness-override

## ID
BD-pairv2-liveliness-override

## Title
pairv2: remove liveliness timing check that overrides verifier verdict

## Status
closed

## Type
bug

## Priority
high

## Created
2026-02-23

## Description
`_read_verification_outcome` (line ~2602) downgrades a verifier FAIL verdict to NEEDS_HUMAN if the verifier was active for less than `minimum_liveliness_seconds` (60s). This overrides the verifier's LLM judgment with a timing heuristic, violating the LLM-recoverable tenet.

If the verifier says FAIL in 30 seconds, that is the verifier's judgment. The correct response is to trust the verdict and retry (if cycles remain), not to silently override it.

## Fix
1. Remove the liveliness check from `_read_verification_outcome`.
2. Log brief verifier activity as a warning note (e.g., "verifier ran for only 30s").
3. Trust the verdict as-is. The retry cycle mechanism handles FAIL verdicts.

## Scope
- `.claude/pair/pair_execute_v2.py` — `_read_verification_outcome` lines 2592-2612

## Acceptance
- [x] Liveliness timing check removed or converted to warning-only
- [x] Verifier FAIL verdict never overridden by timing heuristic
- [x] Tests updated if any depend on NEEDS_HUMAN from liveliness check
