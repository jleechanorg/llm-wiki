---
name: Browser Auto-Open Suppression and Port Conflict Resolution
description: Gating browser opening on multi-port environments and ensuring workspace configs disable openBrowser.
type: reference
bead: jleechan-cvum
---

# Browser Auto-Open Suppression and Port Conflict Resolution

## Context
When running `ao start` or `ao dashboard` in a multi-project/multi-worktree workspace setup, background agents, watchdogs, or test suites may spin up instances of `ao` on various ports (e.g. port 3000). If `openBrowser` is not explicitly set to `false` in their specific workspace configurations, they default to opening browser tabs on the host system to `http://localhost:3000/`.

## Technical Detail
1. **Resolution Priority**: The browser-opening logic `waitForPortAndOpen()` polls the target port and fires a shell spawn command (e.g. `open <url>` on macOS) once the port is occupied.
2. **Three-Layer Suppression**: PR #669 introduced a three-layer suppression mechanism:
   - YAML config field: `openBrowser: false`
   - Env var: `AO_NO_OPEN_BROWSER=1` (or `true`)
   - CLI flag: `--no-open-browser` (or `--no-open`)
3. **Workspace Override Gap**: If a project/workspace has a local `agent-orchestrator.yaml` that overrides the default `port` (e.g. `port: 3000`), but does not define `openBrowser: false`, it defaults to `true`. This bypasses any global setting in the main config file (`~/.agent-orchestrator.yaml`).
4. **Binary Rebuild**: Built CLI binaries (`/Users/jleechan/bin/ao`) must be explicitly rebuilt via `npm run build` after pulling/merging fixes to prevent processes from using older versions of the CLI that do not implement the suppression logic.

## Reusable Pattern
- **Workspace Config**: Always explicitly declare `openBrowser: false` at the top level of any `agent-orchestrator.yaml` workspace configuration files to prevent background sessions from spawning browser tabs.
- **Fail-Safe Exports**: Export `AO_NO_OPEN_BROWSER=true` globally in all shell profiles (`~/.bashrc`, `~/.zshrc`, etc.) so that it propagates to background processes, launchd jobs, and tmux/cmux sessions.
- **Post-Merge Build**: Always rebuild the monorepo using `npm run build` immediately after pulling or merging pull requests.

## References
- PR #669 (Browser auto-open suppression)
- Bead: `jleechan-cvum`
