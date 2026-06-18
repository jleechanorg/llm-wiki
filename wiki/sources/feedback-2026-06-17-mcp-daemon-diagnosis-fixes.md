---
title: "MCP daemon: start_stdio_server env drop + launchd silent death"
type: source
tags: [mcp, launchd, daemon, debugging, claude-code, worldarchitect-ai]
date: 2026-06-17
source_file: feedback_2026-06-17_mcp_daemon_diagnosis_fixes.md
bead: rev-gu8bi
---

## Summary

Two latent bugs in `~/.config/mcp-daemon/start-mcp-daemons.sh` simultaneously broke both the `worldarchitect` MCP (timeout) and the `google-docs` MCP (unable to connect). Bug 1 was a function signature mismatch that silently dropped every stdio server's declared env vars. Bug 2 was a launchd supervisor that stopped re-firing its `StartInterval=300` schedule with no error in the log, leaving crashed MCP daemons unrespawned. Both were diagnosed and fixed on 2026-06-17; the fixes are verified at 11/11 servers up.

## Key Claims

- **`start_stdio_server` parsed env strings from the SERVERS array but never applied them.** The function signature was `(name, cmd, port)`, missing the `envstr` argument. This silently broke every stdio MCP (worldarchitect, context7, gemini-cli, playwright, perplexity, sequential-thinking, memory, ddg, filesystem) — any env vars in their SERVERS entries (PYTHONPATH, WORLDTOOLS_*, etc.) were no-ops at runtime.
- **launchd `StartInterval=300` jobs can silently enter `state = not running, active count = 0`.** No log entry, no error. The job stops re-firing on its schedule, and any process it was supervising dies and is never respawned. Diagnosis requires `launchctl print "gui/$(id -u)/com.jleechan.mcp-daemon"`.
- **The worldarchitect-mcp uv-tool editable install pointed to a deleted worktree path** (`/Users/jleechan/projects/worktree_worker2/mvp_site`). Without `PYTHONPATH` override, the child process crashed on every connection with `ModuleNotFoundError: No module named 'mvp_site'`. The fix was PYTHONPATH (preserves the user's editable install) rather than reinstalling the package.
- **Diagnostic order for "MCP unable to connect":** `start-mcp-daemons.sh status` → `lsof -i :<port>` → tail the log in `~/.config/mcp-daemon/logs/`. If port DOWN with no bash loop, the launchd supervisor is dead → `launchctl unload && load -w`. If port UP but Claude reports timeout, the child is crashing on import → check `Child stderr:` for `ModuleNotFoundError`.

## Key Quotes

> start_stdio_server() was accepting only (name, cmd, port) — env string was parsed by the for entry loop and then thrown away.
>
> Effect: every stdio server (worldarchitect, context7, gemini-cli-mcp, playwright, perplexity, sequential-thinking, memory, ddg, filesystem) had its declared env vars IGNORED at runtime.

> Plist com.jleechan.mcp-daemon.plist uses RunAtLoad=true, KeepAlive=false, StartInterval=300. After a clean RunAtLoad start at 11:08:31, the job stopped re-firing on its 5-min interval. launchctl print showed state = not running, active count = 0. No log error.

## Connections

- [[WorktreeWorkflow]] — relevant for the worktree_worker2 deletion that orphaned the editable install path; worktree churn leaves stale references in installed packages
- [[Hermes Agent Setup]] — the MCP daemon config lives under `~/.config/mcp-daemon/` and is shared across all Hermes-managed sessions
- [[launchd-plist-template]] — the related skill defines the install/portability rules for launchd plists; this bug is a case where the template's `StartInterval` pattern is insufficient and needs `KeepAlive` or a watchdog
- [[IntegrateScriptResetGuard]] — both bugs are anti-patterns in long-lived automation: silent partial failures that surface only when a downstream user reports symptoms
- [[Claude Code MCP Architecture]] — the stdio-vs-HTTP transport split is what made the env string dropping matter; HTTP transport applies env, stdio did not (until the fix)

## Fix Summary

| Bug | File | Change |
|---|---|---|
| start_stdio_server drops env | `~/.config/mcp-daemon/start-mcp-daemons.sh` | Function signature: `(name, cmd, port, envstr)`; env applied via `IFS=';'; for envpair in ...; do export KEY=val; done` (mirrors `start_http_server`); call site updated to pass `"${envstr:-}"` |
| worldarchitect PYTHONPATH | same file, SERVERS array | Added `PYTHONPATH=/Users/jleechan/worldarchitect.ai` to the worldarchitect env string |
| launchd supervisor dead | `~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist` (no edit yet) | `launchctl unload ~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist && launchctl load -w ...` to re-trigger RunAtLoad; durable follow-up: add `KeepAlive` or external watchdog |

## Verification

- `bash ~/.config/mcp-daemon/start-mcp-daemons.sh status` → 11/11 servers running
- `curl -X POST http://127.0.0.1:8010/mcp initialize` → `{"result":{"serverInfo":{"name":"worldai-mcp-stdio","version":"1.0.0"}}}`
- google-docs log shows `StreamableHttp → Child: initialize` → OAuth flow initiated (server healthy)
- `bash -n ~/.config/mcp-daemon/start-mcp-daemons.sh` → syntax OK
- `python3 -c "from mvp_site.worldai_mcp_stdio import main"` (with PYTHONPATH) → imports cleanly

## Pattern to Apply Forward

When adding env vars to any SERVERS array entry, ALWAYS verify the matching `start_*_server` function accepts and applies `envstr`. The http path does; the stdio path did not (until this fix). When debugging a "MCP unable to connect" error, follow the diagnostic order above before assuming the daemon needs restart.
