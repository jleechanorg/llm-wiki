---
title: "MCP tool-search default is already full-deferral + CLAUDE_CONFIG_DIR orphaned-file trap"
type: source
tags: [claude-code, mcp, tool-search, token-cost, config]
date: 2026-07-07
source_file: raw/feedback_2026-07-07_mcp_tool_search_default_and_config_dir_trap.md
---

## Summary

Verified against Anthropic's official docs (`code.claude.com/docs/en/mcp`) that Claude Code's MCP Tool Search feature defers ALL tool schemas by default when `ENABLE_TOOL_SEARCH` is unset — not the `auto` percentage-threshold mode, which is a separate, less-deferred option. Real measured A/B on jeff-ubuntu (same 15-MCP-server config, only the setting changed): 80,012 tokens with deferral off vs 42,259 tokens with deferral on, a 47% reduction. Fixed by explicitly pinning `ENABLE_TOOL_SEARCH=true` in `settings.json`. Separately discovered that `CLAUDE_CONFIG_DIR=~/.claude` (set explicitly) targets an orphaned duplicate `~/.claude/.claude.json` file, not the real `~/.claude.json` used by the plain `claude` command with no env override.

## Key Claims

- `ENABLE_TOOL_SEARCH` unset = full deferral (tool names + brief server instructions only at session start; full schemas load on demand and stay resident once loaded for that session).
- `auto` mode is a DIFFERENT, less-deferred mode: loads schemas upfront if they'd fit within 10% of the context window, defers only the overflow.
- Deferral is per-TOOL, not per-server — using one tool from a 14-tool server doesn't pull in the other 13.
- `CLAUDE_CONFIG_DIR=/Users/jleechan/.claude` (explicit) ≠ unset — creates/edits a separate nested `.claude.json` file with independently drifting state.

## Key Quotes

> "MCP tools are deferred rather than loaded into context upfront, and Claude uses a search tool to discover relevant ones when a task needs them. Only the tools Claude actually uses enter context." — code.claude.com/docs/en/mcp

## Connections

- [[claude-code-mcp-configuration]] — the broader MCP config/scoping concepts this fits into
- [[sidekick-same-name-respawn-race]] — a separate harness-durability finding from the same session
