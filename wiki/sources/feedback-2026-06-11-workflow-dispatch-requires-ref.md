---
title: "Workflow dispatch requires --ref for branch runs (2026-06-11)"
type: source
tags: [ci, github-actions, gh-cli, workflow-dispatch, mcp-smoke-tests]
date: 2026-06-11
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-11_workflow_dispatch_requires_ref.md
---

## Summary
`gh api -X POST repos/<owner>/<repo>/actions/workflows/<workflow>.yml/dispatches` returns HTTP 422 `{"message":"Invalid request. \"ref\" wasn't supplied."}` if the body omits `ref`. The `gh workflow run` CLI injects `ref=main` automatically, but `gh api` does not. Verified against `mcp-smoke-tests.yml`: bad call without `ref=main` returned 422; good call with `-f "ref=main"` returned 202.

## Key Claims
- `gh api workflow_dispatch` requires `ref` in the body, even when the workflow does not use it as a checkout ref.
- `gh workflow run` adds `ref=main` automatically; `gh api` does not.
- Workflow `mcp-smoke-tests.yml` accepts inputs `pr_number` and `test_mode`; `ref` is used as the checkout branch.
- This is the same path as `/smoke` comment trigger and is useful when the runner queue is so deep (416+ jobs on `wa-oss-runner-local`) that automatic smoke-triggered runs may take >1 hour.

## Key Quotes
> "BAD: `gh api -X POST .../dispatches -f "inputs[pr_number]=7352" -f "inputs[test_mode]=real"` → 422" — verified failure

> "GOOD: `gh api -X POST .../dispatches -f "ref=main" -f "inputs[pr_number]=7352" -f "inputs[test_mode]=real"` → 202 (queued)" — verified success

> "The `gh workflow run` CLI adds `ref=main` automatically, but `gh api` does not." — root cause

## Connections
- [[WorktreeWorkflow]] — local workflow dispatch from worktree to a branch
- [[SelfHostedRunners]] — runner queue depth motivates manual dispatch path
- [[McpSmokeTests]] — workflow that was used for verification
- [[GreenGate]] — dispatch entrypoint for green-gate refresh
- [[SkepticGate]] — alternate gate that can be re-dispatched the same way
