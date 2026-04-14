---
title: "Self Correcting Loop"
type: concept
tags: [pairv2, feature-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The self-correcting loop pattern implements cyclic retry with feedback injection. When an agent fails verification, the system loops back to implementation with the verifier's failure reasoning injected into the coder's next prompt, enabling autonomous self-correction.

## Why It Matters

Linear workflows that fail once and stop lose the opportunity for agents to learn from their mistakes. Self-correcting loops enable agents to autonomously improve their work without human intervention, using LLM feedback as the mechanism for learning.

## Key Technical Details

- **Cycle limit**: Maximum number of retry cycles (typically 3)
- **Feedback mechanism**: Extract reasoning from verification reports and inject into next prompt
- **Workspace preservation**: Optionally preserve or clean workspace between retries
- **Related concepts**: VerifyRetryLoop, AgentStallRecovery

## Related Beads

- BD-pairv2-verify-retry-loop
