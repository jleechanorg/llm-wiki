---
title: "ai_orch"
type: entity
tags: [ai-orch, orchestration, agent-spawning, execution]
sources: [orchestration-system-design-justification.md]
last_updated: 2026-04-07
---

ai_orch (at `~/projects/worldarchitect.ai/orchestration/`) handles agent spawning, tmux lifecycle, and CLI invocation. It does NOT provide GitHub PR readiness checking — that responsibility belongs to the orchestration layer.

See: [[Orchestration System Design Justification]]
