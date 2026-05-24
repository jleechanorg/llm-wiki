# CI-Expansion Surfaces Latent Failures

A PR that adds test files / shards / runners to CI coverage will surface
test failures that were latent on `main` (not running anywhere before).
Treat these as expected and budget in-PR fixes.

## Pattern
1. Run the newly-included tests locally **before pushing**.
2. Either fix the failures in the same PR or add xfail with bead-tracked
   rationale.
3. If failures are truly out-of-scope, revert the CI-inclusion commit
   until they're addressed separately.

Do not assume "the new tests will pass because I didn't touch that area".
They probably won't.

## Example
PR #7048 commits `44cef3e22` (include end2end in core-mvp directory-based
tests) and `e7ef154c2` (run mvp end2end in self-hosted shards) surfaced
9 pre-existing test failures. All fixed in same PR.

## Related
- [[pr7048-location-centralization-merged]]

## Source
- ~/.claude/projects/-Users-jleechan-projects-worktree-location-centralize/memory/feedback_2026-05-24_ci_expansion_surfaces_latent_failures.md
