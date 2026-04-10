---
title: "gh_integration.py"
type: entity
tags: [gh-integration, python, orchestration, github-api]
sources: [orchestration-system-design-justification.md]
last_updated: 2026-04-07
---

A thin Python wrapper around the `gh` CLI that provides type-safe orchestration for the repo. Every GitHub API call shells out to `gh` via the `gh()` function at line 85. The wrapper provides:

1. **Type-safe orchestration**: Python dataclasses (`PRInfo`, `MergeReadiness`, `CIStatus`)
2. **Fail-closed error handling**: CI failures propagate, unknown states map to "failed"
3. **GraphQL support**: Unresolved thread detection via `pullRequest.reviewThreads`
4. **Testability**: Function-level mocking via `unittest.mock.patch`

Related: [[GitHub]], [[MergeReadiness]]
