---
title: "User-Facing Modes"
type: concept
tags: [agents, mode-routing]
sources: [internal-mode-rejection-tests]
last_updated: 2026-04-08
---

## Definition

User-facing modes are agent modes that CAN be explicitly requested via the API 'mode' parameter. These are modes where user intent is clear and enabling them explicitly provides better UX.

## Examples

- **MODE_THINK** — triggers [[PlanningAgent]] for structured reasoning
- **MODE_GOD** — triggers [[GodModeAgent]] for narrative generation

## Usage

```python
agent, _ = get_agent_for_input("plan my approach", mock_state, mode=constants.MODE_THINK)
agent, _ = get_agent_for_input("fix the story", mock_state, mode=constants.MODE_GOD)
```

## Comparison

| Mode Type | Can Force via API | Examples |
|----------|-------------------|----------|
| User-Facing | Yes | think, god |
| Internal | No (falls back to StoryMode) | combat, rewards, info |

## Related

- [[InternalModes]] — modes that cannot be explicitly requested
- [[PlanningAgent]] — handles think mode
- [[GodModeAgent]] — handles god mode
