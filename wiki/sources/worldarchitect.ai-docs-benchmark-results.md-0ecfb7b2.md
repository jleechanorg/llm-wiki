---
title: "Genesis vs Ralph Orchestrator Benchmark Results"
type: source
tags: [benchmark, genesis, ralph, codex, claude, orchestration]
sources: []
source_file: /Users/jleechan/repos/worldarchitect.ai
date: 2025-09-27
last_updated: 2026-04-07
---

## Summary

Benchmark comparison of Genesis and Ralph orchestrator systems executed on September 27, 2025, using identical input specifications across three complexity levels (CLI processor, Task Management API, Full-Stack Finance Tracker). Achieved perfect input parity via MD5 verification. Genesis succeeded on all 3 projects using Codex; Ralph succeeded on 2/3 projects with Claude fallback due to codex adapter KeyError.

## Key Claims

- Perfect input parity achieved — byte-for-byte identical specifications across both systems verified via MD5 hashing
- Genesis: 3/3 projects started successfully using Codex agent with tmux session management
- Ralph: 2/3 projects started — codex adapter threw KeyError on Project 1, fell back to Claude for Projects 2-3
- Ralph's codex adapter created but not properly registered in agent mapping
- Execution models differ: Genesis uses tmux sessions (interactive, observable, resumable); Ralph uses background processes (daemon-style, logged, autonomous)
- Agent parity not achieved — apples-to-oranges comparison (Codex vs Claude)

## Key Quotes

> "Genesis (codex) vs Ralph (claude) = Apples vs Oranges" — different underlying AI models affect code generation patterns

> "Both systems are viable orchestration platforms with different strengths" — Genesis excels at session management, Ralph at background execution

## Connections

- [[WorldArchitect.AI]] — the parent project these orchestrators are built for
- [[Codex]] — Genesis's primary agent, Ralph's failed adapter
- [[Claude Code]] — Ralph's fallback agent when Codex failed

## Contradictions

- None identified — this is a standalone benchmark report