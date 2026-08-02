---
name: Bounded PR convergence requires passing acceptance evidence
description: Merge-ready automation must resolve the live PR, require a passing exact-head product verdict, and terminate boundedly on external blockers.
type: feedback
bead: rev-7xdvm
---

# Bounded PR convergence requires passing acceptance evidence

## Context

On 2026-07-28, an all-day recovery attempt targeted
[worldarchitect.ai PR 8489](https://github.com/jleechanorg/worldarchitect.ai/pull/8489)
at head
[`bf6a72eb1c0ad1262c7d736e20149a82f85ed98b`](https://github.com/jleechanorg/worldarchitect.ai/commit/bf6a72eb1c0ad1262c7d736e20149a82f85ed98b).
The local header instead reported already-merged
[PR 8328](https://github.com/jleechanorg/worldarchitect.ai/pull/8328).
One independent diagnostic lane followed that stale header into the wrong PR,
reproducing the same routing defect.

The session added 13 commits, invoked 21 CI reruns, and was rejected by its
self-set `/goal` Stop hook 14 times. Two blocking question menus consumed about
15 hours 32 minutes. The two-hour goal had no expiry or blocked terminal state.

## Technical finding

PR 8489's exact-head real-AGY browser artifact was authentic and current, but
its own assertions failed:

- expected player level 6, observed level 5;
- expected `review_open=True`, observed false;
- expected `in_progress`, observed `available` or missing.

Three deterministic tests also remained red. Despite that, Evidence Gate and
Green Gate Gate 6 passed because an evidence artifact existed. The automation
therefore conflated evidence presence and provenance with evidence proving the
acceptance claim.

## Durable rule

A merge-ready workflow must satisfy all of these:

1. Resolve the live target from the explicit PR URL or number and compare it
   with branch, worktree, goal, and header identity. Any mismatch is a
   fail-closed routing error.
2. Require a structured exact-head product result such as
   `real_acceptance_verdict=PASS`. Artifact presence, checksums, real-provider
   provenance, or `/er` authenticity cannot override failed assertions.
3. Classify exit criteria as `SELF_CONTROLLABLE`, `EXTERNAL`, or
   `HUMAN_DECISION`. External and human criteria need a deadline and a
   `BLOCKED_WITH_PROOF` terminal state.
4. Enforce a convergence budget across heads: one writer, one rerun per
   normalized failure fingerprint, a mandatory re-plan after three repeated
   failures, and a head freeze before final evidence and review.
5. Reject oversized repair missions before editing. More than 15 commits
   requires split analysis; more than 30 commits or a configured file/delta
   ceiling requires explicit human approval for additional cleanup commits.
6. Put CI, reviewer, and runner waiting in a nonblocking monitor. A coding
   agent must not sit inside long sleeps or blocking menus.

## Verification

- Live PR identity, head SHA, size, checks, and PR body were refreshed through
  GitHub.
- The PR body explicitly stated `Current evidence verdict: FAIL for
  merge-readiness` and `This PR is not merge-ready`.
- The Claude transcript recorded the blocking question at
  `2026-07-28T07:12:46Z` and its answer at `18:56:13Z`; a second blocking
  question started at `20:04:18Z` and remained until operator recovery around
  `23:53Z`.
- Parallel history, live-PR, and corrected harness lanes converged on the same
  diagnosis.

## Reusable pattern

Treat PR recovery as a bounded state machine:

`IDENTIFY -> ADMIT -> FIX -> LOCAL_PASS -> FREEZE_HEAD -> REAL_ACCEPTANCE_PASS
-> REVIEW_PASS -> READY`

Any failure returns to the owning state with a counted fingerprint. Deadline,
scope, or retry-budget exhaustion transitions to `BLOCKED_WITH_PROOF`, never
back to an unrestricted coding loop.

## References

- Claude session:
  `/Users/jleechan/.claude/projects/-private-tmp-pr8489-cleanup-97f0r0/59bd6e30-055e-4678-ae29-4f8ad90184ad.jsonl`
- Actual worktree: `/private/tmp/pr8489-cleanup.97f0r0`
- Diagnostic bead: `rev-ajy3a`
- Learning bead: `rev-7xdvm`

