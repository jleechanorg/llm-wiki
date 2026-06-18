---
name: mcp-daemon-stdio-env-drop-and-launchd-silent-death
description: "Two latent bugs in ~/.config/mcp-daemon/start-mcp-daemons.sh — start_stdio_server silently drops env string, and launchd job can enter state=not-running with no obvious error."
type: feedback
bead: rev-gu8bi
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b12ac36a-2b5b-4ec8-b1c2-1d05fb5a4703
---

# MCP daemon: two latent bugs

**When:** 2026-06-17 — /mcp reported worldarchitect timed out + google-docs unable to connect.

**Bug 1: `start_stdio_server` silently drops env string**
- `SERVERS` array entries are `name|cmd|port|transport|env` (5 fields).
- `start_http_server` accepts `(name, cmd, port, envstr)` and applies it.
- `start_stdio_server` was accepting only `(name, cmd, port)` — env string was parsed by the `for entry` loop and then thrown away.
- Effect: every stdio server (worldarchitect, context7, gemini-cli-mcp, playwright, perplexity, sequential-thinking, memory, ddg, filesystem) had its declared env vars IGNORED at runtime. PYTHONPATH/WORLDTOOLS_*/etc. in the SERVERS array were no-ops for stdio transport.
- **Fix:** `start_stdio_server` now takes `${envstr:-}` and applies it via the same `IFS=';'; for envpair in ...` loop as `start_http_server`. Call site updated to pass it.

**Bug 2: launchd `StartInterval` job can silently die**
- Plist `com.jleechan.mcp-daemon.plist` uses `RunAtLoad=true`, `KeepAlive=false`, `StartInterval=300`.
- After a clean `RunAtLoad` start at 11:08:31, the job stopped re-firing on its 5-min interval. `launchctl print` showed `state = not running, active count = 0`. No log error.
- This means the supervisor is *not* durable — when the prior supergateway process for any daemon crashed, nothing respawned it.
- Symptom: server DOWN forever, no error, no log entry beyond the last successful "ready" line.
- **Workaround used:** `launchctl unload ~/Library/LaunchAgents/com.jleechan.mcp-daemon.plist && launchctl load -w ...` triggers `RunAtLoad` and brings everything back.
- **Durable fix needed:** consider adding `KeepAlive=true` (respawns on crash) or a watchdog. The `StartInterval=300` alone is fragile.

**Related — worldarchitect-mcp editable install was pointing at a dead worktree:**
- `~/.local/share/uv/tools/worldarchitect-mcp/lib/python3.13/site-packages/__editable___worldarchitect_mcp_1_0_0_finder.py` mapped `mvp_site` → `/Users/jleechan/projects/worktree_worker2/mvp_site` (a deleted worktree).
- Without `PYTHONPATH` override, the child process crashed on every connection with `ModuleNotFoundError: No module named 'mvp_site'`. The fix was PYTHONPATH, not the editable install, because the user wants to retain the editable install as their source of truth. Long-term: re-run `uv tool install --editable /Users/jleechan/worldarchitect.ai` to repoint the .pth.

**How to apply:**
- When debugging a "MCP connection failed" or "MCP timed out" error, FIRST run `bash ~/.config/mcp-daemon/start-mcp-daemons.sh status` to see if the daemon is up, then `lsof -i :<port>` and `tail` the relevant log in `~/.config/mcp-daemon/logs/`.
- If the port is DOWN and the bash restart loop is missing, the launchd supervisor is dead — kickstart with `launchctl unload && launchctl load -w`.
- If the port is UP but Claude reports timeout, the child is likely crashing — check log for `Child stderr:` and `ModuleNotFoundError`/`import` errors.
- Don't add new env vars to a SERVERS array stdio entry without first verifying `start_stdio_server` actually applies them (it didn't, before the fix).
