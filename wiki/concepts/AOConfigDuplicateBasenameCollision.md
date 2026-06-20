---
title: "AO Config Duplicate Basename Collision"
type: concept
tags: [agent-orchestrator, configuration, validation, verification, anti-pattern]
sources: [feedback-2026-06-14-ao-duplicate-project-id-config-bug.md]
last_updated: 2026-06-14
---

When the user's repo has BOTH `~/.hermes/agent-orchestrator.yaml` AND `~/agent-orchestrator.yaml` (where the latter is a symlink to `~/.hermes_prod/agent-orchestrator.yaml` or another file with the same basename), the `findRepoLocalConfigOverlay` helper walks up from cwd, follows the symlink, and treats it as a separate config file with the same basename as the staging config. The merge step then collides on the `projects.<basename>` key and `ao spawn` fails with `Duplicate project ID detected: "<basename>"` validation error.

## Trigger Condition
- `~/agent-orchestrator.yaml` is a symlink whose target's basename matches any other loaded config's basename (e.g. both are `agent-orchestrator.yaml`)
- AO loads both at startup; the merge sees two `projects.<basename>` blocks with the same key

## Symptom
```
Error: Duplicate project ID detected: "claude-commands"
```
(or similar basename)

## Fix
1. Remove the symlink — one config per user scope (`~/.hermes/agent-orchestrator.yaml` OR `~/agent-orchestrator.yaml`, not both)
2. OR rename the staging config to a unique basename that won't collide

## Workaround for verification (when fix is out of scope)
For env-var or config-pin fixes where the plugin's return value is the test target, **import the built plugin and call it directly** with simulated `launchConfig` objects. This exercises the same code path the runtime uses (`getEnvironment()` is the exact return-value source for `tmux -e KEY=VALUE` and `child_process.env`):

```javascript
import plugin from "./packages/plugins/agent-antigravity/dist/index.js";
const env = plugin.create().getEnvironment({
  sessionId: "wa-9001",
  projectConfig: { path: "/Users/jleechan/project_agento/agent-orchestrator" },
  workspacePath: "/Users/jleechan/project_agento/agent-orchestrator",
});
// Assert env.COLIMA_HOME, env.DOCKER_HOST, etc. directly
```

This is a **Layer 2** end-to-end test (real plugin code, real env, real config) — NOT a Layer 1 mocked unit test. Document the workaround in the PR body's Testing section as the primary multi-worker evidence.

## Scope discipline
- Do not silently fix this in a plugin PR — it touches the user's managed config (Hermes staging layer) and is a separate concern.
- Open a dedicated config-cleanup PR with explicit scope, OR document the workaround and move on.
- If the user explicitly wants it fixed, the fix is <10 lines (remove the symlink in scripts/setup.sh, or check for it in a `ao doctor` health check).

## Detection
```bash
ls -la ~/agent-orchestrator.yaml
# If symlink to ~/.hermes_prod/agent-orchestrator.yaml, this is the trigger.
```

## Related
- [AgentOrchestratorConfiguration](AgentOrchestratorConfiguration.md) — the layered config model
- [ConfigFirstPrinciple](ConfigFirstPrinciple.md) — config > code principle (this is a config violation, not a code one)
- [[evidence-review]] — when this bug blocks verification, /er verdict can still PASS if direct-plugin-invocation evidence is documented
