---
title: "2026-06-14 AO Duplicate Project ID Config Bug"
type: source
tags: ["feedback", "agent-orchestrator", "config", "verification"]
date: 2026-06-14
source_file: raw/feedback-2026-06-14-ao-duplicate-project-id-config-bug.md
---

## Summary
Pre-existing AO config bug: when `~/agent-orchestrator.yaml` is a symlink to `~/.hermes_prod/agent-orchestrator.yaml`, the `findRepoLocalConfigOverlay` helper merges BOTH configs and the merge step collides on `projects.<basename>` (seen: "claude-commands"), causing `ao spawn` to fail with "Duplicate project ID detected" validation error. Discovered 2026-06-14 during PR #686 colima-fix verification; the bug is in the user's managed config layer, not in the plugin. Workaround: import the built plugin and call `getEnvironment()` directly with simulated `launchConfig` objects — exercises the same code path the runtime uses.

## Key Claims
- Live `ao spawn` is blocked when `~/agent-orchestrator.yaml` is a symlink to `~/.hermes_prod/agent-orchestrator.yaml` (or any second managed config with the same basename as `~/.hermes/agent-orchestrator.yaml`).
- The bug is in `findRepoLocalConfigOverlay` (config-loader), not in the agent plugin layer.
- Direct plugin invocation is functionally equivalent for env-var / config-pin verification — the plugin's `getEnvironment()` is the **exact** code path the runtime uses when spawning a worker.
- Do not silently fix this in a plugin PR; it touches the user's managed config and is a separate concern.
- The workaround is a **Layer 2** end-to-end test (real plugin code, real env, real config) — NOT a Layer 1 mocked unit test.

## Key Quotes
> "For env-var or config-pin fixes where the plugin's return value is what the runtime consumes, import the built plugin and call it directly when ao spawn is blocked. This is a Layer 2 end-to-end test (real plugin code, real env, real config), not a Layer 1 unit test."

## Connections
- [[AgentOrchestrator]]
- [[findRepoLocalConfigOverlay]]
- [[PR686ColimaFix]]
- [[evidence-review]]
- [[AOSpawn]]
