---
title: "Context Bloat"
type: concept
tags: ["performance", "context", "llm", "optimization"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

Performance killer in LLM agents. Caused by accumulating too much historical context (logs, conversation history, file contents). Solutions: summarize older logs, archive obsolete guidance, use context truncation.

## Mitigation Strategies
- Periodic summarization of progress logs
- Archiving obsolete AGENTS.md guidance
- Hard context limits with truncation
- Sliding window approaches


## See Also
- [[Self-Improving Coding Agents]]
- [[Memory Persistence]]
- [[Orchestration Architecture Research]]
