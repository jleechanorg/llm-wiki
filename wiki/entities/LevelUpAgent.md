---
title: "LevelUpAgent"
type: entity
tags: [agent, level-up, modal, routing]
sources: []
last_updated: 2026-04-08
---

## Description
Agent responsible for handling level-up modal flow in the game. Receives routing priority when modal lock is active.

## Related Functions
- `get_agent_for_input` routes to this agent when modal lock is active
- `_inject_modal_finish_choice_if_needed` may also route to this agent

## Connections
- [[REV-439p]] — PR that fixed modal lock activation
- [[REV-0g1y]] — related stale flag issue
- [[ModalLock]] — mechanism that triggers routing to this agent
