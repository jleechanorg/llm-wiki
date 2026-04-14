---
title: "AgentMentor"
type: concept
tags: [agent-improvement, execution-monitoring, corrective-instructions, spec-ambiguity, agentic-governance]
sources: [agent-mentor-paper]
last_updated: 2026-04-14
---

## Definition

An external agent mentoring framework that monitors execution logs to detect behavioral failure patterns and injects corrective instructions into the agent's knowledge base. Operates as an "oracle mentor" observing the agent from the outside, deriving corrective statements from semantic features in execution traces.

## Core Insight

Agent failures often stem from imprecise natural language prompt formulations, not flawed agent code. Diagnosing at the prompt/semantics level (via execution logs) is more actionable than inspecting agent internals.

## How It Works

1. **Monitor**: Continuously watch execution logs throughout the agent lifecycle
2. **Extract**: Identify semantic features associated with undesired behaviors
3. **Derive**: Generate corrective statements from observed failure patterns
4. **Inject**: Update the agent's knowledge base with corrective instructions
5. **Iterate**: Repeated runs enable incremental refinement

## Key Properties

- Particularly effective in spec-ambiguity-dominated settings
- Released as open-source library
- Frames as building block for automated agentic governance at scale
- External to the agent (vs internal self-critique loops)

## Related Concepts

- [[Mem2Evolve]] — internal co-evolution of experience+tools vs Agent Mentor's external behavioral monitoring
- [[SelfCritiqueVerificationLoop]] — internal correction loop vs external mentor observation
- [[AgenticGovernance]] — Agent Mentor explicitly frames as governance building block
- [[SpecAmbiguity]] — core problem it addresses
