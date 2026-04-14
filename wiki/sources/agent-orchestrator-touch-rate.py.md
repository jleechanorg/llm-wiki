---
title: "agent-orchestrator touch-rate.py"
type: source
tags: [metrics, github, coderabbit, pr-analysis]
date: 2026-04-14
source_file: /home/jleechan/project_agento/agent-orchestrator/scripts/metrics/touch-rate.py
---

## Summary
A Python CLI tool that calculates first-touch and second-touch rates for merged PRs by analyzing CodeRabbit AI review patterns. It queries the GitHub API to find recently merged PRs, fetches their review data, and computes metrics showing how often CodeRabbit requests changes on its first vs. subsequent reviews.

## Key Claims
- First-touch rate: proportion of PRs where CodeRabbit requests changes exactly once
- Second-touch rate: proportion of PRs where CodeRabbit requests changes exactly twice
- At-most-1 rate: proportion of PRs where CodeRabbit requests changes at most once (≤1)
- Distribution tracking: counts PRs by total number of CodeRabbit change requests

## Key Quotes
> "CodeRabbit bot login — consistent with skeptic-gate.yml and skeptic-cron.yml" — indicates this metric is tied to the CodeRabbit review workflow used in agent-orchestrator's CI/CD pipeline

## Connections
- [[AgentOrchestrator]] — the broader orchestration system this metric monitors
- [[SkepticReviewer]] — CodeRabbit reviews are part of the skeptic review process
- [[MergeGate]] — first/second-touch rates feed into merge quality gates

## Technical Details

### Input Parameters
- `--repo` (required): GitHub repository in `owner/name` format
- `--hours` (default 24): time window for looking at merged PRs

### Output Schema
```json
{
  "repo": "owner/repo",
  "hours": 24,
  "total_merged": N,
  "first_touch_rate_exact_1": 0.xxxx,
  "second_touch_rate_exact_2": 0.xxxx,
  "first_touch_rate_at_most_1": 0.xxxx,
  "distribution": {"0": count, "1": count, "2": count},
  "prs": [{"number": N, "touches": T, "title": "..."}]
}
```

### GitHub API Usage
- Paginated GET requests to `/repos/{repo}/pulls?state=closed&per_page=100`
- Review data: `/repos/{repo}/pulls/{n}/reviews?per_page=100`
- Filters for `user.login == 'coderabbitai[bot]'` and `state == 'CHANGES_REQUESTED'`
- 60-second timeout on all `gh api` calls

## Contradictions
- None identified
