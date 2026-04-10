---
title: "Ralph"
type: entity
tags: [orchestrator, benchmark, claude, background-execution]
sources: []
last_updated: 2026-04-07
---

Ralph is an orchestrator system tested in the September 2025 benchmark against [[Genesis]]. It uses background process execution with logging and required a Claude fallback due to incomplete codex adapter configuration.

## Benchmark Results
- **Project 1 (CLI File Processor)**: ❌ Failed (KeyError: 'codex')
- **Project 2 (Task Management API)**: ✅ Running with Claude (fallback)
- **Project 3 (Full-Stack Finance Tracker)**: ✅ Running with Claude (fallback)

## Technical Characteristics
- Execution Method: Background process with logging
- Agent: Claude (fallback due to codex adapter issue)
- Monitoring: Process ID tracking and log files
- Reliability: 2/3 projects started

## Known Issues
- Codex adapter created but not properly registered in agent mapping

## Connections
- Compared to [[Genesis]] in benchmark
- Uses [[Claude]] as fallback agent
