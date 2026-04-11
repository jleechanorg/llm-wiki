---
title: "Agent Loop Demo"
type: source
tags: [AgentLoop, orchestration, behavior-trees, AI-agents, CMUX, Codex, Minimax]
sources: []
last_updated: 2026-04-08
---

## Summary

A technical discussion and demo between Jeff and the Agent Loop team exploring orchestration strategies, workflow optimization, and model selection. The conversation covers AgentLoop's behavior tree approach to deterministic AI execution, CMUX terminal integration, and practical strategies for managing multiple AI models based on cost and capability. Key topics include parallel agent execution, dependency graphs, and the balance between open source and proprietary strategies.

## Key Claims

- Behavior trees provide deterministic execution vs pure LLM approaches with 80% more reliability
- Programmatic validation at each step enables explicit failure states instead of hallucination
- Current focus on parallel agent execution with dependency graphs
- Built-in merge resolvers handle parallel task coordination
- Monthly AI spend typically around $300 (Anthropic $200, Cursor $60, Minimax $40)
- Minimax emerging as cost-effective for volume work despite quality gap vs Codex/Claude

## Key Quotes

> "Agents run as microservices with behavior tree loops. Agent-to-agent communication through structured messaging. Automatic PR creation and merge resolution."

> "I found 5.4 uses more tokens. I feel. I ran my week out and then I got a refresh and even that ran."

> "Codex works really fine because it's smart enough to, like, use that, like, as, like, a steering wheel, whereas Minimax will sometimes, like, break free from it."

## Connections

- [[AgentLoop]] - Orchestration platform with TUI
- [[CMUX]] - Terminal multiplexer for AI workflows
- [[Codex]] - Primary coding model
- [[Minimax]] - Cost-effective alternative
- [[Claude]] - Review and evidence checking
- [[BehaviorTrees]] - Deterministic execution framework

## Model Selection Strategy

| Model | Use Case | Notes |
|-------|----------|-------|
| Codex | Complex code reviews, architectural decisions | Expensive, weekly limits |
| Claude | Evidence review, quality checking | $200/month |
| Minimax | Volume work, initial drafts | Cheap, needs supervision |
| Gemini | Game state management, structured JSON | Flash for speed |

## Business Model Discussion

- Current landscape saturated with basic LLM wrappers
- AgentLoop advantages: deterministic behavior trees, long-running persistent agents
- Full-stack Airbnb app replication as benchmark test
- Dual approach: B2B product + AI development agency
- Considering freemium model with bring-your-own-keys option
