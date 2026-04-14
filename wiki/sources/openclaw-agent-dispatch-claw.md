---
title: "OpenClaw Agent Dispatch (/claw)"
type: source
tags: [orchestration, ao-spawn, parallel-agents, tmux, agent-dispatch]
sources: []
last_updated: 2026-04-14
---

## Summary

Claw routes tasks to the right execution path: Coding tasks use ao spawn + ao send for parallel tmux sessions, while non-coding tasks use OpenClaw gateway HTTP. This replaces sequential single-agent processing with parallel multi-session execution.

## Key Claims

- Path A (Coding): ao spawn + ao send for parallel tmux sessions. Routes based on issue prefix (orch-* -> jleechanclaw, wa-* -> worldarchitect, ao-* -> agent-orchestrator, etc.)
- Path B (Non-coding): OpenClaw gateway HTTP for read-only/summarize tasks
- Auto-creates beads for tasks without issue ID
- Learning-loop gate: appends /learn to capture reusable patterns unless explicitly skipped
- Slash command resolution: inlines command definition before dispatch
- Bead routing: orch-sq2 for parallel ao spawn routing

## Key Quotes

> "Coding tasks: involves writing/modifying/fixing/creating code, PRs, tests, config, or deploys"

> "When in doubt, classify as coding — err toward spawning a session"

## Connections

- [[CommandSystemDocumentation]] — Orchestration commands
- [[PairProtocol]] — Agent coordination
- [[Auton]] — AO ecosystem health monitoring

## Contradictions

- None identified
