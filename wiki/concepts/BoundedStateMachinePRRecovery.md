---
title: "Bounded State Machine PR Recovery"
type: concept
tags: [PR-automation, convergence, evidence, failure-pattern]
last_updated: 2026-07-28
---

Reusable pattern for autonomous PR recovery/convergence loops: treat the recovery as an explicit bounded state machine rather than an open-ended retry loop.

## States

`IDENTIFY -> ADMIT -> FIX -> LOCAL_PASS -> FREEZE_HEAD -> REAL_ACCEPTANCE_PASS -> REVIEW_PASS -> READY`

Any failure returns to the owning state with a counted fingerprint (not a blanket restart). Deadline, scope, or retry-budget exhaustion transitions to `BLOCKED_WITH_PROOF` — never back to an unrestricted coding loop.

## Required invariants

1. **Live-target resolution** — resolve the target PR from the explicit URL/number and cross-check against branch, worktree, goal, and any cached header; any mismatch is a fail-closed routing error (a stale header misrouted one diagnostic lane to an already-merged PR in the source incident).
2. **Structured passing acceptance signal** — require something like `real_acceptance_verdict=PASS` at the exact head SHA. Artifact presence, checksums, and real-provider provenance cannot override failed assertions inside that artifact — see [[EvidenceTheater]].
3. **Exit-criteria classification** — `SELF_CONTROLLABLE`, `EXTERNAL`, `HUMAN_DECISION`. External/human criteria need a deadline and a `BLOCKED_WITH_PROOF` terminal state — see [[GoalHarnessTerminalStates]].
4. **Convergence budget** — one writer, one rerun per normalized failure fingerprint, mandatory re-plan after three repeated failures, head freeze before final evidence/review.
5. **Oversized-mission gate** — >15 commits requires split analysis; >30 commits (or a configured file/delta ceiling) requires explicit human approval for additional cleanup commits.
6. **Nonblocking waits** — CI, reviewer, and runner waiting go through a nonblocking monitor; the coding agent must not sit inside long sleeps or blocking question menus.

## Origin incident

Derived from a 2026-07-28 recovery attempt on [worldarchitect.ai PR 8489](https://github.com/jleechanorg/worldarchitect.ai/pull/8489): 13 commits, 21 CI reruns, 14 Stop-hook rejections, ~15h32m consumed by two blocking question menus, and a two-hour goal with no expiry. See [[bounded-pr-convergence-requires-passing-acceptance-evidence]].

## Connections

- [[EvidenceTheater]] — evidence-presence vs evidence-proves-the-claim gap this pattern closes.
- [[RealAcceptanceVerdict]] — the structured PASS/FAIL signal states 4–7 of the machine gate on.
- [[GoalHarnessTerminalStates]] — the deadline/terminal-state requirement for EXTERNAL/HUMAN_DECISION criteria.
