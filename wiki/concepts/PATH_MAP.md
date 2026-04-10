---
title: "PATH_MAP"
type: concept
tags: [configuration, prompt-loading]
sources: ["test-prompt-loading-via-service"]
last_updated: 2026-04-08
---

Constant in [[AgentPrompts]] that maps prompt type keys (e.g., "narrative", "character") to file paths (e.g., "prompts/narrative.md").

## Purpose
- Registers all prompt files to prevent orphaned prompts
- Enables reverse lookup from file to usage
- Tested by [[TestPromptLoadingViaService]] for filesystem synchronization
