---
title: "Trunk-Based Development"
type: concept
tags: [git-workflow, ci, review-cycle, pr-discipline]
---

## Definition

A source control branching model where all developers integrate code to a single shared branch (trunk/main) frequently — ideally daily. Feature branches are short-lived (hours to 1-2 days), not days to weeks.

## Why It Matters for AI Agent Workflows

Long-lived feature branches compound several agent-workflow problems:

| Problem | Trunk-based mitigation |
|---|---|
| Merge conflicts accumulate | Small diffs → fewer conflict pairs |
| CodeRabbit re-reviews full diff on every push | Smaller diff → fewer review threads generated |
| Agent drift expands scope over time | Short branches expire before drift compounds |
| Evidence bundles become stale | Frequent merges keep evidence tied to current HEAD |
| Worktree/branch hygiene debt | Fewer simultaneous branches = less confusion |

## The Level-Up Case

The level-up bug fix (2026-04-18) spent weeks on a ~20-line fix because:
- PR grew to 800 lines across weeks of iteration
- CodeRabbit generated 15-20 new threads per push on the full diff
- Splitting into 4 PRs (#6370-#6373) created 7 merge-conflict pairs

A trunk-based approach would have landed incremental pieces each day, each with <100-line diffs, accumulating far less review surface.

## Implementation

- Max branch age: 2 days before forced merge or abandon decision
- Max PR size: 200 lines production code (hard), 400 lines total with tests
- Feature flags for incomplete features rather than long-lived branches
- Evidence bundles committed on same-day branches, not accumulated over weeks

## Connections

- [[AgentDrift]] — long branches are the primary drift vector
- [[LevelUpBugFixPostMortem20260418]] — key lesson from this case
- [[BugClassification]] — classify first, then ship in small PRs per class
