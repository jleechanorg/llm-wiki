# Skeptic Cron Auto-Merge

Automated 7-green PR merge gate running as GitHub Actions cron workflow.

## How it works
- Runs every 30 min evaluating all open non-draft PRs
- 6 gates: CI green, no conflicts, CR APPROVED, Bugbot clean, comments resolved, evidence review
- When SKEPTIC_NO_VERDICT (no prior VERDICT comment), cron IS the skeptic — evaluates gates 1-6, posts VERDICT: PASS, and merges in same run
- Gate 1: repo-agnostic — excludes named gates, evaluates all other check-runs
- Gate 3: CR incremental stall fallback — matches verdict comment patterns
- Gate 4: Bugbot HIGH/CRITICAL severity only, filtered by original_commit_id

## Deployment
- hermes-agent: skeptic-cron.yml (workflow ID 277039266) + green-gate.yml (workflow ID 277040104)
- Self-hosted runners via `SELF_HOSTED_RUNNER_LABELS` org var

## Related
- [[green-gate-ci-pattern]]
- [[CodeRabbitDismissedPattern]]
