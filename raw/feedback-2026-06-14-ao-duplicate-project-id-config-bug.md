---
name: feedback-2026-06-14-ao-duplicate-project-id-config-bug
description: "Live `ao spawn` fails with 'Duplicate project ID detected' when `~/agent-orchestrator.yaml` is a symlink to `~/.hermes_prod/agent-orchestrator.yaml` — findRepoLocalConfigOverlay merges BOTH and produces duplicate basenames. Pre-existing, not caused by colima fix."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8e1493a5-115a-4b66-9790-42973f21fc27
---

`ao spawn` fails with `Duplicate project ID detected: "<basename>"` (seen: `claude-commands`) when the user's repo has BOTH `~/.hermes/agent-orchestrator.yaml` AND `~/agent-orchestrator.yaml` (where the latter is a symlink to the former or to `~/.hermes_prod/agent-orchestrator.yaml`). The `findRepoLocalConfigOverlay` helper walks up from cwd, finds the symlink, and treats it as a separate config file with the same basename as the staging config — the merge step then collides on the `projects.<basename>` key.

**Why this blocked PR #686 verification** (2026-06-14):
- Direct multi-worker verification via `ao spawn` was unavailable due to this bug
- Worked around by importing the built plugin and invoking `getEnvironment()` directly with 3 simulated `launchConfig` objects (`/tmp/multi-worker-colima-test.mjs`)
- The plugin's `getEnvironment()` is the **exact code path** the runtime uses when spawning a worker — direct invocation is functionally equivalent for env-var assertion purposes (no runtime layer between plugin return and the env vars we observe)
- The test is not a "no-op unit test" — it executes real plugin code against real config + real `os.homedir()` and observes what the runtime would observe

**How to identify the bug**:
```bash
ls -la ~/agent-orchestrator.yaml
# If symlink to ~/.hermes_prod/agent-orchestrator.yaml, this is the trigger.
# Fix: remove the symlink (one config per user scope) or rename the staging config
# to a unique basename.
```

**How to apply**:
- For env-var or config-pin fixes where the plugin's return value is what the runtime consumes, **import the built plugin and call it directly** when `ao spawn` is blocked. This is a Layer 2 end-to-end test (real plugin code, real env, real config), not a Layer 1 unit test.
- Do NOT try to "fix" the duplicate project ID bug in the same PR as an env-var fix — it's a separate concern (config layer, not plugin layer) and changing it touches the user's managed config.
- Document the workaround in the PR body's Testing section as the primary multi-worker evidence when live `ao spawn` is blocked.

**Why**: PR #686 colima fix (2026-06-14) had to prove the fix worked with multiple AO workers. Live `ao spawn` was blocked by this pre-existing config bug. Direct plugin invocation provided 3-worker evidence (wa-9001, wa-9002, wa-9003) that all assertions pass: COLIMA_HOME = user home, no .colima/ in session home, DOCKER_HOST set on darwin, DOCKER_HOST key absent on non-darwin. /er verdict: PASS. The bug itself is documented here for future sessions; do not silently let it block future PRs.
