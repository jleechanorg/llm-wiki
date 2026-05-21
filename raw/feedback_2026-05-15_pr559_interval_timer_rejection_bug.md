---
name: project-supervisor-interval-timer-rejection-bug
description: Interval timer callers must not be rejected when reconcile errors occur
type: feedback
bead: none
---

## Context

During PR #559 (`feat/upstream-integration-may2026`) merge process, a critical bug was
identified in `packages/cli/src/lib/project-supervisor.ts`. The `startProjectSupervisor`
function runs a reconcile loop on an interval timer, with a `reconcileNow` method for
explicit invocation. Both callers share the same waiter queue.

## Technical Detail

The bug was in the waiter resolution logic:

```typescript
// BEFORE (buggy — AO worker left this form):
for (const w of pendingWaiters) {
  if (err && !options.swallowErrors) w.reject(err);
  else w.resolve();
}

// AFTER (correct):
for (const w of pendingWaiters) {
  if (err && options.swallowErrors === false) w.reject(err);
  else w.resolve();
}
```

The interval timer calls `run({ swallowErrors: true })`. When `err` is set and
`swallowErrors=true`, the buggy code would call `w.reject(err)` because `!options.swallowErrors`
is `true` when `swallowErrors=true` (double negative). The fix changes the condition to
`options.swallowErrors === false` so only `reconcileNow` callers (who pass the default
`swallowErrors=undefined`) get rejected on error.

## Related Pattern

Same pattern appears in `packages/cli/src/lib/project-supervisor.ts:156-158` where
`swallowErrors=true` interval callers get resolved even when `err` is set.

## Verification

- Commit `aaa6d7238` (AO worker) left the buggy form
- Fixed in final PR #559 commits
- GraphQL `resolveReviewThread` mutation resolves CodeRabbit review threads

## References

- [PR #559 merged](https://github.com/jleechanorg/agent-orchestrator/pull/559) — commit `a12ef2c68`
- `packages/cli/src/lib/project-supervisor.ts` lines 154-159
- GraphQL: `resolveReviewThread` mutation for CodeRabbit thread resolution
- `packages/web/src/app/sessions/[id]/page.tsx` — restored after upstream refactor deleted it
- `gh run list` requires `cd` to repo root; CWD issue with worktrees