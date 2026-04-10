---
title: "Mission Control"
type: entity
tags: [mission-control, ui, control-plane]
sources: [orchestration-system-design-justification.md]
last_updated: 2026-04-07
---

Mission Control was evaluated as a UI/control-plane application, not as the authoritative execution path. The current direction is documented in `roadmap/MCTRL_NO_OSS_MISSION_CONTROL.md`: mctrl owns orchestration state, ai_orch owns execution, and GitHub/Slack integrations hang directly off that stack.

Related: [[OpenClaw]], [[mctrl]], [[ai_orch]]
