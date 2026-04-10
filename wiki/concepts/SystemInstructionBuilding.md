---
title: "System Instruction Building"
type: concept
tags: [llm, prompt-generation]
sources: ["agent-architecture-end2end-integration-test"]
last_updated: 2026-04-08
---

System instruction building is the process by which each agent type constructs the system prompt sent to the LLM. In WorldArchitect, agents use PromptBuilder to load and assemble instruction files appropriate to their mode.

## Flow
1. Agent receives user input
2. Agent calls `build_system_instructions()` with selected prompt types
3. PromptBuilder loads relevant prompt files
4. Instructions are combined and returned
5. Sent to LLM with user input


## Related
- [[PromptBuilder]]
- [[StoryModeAgent]]
- [[GodModeAgent]]
