---
title: "Environment Variable Cleanup"
type: concept
tags: [environment, security, configuration]
sources: []
last_updated: 2026-04-07
---

Critical security and configuration practice in multi-provider orchestration. When switching between CLI providers (e.g., MiniMax to Claude), environment variables like ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, ANTHROPIC_BASE_URL, and ANTHROPIC_MODEL must be explicitly unset to prevent credential conflicts.

**Key Fix:** Added to Claude profile in `orchestration/task_dispatcher.py`:
```python
"env_unset": [
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "ANTHROPIC_MODEL",
    "ANTHROPIC_SMALL_FAST_MODEL",
]
```

**Related:** [[Orchestration]], [[Authentication]]
