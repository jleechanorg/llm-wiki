---
title: "GraphQL Review Threads"
type: concept
tags: [graphql, github, review-threads, pr, api]
sources: [orchestration-system-design-justification.md]
last_updated: 2026-04-07
---

GitHub's GraphQL API provides access to `pullRequest.reviewThreads` which exposes thread resolution state not available in `gh pr view --json`. The wrapper encapsulates this query with injection-safe `-f` variable passing.

This is necessary for the unresolved-thread merge gate, which requires knowing whether review comments have been resolved before allowing merge.

See: [[gh_integration.py]], [[GitHub]]
