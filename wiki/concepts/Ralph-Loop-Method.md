---
title: "Ralph Loop Method"
type: concept
tags: ["agents", "loop", "iteration", "ralph"]
sources: ["orchestration-architecture-research"]
last_updated: 2026-04-07
---

Core mechanism for continuous agent iteration: agents pick tasks, implement code, validate changes, commit, update status, reset context for next iteration. Philosophy: "each improvement should make future improvements easier."

## Memory Persistence (Four Channels)
1. Git commit history — code changes visible via diffs
2. Progress logs — chronological records of attempts
3. Task state files — JSON tracking completion status
4. AGENTS.md — accumulated semantic wisdom

## See Also
- [[Nested Agent Loops]]
- [[Self-Improving Coding Agents]]
- [[Orchestration Architecture Research]]
