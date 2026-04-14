# PR #3: feat: Add lazy loading foundation for MCP tools (60% context reduction)

**Repo:** jleechanorg/mcp_agent_mail
**Merged:** 2025-11-05
**Author:** jleechan2015
**Stats:** +180/-0 in 2 files

## Summary
Adds foundation for lazy loading MCP tools by categorizing them into core (8 tools) and extended (19 tools) sets. This is Phase 1 of a multi-phase implementation to reduce context usage from ~25k to ~10k tokens (60% reduction).

## Raw Body
## Summary

Adds foundation for lazy loading MCP tools by categorizing them into core (8 tools) and extended (19 tools) sets. This is Phase 1 of a multi-phase implementation to reduce context usage from ~25k to ~10k tokens (60% reduction).

## Problem

MCP Agent Mail exposes 27 tools consuming ~25k tokens (28% of Claude's 200k context window). This limits workspace for actual conversations, especially for power users with multiple MCP servers.

Related: anthropics/claude-code#7336

## Solution - Phase 1: Foundation

### Tool Categorization Constants
- **CORE_TOOLS** (8 tools, ~9k tokens): Essential coordination
  - `health_check`, `ensure_project`, `register_agent`, `whois`
  - `send_message`, `reply_message`, `fetch_inbox`, `mark_message_read`

- **EXTENDED_TOOLS** (19 tools, ~16k tokens): Advanced features
  - Messaging, Search, Identity, Contacts, File Reservations, Macros, Infrastructure

### Metadata & Registry
- **EXTENDED_TOOL_METADATA**: Category and description for each tool
- **_EXTENDED_TOOL_REGISTRY**: Placeholder for future dynamic invocation

## Changes

✅ Added tool categorization constants in `src/mcp_agent_mail/app.py`
✅ Added comprehensive documentation in `docs/LAZY_LOADING.md`
✅ Zero breaking changes - all 27 tools remain functional
✅ Server validated and running

## Context Reduction Potential

| Mode | Tools | Tokens | Reduction |
|------|-------|--------|-----------|
| Extended (current) | 27 | ~25k | - |
| Core (future) | 10 | ~10k | **60%** |

## Implementation Roadmap

**Phase 1: Foundation (This PR)** ✅
- Tool categorization constants
- Metadata for discovery
- Documentation

**Phase 2: Meta-Tools (Next PR)**
- `list_extended_tools` - Discover available extended tools
- `call_extended_tool` - Dynamically invoke extended tools
- Environment variable support (`MCP_TOOLS_MODE`)

**Phase 3: Runtime Filtering (Future)**
- Conditional registration mechanism
- FastMCP enhancement or workaround
- Full context savings validation

## Why Foundation 
