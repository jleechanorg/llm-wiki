---
title: "Agent Mode Detection"
type: concept
tags: [routing, intent-classification]
sources: ["agent-architecture-end2end-integration-test"]
last_updated: 2026-04-08
---

Agent mode detection is the process of selecting the appropriate agent (StoryModeAgent, GodModeAgent, or SpicyModeAgent) based on user input in WorldArchitect. The system uses a two-stage approach:

1. **Prefix Priority**: Check if input starts with "GOD MODE:" — bypasses classifier
2. **Intent Classification**: Use IntentClassifier to determine mode

This allows both natural language routing (via classifier) and direct commands (via prefix).

## Related
- [[IntentClassifier]]
- [[get_agent_for_input]]
