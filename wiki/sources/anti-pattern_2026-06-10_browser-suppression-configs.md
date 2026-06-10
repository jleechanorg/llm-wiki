---
title: "Browser Auto-Open Suppression and Port Conflict Resolution"
type: source
tags: [agent-orchestrator, configuration, open-browser, port-conflict, launchd, shell-profiles, build-binary]
source_file: "raw/anti-pattern_2026-06-10_browser-suppression-configs.md"
sources: []
last_updated: 2026-06-10
---

## Summary
Background agents, watchdogs, and test harnesses frequently launch instances of the `ao` command line tool on dynamic ports (e.g. port 3000). If configuration overrides (such as workspace-specific `agent-orchestrator.yaml` files) customize the port but omit the `openBrowser` field, they default to launching the browser on the host system to `http://localhost:3000/`. A three-layer suppression mechanism (YAML config, env var, CLI flag) is available but must be correctly populated and built to take effect.

## Key Claims
- **Config Override Priority**: Workspace-level configuration files (`agent-orchestrator.yaml`) that customize `port` will override default suppression settings unless they explicitly define `openBrowser: false`.
- **Three-Layer Suppression**: Auto-open browser is suppressed if `openBrowser: false` is in YAML config, `AO_NO_OPEN_BROWSER=1|true` is in environment variables, or `--no-open-browser` is passed as a CLI flag.
- **Build Invariant**: Merging PR fixes (e.g. PR #669) does not immediately update the executed binaries in the environment. Local binaries (`/Users/jleechan/bin/ao`) must be rebuilt using `npm run build` after merges.

## Reusable Rules
1. **Always declare `openBrowser: false`** in any workspace-specific `agent-orchestrator.yaml` configuration files that customize ports.
2. **Export `AO_NO_OPEN_BROWSER=true`** globally in all user shell profile startup files (`~/.bashrc`, `~/.zshrc`, `~/.bash_profile`, `~/.profile`) to serve as a fail-safe.
3. **Rebuild the project** using `npm run build` after pulling/merging updates to ensure local launcher binaries are fully up to date.

## Connections
- [[AgentOrchestratorConfiguration]] — Workspace configuration defaults.
- [[WatchdogArchitecture]] — Background daemon process execution environment.
- [[HeadlessTesting]] — CLI execution in non-interactive environment.

## Contradictions
- None.
