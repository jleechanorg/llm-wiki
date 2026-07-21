---
name: agy-provider-verified-working-on-origin-main
description: "AGY CLI provider verified end-to-end on fresh origin/main (2d65754fa3, 2026-07-17) — real-mode testing_mcp test 2/2 pass, provider_mode=agy, server-owned dice tool executed"
metadata: 
  node_type: memory
  type: project
  originSessionId: 0f6832c8-ae63-471f-9726-5d64345efa4e
---

The AGY CLI provider works on origin/main as of 2026-07-17
(`2d65754fa309bc56d4e34f908de54349ed8923cb`). Verified locally on fresh branch
`dev-agy-verify` via the real-mode integration test (real gunicorn server, real
AGY subprocess LLM calls, no mocks):

```
env -u AGY_PROVIDER_ENABLED TESTING_AUTH_BYPASS=true ALLOW_TEST_AUTH_BYPASS=true \
  PYTHONPATH="$(pwd):$(pwd)/mvp_site" \
  python3 testing_mcp/dice/test_agy_provider_default_integration.py
```

Result: 2/2 scenarios passed. Evidence bundle:
`/tmp/worldarchitect.ai/dev-agy-verify/agy_provider_default/iteration_001`
(20 files with checksums). Load-bearing assertions confirmed from
`scenario_results_checkpoint.json`: `provider_mode=agy`, `provider_type=agy`,
`tool_requests_executed=True` with a real `roll_skill_check` typed-tool request
(AGY requests the tool; server owns dice execution — no Gemini code-exec claim).

Preconditions that were already satisfied on this machine: agy CLI liveness
probe (`agy --print --new-project --sandbox --prompt "Reply with just the word
pong"` → `pong`) and sanitized runtime home at
`~/.cache/worldai/agy-clean-home-v1` (the test's default `AGY_RUNTIME_HOME`).

The remaining delta on `origin/feat/agy-provider-follows-gemini` (15 commits not
in main) is follow-on work, not required for the provider to function on main.
Related: [[agy-provider-default-on-stale-belief]],
[[integrate-sh-fails-in-worktree-when-main-is-checked-out-elsewhere]].
