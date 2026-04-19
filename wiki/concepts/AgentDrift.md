---
title: "Agent Drift"
type: concept
tags: [agents, orchestration, pr-discipline, scope-management]
---

## Definition

Agent drift occurs when spawned sub-agents deviate from their intended scope because they are anchored only to a PR number, with no bead or design-doc context explaining *why* the PR exists or what its boundaries are.

## Mechanism

When an agent is spawned with "fix PR #6370" as its only context:
- It infers scope from PR title and open comments alone
- Review churn generates new action items that look like scope
- The agent addresses review items, adds polish, and makes tangential fixes
- The final diff includes substantial work outside the original intent

## Measured Impact

In the level-up bug fix work (2026-04-18): 13 of 29 post-roadmap PRs drifted from intended scope. The primary vector was PR-number anchoring without bead/design-doc context.

## Prevention

1. Always spawn agents with a bead reference (`/bead <id>`) or design-doc section as the primary anchor
2. Scope statements must name what is **excluded**, not just what is included
3. PRs should be created from a bead or design-doc task, not the reverse
4. Size cap: PRs >200 lines of production code are drift-prone — split proactively
5. For the level-up fix family, anchor future work to bead `rev-7vyc` and `/Users/jleechan/roadmap/2026-04-18-level-up-central-tracker.md`, not just a GitHub PR number.

## Correct Spawn Pattern

```
/agent fix PR #6370 — scope: ONLY tri-state flag fixes in agents.py per bead LEVEL_UP_ATOMIC_FIX; do NOT address review style comments or expand to world_logic.py
```

## Connections

- [[LevelUpBugFixPostMortem20260418]] — 13/29 PRs drifted in this case
- [[TrunkBasedDevelopment]] — smaller PRs reduce drift surface
- [[BugClassification]] — classify all classes before splitting into PRs
