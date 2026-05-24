---
title: "Smasher"
type: entity
tags: [attractor-pattern, pipeline-runner, rust, dark-factory]
date: 2026-05-24
---
## Overview
Smasher is 2389 Research's Rust DOT-based pipeline runner with an HTMX web dashboard, live SSE streaming, graph visualization, and a `smasher chat` REPL. It is the 2389 implementation used day-to-day.

## Key Properties
- **Type**: DOT-based pipeline runner (Rust)
- **Key features**: 5 crates (LLM client, agent, attractor, web dashboard, CLI), HTMX frontend, live SSE streaming, graph visualization, 6 built-in agent tools, `smasher chat` REPL
- **Source**: https://github.com/2389-ai/smasher (private or moved)
- **Architecture**: smasher-llm (streaming, retries, provider quirks), smasher-agent (6 tools, steering, subagents), smasher-attractor (winnow parser, tokio broadcast)

## Connections
- [[2389Research]] — 2389 Research built Smasher
- [[Mammoth]] — Mammoth is 2389's Go alternative (larger, more features)
- [[AttractorPattern]] — Smasher converges on the three-layer attractor architecture

## See Also
- [[2389Research]]
- [[Mammoth]]
