---
title: "Pair Protocol"
type: source
tags: [agent-protocol, mcp-mail, pair-programming, coordination]
sources: []
last_updated: 2026-04-14
---

## Summary

The Pair Protocol defines asynchronous agent-to-agent coordination using MCP mail while maintaining human-in-the-loop oversight at critical decision points. It uses a Planner/Builder role separation with immutable test contracts and change order workflows.

## Key Claims

- Protocol version 3.1 with 12 message types (PAIR_INIT, CONTRACT_DRAFT, CONTRACT_FINAL, BUILD_COMPLETE, CHANGE_ORDER, CHANGE_ORDER_ACCEPTED, CHANGE_ORDER_REJECTED, SESSION_COMPLETE, SESSION_ABORT, CLARIFICATION_REQUEST, CLARIFICATION_RESPONSE, TIMEOUT_WARNING)
- Tests are immutable once CONTRACT_FINAL is sent — any modification triggers CRITICAL alert
- Human review checkpoints at contract generation and implementation review phases
- Timeout configuration: PAIR_INIT (5min), CONTRACT_FINAL (30min), BUILD_COMPLETE (60min), CHANGE_ORDER (30min)
- Change orders allow builders to request contract modifications when blocked

## Key Quotes

> "IMMUTABLE_TESTS law is absolute — Don't Touch Tests"

> "Human checkpoints exist for a reason — Trust the Protocol"

## Connections

- [[CommandSystemDocumentation]] — Part of the command system
- [[Claw]] — Uses MCP mail for agent dispatch
- [[Auton]] — Autonomy diagnostic for AO system health

## Contradictions

- None identified
