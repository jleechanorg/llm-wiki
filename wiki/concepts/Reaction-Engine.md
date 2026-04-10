---
title: "Reaction Engine"
type: concept
tags: ["orchestration", "reaction", "automation"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

Pattern used by Composio where orchestration triggers predefined agent responses based on events. Example configuration:

```yaml
reactions:
  ci_failed:
    action: spawn_agent
    prompt: "CI failed. Read failure logs and fix issues."
  changes_requested:
    action: spawn_agent
    prompt: "Address review comments and push fixes."
```

## See Also
- [[Composio]] — implementation reference
- [[Hybrid Orchestration]]
- [[Orchestration Architecture Research]]
