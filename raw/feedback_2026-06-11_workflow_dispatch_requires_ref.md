---
name: workflow-dispatch-requires-ref
description: "gh api workflow_dispatch POST fails HTTP 422 if `ref` is not in the body; use `-f \"ref=main\"` with `inputs[N]=...` for the value"
metadata:
  type: feedback
---

`gh api -X POST repos/<owner>/<repo>/actions/workflows/<workflow>.yml/dispatches` requires `ref` in the body. Without it, you get HTTP 422 `{"message":"Invalid request. \"ref\" wasn't supplied."}`.

**Verified on 2026-06-11** for `mcp-smoke-tests.yml`:
- BAD: `gh api -X POST .../dispatches -f "inputs[pr_number]=7352" -f "inputs[test_mode]=real"` → 422
- GOOD: `gh api -X POST .../dispatches -f "ref=main" -f "inputs[pr_number]=7352" -f "inputs[test_mode]=real"` → 202 (queued)

**Why:** GitHub's workflow_dispatch API spec requires `ref` (the branch or tag to dispatch from) explicitly, even for workflows that don't need it for the action. The `gh workflow run` CLI adds `ref=main` automatically, but `gh api` does not.

**How to apply:**
- When triggering workflow_dispatch via `gh api` directly, always include `-f "ref=main"` (or the appropriate branch/SHA).
- For `mcp-smoke-tests.yml`, the workflow reads `inputs.pr_number` and `inputs.test_mode`; the `ref` is used as the checkout branch.
- This is the same path as `/smoke` comment trigger but useful when the runner queue is so deep (416+ jobs on `wa-oss-runner-local`) that an automatic /smoke-triggered run may take >1 hour.
