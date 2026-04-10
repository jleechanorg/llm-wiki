---
title: "Tool Selection Optimization"
type: concept
tags: [optimization, tool-routing, token-reduction]
sources: ["context-optimization-implementation-plan-phases-2-4"]
last_updated: 2026-04-08
---

## Description
Phase 2 of the Context Optimization Implementation Plan focused on enforcing Serena MCP priority routing to reduce context consumption by 30-40% through smarter tool selection.

## Key Components

### Pre-Command Optimization Hook
File: `.claude/hooks/pre_tool_optimize.py`
- Intercepts tool calls and suggests optimizations
- Analyzes tool request patterns in real-time

### Tool Hierarchy
1. Serena MCP — Code analysis and symbol search
2. grep_targeted — Pattern search with limits
3. read_limited — File reading with offset/limit
4. edit_batched — Multiple edits in single call
5. bash_minimal — Only for OS operations

## Success Metrics
- 30-40% reduction in Read tool usage
- Increased Serena MCP adoption
- Reduced full-file reads

## Connections
- [[Serena MCP]] — Priority routing target
- [[Context Optimization Implementation Plan Phases 2-4]] — Parent plan
- [[Command Output Trimmer Hook]] — Phase 1 implementation
