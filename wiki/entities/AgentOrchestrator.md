---
title: "Agent Orchestrator"
type: entity
tags: [agent-orchestrator, orchestration, ai-agents, automation]
sources: []
last_updated: 2026-04-07
---

## Definition
Agent Orchestrator (AO) is a system that orchestrates multiple AI agents (Cursor, Codex, Claude) to work on pull requests in parallel. It coordinates work across repositories using git worktrees and provides cron-based monitoring.

## Key Capabilities
- Spawns isolated git worktrees for each agent task
- Coordinates parallel agent execution
- Monitors via cron-based polling
- Integrates with skeptic for automated verification

## Connections
- Works with [[Cursor]] as worker agent
- Targets [[WorldArchitectAI]] repository
- Uses [[Skeptic]] for verdict verification
