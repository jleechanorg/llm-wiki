---
title: "Goal Harness Terminal States"
type: concept
tags: [goal-harness, autonomy, convergence, failure-pattern]
last_updated: 2026-07-28
---

Requirement that any autonomous goal/convergence harness classify its exit criteria and give EXTERNAL/HUMAN_DECISION criteria a deadline and an explicit bounded terminal state, instead of only a binary pass/retry loop.

## Classification

- **SELF_CONTROLLABLE** — the agent can directly cause this to become true (fix code, rerun a test).
- **EXTERNAL** — depends on a third party or system outside the agent's control (CI runner availability, reviewer bot latency, external service state).
- **HUMAN_DECISION** — depends on a human choice (approval, an answer to a blocking question).

## Rule

EXTERNAL and HUMAN_DECISION criteria must carry a deadline. On deadline, scope, or retry-budget exhaustion, the harness must transition to a `BLOCKED_WITH_PROOF` terminal state — never fall back into an unrestricted coding/retry loop.

## Origin incident

A 2026-07-28 recovery session's `/goal` Stop hook rejected the agent 14 times over a "two-hour goal" that had no expiry or blocked terminal state; two blocking question menus alone consumed ~15h32m of the day. See [[bounded-pr-convergence-requires-passing-acceptance-evidence]]. Related to the existing CLAUDE.md-level "Autonomy time-box — max 3 hours without explicit re-approval" policy, but this incident shows the gap is specifically the *terminal state*, not just the time-box: a harness can already be timeboxed and still lack anywhere useful to land other than "keep grinding" or "ask a blocking question."

## Connections

- [[BoundedStateMachinePRRecovery]] — the state machine this classification feeds into.
- [[bounded-pr-convergence-requires-passing-acceptance-evidence]] — origin incident.
