---
title: "jeffrey-oracle-agent"
type: synthesis
tags: [jeffrey, oracle, agent, orchestration, parallel]
sources: [jeffrey-oracle, TmuxBasedAgentOrchestration, AgentArchitecture, Hybrid-Orchestration]
last_updated: 2026-04-11
---

# Jeffrey Oracle: Agent Orchestration

Specialized oracle for agent spawning decisions: when to delegate, sequential vs parallel execution, team creation, and agent coordination patterns.

## When Jeffrey Evaluates Agent Use

| Situation | Jeffrey's Response |
|-----------|-------------------|
| One agent enough, human could do it | Just do it — no need to spawn |
| Multiple independent tasks | Parallel agents — tmux sessions + worktree isolation |
| Complex multi-step task | Sequential with checkpoints — verify each phase |
| Team creation proposal | "What does each agent own? Who coordinates?" |
| New agent type proposed | Factory pattern coverage? All branches tested? |
| Subagent spawn in existing agent | Worktree isolation? Caller verified? |
| Cross-repo delegation | CrossRepoDelegation pattern — verify auth and scope |
| Agent-to-agent coordination | MCP Agent Mail — verify message delivery |
| Tmux session proliferation | Each session needs a purpose — no orphan sessions |

## Agent Principles (from wiki)

- **Worktree isolation per agent** — Each task agent in dedicated git worktree (TmuxBasedAgentOrchestration)
- **Factory selection** — `get_agent_for_input` pattern with fallbacks (AgentArchitecture)
- **Parallel safety** — Zero cross-agent interference via isolation (Hybrid-Orchestration)
- **Fault tolerance** — Individual failures don't crash system (TmuxBasedAgentOrchestration)
- **Minimal spawning** — Spawn only when task complexity warrants

## Spawning Decision Tree

1. Is the task complex enough? → Simple tasks stay in main session
2. Independent subtasks? → Parallel tmux + worktree agents
3. Multi-phase with dependencies? → Sequential with `.agent-N-done` markers
4. Cross-repo scope? → CrossRepoDelegation with auth verification
5. Agent needs to coordinate? → MCP Agent Mail with ack tracking
6. One PR per worktree? → Always — no multi-task pollution

## Jeffrey's Agent Red Flags

- Agent spawned for a task a human could do faster
- tmux session without worktree isolation
- Parallel agents without coordination mechanism
- New agent type without factory pattern / selection logic
- Agent spawn that creates worktree conflicts
- Cross-repo delegation without identity verification

## Parent Oracle
[[jeffrey-oracle]] — the full decision framework
