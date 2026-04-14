# MCP Server Context Optimization Analysis

**Date:** 2026-04-05
**Session:** Agent Orchestrator fork worktree

---

## MCP Servers Inventory

### Source Locations

| Source File | Servers Defined |
|---|---|
| `~/.claude/plugins/cache/claude-commands-marketplace/claude-commands/1.0.0/.claude/settings.json` | chrome-superpower, sequential-thinking, context7, gemini-cli-mcp, ddg-search, memory-server, filesystem, grok-mcp, perplexity-ask, render, serena, ios-simulator-mcp, worldarchitect |
| `~/.claude/settings.json` | mcp-agent-mail |
| `~/.claude/plugins/cache/thedotmack/claude-mem/10.5.4/.mcp.json` | mcp-search |
| `~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/slack/.mcp.json` | slack (OAuth HTTP to mcp.slack.com) |

### Slack MCP Origin (was unknown)

**Found:** Slack is configured in the `claude-plugins-official` marketplace external plugin:
`~/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/slack/.mcp.json`

It uses OAuth HTTP transport to `https://mcp.slack.com/mcp` with client ID `1601185624273.8899143856786`.

---

## Tool Counts (from deferred tools list)

| Server | Prefix | Tool Count | Status |
|---|---|---|---|
| ddg-search | `mcp__ddg-search__` | 3 | Connected |
| filesystem | `mcp__filesystem__` | 14 | Connected |
| ios-simulator-mcp | `mcp__ios-simulator-mcp__` | 12 | Connected |
| mcp-agent-mail | `mcp__mcp-agent-mail__` | 17 | Connected |
| perplexity-ask | `mcp__perplexity-ask__` | 1 | Connected |
| slack | `mcp__slack__` | 11 | Connected |
| worldai | `mcp__worldai__` | 16 | Connected |
| **TOTAL connected** | | **74** | |

### Servers NOT appearing in deferred tools (not connected / failed to start)

| Server | Likely Reason |
|---|---|
| chrome-superpower | Plugin binary may not be built/available |
| sequential-thinking | npx server, likely not started |
| context7 | npx server, likely not started |
| gemini-cli-mcp | npx server, likely not started |
| memory-server | npx server, likely not started |
| grok-mcp | Requires XAI_API_KEY env var |
| render | Requires RENDER_API_KEY, HTTP type |
| serena | uvx/git dependency, may fail to start |
| mcp-search | thedotmack plugin script |

These 9 servers are defined but NOT connected in this session. They consume zero runtime context (no deferred tools registered). However, their config definitions still occupy space in the settings files loaded at session init.

---

## Classification

### KEEP (actively used in core workflows)

| Server | Tools | Justification |
|---|---|---|
| **worldai** | 16 | Core project -- WorldArchitect.AI game engine, campaigns, deployment |
| **mcp-agent-mail** | 17 | Inter-agent coordination, core to AO worker dispatch |
| **slack** | 11 | Notifications, team coordination, Stop hooks reference Slack |
| **ddg-search** | 3 | Web search for research tasks |
| **perplexity-ask** | 1 | AI-powered search, research complement |
| **filesystem** | 14 | File operations on ~/projects (redundant with built-in Read/Write/Glob but used by some workflows) |
| **KEEP subtotal** | **62** | |

### TRIM (rarely/never used, consuming context)

| Server | Tools | Justification |
|---|---|---|
| **ios-simulator-mcp** | 12 | No iOS development in AO or WorldAI workflows. 12 tools registered as deferred -- each tool name/description consumes tokens in every system-reminder block. |
| **chrome-superpower** | 0 (not connected) | Not connected this session. When connected, overlaps with Playwright MCP and built-in browser tools. |
| **sequential-thinking** | 0 (not connected) | Think tool is built-in to Claude. Redundant. |
| **context7** | 0 (not connected) | Documentation lookup -- rarely used vs built-in WebFetch. |
| **gemini-cli-mcp** | 0 (not connected) | Cross-model querying -- /secondo skill handles this already. |
| **memory-server** | 0 (not connected) | MCP memory server -- redundant with MEMORY.md + mem0 hooks already in place. |
| **grok-mcp** | 0 (not connected) | Requires API key, cross-model -- covered by /secondo. |
| **render** | 0 (not connected) | Cloud deployment -- not used in current workflows. |
| **serena** | 0 (not connected) | Code intelligence server -- not connected, Claude's built-in tools cover this. |
| **mcp-search** | 0 (not connected) | thedotmack plugin search -- not connected. |
| **TRIM subtotal** | **12 connected + 0 others** | |

---

## Token Impact Estimate

### Deferred tools context cost

Each deferred tool occupies approximately **15-25 tokens** in the system-reminder block (tool name with prefix). Connected tools with full schemas fetched on-demand add more when invoked, but the deferred listing itself is the persistent cost.

| Category | Deferred Tool Entries | Est. Tokens (persistent) |
|---|---|---|
| KEEP servers | 62 tools | ~1,200 tokens |
| TRIM servers (connected) | 12 tools (ios-simulator-mcp) | ~240 tokens |
| TRIM servers (not connected) | 0 tools | 0 tokens (config-only) |

### Config definition cost

Each MCP server definition in `settings.json` occupies ~50-150 tokens when the file is loaded. With 13 servers in the plugin settings file:

| | Servers | Est. Config Tokens |
|---|---|---|
| KEEP | 6 | ~500 |
| TRIM | 7+ | ~600 |

### Savings from trimming

| Action | Token Savings | Impact |
|---|---|---|
| Remove ios-simulator-mcp from plugin settings | ~240 tokens/turn (deferred list) + ~80 tokens (config) | **High** -- only TRIM server actually connected and injecting tools |
| Remove 8 other TRIM servers from plugin settings | ~600 tokens (config load, one-time) | **Low** -- these aren't connecting anyway |
| **Total potential savings** | **~920 tokens** | Modest but clean |

### Qualitative benefits of trimming

1. **Reduced system-reminder noise** -- 12 fewer `mcp__ios-simulator-mcp__*` entries in every deferred tools block
2. **Faster session startup** -- fewer MCP server connection attempts (npx/uvx spawns that timeout)
3. **Cleaner tool routing** -- model spends zero attention on irrelevant tool options
4. **Reduced permission surface** -- fewer tools that could be accidentally invoked

---

## Recommendations

### Priority 1: Remove ios-simulator-mcp
This is the only TRIM server that is actually connected and injecting 12 deferred tools into every system-reminder. Removing it from the plugin settings eliminates persistent per-turn context waste.

**File:** `~/.claude/plugins/cache/claude-commands-marketplace/claude-commands/1.0.0/.claude/settings.json`
**Action:** Delete the `"ios-simulator-mcp"` key from `mcpServers`

### Priority 2: Remove non-connecting servers
These 8 servers fail to connect but still cause startup delays (npx/uvx spawn attempts) and occupy config space:
- sequential-thinking
- context7
- gemini-cli-mcp
- memory-server
- grok-mcp
- render
- serena
- chrome-superpower

### Priority 3: Evaluate filesystem redundancy
The `filesystem` MCP server (14 tools) overlaps significantly with Claude Code's built-in Read, Write, Glob, and Bash tools. It is scoped to `~/projects` only. Consider whether any workflow actually uses `mcp__filesystem__*` tools instead of the built-ins.

### Not recommended to trim
- **mcp-search** (thedotmack plugin) -- already not connecting, removing requires editing a different plugin's `.mcp.json`
- **slack** -- actively used for team coordination despite not being in the original plugin settings list

---

## Summary

| Metric | Value |
|---|---|
| Total MCP servers configured | 16 |
| Actually connected this session | 7 |
| Total deferred tools registered | 74 |
| Tools from TRIM servers | 12 (all ios-simulator-mcp) |
| Estimated token savings from full trim | ~920 tokens |
| Startup time savings | Eliminates ~8 failed npx/uvx spawn attempts |
