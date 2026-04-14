---
title: "Escalation Router"
type: concept
tags: [escalation, deterministic, router, ci-failed, merge-ready, failure-budget]
last_updated: 2026-03-15
sources: [jleechanclaw-orchestration-system-design]
---

## Summary
The escalation router applies deterministic rules to route reactions (CI failures, review comments, session stuck events) to the appropriate action type. The routing engine (`escalation_router.py`) applies rules top-to-bottom, only calling the LLM when deterministic rules have no answer.

## The Decision Matrix

| Signal | Who decides | Action type |
|--------|-------------|-------------|
| CI failed <= retry cap | AO deterministic rule | RetryAction |
| Review comment received | AO deterministic rule | RetryAction |
| CI failed, retry budget >= 2 remaining, parseable error | OpenClaw spawns parallel fix strategies | ParallelRetryAction |
| Agent session idle > threshold | OpenClaw kills and respawns | KillAndRespawnAction |
| Retry budget exhausted | OpenClaw escalates to developer | NotifyJeffreyAction |
| PR approved + CI green | OpenClaw LLM reviews PR | auto_review_trigger → pr_reviewer |
| Vague review comment | OpenClaw LLM interprets + dispatches fix | NeedsJudgmentAction |
| Risky change in sensitive path | OpenClaw LLM escalates with warning | NeedsJudgmentAction |

## Routing Flow

```
reaction.escalated
  ├── attempts ≤ max_retries AND budget ≥ 2 AND parseable CI error
  │     → ParallelRetryAction (spawn 2–3 sessions with different strategies)
  ├── attempts ≤ max_retries (single retry path)
  │     → RetryAction (ao send enriched prompt)
  └── attempts > max_retries
        → NotifyJeffreyAction (budget exhausted)

session.stuck (idle > threshold)
  → KillAndRespawnAction

merge.ready
  → auto_review_trigger → OpenClaw LLM reviews PR
    ├── approve   → post GH review + notify developer "ready to merge"
    ├── changes   → post GH review + RetryAction
    └── escalate  → notify developer "needs your eyes"
```

## Failure Budget

Each action type consumes from a failure budget. The budget prevents infinite retry loops:
- Budget >= 2 remaining + parseable CI error → parallel retry (2-3 worktrees)
- Budget remaining → single retry
- Budget exhausted → escalation to developer via Slack

## Confidence Score Gate

Confidence scores gate LLM judgment calls. If `confidence < 0.6`, the system escalates rather than acting on a low-confidence decision. This prevents the LLM from making high-stakes decisions when uncertain.

## Why Deterministic First

The LLM is expensive, slow, and occasionally wrong. CI failed? That's a deterministic reaction. Review comment? Deterministic. The LLM is called only when the deterministic router has no rule — ambiguous reviews, strategy decisions, task decomposition.

## Related Concepts
- [[AutonomousAgentLoop]]
- [[MemoryTierArchitecture]]
- [[HarnessEngineering]]
- [[MergeReadinessContract]]