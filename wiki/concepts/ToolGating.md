---
title: "Tool Gating"
type: concept
tags: [tool-selection, conditional-availability, feature-flags]
sources: []
last_updated: 2026-04-08
---

## Definition
A pattern where available tools/functions are conditionally included or excluded from an LLM's toolset based on runtime state, configuration flags, or game mode settings.

## Use Cases
- **Faction Minigame**: Disable faction-specific tools when the minigame is not active
- **Feature Flags**: Toggle tool availability based on user subscriptions or experimental features
- **Contextual Tools**: Provide tools only when relevant to current game state


## Implementation Pattern
1. Check configuration/state flag (e.g., `faction_minigame.enabled`)
2. Filter tool list conditionally before passing to LLM
3. Include/exclude based on the flag value

## Related Concepts
- [[Feature Flags]]
- [[Tool Selection]]
- [[Provider-Specific Tool Handling]]
