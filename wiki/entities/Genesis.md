---
title: "Genesis"
type: entity
tags: [orchestrator, benchmark, codex, tmux]
sources: []
last_updated: 2026-04-07
---

Genesis is an orchestrator system tested in the September 2025 benchmark against [[Ralph]]. It uses tmux-based session management for agent execution and works with the [[Codex]] agent by default.

## Benchmark Results
- **Project 1 (CLI File Processor)**: ✅ Running with codex
- **Project 2 (Task Management API)**: ✅ Running with codex  
- **Project 3 (Full-Stack Finance Tracker)**: ✅ Running with codex

## Technical Characteristics
- Execution Method: tmux sessions
- Agent: Codex (working by default)
- Monitoring: tmux session management
- Reliability: All 3 projects started successfully

## Connections
- Compared to [[Ralph]] in benchmark
- Uses [[Codex]] as primary agent
