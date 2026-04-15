---
title: "Repo Level Merge Guard"
type: concept
tags: [merge, guard, repo, ci, protection]
last_updated: 2026-04-14
---

## Summary

Repo Level Merge Guard is a set of branch protection rules applied at the repository level that prevent merging unless specific conditions are met (e.g., all checks pass, required reviewers approve, no unresolved threads).

## GitHub Branch Protection Rules

**Required status checks**:
```bash
# Required checks before merge
- Unit tests (test.yml)
- Integration tests (integration.yml)
- Evidence gate (evidence-gate.yml)
- Doc size check (doc-size-check.yml)
```

**Required reviewers**:
- Minimum 1 approved review
- Dismiss stale reviews when new commits pushed

**Thread resolution**:
- All CodeRabbit threads must be resolved
- No CHANGES_REQUESTED reviews remaining

## Implementation

```bash
# GitHub CLI to set protection
gh api repos/{owner}/{repo}/branches/main/protection \
  --method PUT \
  -f required_status_checks[]=test.yml \
  -f required_status_checks[]=evidence-gate.yml \
  -f enforce_admins=true
```

## Failure Modes

1. **Check not run** — Workflow disabled or skipped
2. **Check flapped** — Non-deterministic test failure
3. **Check passed but merged anyway** — Protection not fully enforced

## Connections
- [[MergeGate]] — Merge gate logic
- [[SkepticGate]] — Skeptic gate system
- [[PRRegressionResolution]] — Regression handling
