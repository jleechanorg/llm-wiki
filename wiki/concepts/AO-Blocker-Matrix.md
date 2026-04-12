---
title: "AO Blocker Matrix"
type: concept
tags: [agent-orchestrator, PR, triage, blocker, CI]
last_updated: 2026-04-08
---

When several serious PRs are red at once, blind reruns and extra workers waste time. Need fail-closed classification first: conflict, checks-running, failing-checks, unresolved-threads, or review-not-approved.

## 5 Blocker Categories

1. **conflict** — merge conflict with base branch
2. **checks-running** — CI still in progress
3. **failing-checks** — CI failed
4. **unresolved-threads** — PR has unresolved review comments
5. **review-not-approved** — review decision is not APPROVED

## Scripts

- `pr-rescue-status.sh` — checks current PR state
- `pr-blocker-matrix.sh` — classifies PRs into blocker categories

## Pattern

Before trying to make open bug-fix PRs "7-green," classify each into CI failure vs review/gate debt. PRs #6157 and #6161 were review-blocked despite green CI. PR #6165 had a real failing shard.

## Connections

- [[AO-Claim-Fail-Closed]] — AO claim fail-closed execution
- [[AO-Split-Brain]] — AO split-brain with duplicate workers
- [[AO-Daemon-Incident]] — AO daemon incidents masking blockers
- [[MergeReadiness]] — merge readiness criteria
