---
name: gh-run-rerun-clears-stale-statuscheckrollup
description: gh run rerun <failed-PR-event-run-id> clears stale Green Gate FAIL in statusCheckRollup — no empty commit needed
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: cbf71cb9-9eec-4fef-b34b-20233fa240dc
---

## Rule

When a PR-event-triggered required check (e.g. Green Gate) fails due to a transient race condition, use `gh run rerun <run-id>` to re-execute the same PR-event workflow run. The rerun updates the **same statusCheckRollup entry**, flipping `mergeStateStatus` from UNSTABLE → CLEAN without requiring a new push.

**Why:** `gh run rerun` replaces the existing check-run entry in statusCheckRollup. A `workflow_dispatch` re-run does NOT update statusCheckRollup (it creates a separate run record). Only PR-event runs (triggered by push/synchronize) or reruns of those same runs update the required-checks bucket.

## The specific race (PR #7871, 2026-06-24)

Timeline:
1. Push `33b0156afd` at 09:20:46Z → PR-event Green Gate (run 28088452139) starts
2. First smoke run fires immediately → deploy-preview NOT ready → smoke run fails → posts fail comment
3. Green Gate Gate-8: reads fail comment → exits FAIL immediately (no retry for later PASS comments)
4. Green Gate run 28088452139 fails at 09:23:49Z → stuck in statusCheckRollup as FAIL
5. Second smoke run succeeds at 09:33:11Z → PASS comment for `33b0156afd` posted
6. Skeptic PASS for `33b0156afd` at 09:33:48Z
7. `gh run rerun 28088452139` at ~09:40Z → finds PASS comment → all 8 gates PASS
8. `mergeStateStatus` flips UNSTABLE → **CLEAN**

## How to apply

When `mergeStateStatus: UNSTABLE` and the only stale failure is a PR-event Green Gate that raced ahead of its dependencies:

```bash
# Identify the failing PR-event run
gh pr checks <PR> --json name,bucket,databaseId | jq '.[] | select(.name == "Green Gate" and .bucket == "fail") | .databaseId'

# Rerun it (NOT workflow_dispatch — that won't update statusCheckRollup)
gh run rerun <run-id> --repo jleechanorg/worldarchitect.ai

# Monitor
gh run view <run-id> --json status,conclusion
```

## Anti-pattern avoided

Previous approach: push empty commit → new CI cycle → new smoke → new Skeptic → new Green Gate. Full cycle: 15-20 min. The rerun took ~3 min and required no new SHA.

## Gate-8 behavior that causes the race

Green Gate Gate-8 reads smoke PR comments immediately and **exits FAIL on the first matching fail comment** without polling for later PASS comments. This is by design (fail fast). The race: if a smoke run fires before deploy-preview is ready (first auto-smoke on push), its fail comment permanently gates the PR-event Green Gate run for that SHA.

**References**: PR [#7871](https://github.com/jleechanorg/worldarchitect.ai/pull/7871) merged 2026-06-24T15:15:35Z; SHA `33b0156afd4b3544a8bd62f5b540e236d767ce7a`; rerun id 28088452139 (conclusion: success at ~09:43Z).
