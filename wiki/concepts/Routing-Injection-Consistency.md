---
title: "Routing-Injection Consistency"
type: concept
tags: [modal-agent, routing, state-management]
sources: ["modal-state-management-integration-tests"]
last_updated: 2026-04-08
---

## Definition
The principle that both routing logic (determining which agent handles input) and injection logic (adding context to prompts) must agree on modal active state and check for stale flags consistently.

## Key Issue
Routing and injection may check different conditions for stale flags, causing behavior divergence where routing thinks modal is inactive but injection still applies modal-specific prompts.

## Fix (commit 11ef8e4f5)
Both routing and injection must check for stale level_up_in_progress=False flag.

## Related Tests
- [[Modal State Management Integration Tests]]
