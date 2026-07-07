---
title: "GitHub Actions reusable-workflow concurrency-group collision"
type: concept
tags: [github-actions, workflow_call, concurrency, ci]
date: 2026-07-07
---

## Concept
Inside a `workflow_call` (reusable workflow invocation), the context expression `github.workflow` resolves to the **caller's** workflow name, not the callee's. If a reusable workflow's `concurrency.group` is built from `${{ github.workflow }}-${{ github.ref }}`, and the caller happens to use the same pattern, the caller and callee land in the same concurrency group. With `cancel-in-progress: true`, the nested (callee) run's start event cancels its own in-progress parent run — the reusable workflow self-cancels the very run that invoked it.

## Why it's easy to introduce
A concurrency-group pattern rolled out across many workflows in one pass (e.g. a security/hygiene sweep adding `cancel-in-progress` everywhere) looks uniform and safe if reviewed file-by-file, but is only safe on workflows that are never invoked via `workflow_call`. The bug only appears for the subset of workflows that are both directly dispatchable AND reusable.

## Detection
`actionlint` does not flag this — it's a cross-workflow semantic issue, not a syntax error. Detect it via run-history diffing: compare job lists before/after the concurrency-pattern rollout for any workflow with a `workflow_call:` trigger; a job silently disappearing from the run without an explicit failure is the signature.

## Fix
Use a literal, non-`github.workflow`-derived group name for any workflow that has a `workflow_call:` trigger, e.g. `deploy-dev-${{ github.ref }}` instead of `${{ github.workflow }}-${{ github.ref }}`.

## Connections
- [[project-2026-07-07-pr8198-ci-workflow-regressions]] — the incident this concept was extracted from (worldarchitect.ai PR #8175 regression, fixed in PR #8198)
- [[GitHubActionsExpressionCommentTrap]] — sibling bug class, same incident
- [[CICDWorkflows]]
