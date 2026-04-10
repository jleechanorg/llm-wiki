---
title: "Compaction"
type: concept
tags: ["memory", "context", "optimization"]
sources: ["genesis-persistent-orchestration-layer-openclaw"]
last_updated: 2026-04-07
---

OpenClaw's memory management system that handles context window limits.

## Memory Flush
- **Enabled by default**: Reminds agent to persist important context before session context window fills
- **Trigger**: When context approaches limit
- **Action**: Agent must save important context to persistent memory files

## Purpose
Prevents context loss by proactively prompting the agent to:
1. Save important decisions to MEMORY.md
2. Update USER.md with new preferences discovered
3. Log significant session events to daily notes

## Related Concepts
- [[MemorySearch]] — retrieval system
- [[Memory System]] — storage layer
