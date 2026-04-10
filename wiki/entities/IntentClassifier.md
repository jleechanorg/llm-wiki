---
title: "IntentClassifier"
type: entity
tags: [classification, routing]
sources: ["agent-architecture-end2end-integration-test"]
last_updated: 2026-04-08
---

IntentClassifier determines user intent for agent routing in WorldArchitect. Returns mode constants (MODE_CHARACTER, MODE_GOD, etc.) with confidence scores. God mode inputs bypass the classifier due to prefix priority.

## Related
- [[get_agent_for_input]] — uses classifier output
- [[StoryModeAgent]] — selected for MODE_CHARACTER
- [[GodModeAgent]] — triggered by prefix, not classifier
