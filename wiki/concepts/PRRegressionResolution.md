---
title: "PR Regression Resolution"
type: concept
tags: [pr, regression, resolution, ci, worldai]
last_updated: 2026-04-14
---

## Summary

PR Regression Resolution is the process of identifying and fixing regressions introduced by a pull request before merge. A regression is any behavior that worked before the PR but breaks after it.

## Resolution Workflow

```
Regression detected → Identify root cause → Implement fix → Verify with test → Merge
```

## Detection Methods

**Automated CI gates**:
- Unit tests (fast, catches obvious breaks)
- Integration tests (slower, catches data flow issues)
- E2E tests (slowest, catches UX breaks)

**Manual review**:
- CodeRabbit / AI review for logical errors
- Human review for design issues

## Fix Priority

1. **Critical regressions** — Blocks merge, must fix before proceeding
2. **Non-critical regressions** — Should fix but can be deferred with agreement
3. **False positives** — Test itself is wrong, not the code

## Common Regression Patterns

- Removing or weakening a validation check
- Changing default values unexpectedly
- Introducing non-idempotent behavior
- Breaking backward compatibility in API responses

## Connections
- [[SkepticGateCodeRabbit]] — CodeRabbit integration for review
- [[MergeGate]] — Merge prevention for regressions
- [[RepoLevelMergeGuard]] — Repository-level merge guards
