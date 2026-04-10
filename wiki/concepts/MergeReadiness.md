---
title: "Merge Readiness"
type: concept
tags: [merge-readiness, pr, ci, github, aggregation]
sources: [orchestration-system-design-justification.md]
last_updated: 2026-04-07
---

The aggregation of 4 independent checks (CI status, review approvals, unresolved review threads, merge conflicts) into a single boolean with a blockers list. The `get_merge_readiness()` function composes these checks — this composition doesn't exist in the `gh` CLI natively.

See: [[gh_integration.py]], [[GitHub]]
