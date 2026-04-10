---
title: "Parallelization"
type: concept
tags: [AI-agents, git-worktrees, concurrency]
sources: [openclaw-workshop-notes, agent-loop-demo]
last_updated: 2026-04-08
---

## Definition

Stage 5 of the 8-stage AI coding evolution. Using git worktrees to isolate tasks, spawning multiple agents working on different branches simultaneously. Eliminates merge conflicts during generation phase and massively increases throughput.

## The Evolution of AI Coding

| Stage | Name | Description |
|-------|------|-------------|
| 1 | No AI | Traditional software engineering |
| 2 | Autocomplete | Early Copilot, predicting line ends |
| 3 | Code Assist | Pair programming paradigm, ~50% code by AI |
| 4 | Agent/Cloud Code | AI becomes primary author |
| 5 | **Parallelization** | Multiple agents in worktrees |
| 6 | Ralph Loops | Continuous execution scripts |
| 7 | Orchestrators | Fleets of looping agents |
| 8 | Self-Evolving | Autonomous PR merging |

## Benefits

- **No merge conflicts**: Agents work in isolated branches
- **Massive throughput**: Multiple tasks simultaneously
- **Token efficiency**: Different models for different tasks
- **Risk isolation**: One agent failing doesn't block others

## Implementation

### Git Worktrees
```bash
git worktree add ../feature-a feature-branch
git worktree add ../feature-b feature-branch
# Run different agents in each worktree
```

### CMUX Integration
[[CMUX]] provides programmatic access to multiple terminal tabs:
- One tab can write to another tab
- Agents can coordinate between worktrees
- Notification rings show status

## The Smart Claw Vision

Autonomous scanning, bug hunting, code review - all running in parallel across repositories.

## Connections

- [[CMUX]] - Terminal management for parallel agents
- [[ModelRouting]] - Different models for different tasks
- [[AgentOrchestrator]] - Managing fleets of parallel agents
