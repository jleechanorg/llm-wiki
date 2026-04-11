---
title: "Genesis vs Ralph Orchestrator Benchmark Results"
type: source
tags: [benchmark, genesis, ralph, orchestrator, codex, claude, agent-adapters]
source_file: "raw/genesis-vs-ralph-orchestrator-benchmark-results.md"
sources: []
last_updated: 2026-04-07
---

## Summary
Benchmark comparison of Genesis and Ralph orchestrator systems using identical input specifications across three complexity levels (CLI processor, Task Management API, Full-Stack Finance Tracker). Genesis succeeded on all 3 projects with Codex; Ralph succeeded on 2/3 with Claude fallback due to incomplete codex adapter.

## Key Claims

- **Input Parity Verified**: MD5 hash verification confirmed byte-for-byte identical specifications across both systems
- **Genesis Success Rate**: 3/3 projects started (Codex agent, tmux sessions)
- **Ralph Success Rate**: 2/3 projects (Claude fallback, background execution)
- **Critical Issue**: Ralph's codex adapter not properly registered in agent mapping (KeyError: 'codex')

## Key Quotes
> "Genesis (codex) vs Ralph (claude) = Apples vs Oranges" — different underlying AI models affect code generation patterns

> "Input Parity Protocol: MD5 verification ensures identical specifications"

## Connections
- [[Genesis]] — orchestrator with tmux-based session management
- [[Ralph]] — orchestrator with background execution model
- [[Codex]] — primary agent for Genesis benchmarks
- [[Claude]] — fallback agent for Ralph due to adapter issue

## Contradictions
- None identified
