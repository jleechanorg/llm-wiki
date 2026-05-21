# project-supervisor interval timer rejection bug

## Metadata
- **type**: feedback
- **date**: 2026-05-15
- **classification**: Critical
- **bead**: none
- **source**: `~/.claude/projects/-Users-jleechan--project_agento-agent-orchestrator/memory/feedback_2026-05-15_pr559_interval_timer_rejection_bug.md`

## Problem

During PR #559 (`feat/upstream-integration-may2026`) merge, a bug was found in `packages/cli/src/lib/project-supervisor.ts` in `startProjectSupervisor`. The interval timer and `reconcileNow` share a waiter queue. When an error occurs during reconcile, the waiter resolution logic incorrectly rejected interval timer callers.

## Root Cause

```typescript
// BUGGY (double-negative — !true === true):
if (err && !options.swallowErrors) w.reject(err);

// FIXED:
if (err && options.swallowErrors === false) w.reject(err);
```

`run({ swallowErrors: true })` is called by the interval timer. With the buggy code, when `err` is set and `swallowErrors=true`, `!options.swallowErrors` evaluates to `true`, causing the waiter to be rejected. The interval timer should never reject — it swallows errors silently.

## Resolution

- PR #559 merged at commit `a12ef2c68`
- Bug fixed in final commits on the branch
- Key fix location: `packages/cli/src/lib/project-supervisor.ts:154-159`

## Related Patterns

1. **GraphQL `resolveReviewThread`** — used to auto-resolve CodeRabbit review threads via GitHub GraphQL API
2. **`sessions/[id]/page.tsx` restoration** — upstream refactor deleted this file; restored from origin/main for Gate 5 resolution
3. **`gh run list` CWD issue** — requires `cd` to repo root in worktree context; gh CLI finds wrong git repo if run from worktree subdirectory

## References

- [PR #559](https://github.com/jleechanorg/agent-orchestrator/pull/559)
- `packages/cli/src/lib/project-supervisor.ts`
- `packages/web/src/app/sessions/[id]/page.tsx`