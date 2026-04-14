---
title: "Terminal Memory Agents"
type: concept
tags: [memory, terminal, context-management, MemGPT, coding-agent, persistent-context]
sources: [extended-reasoning-frontier, swe-bench-2026]
last_updated: 2026-04-14
---

## Summary

Terminal Memory Agents apply hierarchical memory management principles (inspired by [[MemGPT]]) to long-horizon terminal-based coding tasks. The core insight: a coding agent navigating a large codebase through a terminal needs memory tiers analogous to MemGPT's memory hierarchy — distinguishing between working context (current file, current function), recent context (recently visited files, recent commands), and long-term memory (patterns learned, PR conventions, project architecture). Without memory tiers, context windows are wasted on irrelevant state.

## Key Claims

### Why Terminal Coding Tasks Break Memory

- Terminal-based coding (as in [[TerminalBench]]/[[TerminalBench-2]]) requires multi-step navigation: `cd` → `grep` → `cat` → `edit` → `test` → repeat
- Each step adds to context, but most context is irrelevant to the current task
- Standard context management treats all information equally — wastes the window on stale state
- After 20+ terminal steps, the agent often loses track of where it is in the larger task

### Memory Tier Architecture for Terminal Agents

| Tier | Contents | When Evicted | Purpose |
|------|----------|--------------|---------|
| **Working** | Current file, current function, active diff | Every step | Immediate task |
| **Recent** | Last 10 commands, last 5 files visited | After 50 steps | Recovery from interruption |
| **Project** | File tree snapshot, key patterns, architecture | Never | Global coherence |
| **Lesson** | Patterns from prior similar tasks | Never | Learning from experience |

### Connection to MemGPT

[[MemGPT]] pioneered tiered memory for LLM conversations:
- Treats context window like an OS with virtual memory
- Pages in/out based on relevance
- Enables agents to "remember" across arbitrarily long conversations

Terminal Memory Agents apply the same principle to code navigation:
- Project tier = MemGPT's archival memory
- Recent tier = MemGPT's context memory
- Working tier = MemGPT's immediate attention

### Integration with [[MetaHarness]]

Meta-Harness achieves #1 on [[TerminalBench-2]] partly because its filesystem history access acts as a memory system. The lessons from Meta-Harness + MemGPT suggest:
- Filesystem access can substitute for explicit memory management
- But explicit memory tiers would make filesystem access more efficient
- Future: combine MemGPT-style memory with filesystem-backed persistence

## Connections

- [[MemGPT]] — inspiration for hierarchical memory management
- [[TerminalBench]] / [[TerminalBench-2]] — the benchmark where memory management matters
- [[MetaHarness]] — achieves strong results partly via filesystem-backed "memory"
- [[ExtendedThinking]] — memory management affects how effectively extended thinking can operate
- [[ContextManagement]] — broader concept; terminal memory is a specific instance

## See Also

- [[MemGPT]] — the foundational memory-augmented LLM
- [[TerminalBench-2]] — where this matters in practice
- [[MetaHarness]] — filesystem history as implicit memory
