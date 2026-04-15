---
title: "Skeptic Gate CodeRabbit"
type: concept
tags: [skeptic-gate, coderabbit, review, ai-review, worldai]
last_updated: 2026-04-14
---

## Summary

Skeptic Gate CodeRabbit is the integration between the Skeptic Gate automated quality verification system and CodeRabbit's AI-powered code review. CodeRabbit's CHANGES_REQUESTED reviews can block merge when the gate is configured to respect them.

## Integration Points

### 1. Review Watch
Skeptic gate monitors CodeRabbit review states:
```python
async def check_coderabbit_reviews(pr_number: int) -> ReviewState:
    reviews = await gh.api.repos/{owner}/{repo}/pulls/{pr_number}/reviews
    for review in reviews:
        if review.state == "CHANGES_REQUESTED":
            return ReviewState.CHANGES_REQUESTED
    return ReviewState.APPROVED
```

### 2. Thread Resolution Tracking
All CodeRabbit threads must be resolved before merge:
```python
threads = await coderabbit.get_threads(pr_number)
if any(t.status == "open" for t in threads):
    raise MergeBlockError("Unresolved CodeRabbit threads")
```

### 3. Gate Enforcement
Gate blocks merge when:
- CodeRabbit returns CHANGES_REQUESTED
- Any open unresolved threads
- CodeRabbit check status is "failure"

## Configuration

```yaml
skeptic_gate:
  coderabbit:
    required_for_merge: true
    dismiss_on_approve: true  # Clear CHANGES_REQUESTED when re-review approves
```

## Connections
- [[SkepticGate]] — General Skeptic gate system
- [[MergeGate]] — Merge gate logic
- [[RepoLevelMergeGuard]] — Repository-level protection
