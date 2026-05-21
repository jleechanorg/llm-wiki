# Green Gate 6-Gate Deterministic CI Pattern

**Date**: 2026-05-14
**Source**: PR #568 (jleechanorg/jleechanclaw), `.github/workflows/green-gate.yml`
**Bead**: orch-8zvm

## Summary

Green Gate (479 lines) implements 6 deterministic gates for PR merge eligibility:

| Gate | Check | Pass condition |
|------|-------|---------------|
| 1 | CI green | Required core jobs pass; fallback: STAGING_CANARY_OK>=1 and 0 failures |
| 2 | No merge conflicts | `mergeable=true` or already merged |
| 3 | CR APPROVED | Latest CodeRabbit review state is APPROVED |
| 4 | Bugbot clean | Cursor Bugbot check-run not "failure" |
| 5 | Comments resolved | Zero unresolved non-nit inline comments (waived if CR APPROVED) |
| 6 | Evidence format | Advisory only (WARN, never FAIL) |

## Key Constraints

- No LLM evaluation — all gates are deterministic
- Staging canary fallback must count distinct run IDs (not raw success count)
- Cancelled core jobs should NOT be treated as green (line 95 bug)
- Gate 6 is the only advisory gate — all others are hard blockers

## Related

- [[BlindRenamePitfalls]]
- [[MergeEligibility]]
