---
title: "Mode Detection"
type: concept
tags: [detection, parsing, worldarchitect]
sources: []
last_updated: 2026-04-08
---

## Summary
Mode Detection in WorldArchitect is the mechanism for identifying the type of interaction the user wants—storytelling, administrative commands, or adult content. The detection happens during agent selection and influences which agent processes the input.

## Detection Methods
- **Prefix Detection**: "GOD MODE:" prefix triggers GodModeAgent
- **Settings Detection**: spicy_mode user setting triggers SpicyModeAgent
- **Default**: No special markers routes to StoryModeAgent

## Detection in Context
Mode detection operates at the input parsing stage, before the LLM is invoked. This allows the correct agent to be selected early in the request pipeline, ensuring appropriate system instructions are built from the start.

## Related Concepts
- [[AgentSelection]] — uses mode detection for routing
- [[GodModeAgent]] — activated by mode detection
- [[SpicyModeAgent]] — activated by mode detection
- [[StoryModeAgent]] — default mode when no detection matches

## Source References
- [[Agent Architecture End-to-End Integration Test]] — validates end-to-end mode detection
