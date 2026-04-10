---
title: "Agent Routing"
type: concept
tags: [architecture, multi-agent]
sources: ["agent-architecture-end2end-integration-test", "agent-routing-schema-validation-tests"]
last_updated: 2026-04-08
---

Agent routing is the architecture pattern used in WorldArchitect where different agent types handle different interaction modes. The `get_agent_for_input` function selects the appropriate agent based on:

- User input content
- Current game state
- Mode detection results

## Benefits
- Separation of concerns between narrative and administrative functions
- Extensible — new agent types can be added
- Testable — each agent can be unit tested independently

## Related
- [[get_agent_for_input]]
- [[BaseAgent]]
