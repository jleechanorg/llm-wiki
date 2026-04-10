---
title: "Nested Agent Loops"
type: concept
tags: ["agents", "loops", "iteration", "self-improvement"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

Pattern where agents operate in continuous loops: pick tasks, implement code, validate changes, commit, update status, reset context for next iteration. Stateless-but-iterative design prevents context overflow.

## Related Patterns
- [[Ralph Loop Method]] — specific implementation
- [[Compound Loops]] — chaining phases (Analysis → Planning → Execution)
- [[Planner-Worker Hierarchies]] — decomposition and execution separation

## See Also
- [[Self-Improving Coding Agents]]
- [[Memory Persistence]]
- [[Orchestration Architecture Research]]
