# PR #3: feat: add cmux MCP server for terminal control

**Repo:** jleechanorg/cmux
**Merged:** 2026-03-12
**Author:** jleechan2015
**Stats:** +5378/-1 in 6 files

## Summary
- Add MCP server implementation to control cmux terminals, workspaces, windows, and tabs
- Includes Python and JavaScript server implementations
- Provides tools for steering and interacting with cmux programmatically

## Raw Body
## Summary
- Add MCP server implementation to control cmux terminals, workspaces, windows, and tabs
- Includes Python and JavaScript server implementations
- Provides tools for steering and interacting with cmux programmatically

## Changes
- Add `scripts/cmux_mcp_server.py` (Python MCP server)
- Add `scripts/cmux-mcp-server.mjs` (JavaScript MCP server)
- Update package.json with MCP server entry
- Update README with MCP server documentation

## Testing
- MCP server can be run standalone: `node scripts/cmux-mcp-server.mjs` or `python scripts/cmux_mcp_server.py`
- Provides tools: list_workspaces, list_terminals, send_text, create_workspace, etc.

## Known Limitations
- Requires cmux to be running with IPC enabled
- Some features may require additional cmux API exposure

<!-- COPILOT_TRACKING_START -->
## Copilot Review Tracking

**Last run:** 2026-03-08 | **Total comments:** 19 | **New this run:** 19 | **Carried forward:** 0

| # | Comment ID | Reviewer | File:Line | Severity | Status | Summary |
|---|-----------|----------|-----------|----------|--------|---------|
| 1 | 2902197455 | coderabbitai | cmux-mcp-server.mjs:156 | CRITICAL | Deferred | `runCmux` error at mjs:154-156 joins raw argv including `--socket-password` value into the error message, leaking credentials to HTTP logs and MCP clients. Fix: redact password value before argv.join. Deferred — edit permissions not granted this run; ~3-line fix ready for next run. |
| 2 | 2902197460 | coderabbitai | cmux-mcp-server.mjs:865 | CRITICAL | Deferred | `httpServer.listen(config.httpPort, config.httpHost)` at mjs:861 accepts any host including non-loopback, exposing terminal control/screen-read endpoints. Fix: validate host is loopback or require CMUX_MCP_ALLOW_REMOTE=1 opt-in. Deferred — edit permissions not granted; ~4-line fix ready. |
| 3 | 2902188079 | cursor[bot] | cmux-mcp-server.mjs:62 | BLOCKING | Deferred | `compactArgs` at mjs:60-62 filters undefined values individually from interleaved flag-value pairs
