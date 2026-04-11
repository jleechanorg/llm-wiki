---
title: "Post-Merge Duplicate PR Loop"
type: concept
tags: [agent-orchestration, pr-workflow, duplicate, loop, ao-worker]
sources: []
last_updated: 2026-04-11
---

## Description
AO workers create "fix review comments" PRs after the original PR has already been merged. This creates orphaned fix PRs that have no base to merge against, wasting CI resources and creating noise.

## Symptoms
- Multiple fix PRs created for the same original PR after it was merged
- Fix PRs show "no changes" or only trivial changes
- Worker continues creating PRs despite no action needed

## Root Cause
Workers receive lifecycle events (e.g., "CHANGES_REQUESTED" review) but act on stale state. By the time the worker processes the event, the original PR has already been merged. The worker doesn't check PR merge status before creating a fix branch.

## Fix
Add a merge-status check before creating fix branches:
```python
# Check PR state before acting on review events
pr = gh.get_pull_request(repo, pr_number)
if pr.state == 'merged':
    return  # Don't create fix PR for already-merged PR
if pr.review_decision == 'CHANGES_REQUESTED' and not pr.mergeable:
    # PR has review comments but can't merge — check if already merged
```

Also: subscribe workers to `merge` events, not just `review` events, so they know when to stop.

## Connections
- [[Compound-Loops]] — related: loop without exit condition detection
- [[PRWatchdog]] — PR monitoring; should detect this loop
- [[CronJobAutomation]] — worker scheduling that triggers these loops
