---
title: "mctrl"
type: entity
tags: [mctrl, orchestration, state-management]
sources: [orchestration-system-design-justification.md]
last_updated: 2026-04-07
---

mctrl is the component that owns orchestration state in the current architecture. It works alongside [[ai_orch]] which owns execution. GitHub and Slack integrations hang directly off this stack.

See: [[Orchestration System Design Justification]]
