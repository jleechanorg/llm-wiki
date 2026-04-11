---
title: "Agent Orchestrator"
type: entity
tags: [agent-orchestrator, orchestration, ai-agents, automation, ao]
sources: [agent-orchestrator-fork-summary.md, agent-orchestration.md]
last_updated: 2026-04-11
---

## Summary

Agent Orchestrator (AO) is a system that manages fleets of AI coding agents working in parallel on a codebase. Each agent gets its own git worktree, its own branch, and its own PR. When CI fails, the agent fixes it. When reviewers leave comments, the agent addresses them. AO is agent-agnostic, runtime-agnostic, and tracker-agnostic.

There are two distinct variants: the upstream **ComposioHQ/agent-orchestrator** (general-purpose CI tool) and the **jleechanorg/agent-orchestrator** fork (autonomous zero-touch PR merging pipeline). See [[AgentOrchestratorFork]] for fork-specific detail.

## Key Capabilities

- Spawns isolated git worktrees for each agent task
- Coordinates parallel agent execution
- Monitors via cron-based polling and a lifecycle worker
- Integrates with [[SkepticGate]] for automated LLM verification (fork only)
- Supports reactions, agentRules, and per-project config via `agent-orchestrator.yaml`
- Evolve loop continuously drives open PRs toward merge (fork only)

## Plugin Ecosystem

AO is plugin-first. New capabilities should be implemented as plugins before touching core.

**Agent plugins** (coding agents):
- `ao-plugin-agent-cursor` — Cursor IDE agent
- `ao-plugin-agent-codex` — OpenAI Codex agent (primary LLM for skeptic evals)
- `ao-plugin-agent-gemini` — Gemini agent
- `ao-plugin-agent-aider` — Aider agent
- `ao-plugin-agent-opencode` — OpenCode agent

**Runtime plugins** (process execution):
- `ao-plugin-runtime-tmux` — tmux pane-based execution
- `ao-plugin-runtime-process` — direct child process execution

**SCM/tracker plugins**:
- `ao-plugin-scm-github` — GitHub integration (PRs, checks, rate-limit fallback)
- `ao-plugin-scm-gitlab` — GitLab integration
- `ao-plugin-tracker-linear` — Linear issue tracker
- `ao-plugin-tracker-beads` — Beads JSONL issue tracker (fork-specific)

**Notifier plugins**:
- `ao-plugin-notifier-openclaw` — OpenClaw/Slack notifications

## Development Hierarchy

Before writing any code, follow this order:
1. **Config** — `agent-orchestrator.yaml` (reactions, agentRules, routing)
2. **New plugin** in an existing slot
3. **New plugin type** (new slot in plugin-registry)
4. **Core code change** — only when 1–3 are insufficient; justify in PR

Core code (`packages/core/src/`) is treated as stable infrastructure.

## AO Workers as Default Execution Model

When working in the fork, always dispatch an AO worker for non-trivial tasks rather than running `claude -p` directly. Workers can claim a PR (`ao spawn --claim-pr N`), a bead (`ao spawn --bead <id>`), or an arbitrary task string.

## Zero-Framework Cognition (ZFC)

AO enforces ZFC: no keyword routing, heuristic scoring, or semantic classification in application code. All such judgment must be delegated to model API calls. See [[AgentOrchestratorFork]] for enforcement details.

## 7-Green Merge Gates (fork)

All seven must hold before a PR can merge:
1. CI green
2. Mergeable (no conflicts)
3. CodeRabbit APPROVED
4. Bugbot clean
5. Inline threads resolved
6. Evidence bundle present (when required)
7. Skeptic PASS (not SKIPPED)

## Beads Issue Tracker

Fork-specific issues live in `.beads/issues.jsonl`. Use the `br` CLI to create, update, and close beads. Beads IDs follow the pattern `bd-XXXX`.

## Connections

- [[AgentOrchestratorFork]] — fork-specific autonomous pipeline details
- [[SkepticGate]] — 7th merge gate, LLM-based PR verifier
- [[Cursor]] — primary worker agent
- [[WorldArchitectAI]] — target repository for fork dogfooding
- [[ZeroFrameworkCognition]] — ZFC design principle enforced in this repo
