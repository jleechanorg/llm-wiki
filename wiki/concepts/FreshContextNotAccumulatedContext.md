---
title: "Fresh Context, Not Accumulated Context"
type: concept
tags: ["context", "prompting", "performance", "headless"]
sources: ["harness-engineering-philosophy"]
last_updated: 2026-04-07
---

The principle that each headless agent call gets a clean prompt with all context injected upfront — no memory of previous attempts. The harness (AO session metadata + OpenClaw memory) handles persistence, not the agent itself.

## Why This Matters
Accumulated context causes performance degradation in long-running agent loops. By keeping each call fresh with injected context, the system avoids context bloat.

## Implementation
- Harness stores session metadata
- OpenClaw provides persistent memory
- Coding agent never accumulates context between calls

## Related Concepts
- [[Harness Engineering]] — overall discipline
- [[OpenClaw]] — provides persistent memory
- [[Agent Orchestrator]] — stores session metadata
