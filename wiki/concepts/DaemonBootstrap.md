---
title: "Daemon Bootstrap"
type: concept
tags: [symphony, daemon, bootstrap, startup]
sources: [symphony-runtime-dedupe-contract]
last_updated: 2026-04-07
---

## Definition
The process of starting the Symphony daemon with environment configuration and workflow loading. The bootstrap phase must NOT expand local policies or generate runtime artifacts.


## Constraints
- No `WORKFLOW.md` generation at setup time
- No policy expansion in bootstrap path
- No default RPC enqueue for non-benchmark dispatch

## Rollback Mechanism
Set `SYMPHONY_MEMORY_QUEUE_MODE=always` to revert to previous enqueue behavior.
