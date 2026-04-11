---
title: "ZOE: OpenClaw + Agent Swarm Reference"
type: source
tags: [openclaw, agent-swarm, orchestration, codex, claude-code, tmux, cron, workflow]
source_file: "raw/llm_wiki-raw-worldarchitect.ai-zoe_openclaw_agent_swarm_reference.md-6bf1d2b3.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Email from Elvis (@eRvissun) documenting the "replace me" architecture: OpenClaw as orchestrator (Zoe) spawning Codex/Claude agents, monitoring via cron, notifying on completion. Two-tier system where context windows are zero-sum — orchestrator handles business context while coding agents handle codebase execution.

## Key Claims
- **Two-tier context system**: Orchestrator (Zoe/OpenClaw) holds business context, decisions, memory; coding agents (Codex/Claude) handle task execution with codebase context
- **94 commits in one day**: With 3 client calls and editor never opened, ~50 commits/day average
- **8-step workflow**: Scope → Spawn Agent → Monitor (cron) → Create PR → Automated Review → Automated Testing → Human Review → Merge
- **Tmux over exec**: Mid-task redirection without killing agents via `tmux send-keys`
- **Three-model code review**: Codex (edge cases), Gemini (security/scalability), Claude Code (validation)
- **Ralph Loop V2 improvement**: When agent fails, Zoe uses full business context to unblock rather than respawning with same prompt

## Key Quotes
> "I went from managing claude code, to managing an openclaw agent that manages a fleet of other claude code and codex agents."
> "Context windows are zero-sum. Two-tier system: Orchestrator (Zoe/OpenClaw): business context, decisions, memory, prompt-writing; Coding agents (Codex/CC): codebase, conventions, task execution"

## Connections
- [[OpenClaw]] — orchestrator platform acting as Zoe in this setup
- [[Codex]] — primary coding agent (90% of tasks, backend logic, complex bugs, multi-file refactors)
- [[Claude Code]] — coding agent for frontend, git operations, faster turnaround
- [[Gemini]] — UI design agent generating HTML/CSS specs for Claude to implement
- [[Git Worktrees]] — each agent gets isolated worktree
- [[Tmux Sessions]] — per-agent sessions enabling mid-task redirection

## Contradictions
- []
