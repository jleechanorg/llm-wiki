---
title: "Bounded PR convergence requires passing acceptance evidence"
type: source
tags: [evidence, PR-automation, convergence, goal-harness, evidence-theater]
date: 2026-07-28
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worktree_fable_bulk_restored/memory/feedback_2026-07-28_bounded_pr_convergence_requires_passing_acceptance.md
---

## Summary

An all-day (~15h32m) autonomous recovery session on [worldarchitect.ai PR 8489](https://github.com/jleechanorg/worldarchitect.ai/pull/8489) added 13 commits, triggered 21 CI reruns, and was rejected by its own `/goal` Stop hook 14 times — while the PR's own exact-head acceptance artifact showed failing assertions (expected level 6 observed 5, `review_open` expected True observed False, expected `in_progress` observed `available`/missing) and three deterministic tests stayed red. Evidence Gate and Green Gate Gate 6 passed anyway, because both gates check for evidence *presence/provenance*, not whether the evidence *proves* the acceptance claim. A stale local header also misrouted one diagnostic lane to the wrong (already-merged) PR 8328.

## Key Claims

- Artifact authenticity/provenance (real-AGY browser capture, exact head SHA, checksums) is orthogonal to whether the artifact's own assertions pass — evidence gates conflated the two.
- A goal with a sustained-time criterion but no expiry/blocked terminal state can grind indefinitely against an unfixable external blocker.
- Bounded PR recovery should be modeled as an explicit state machine: `IDENTIFY -> ADMIT -> FIX -> LOCAL_PASS -> FREEZE_HEAD -> REAL_ACCEPTANCE_PASS -> REVIEW_PASS -> READY`, with any failure returning to the owning state under a counted fingerprint, and deadline/scope/retry-budget exhaustion routing to `BLOCKED_WITH_PROOF` rather than back into unrestricted grinding.
- Exit criteria should be classified `SELF_CONTROLLABLE` / `EXTERNAL` / `HUMAN_DECISION`; external/human criteria need a deadline and a bounded terminal state.
- Oversized repair missions (>15 commits) need a split-analysis checkpoint; >30 commits needs explicit human approval.
- CI/reviewer/runner waits belong in a nonblocking monitor — a coding agent must not sit inside long sleeps or blocking question menus (two blocking menus alone consumed ~15h32m here).

## Key Quotes

> "PR 8489's exact-head real-AGY browser artifact was authentic and current, but its own assertions failed... Despite that, Evidence Gate and Green Gate Gate 6 passed because an evidence artifact existed. The automation therefore conflated evidence presence and provenance with evidence proving the acceptance claim."

> "The PR body explicitly stated `Current evidence verdict: FAIL for merge-readiness` and `This PR is not merge-ready`."

## Connections

- [[EvidenceTheater]] — same failure class (gate accepts weaker proof than the claim requires); this incident is a variant where the *artifact* is real and current but its assertions still fail, and the gate doesn't check assertion results at all.
- [[BoundedStateMachinePRRecovery]] — the reusable state-machine pattern this incident produced.
- [[GoalHarnessTerminalStates]] — the missing `BLOCKED_WITH_PROOF` terminal state / deadline requirement for EXTERNAL and HUMAN_DECISION exit criteria.
- [[RealAcceptanceVerdict]] — the proposed structured pass/fail signal (`real_acceptance_verdict=PASS`) that artifact presence alone cannot substitute for.
