---
title: "Claude Code MCP Tool Search"
type: concept
tags: [claude-code, mcp, tool-search]
date: 2026-07-07
---

## Definition

Anthropic's mechanism in Claude Code for deferring MCP tool schemas out of context until actually needed, controlled by the `ENABLE_TOOL_SEARCH` env var. Default (unset) is full deferral; `auto`/`auto:N` is a percentage-of-context threshold mode; `true`/`false` force always-defer / never-defer.

## Related

- [[feedback-2026-07-07-mcp-tool-search-default-and-config-dir-trap]] — the session that verified this against primary docs with a real token A/B
