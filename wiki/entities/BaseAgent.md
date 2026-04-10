---
title: "BaseAgent"
type: entity
tags: [python-protocol, agent-system, typing]
sources: []
last_updated: 2026-04-08
---

Python Protocol class defining the interface for agents in the system. Uses @runtime_checkable decorator for structural subtyping.

## Required Methods
- prompt_order() -> tuple[str, ...]
- builder_flags() -> dict[str, Any]

## Usage
Agents implementing this protocol can be used with the prompt_generator module for standardized prompt construction.

## Related
- [[PromptGenerator]]
- [[AgentProtocol]]
