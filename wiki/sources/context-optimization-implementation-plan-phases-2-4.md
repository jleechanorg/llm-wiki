---
title: "Context Optimization Implementation Plan: Phases 2-4"
type: source
tags: [token-reduction, optimization, hooks, context-management, phases-2-4]
source_file: "raw/context-optimization-implementation-plan-phases-2-4.md"
sources: ["context-optimization-implementation-plan"]
last_updated: 2026-04-08
---

## Summary
Extension of the Context Optimization Implementation Plan covering Phases 2-4: Tool Selection Optimization (2 hours), Serena MCP Integration Layer (4 hours), and Response Compression System (3 hours). Phase 1 is already complete with the Command Output Trimmer Hook.

## Key Claims
- **Phase 1 Complete**: Command Output Trimmer Hook achieving 50-70% reduction in slash command output tokens
- **Key Discovery**: Most verbose output comes from Claude's execution responses, not from echo statements in .md files
- **Phase 2 Target**: 30-40% reduction via Serena MCP priority routing for tool selection
- **Phase 3 Target**: 50-70% of code reads diverted to Serena MCP with >30% cache hit rate
- **Phase 4 Target**: 40-50% token reduction through smart truncation and summarization

## Phase 2: Tool Selection Optimization

### 2.1 Pre-Command Optimization Hook
- File: `.claude/hooks/pre_tool_optimize.py`
- Intercepts tool calls and suggests optimizations
- Tool hierarchy: Serena MCP > grep_targeted > read_limited > edit_batched > bash_minimal

### 2.2 Integration Points
- Hook into PreToolUse event
- Analyze tool request patterns
- Suggest optimizations in real-time

### 2.3 Success Metrics
- 30-40% reduction in Read tool usage
- Increased Serena MCP adoption

## Phase 3: Serena MCP Integration Layer

### 3.1 Serena Router Service
- File: `.claude/services/serena_router.py`
- Automatically routes code analysis tasks to Serena MCP
- Triggers: 'find function', 'search for class', 'analyze code', etc.

### 3.2 Caching Layer
- File: `.claude/cache/serena_cache.py`
- Cache responses for repeated lookups
- 5-minute TTL with symbol_cache

### 3.3 Integration Workflow
1. Intercept code analysis requests
2. Check cache for recent lookups
3. Route to Serena MCP if appropriate
4. Cache successful responses
5. Fall back to Read tool if needed

### 3.4 Success Metrics
- 50-70% of code reads go through Serena
- Cache hit rate >30%
- Average response size reduced by 60%

## Phase 4: Response Compression System

### 4.1 Response Compressor
- File: `.claude/hooks/response_compressor.py`
- Smart compression rules per response type:
  - test_output: preserve failures/errors/summary, compress passed_tests
  - file_listing: preserve directories/important_files
  - search_results: preserve matches/context

### 4.2 Smart Summarization
- File: `.claude/services/response_summarizer.py`
- Applies compression based on tool type

## Connections
- [[Context Optimization Implementation Plan]] — Phase 1 foundation
- [[Command Output Trimmer Hook]] — Phase 1 complete implementation
- [[Serena MCP]] — Phase 2-3 routing target
- [[Claude Code]] — Execution environment for hooks
