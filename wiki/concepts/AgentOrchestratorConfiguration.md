---
title: "Agent Orchestrator Configuration"
type: concept
tags: [agent-orchestrator, configuration, open-browser, port-conflict, environment-variables]
sources: [anti-pattern_2026-06-10_browser-suppression-configs.md]
last_updated: 2026-06-10
---

Agent Orchestrator (`ao`) uses configuration files named `agent-orchestrator.yaml` to specify project paths, port allocations, and default agent runtimes.

## Configuration Hierarchy
1. **Global Configuration**: Stored in `~/.agent-orchestrator.yaml` or `~/.hermes/agent-orchestrator.yaml`.
2. **Workspace Configuration**: Stored within individual workspaces/worktrees (e.g. `~/.openclaw/workspace/agent-orchestrator.yaml` or in project subdirectories).

## Browser Auto-Open Suppression
To prevent daemon tasks, watchdogs, or test harnesses from launching browser instances on the host when starting or polling ports:
- **YAML suppression**: Explicitly define `openBrowser: false` in the configuration files (both global and workspace-level overrides).
- **Environment Variable**: Export `AO_NO_OPEN_BROWSER=true` globally to act as a fail-safe.
- **CLI Flag**: Pass `--no-open-browser` (or `--no-open`) to skip browser launching on start.
