---
title: "Mode Forcing Prevention"
type: concept
tags: [security, agents, mode-routing]
sources: [internal-mode-rejection-tests]
last_updated: 2026-04-08
---

## Definition


Mode forcing prevention is a security measure that prevents users from bypassing intended game mechanics by explicitly requesting internal modes via the API.

## Mechanism


The `get_agent_for_input()` function in `mvp_site.agents` validates the requested mode:
1. If mode is an internal mode (combat, rewards, info, etc.), reject and return [[StoryModeAgent]] instead
2. If mode is a user-facing mode (think, god), allow it
3. If mode is not specified, rely on intent classifier

## Security Rationale

Allowing users to force internal modes would enable:
- Skipping combat encounters
- Claiming rewards without earning them
- Bypassing character creation workflow

## Implementation

```python
def get_agent_for_input(user_input, state, mode=None):
    # Reject internal modes for security
    if mode in INTERNAL_MODES:
        mode = constants.MODE_STORY  # Fall back to StoryMode
    
    # ... rest of logic
```

## Related

- [[InternalModes]]
- [[StoryModeAgent]]
- [[get_agent_for_input]]
