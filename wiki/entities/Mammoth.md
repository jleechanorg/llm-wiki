---
title: "Mammoth"
type: entity
tags: [attractor-pattern, pipeline-runner, go, dark-factory]
date: 2026-05-24
---
## Overview
Mammoth is 2389 Research's Go DOT-based pipeline runner for LLM agent workflows. It scope-crept into a full spec engine with a 21-rule DOT linter, fan-in nodes, verification nodes, and a 5-phase node lifecycle.

## Key Properties
- **Type**: DOT-based pipeline runner (Go)
- **Key features**: 21-rule DOT linter, fan-in with configurable join policies (all-success, majority, first-success), verification nodes (zero token cost), 5-phase node lifecycle, web UI, TUI, MCP server
- **Source**: https://github.com/2389-research/mammoth
- **Architecture**: llm/ (unified SDK), tracker (pipeline execution), runstate/ (persistence), dot/ (parser/validator), web/, tui/, mcp/
- **Test suite**: 5,200+ tests

## Connections
- [[2389Research]] — 2389 Research built Mammoth
- [[Tracker]] — Mammoth uses tracker for pipeline execution
- [[AttractorPattern]] — Mammoth converges on the three-layer attractor architecture
- [[Smasher]] — Smasher is 2389's Rust alternative (leaner, used day-to-day)

## See Also
- [[2389Research]]
- [[Tracker]]
- [[Smasher]]
