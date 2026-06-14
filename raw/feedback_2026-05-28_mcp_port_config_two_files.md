---
name: feedback_2026-05-28_mcp_port_config_two_files
description: MCP server port URLs must be updated in BOTH ~/.claude/settings.json AND ~/.claude.json — updating only one leaves claude mcp list reading the old port
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: f75604c7-21c6-490b-9412-fc02039959a8
---

MCP server URL config lives in two separate files that both feed `claude mcp list`:
1. `~/.claude/settings.json` (mcpServers block)
2. `~/.claude.json` (top-level mcpServers key)

The binary reads `.claude.json` first. If only `settings.json` is updated, `claude mcp list` still reports the old port from `.claude.json`.

**Why:** Discovered 2026-05-28 when moving playwright-mcp from 8003→8012. Updated settings.json, but `claude mcp list` kept showing 8003 and `✗ Failed to connect`. Root cause: `.claude.json` still had the old entry.

**How to apply:** Any time you change an MCP server port or URL, run:
```python
import json
for path in ['/Users/jleechan/.claude/settings.json', '/Users/jleechan/.claude.json']:
    d = json.load(open(path))
    # update d['mcpServers'][name]['url'] in both
```
Or use: `grep -n "playwright-mcp\|<server>" ~/.claude/settings.json ~/.claude.json` to verify both are in sync.
