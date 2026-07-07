---
title: "PR #8198 — two CI workflow regressions broke main repo-wide"
type: source
tags: [github-actions, ci, workflow-syntax, self-hosted-runners, regression]
date: 2026-07-07
source_file: raw/project_2026-07-07_pr8198_ci_workflow_regressions.md
---

## Summary
Two independent one-file GitHub Actions bugs landed on `main` within a day of each other and broke CI repo-wide on every branch, because workflow-file triggers (`issue_comment`, `workflow_dispatch`) always load the definition from `main`'s copy. Both were fixed together in PR #8198 (merged 2026-07-07T03:18:05Z, commit `42b963099b92cabe187659e005b2c7565372395e`), tracked by bead `rev-j9so3` (closed).

## Key Claims
- A `#` comment placed **inside** a GitHub Actions `if: >-` folded-scalar expression is not a comment — the Actions expression lexer has no comment syntax, so `#` becomes literal expression text and the whole workflow fails to parse (`startup_failure`) on every branch. Introduced in commit `0586722c2b` (PR #8192) in `.github/workflows/mcp-smoke-tests.yml` line 48.
- Inside a `workflow_call` (reusable workflow), `github.workflow` resolves to the **caller's** name, not the callee's. A concurrency group built from `${{ github.workflow }}-${{ github.ref }}` therefore collides between caller and callee when a workflow is invoked via `workflow_call` — the nested run's start event cancels its own in-progress parent. Introduced in commit `2545575c82` (PR #8175) applying a 21-workflow-wide pattern uniformly without auditing which of the 21 were `workflow_call`-able; `deploy-dev.yml` was the only one that was, called from `auto-deploy-dev.yml`. Every Auto-Deploy Dev run since 2026-07-05T22:29:14Z had its `deploy` job silently missing.
- `actionlint` catches the first bug directly (lexer error on the exact line); the second bug required run-history diffing (job present pre-regression, absent post-regression) since `actionlint` doesn't flag cross-workflow concurrency-group collisions.

## Key Quotes
> "got unexpected character '#' while lexing expression, expecting 'a'..'z', 'A'..'Z', ..." — actionlint output on the broken `mcp-smoke-tests.yml`, PR #8198 body

## Connections
- [[worldarchitect.ai]] — repo where both regressions landed
- [[GitHubActionsReusableWorkflowConcurrencyCollision]] — new concept extracted from bug 2
- [[GitHubActionsExpressionCommentTrap]] — new concept extracted from bug 1
- [[HostAgnosticCIWorkflows]] — related CI workflow reliability concept
- [[Self-Hosted-Runner-Infra-Flake-vs-Real-Failure]] — adjacent diagnostic discipline (distinguishing real code regressions from infra flake)
