---
name: gg-cascade-from-pr-comments
description: AO worker PR comments (e.g. @coderabbitai re-review) trigger GG re-runs that cascade-cancel each other via cancel-in-progress
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: 9cb0a4f4-d2f7-4033-96aa-909ce5c4a2b2
---

When an AO worker posts comments on a PR (e.g. `@coderabbitai re-review please`), each comment triggers a new Green Gate run. The GG workflow has `concurrency: cancel-in-progress: true`, so each new triggered run immediately cancels the previous pending run.

**Observed (2026-06-15):** PR #7578 had 5+ consecutive GG runs all cancelled within minutes of each other on the same SHA `695caf24`. wa-2358 had been posting multiple CR re-review pings and other comments.

**Impact:** The GG run never completes as long as new comments keep arriving. The cascade stops naturally when the worker goes idle.

**Why:** Green Gate triggers on `issue_comment`, `pull_request_review`, and `push` events. Any PR comment (not just `/green` commands) can trigger it. The cancel-in-progress concurrency setting ensures only one run proceeds at a time, but a cascade of comments keeps re-cancelling.

**How to apply:**
- When AO workers are posting comments on a PR, expect GG runs to be in a cancel cascade
- Wait for the worker to go IDLE before checking GG status
- Do not retry GG manually while a worker is still active on the PR
- If a worker posts `@coderabbitai re-review please`, that alone will trigger a new GG run

**References:** PR #7578 (fix/green-gate-add-checkout), SHA 695caf24, 2026-06-15 ~01:00–01:17Z.
